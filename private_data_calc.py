import pandas as pd
import numpy as np

def email_map(email_format: str) -> str:
    """
    Map email address format string to more restricted format string where only '@' and '.' are preserved.
    """
    mapped_format = ''
    for ch in email_format:
        if ch in ['@', '.']:
            mapped_format += ch
        else:
            mapped_format += 'x'
    return mapped_format

def name_map(name: str) -> str:
    """
    Map name format string to more restricted format string where only spaces (underscores) are preserved.
    """
    mapped_name = ''
    for ch in name:
        if ch == '_':
            mapped_name += ch
        else:
            mapped_name += 'x'
    return mapped_name

def city_map(city: str) -> str:
    """
    Map city format string to more restricted format string where only spaces (underscores) are preserved.
    """
    mapped_city = ''
    for ch in city:
        if ch == '_':
            mapped_city += ch
        else:
            mapped_city += 'x'
    return mapped_city

def address_map(address: str) -> str:
    """
    Map address format string to more restricted format string where only spaces (underscores) are preserved.
    """
    mapped_address = ''
    for ch in address:
        if ch == '_':
            mapped_address += ch
        else:
            mapped_address += 'x'
    return mapped_address

def re_format(df: pd.DataFrame, map_func) -> pd.DataFrame:
    """
    Reformat the 'Format property string' column of the dataframe using the provided mapping function.
    The 'Count' column is converted to numeric and aggregated by the reformatted 'Format property string'.
    Args:
        df (pd.DataFrame): Input dataframe with 'Format property string' and 'Count' columns.
        map_func (function): Mapping function to apply to the 'Format property string' column.
    Returns:
        pd.DataFrame: Reformatted dataframe with aggregated counts.
    """
    formatted = df.dropna(subset=['Format property string']).copy()
    formatted['Format property string'] = formatted['Format property string'].astype(str).apply(map_func)
    formatted['Count'] = pd.to_numeric(formatted['Count'], errors='coerce').fillna(0) 
    return (
        formatted
        .groupby('Format property string', as_index=False)['Count']
        .sum()
        .sort_values('Count', ascending=False)
        .reset_index(drop=True)
    )

def get_map_function(sheet_name: str):
    key = sheet_name.strip().lower()
    if 'mail' in key:
        return email_map
    if 'address' in key:
        return address_map
    if 'city' in key:
        return city_map
    if 'name' in key:
        return name_map
    return None


if __name__ == "__main__":
    
    # Read all four sheets and combine into one dataframe
    sheets = pd.read_excel("Raw Data/private_data.xlsx",
                           sheet_name=None,
                           usecols=[0,1],
                           header=0)

    rows = {}
    for sheet_name, df in sheets.items():
        map_func = get_map_function(sheet_name)
        
        formatted_df = re_format(df, map_func)

        count_series = formatted_df['Count'].dropna()
        count_values = count_series.to_numpy(dtype=float)
        total_count = count_values.sum()
        distinct_count = len(count_values)
        unique_count = count_series.eq(1).sum()
        pct = (unique_count / total_count * 100) if total_count > 0 else 0.0
        p_f = count_values / total_count

        # Only format-class counts are available, so the prior is uniform over the
        # records (every record is treated as a distinct, equally likely plaintext).
        h_x = np.log2(total_count)
        mutual_information = -np.sum(p_f * np.log2(p_f))
        min_leakage_uniform = np.log2(distinct_count)

        rows[sheet_name] = {
            "Total": total_count,
            "Distinct": distinct_count,
            "Unique": unique_count,
            "Pct": pct,
            "I(X;F)": mutual_information,
            "H_inf": h_x,
            "L_inf": min_leakage_uniform,
        }

    statistics = pd.DataFrame.from_dict(rows, orient="index")
    statistics = statistics.astype({"Total": int, "Distinct": int, "Unique": int, "Pct": float,
                                    "I(X;F)": float, "H_inf": float, "L_inf": float})
    print(statistics.round(2))