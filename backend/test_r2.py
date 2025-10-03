"""
Teste direto da conexão com Cloudflare R2
"""
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def test_r2_connection():
    """Testa conexão direta com R2"""
    
    # Credenciais do .env.private
    CLOUDFLARE_R2_ACCESS_KEY = "6044cd4d9920ca747054dd3eed4eb209"
    CLOUDFLARE_R2_SECRET_KEY = "53bc25cc8f6eaa6319712de23239f9d7159e5b2ed4a4a9ab8dedba3d8acb7a14"
    CLOUDFLARE_R2_ENDPOINT = "https://8445c60c25a2de79dcc7c5ccd322626a.r2.cloudflarestorage.com"
    CLOUDFLARE_R2_BUCKET = "democratiza-ai-contracts"

    print("🔗 Testando conexão com Cloudflare R2...")
    print(f"   Endpoint: {CLOUDFLARE_R2_ENDPOINT}")
    print(f"   Bucket: {CLOUDFLARE_R2_BUCKET}")
    print()

    try:
        # Criar cliente S3-compatível para R2
        s3_client = boto3.client(
            's3',
            endpoint_url=CLOUDFLARE_R2_ENDPOINT,
            aws_access_key_id=CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=CLOUDFLARE_R2_SECRET_KEY,
            config=Config(
                region_name='auto',
                retries={'max_attempts': 3},
                max_pool_connections=50
            )
        )
        
        print("✅ Cliente R2 criado com sucesso")
        
        # Testar acesso ao bucket
        print("🪣 Testando acesso ao bucket...")
        try:
            response = s3_client.head_bucket(Bucket=CLOUDFLARE_R2_BUCKET)
            print("✅ SUCESSO: Bucket encontrado e acessível!")
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print("⚠️  Bucket não existe. Tentando criar...")
                try:
                    s3_client.create_bucket(Bucket=CLOUDFLARE_R2_BUCKET)
                    print("✅ SUCESSO: Bucket criado!")
                except ClientError as create_error:
                    print(f"❌ ERRO ao criar bucket: {create_error}")
                    return False
            else:
                print(f"❌ ERRO ao acessar bucket: {e}")
                return False
        
        # Listar objetos existentes
        print("📄 Listando objetos no bucket...")
        try:
            response = s3_client.list_objects_v2(
                Bucket=CLOUDFLARE_R2_BUCKET, 
                MaxKeys=5
            )
            
            if 'Contents' in response:
                print(f"   Encontrados {len(response['Contents'])} objetos:")
                for obj in response['Contents']:
                    print(f"   📄 {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("   📂 Bucket vazio (normal para novo setup)")
                
        except Exception as list_error:
            print(f"❌ ERRO ao listar objetos: {list_error}")
            return False
        
        print()
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("   ✅ Conexão estabelecida")
        print("   ✅ Credenciais válidas")  
        print("   ✅ Bucket acessível")
        print("   ✅ Operações básicas funcionando")
        return True
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO na conexão: {str(e)}")
        import traceback
        print("\nDetalhes do erro:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_r2_connection()
    exit(0 if success else 1)