import httpx
import asyncio
import json

async def list_gemini_models():
    url = "https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyDerKvFkArJqq524PAeW-1lhCWT7zkJIrI"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        
        print("📋 Modelos Gemini disponíveis:")
        print()
        
        for model in data.get('models', []):
            name = model.get('name', '')
            if 'gemini' in name.lower():
                display_name = model.get('displayName', '')
                supported_methods = model.get('supportedGenerationMethods', [])
                
                print(f"✅ {name}")
                print(f"   Nome: {display_name}")
                print(f"   Métodos: {', '.join(supported_methods)}")
                print()

asyncio.run(list_gemini_models())