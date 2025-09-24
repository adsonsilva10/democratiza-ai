import pytest
import json
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from app.main import app

@pytest.mark.integration
class TestAuthAPI:
    """Test authentication API endpoints."""
    
    @pytest.mark.asyncio
    async def test_register_user(self, client: AsyncClient, sample_user_data):
        """Test user registration."""
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == sample_user_data["email"]
    
    @pytest.mark.asyncio
    async def test_login_user(self, client: AsyncClient, sample_user_data):
        """Test user login."""
        # First register the user
        await client.post("/api/v1/auth/register", json=sample_user_data)
        
        # Then login
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        login_data = {
            "email": "invalid@email.com",
            "password": "wrongpassword"
        }
        
        response = await client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, client: AsyncClient, sample_user_data):
        """Test getting current user info."""
        # Register and login
        await client.post("/api/v1/auth/register", json=sample_user_data)
        login_response = await client.post("/api/v1/auth/login", json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]

@pytest.mark.integration  
class TestContractsAPI:
    """Test contracts API endpoints."""
    
    async def get_auth_headers(self, client: AsyncClient, sample_user_data):
        """Helper to get authentication headers."""
        await client.post("/api/v1/auth/register", json=sample_user_data)
        login_response = await client.post("/api/v1/auth/login", json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.mark.asyncio
    async def test_upload_contract(self, client: AsyncClient, sample_user_data):
        """Test contract upload."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        # Mock file upload
        files = {
            "file": ("test_contract.pdf", b"fake pdf content", "application/pdf")
        }
        
        with patch("app.services.file_service.upload_file") as mock_upload:
            mock_upload.return_value = {
                "file_url": "https://example.com/contract.pdf",
                "file_id": "test-file-123"
            }
            
            response = await client.post(
                "/api/v1/contracts/upload", 
                files=files,
                headers=headers
            )
        
        assert response.status_code == 201
        data = response.json()
        assert "contract_id" in data
        assert data["status"] == "uploaded"
    
    @pytest.mark.asyncio
    async def test_get_contracts(self, client: AsyncClient, sample_user_data):
        """Test getting user contracts."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        response = await client.get("/api/v1/contracts", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "contracts" in data
        assert isinstance(data["contracts"], list)
    
    @pytest.mark.asyncio  
    async def test_get_contract_analysis(self, client: AsyncClient, sample_user_data):
        """Test getting contract analysis."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        # First upload a contract (mocked)
        with patch("app.services.file_service.upload_file") as mock_upload, \
             patch("app.workers.document_processor.DocumentProcessor.process_contract") as mock_process:
            
            mock_upload.return_value = {
                "file_url": "https://example.com/contract.pdf",
                "file_id": "test-file-123"
            }
            
            mock_process.return_value = {
                "status": "completed",
                "analysis": {
                    "contract_type": "locacao",
                    "risk_level": "medium",
                    "summary": "Test analysis"
                }
            }
            
            # Upload contract
            files = {"file": ("test.pdf", b"fake content", "application/pdf")}
            upload_response = await client.post(
                "/api/v1/contracts/upload", 
                files=files,
                headers=headers
            )
            
            contract_id = upload_response.json()["contract_id"]
            
            # Get analysis
            response = await client.get(
                f"/api/v1/contracts/{contract_id}/analysis",
                headers=headers
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
    
    @pytest.mark.asyncio
    async def test_delete_contract(self, client: AsyncClient, sample_user_data):
        """Test contract deletion."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        # Mock contract creation and deletion
        with patch("app.services.file_service.upload_file") as mock_upload, \
             patch("app.services.file_service.delete_file") as mock_delete:
            
            mock_upload.return_value = {
                "file_url": "https://example.com/contract.pdf", 
                "file_id": "test-file-123"
            }
            mock_delete.return_value = {"status": "deleted"}
            
            # Upload contract first
            files = {"file": ("test.pdf", b"fake content", "application/pdf")}
            upload_response = await client.post(
                "/api/v1/contracts/upload",
                files=files, 
                headers=headers
            )
            
            contract_id = upload_response.json()["contract_id"]
            
            # Delete contract
            response = await client.delete(
                f"/api/v1/contracts/{contract_id}",
                headers=headers
            )
        
        assert response.status_code == 200
        assert response.json()["status"] == "deleted"

@pytest.mark.integration
class TestChatAPI:
    """Test chat API endpoints."""
    
    async def get_auth_headers(self, client: AsyncClient, sample_user_data):
        """Helper to get authentication headers."""
        await client.post("/api/v1/auth/register", json=sample_user_data)
        login_response = await client.post("/api/v1/auth/login", json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.mark.asyncio
    async def test_create_chat_session(self, client: AsyncClient, sample_user_data):
        """Test creating a chat session."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        session_data = {
            "agent_type": "rental", 
            "contract_id": None
        }
        
        response = await client.post(
            "/api/v1/chat/sessions",
            json=session_data,
            headers=headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "session_id" in data
        assert data["agent_type"] == "rental"
    
    @pytest.mark.asyncio
    async def test_send_message(self, client: AsyncClient, sample_user_data):
        """Test sending a message in chat."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        # Create session first
        session_response = await client.post(
            "/api/v1/chat/sessions",
            json={"agent_type": "rental", "contract_id": None},
            headers=headers
        )
        session_id = session_response.json()["session_id"]
        
        # Send message
        message_data = {
            "content": "Olá, preciso de ajuda com meu contrato",
            "message_type": "user"
        }
        
        with patch("app.api.v1.chat.generate_ai_response") as mock_ai:
            mock_ai.return_value = {
                "content": "Olá! Como posso ajudá-lo com seu contrato?",
                "message_type": "assistant"
            }
            
            response = await client.post(
                f"/api/v1/chat/sessions/{session_id}/messages",
                json=message_data,
                headers=headers
            )
        
        assert response.status_code == 201
        data = response.json()
        assert "message_id" in data
        assert "ai_response" in data
    
    @pytest.mark.asyncio
    async def test_get_chat_history(self, client: AsyncClient, sample_user_data):
        """Test getting chat history."""
        headers = await self.get_auth_headers(client, sample_user_data)
        
        # Create session
        session_response = await client.post(
            "/api/v1/chat/sessions",
            json={"agent_type": "rental", "contract_id": None},
            headers=headers
        )
        session_id = session_response.json()["session_id"]
        
        # Get history
        response = await client.get(
            f"/api/v1/chat/sessions/{session_id}/messages",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert isinstance(data["messages"], list)

@pytest.mark.integration
class TestHealthAPI:
    """Test health check endpoints."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test basic health check."""
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

@pytest.mark.integration
class TestAPIErrorHandling:
    """Test API error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        """Test accessing protected endpoints without auth."""
        response = await client.get("/api/v1/contracts")
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_invalid_json(self, client: AsyncClient):
        """Test sending invalid JSON."""
        response = await client.post(
            "/api/v1/auth/register",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_not_found_endpoint(self, client: AsyncClient):
        """Test accessing non-existent endpoint."""
        response = await client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404

@pytest.mark.slow
class TestAPIPerformance:
    """Test API performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_response_time(self, client: AsyncClient):
        """Test API response times."""
        import time
        
        start_time = time.time()
        response = await client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        # Health check should be fast
        assert (end_time - start_time) < 1.0
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client: AsyncClient):
        """Test handling concurrent requests."""
        import asyncio
        
        # Make multiple concurrent requests
        tasks = [
            client.get("/health")
            for _ in range(10)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        assert len(responses) == 10
        assert all(r.status_code == 200 for r in responses)