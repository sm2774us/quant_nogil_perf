import click
import pandas as pd
from quant_nogil_perf.core import RuntimeTelemetry, CoreEngineBenchmark
from quant_nogil_perf.viz import HighPerformanceVisualizer

@click.group()
def main():
    """Quant NoGIL Performance Suite CLI Orchestrator Execution Module."""
    pass

@main.command()
@click.option("--threads", default=4, help="Max thread allocation boundary.")
@click.option("--workload", default=1000000, help="Total computational loop size per thread.")
@click.option("--output", default="benchmark_output.csv", help="Target CSV output location.")
@click.option("--plot-dest", default="plots/runtime_profile.png", help="🔥 Updated target path default.")
def execute_run(threads: int, workload: int, output: str, plot_dest: str):
    """Executes a performance run on the current native Python runtime."""
    telemetry = RuntimeTelemetry.get_status()
    click.echo(f"Initializing Target Node Evaluation Context...")
    click.echo(f"Engine: CPython {telemetry['python_version']} | Mode: {telemetry['interpreter_tag']}")
    
    benchmark = CoreEngineBenchmark()
    records = []
    
    # Trace profile scaling out from single threaded to max specified boundary
    for t in range(1, threads + 1):
        click.echo(f"Processing Thread State: Count={t}...")
        duration = benchmark.run_parallel_execution(t, workload)
        records.append({
            "python_version": telemetry["python_version"],
            "interpreter_mode": telemetry["interpreter_tag"],
            "threads": t,
            "workload_size": workload,
            "execution_time": duration
        })
        
    df = pd.DataFrame(records)
    df.to_csv(output, index=False)
    click.echo(f"Metrics written successfully to disk: {output}")
    
    HighPerformanceVisualizer.plot_scaling_profile(df, telemetry["python_version"], plot_dest)
    click.echo(f"Visualizations generated successfully at: {plot_dest}")

if __name__ == "__main__":
    main()
