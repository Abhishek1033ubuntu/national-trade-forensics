import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")

def plot_benford_distribution(obs_counts: pd.Series, chi_square: float, save_path: str = None):
    total = obs_counts.sum()
    obs_pct = (obs_counts / total * 100) if total > 0 else obs_counts
    exp_pct = [np.log10(1 + 1/d) * 100 for d in range(1, 10)]
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    digits = np.arange(1, 10)
    
    ax.bar(digits - 0.175, obs_pct, 0.35, label='Observed Trade Data', color='#1f77b4', alpha=0.85)
    ax.plot(digits, exp_pct, color='#d62728', marker='o', linewidth=2.5, label="Benford's Curve")
    
    ax.set_title(f"Benford's Law First-Digit Analysis\nChi-Square Statistic = {chi_square:.4f} (Critical Threshold = 15.507)", fontweight='bold')
    ax.set_xlabel("First Leading Digit (1-9)")
    ax.set_ylabel("Frequency (%)")
    ax.set_xticks(digits)
    ax.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

def plot_unit_value_dispersion(audit_df: pd.DataFrame, save_path: str = None):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    group_col = 'cmd_code' if 'cmd_code' in audit_df.columns else 'period'
    
    sns.boxplot(
        data=audit_df,
        x=group_col,
        y='unit_value',
        ax=ax,
        palette='Set2',
        showfliers=True,
        flierprops=dict(marker='o', color='red', markersize=6)
    )
    
    ax.set_yscale('log')
    ax.set_title("Unit Value Dispersion by Commodity ($/kg, Log Scale)", fontweight='bold')
    ax.set_xlabel("Commodity / Chapter Code")
    ax.set_ylabel("Unit Value (USD / kg, Log Scale)")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
