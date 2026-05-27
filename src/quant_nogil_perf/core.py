import sys
import time
import sysconfig
import hashlib
from typing import Dict, Any, List
from threading import Thread

class RuntimeTelemetry:
    """Provides low-level metadata regarding the active CPython binary compilation layers."""
    
    @staticmethod
    def get_status() -> Dict[str, Any]:
        # Recommended canonical mechanism for build determination under PEP 703
        gil_disabled_var = sysconfig.get_config_var("Py_GIL_DISABLED")
        
        # Check runtime state flag (introduced in recent iterations)
        runtime_disabled = False
        if hasattr(sys, "_is_gil_enabled"):
            runtime_disabled = not sys._is_gil_enabled()
        elif gil_disabled_var == 1:
            runtime_disabled = True

        return {
            "python_version": sys.version.split()[0],
            "compiled_no_gil": gil_disabled_var == 1,
            "runtime_gil_disabled": runtime_disabled,
            "interpreter_tag": "free-threaded (t)" if runtime_disabled else "standard (gil)"
        }

class CoreEngineBenchmark:
    """Executes deterministic, thread-isolated workloads to measure lock contention."""
    
    @staticmethod
    def pure_cpu_workload(iterations: int) -> str:
        """
        Pure CPU-bound task using standard cryptographic cascading functions.
        Forces allocations within the evaluator loop to expose allocation lock overheads.
        """
        state = b"alpha_generation_vector_seed_data_node_0xDEADBEEF"
        for _ in range(iterations):
            state = hashlib.sha256(state).digest()
        return state.hex()

    def run_parallel_execution(self, thread_count: int, workload_size: int) -> float:
        """Spawns system threads, executing tasks concurrently across the OS topology."""
        threads: List[Thread] = []
        for _ in range(thread_count):
            t = Thread(target=self.pure_cpu_workload, args=(workload_size,))
            threads.append(t)
            
        start_time = time.perf_counter()
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            
        end_time = time.perf_counter()
        return end_time - start_time
