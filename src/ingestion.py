import os
import pandas as pd

def load_trade_data(file_path: str) -> pd.DataFrame:
    """
    Loads trade data from a local CSV or Excel file and standardizes schema.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Target data file not found: {file_path}")
        
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, sep=None, engine='python')
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
    # Standardize column naming
    cols_map = {str(c).strip().lower(): c for c in df.columns}
    
    val_col = next((cols_map[k] for k in cols_map if any(v in k for v in ['val', 'usd', 'value', 'amount'])), None)
    qty_col = next((cols_map[k] for k in cols_map if any(q in q for q in ['qty', 'weight', 'netwgt', 'kg'])), None)
    cmd_col = next((cols_map[k] for k in cols_map if any(c in c for c in ['cmd', 'hs', 'code', 'chapter'])), None)
    
    renames = {}
    if val_col: renames[val_col] = 'trade_value_usd'
    if qty_col: renames[qty_col] = 'net_weight_kg'
    if cmd_col: renames[cmd_col] = 'cmd_code'
    
    df = df.rename(columns=renames)
    
    # Ensure numeric conversion
    if 'trade_value_usd' in df.columns:
        df['trade_value_usd'] = pd.to_numeric(df['trade_value_usd'].astype(str).str.replace(',', ''), errors='coerce')
    if 'net_weight_kg' in df.columns:
        df['net_weight_kg'] = pd.to_numeric(df['net_weight_kg'].astype(str).str.replace(',', ''), errors='coerce')
        
    return df
