from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Democratiza AI - Backend",
    description="API para análise inteligente de contratos brasileiros",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Democratiza AI - Backend API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Basic API endpoints for frontend integration
@app.post("/api/v1/auth/login")
async def login():
    return {"message": "Login endpoint - to be implemented"}

@app.post("/api/v1/auth/register")
async def register():
    return {"message": "Register endpoint - to be implemented"}

@app.get("/api/v1/contracts")
async def get_contracts():
    return {"data": [], "message": "Contracts endpoint - to be implemented"}

@app.post("/api/v1/contracts/upload")
async def upload_contract():
    return {"message": "Upload endpoint - to be implemented"}

@app.post("/api/v1/chat/sessions")
async def create_chat_session():
    return {"message": "Chat session endpoint - to be implemented"}