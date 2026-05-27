import pytest
import pandas as pd
from pathlib import Path
from quant_nogil_perf.viz import HighPerformanceVisualizer

@pytest.fixture
def sample_metrics_dataframe() -> pd.DataFrame:
    """Provides a standardized data table with clean datatypes to populate charting test contexts."""
    return pd.DataFrame([
        {"python_version": "v3.13", "interpreter_mode": "standard (gil)", "threads": 1, "execution_time": 1.5},
        {"python_version": "v3.13", "interpreter_mode": "standard (gil)", "threads": 2, "execution_time": 3.0},
        {"python_version": "v3.14", "interpreter_mode": "free-threaded (t)", "threads": 1, "execution_time": 1.6},
        {"python_version": "v3.14", "interpreter_mode": "free-threaded (t)", "threads": 2, "execution_time": 1.7},
    ])

def test_ensure_directory_creates_missing_folders(tmp_path: Path):
    """Verifies that _ensure_directory_exists uses pathlib to build missing directories safely."""
    nested_target_file = tmp_path / "deep" / "nested" / "plots" / "test_chart.png"
    assert not nested_target_file.parent.exists()
    
    HighPerformanceVisualizer._ensure_directory_exists(str(nested_target_file))
    assert nested_target_file.parent.exists()

def test_plot_scaling_profile_generation(tmp_path: Path, sample_metrics_dataframe: pd.DataFrame):
    """Ensures line charts are built, styled, and saved to disk properly."""
    target_plot = tmp_path / "plots" / "scaling_profile.png"
    
    HighPerformanceVisualizer.plot_scaling_profile(
        results_df=sample_metrics_dataframe,
        target_version="3.14",
        output_path=str(target_plot)
    )
    
    assert target_plot.exists()
    assert target_plot.stat().st_size > 0

def test_plot_cross_version_comparison_generation(tmp_path: Path, sample_metrics_dataframe: pd.DataFrame):
    """Ensures comparative bar charts generate correctly and resolve internal styling logic."""
    target_plot = tmp_path / "plots" / "cross_matrix.png"
    
    HighPerformanceVisualizer.plot_cross_version_comparison(
        results_df=sample_metrics_dataframe,
        output_path=str(target_plot)
    )
    
    assert target_plot.exists()
    assert target_plot.stat().st_size > 0