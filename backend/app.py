from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.config import settings
from backend.routes.api import router

# Create FastAPI app
app = FastAPI(
    title="Network Dashboard API",
    description="Advanced Network Monitoring Dashboard API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Network Dashboard API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "backend.app:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.debug
    )
