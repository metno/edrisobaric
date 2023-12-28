"""App1.py"""
import uvicorn
from fastapi import FastAPI


app = FastAPI()

def create_landing_page():
    """Create content."""
    return "Hello"

@app.get("/")
async def get_landing_page():
    """Link path to function."""
    return create_landing_page()

if __name__ == "__main__":
    uvicorn.run("app1:app",
                host='0.0.0.0',
                port=5000)
