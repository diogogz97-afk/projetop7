from fastapi import APIRouter
from backend.utils.network_monitor import NetworkMonitor
from backend.models.network import NetworkStats, CPUStats, MemoryStats, DiskStats, ProcessStats
from typing import List

router = APIRouter(prefix="/api", tags=["metrics"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@router.get("/network", response_model=List[NetworkStats])
async def get_network_stats():
    """Get network statistics"""
    return NetworkMonitor.get_network_stats()


@router.get("/cpu", response_model=CPUStats)
async def get_cpu_stats():
    """Get CPU statistics"""
    return NetworkMonitor.get_cpu_stats()


@router.get("/memory", response_model=MemoryStats)
async def get_memory_stats():
    """Get memory statistics"""
    return NetworkMonitor.get_memory_stats()


@router.get("/disk", response_model=List[DiskStats])
async def get_disk_stats():
    """Get disk statistics"""
    return NetworkMonitor.get_disk_stats()


@router.get("/processes", response_model=List[ProcessStats])
async def get_top_processes(top_n: int = 10):
    """Get top processes"""
    return NetworkMonitor.get_top_processes(top_n)


@router.get("/stats")
async def get_all_stats():
    """Get all system statistics"""
    return NetworkMonitor.get_all_stats()
