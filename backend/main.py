from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, contracts, chat, payments, signatures, image_processing, async_jobs, storage
from app.core.config import settings

app = FastAPI(
    title="Contrato Seguro API",
    description="API para análise inteligente de contratos brasileiros",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["contracts"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(signatures.router, prefix="/api/v1/signatures", tags=["signatures"])
app.include_router(image_processing.router, prefix="/api/v1", tags=["image-processing"])
app.include_router(async_jobs.router, prefix="/api/v1/async", tags=["async-processing"])
app.include_router(storage.router, prefix="/api/v1/storage", tags=["storage"])

@app.get("/")
async def root():
    return {
        "message": "Contrato Seguro API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
