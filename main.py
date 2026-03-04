import uvicorn
from app import create_app
from dotenv import load_dotenv

# Create FastAPI app
app = create_app()


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
