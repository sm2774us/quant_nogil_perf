from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class HighPerformanceVisualizer:
    """Generates crisp, publication-grade analytical charts for quantitative review."""
    
    @staticmethod
    def configure_engine_style():
        sns.set_theme(style="whitegrid", context="talk")
        plt.rcParams.update({
            "font.family": "sans-serif",
            "figure.figsize": (11, 6),
            "axes.edgecolor": "#111111",
            "axes.linewidth": 1.2
        })

    @classmethod
    def _ensure_directory_exists(cls, file_path: str):
        """Extracts target base path parameters and enforces directory creation via pathlib."""
        # Instantiates a pure Path object, isolates the parent folder component,
        # and recursively generates missing folder segments in a single, atomic step.
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def plot_scaling_profile(cls, results_df: pd.DataFrame, target_version: str, output_path: str = "plots/scaling_profile.png"):
        """Plots execution time as a function of thread scaling."""
        cls.configure_engine_style()
        cls._ensure_directory_exists(output_path)  # 🔥 Pathlib runtime intercept verification
        
        fig, ax = plt.subplots()
        
        sns.lineplot(
            data=results_df,
            x="threads",
            y="execution_time",
            hue="interpreter_mode",
            marker="o",
            linewidth=2.5,
            markersize=8,
            palette={"standard (gil)": "#D95F02", "free-threaded (t)": "#1B9E77"},
            ax=ax
        )
        
        ax.set_title(f"CPython {target_version} Multi-Threaded Scalability Profile", pad=20, weight="bold")
        ax.set_xlabel("Concurrent Thread Volume (Worker Pool)", labelpad=10)
        ax.set_ylabel("Execution Time (Seconds)", labelpad=10)
        ax.legend(title="Runtime Engine State")
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

    @classmethod
    def plot_cross_version_comparison(cls, results_df: pd.DataFrame, output_path: str = "plots/cross_version_matrix.png"):
        """Generates cross-version performance matrix visualizations."""
        cls.configure_engine_style()
        cls._ensure_directory_exists(output_path)  # 🔥 Pathlib runtime intercept verification
        
        fig, ax = plt.subplots()
        results_df["Runtime Identifier"] = results_df["python_version"] + " " + results_df["interpreter_mode"]
        
        sns.barplot(
            data=results_df,
            x="threads",
            y="execution_time",
            hue="Runtime Identifier",
            palette="Deep",
            ax=ax,
            edgecolor="black",
            linewidth=1.0
        )
        
        ax.set_title("Cross-Generational Parallel Performance Evaluation (3.13 vs 3.14)", pad=20, weight="bold")
        ax.set_xlabel("Thread Scale Count", labelpad=10)
        ax.set_ylabel("Total Latency / Execution Time (Seconds)", labelpad=10)
        ax.legend(title="Engine Profiles")
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()