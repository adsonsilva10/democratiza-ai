"""
Minimal FastAPI test to check imports
"""
from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
def root():
    return {"message": "Test API working"}

@app.get("/health") 
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("✅ Imports working correctly!")
    print("✅ FastAPI app created successfully!")
    print("🚀 Ready to test full application!")