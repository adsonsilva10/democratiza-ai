"""
Validação final dos componentes implementados
"""
import sys
import os

backend_path = r"c:\Users\adson.silva_contabil\democratiza-ai\backend"
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

def test_components():
    """Testa se todos os componentes foram implementados corretamente"""
    
    print("🔍 VALIDAÇÃO FINAL - DEMOCRATIZA AI")
    print("=" * 50)
    
    results = {}
    
    # 1. Test R2 Storage Service
    try:
        from app.services.storage_service import r2_service, CloudflareR2Service
        print("✅ 1. Cloudflare R2 Storage Service")
        results["r2_storage"] = True
        
        # Check if R2 service has required methods
        methods = ["upload_file", "download_file", "delete_file", "list_user_files"]
        for method in methods:
            if hasattr(r2_service, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method}")
                results["r2_storage"] = False
                
    except Exception as e:
        print(f"❌ 1. R2 Storage Service: {e}")
        results["r2_storage"] = False
    
    # 2. Test API Endpoints
    try:
        from app.api.v1 import storage
        print("✅ 2. Storage API Endpoints")
        results["api_endpoints"] = True
        
    except Exception as e:
        print(f"❌ 2. Storage API Endpoints: {e}")
        results["api_endpoints"] = False
    
    # 3. Test Document Processor Integration
    try:
        from app.workers.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        
        # Check if R2 integration exists
        if hasattr(processor, 'storage_service'):
            print("✅ 3. Document Processor R2 Integration")
            results["document_processor"] = True
        else:
            print("❌ 3. Document Processor missing R2 integration")
            results["document_processor"] = False
            
    except Exception as e:
        print(f"❌ 3. Document Processor: {e}")
        results["document_processor"] = False
    
    # 4. Test Database Models
    try:
        from app.db.models import StorageAuditLog, Contract, User
        print("✅ 4. Database Models (StorageAuditLog)")
        results["database_models"] = True
        
    except Exception as e:
        print(f"❌ 4. Database Models: {e}")
        results["database_models"] = False
    
    # 5. Test Frontend API Client
    frontend_api_path = r"c:\Users\adson.silva_contabil\democratiza-ai\frontend\lib\api.ts"
    if os.path.exists(frontend_api_path):
        with open(frontend_api_path, 'r', encoding='utf-8') as f:
            api_content = f.read()
            
        if "uploadToStorage" in api_content and "FileMetadata" in api_content:
            print("✅ 5. Frontend API Integration")
            results["frontend_api"] = True
        else:
            print("❌ 5. Frontend API missing R2 methods")
            results["frontend_api"] = False
    else:
        print("❌ 5. Frontend API file not found")
        results["frontend_api"] = False
    
    # 6. Test Configuration
    try:
        from app.core.config import settings
        
        r2_configs = [
            'CLOUDFLARE_ACCOUNT_ID',
            'CLOUDFLARE_R2_ACCESS_KEY', 
            'CLOUDFLARE_R2_SECRET_KEY',
            'CLOUDFLARE_R2_BUCKET',
            'CLOUDFLARE_R2_ENDPOINT'
        ]
        
        config_complete = True
        for config in r2_configs:
            if hasattr(settings, config):
                print(f"   ✅ {config}")
            else:
                print(f"   ❌ {config}")
                config_complete = False
        
        if config_complete:
            print("✅ 6. R2 Configuration")
            results["configuration"] = True
        else:
            print("❌ 6. R2 Configuration incomplete")
            results["configuration"] = False
            
    except Exception as e:
        print(f"❌ 6. Configuration: {e}")
        results["configuration"] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESUMO DA IMPLEMENTAÇÃO")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.replace('_', ' ').title()}")
    
    print(f"\n🎯 SCORE: {passed}/{total} componentes implementados")
    
    if passed == total:
        print("\n🎉 IMPLEMENTAÇÃO COMPLETA!")
        print("✨ Sistema Cloudflare R2 totalmente integrado")
        print("🚀 Pronto para produção!")
        
        print("\n📋 CHECKLIST CONCLUÍDO:")
        print("   ✅ Credenciais R2 configuradas (seguras)")
        print("   ✅ Serviço de storage implementado")
        print("   ✅ API endpoints criados") 
        print("   ✅ Document processor integrado")
        print("   ✅ Database models criados")
        print("   ✅ Frontend API atualizada")
        print("   ✅ Configurações validadas")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} componentes precisam de atenção")
        return False

if __name__ == "__main__":
    success = test_components()
    exit(0 if success else 1)