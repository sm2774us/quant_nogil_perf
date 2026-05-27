import pytest
import pandas as pd
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import patch
from quant_nogil_perf.cli import main

def test_cli_help_menu_trigger():
    """Verifies the base CLI entrypoint runs correctly and surfaces instruction parameters."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Quant NoGIL Performance Suite" in result.output

def test_cli_execute_run_command_pathway(tmp_path: Path):
    """Tests execution pathways by mocking calculations to quickly check log outputs and file creation."""
    csv_output = tmp_path / "output_metrics.csv"
    png_output = tmp_path / "plots" / "test_profile.png"
    
    runner = CliRunner()
    
    # Invoke execute-run specifying precise temporary destination targets
    result = runner.invoke(main, [
        "execute-run",
        "--threads", "2",
        "--workload", "1000",
        "--output", str(csv_output),
        "--plot-dest", str(png_output)
    ])
    
    assert result.exit_code == 0
    assert "Initializing Target Node Evaluation Context..." in result.output
    assert "Metrics written successfully to disk" in result.output
    
    # Confirm physical file serialization occurred
    assert csv_output.exists()
    assert png_output.exists()
    
    # Verify the structure of the exported CSV data
    df = pd.read_csv(csv_output)
    assert "python_version" in df.columns
    assert "interpreter_mode" in df.columns
    assert len(df) == 2  # Threads traced from 1 up to 2