import pandas as pd
import numpy as np

def _calc_mad_zscore(group: pd.DataFrame) -> pd.DataFrame:
    median = group['unit_value'].median()
    mad = (group['unit_value'] - median).abs().median()
    if mad == 0:
        mad = 1e-6
    group['mad_zscore'] = (group['unit_value'] - median) / (1.4826 * mad)
    return group

def run_unit_value_audit(df: pd.DataFrame, threshold: float = 2.5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes $/kg unit values and flags anomalies exceeding Z_MAD threshold.
    """
    audit_df = df.dropna(subset=['trade_value_usd', 'net_weight_kg']).copy()
    audit_df = audit_df[(audit_df['trade_value_usd'] > 0) & (audit_df['net_weight_kg'] > 0)]
    audit_df['unit_value'] = audit_df['trade_value_usd'] / audit_df['net_weight_kg']

    if 'cmd_code' in audit_df.columns:
        audit_df = audit_df.groupby('cmd_code', group_keys=False).apply(_calc_mad_zscore)
    else:
        audit_df = _calc_mad_zscore(audit_df)

    anomalies = audit_df[audit_df['mad_zscore'].abs() > threshold]
    return audit_df, anomalies

def run_benford_test(df: pd.DataFrame) -> tuple[float, pd.Series, list]:
    """
    Executes Chi-Square goodness-of-fit test against Benford's Law distribution.
    """
    valid_values = df['trade_value_usd'].dropna()
    leading_digits = valid_values.astype(str).str.lstrip('0.').str[0]
    valid_digits = leading_digits[leading_digits.isin([str(i) for i in range(1, 10)])]

    obs_counts = valid_digits.value_counts().reindex([str(i) for i in range(1, 10)], fill_value=0)
    total_count = len(valid_digits)
    
    if total_count == 0:
        return 0.0, obs_counts, []

    exp_counts = [np.log10(1 + 1/d) * total_count for d in range(1, 10)]
    chi_square = float(np.sum((obs_counts - exp_counts)**2 / exp_counts))

    return chi_square, obs_counts, exp_counts
