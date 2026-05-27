import sys
import sysconfig
import pytest
from unittest.mock import patch, MagicMock
from quant_nogil_perf.core import RuntimeTelemetry, CoreEngineBenchmark

def test_runtime_telemetry_with_is_gil_enabled_true():
    """Tests status mapping when sys._is_gil_enabled() indicates the GIL is fully active."""
    with patch.object(sys, "_is_gil_enabled", return_value=True, create=True), \
         patch.object(sysconfig, "get_config_var", return_value=0):
        
        status = RuntimeTelemetry.get_status()
        assert status["compiled_no_gil"] is False
        assert status["runtime_gil_disabled"] is False
        assert status["interpreter_tag"] == "standard (gil)"

def test_runtime_telemetry_with_is_gil_enabled_false():
    """Tests status mapping when sys._is_gil_enabled() indicates the GIL is deactivated."""
    with patch.object(sys, "_is_gil_enabled", return_value=False, create=True), \
         patch.object(sysconfig, "get_config_var", return_value=1):
        
        status = RuntimeTelemetry.get_status()
        assert status["compiled_no_gil"] is True
        assert status["runtime_gil_disabled"] is True
        assert status["interpreter_tag"] == "free-threaded (t)"

def test_runtime_telemetry_fallback_gil_disabled():
    """Tests the fallback path when sys._is_gil_enabled doesn't exist but Py_GIL_DISABLED == 1."""
    with patch.object(sys, "_is_gil_enabled", create=True) as mock_sys:
        if hasattr(sys, "_is_gil_enabled"):
            del sys._is_gil_enabled  # Force deletion for total branch testing isolation
            
        with patch.object(sysconfig, "get_config_var", return_value=1):
            status = RuntimeTelemetry.get_status()
            assert status["compiled_no_gil"] is True
            assert status["runtime_gil_disabled"] is True
            assert status["interpreter_tag"] == "free-threaded (t)"

def test_runtime_telemetry_fallback_gil_enabled():
    """Tests the fallback path when sys._is_gil_enabled doesn't exist and Py_GIL_DISABLED is clear."""
    with patch.object(sys, "_is_gil_enabled", create=True) as mock_sys:
        if hasattr(sys, "_is_gil_enabled"):
            del sys._is_gil_enabled
            
        with patch.object(sysconfig, "get_config_var", return_value=0):
            status = RuntimeTelemetry.get_status()
            assert status["compiled_no_gil"] is False
            assert status["runtime_gil_disabled"] is False
            assert status["interpreter_tag"] == "standard (gil)"

def test_benchmark_workload_determinism():
    """Validates the cryptographic hashing function executes correctly and outputs expected lengths."""
    engine = CoreEngineBenchmark()
    res_a = engine.pure_cpu_workload(10)
    res_b = engine.pure_cpu_workload(10)
    assert isinstance(res_a, str)
    assert len(res_a) == 64  # SHA-256 output length check
    assert res_a == res_b

def test_parallel_execution_threading():
    """Ensures parallel orchestrations terminate accurately and yield precise duration data."""
    engine = CoreEngineBenchmark()
    duration = engine.run_parallel_execution(thread_count=2, workload_size=100)
    assert isinstance(duration, float)
    assert duration > 0.0