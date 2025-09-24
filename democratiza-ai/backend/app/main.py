from fastapi import FastAPI
from app.api.v1 import auth, contracts, chat, payments
from app.config import settings

app = FastAPI(title="Democratiza AI - Contrato Seguro Platform")

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(contracts.router, prefix="/api/v1/contracts", tags=["contracts"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Democratiza AI - Contrato Seguro Platform API!"}