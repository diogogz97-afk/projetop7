import psutil
from datetime import datetime
from typing import Dict, List
from backend.models.network import (
    NetworkStats, CPUStats, MemoryStats, 
    DiskStats, ProcessStats
)


class NetworkMonitor:
    """Monitor system network, CPU, memory, and disk resources"""
    
    @staticmethod
    def get_network_stats(interface: str = None) -> List[NetworkStats]:
        """Get network statistics"""
        try:
            stats = psutil.net_if_stats()
            io_counters = psutil.net_io_counters(pernic=True)
            
            result = []
            for iface, counters in io_counters.items():
                if interface and iface != interface:
                    continue
                    
                result.append(NetworkStats(
                    timestamp=datetime.now(),
                    interface=iface,
                    bytes_sent=counters.bytes_sent,
                    bytes_recv=counters.bytes_recv,
                    packets_sent=counters.packets_sent,
                    packets_recv=counters.packets_recv,
                    errin=counters.errin,
                    errout=counters.errout,
                    dropin=counters.dropin,
                    dropout=counters.dropout
                ))
            return result
        except Exception as e:
            print(f"Error getting network stats: {e}")
            return []
    
    @staticmethod
    def get_cpu_stats() -> CPUStats:
        """Get CPU statistics"""
        try:
            return CPUStats(
                timestamp=datetime.now(),
                percent=psutil.cpu_percent(interval=1),
                count=psutil.cpu_count(),
                freq=psutil.cpu_freq().current if psutil.cpu_freq() else 0
            )
        except Exception as e:
            print(f"Error getting CPU stats: {e}")
            return None
    
    @staticmethod
    def get_memory_stats() -> MemoryStats:
        """Get memory statistics"""
        try:
            mem = psutil.virtual_memory()
            return MemoryStats(
                timestamp=datetime.now(),
                total=mem.total,
                available=mem.available,
                percent=mem.percent,
                used=mem.used,
                free=mem.free
            )
        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return None
    
    @staticmethod
    def get_disk_stats() -> List[DiskStats]:
        """Get disk statistics"""
        try:
            partitions = psutil.disk_partitions()
            result = []
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    result.append(DiskStats(
                        timestamp=datetime.now(),
                        device=partition.device,
                        total=usage.total,
                        used=usage.used,
                        free=usage.free,
                        percent=usage.percent,
                        mountpoint=partition.mountpoint
                    ))
                except PermissionError:
                    continue
            
            return result
        except Exception as e:
            print(f"Error getting disk stats: {e}")
            return []
    
    @staticmethod
    def get_top_processes(top_n: int = 10) -> List[ProcessStats]:
        """Get top processes by CPU and memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'username': proc_info['username'],
                        'cpu_percent': proc_info['cpu_percent'] or 0,
                        'memory_percent': proc_info['memory_percent'] or 0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by memory usage
            sorted_procs = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:top_n]
            
            result = []
            for proc in sorted_procs:
                try:
                    p = psutil.Process(proc['pid'])
                    result.append(ProcessStats(
                        timestamp=datetime.now(),
                        pid=proc['pid'],
                        name=proc['name'],
                        username=proc['username'] or 'N/A',
                        cpu_percent=proc['cpu_percent'],
                        memory_percent=proc['memory_percent'],
                        memory_rss=p.memory_info().rss,
                        num_threads=p.num_threads(),
                        status=p.status()
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return result
        except Exception as e:
            print(f"Error getting top processes: {e}")
            return []
    
    @staticmethod
    def get_all_stats() -> Dict:
        """Get all system statistics"""
        return {
            'network': NetworkMonitor.get_network_stats(),
            'cpu': NetworkMonitor.get_cpu_stats(),
            'memory': NetworkMonitor.get_memory_stats(),
            'disk': NetworkMonitor.get_disk_stats(),
            'processes': NetworkMonitor.get_top_processes()
        }
