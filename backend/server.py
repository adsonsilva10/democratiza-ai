from fastapi import FastAPI

app = FastAPI(title="Democratiza AI Backend")

@app.get("/")
def read_root():
    return {"message": "Democratiza AI Backend is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}