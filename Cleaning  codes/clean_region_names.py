import pandas as pd
import unicodedata

rules = {
        "yasamal": "bakı şəhəri yasamal rayonu",
        "binəqədi": "bakı şəhəri binəqədi rayonu",
        "xətai": "bakı şəhəri xətai rayonu",
        "nərimanov": "bakı şəhəri nərimanov rayonu",
        "qaradağ": "bakı şəhəri qaradağ rayonu",
        "naxçıvan şəhəri": "naxçıvan şəhəri",
        "şəmkir": "şəmkir rayonu",
        "yevlax": "yevlax rayonu",
        "şəki": "şəki rayonu",
        "qubadli": "qubadlı rayonu",
        "laçin": "laçın rayonu",
        "lənkəran": "lənkəran rayonu",
        "masalli": "masallı rayonu",
        "cəbrayil": "cəbrayıl rayonu",
        "xanlar": "göygöl rayonu",
        "dəvəçi": "şabran rayonu",
        "səbayel": "bakı şəhəri səbail rayonu",
        "türk liseyləri": "xocavənd rayonu",
        "əli-bayramlı": "şirvan şəhəri",
        "şuşa": "şuşa şəhəri",
        "naxçivan şəhəri̇": "naxçıvan şəhəri",
        "naxçivan mr culfa rayonu": "naxçıvan mr culfa rayonu"
    }


def normalize_text(s):
    if pd.isna(s):
        return s
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()

def replacing(df, col_name):
    # Şəhər və rayonu əvəz et
    df[col_name] = (
        df[col_name]
        .str.lower()
        .str.replace("baki ş.", "bakı şəhəri", regex=False)
        .str.replace("ray.", "rayonu", regex=False)
        .str.replace("bakı ş.", "bakı şəhəri", regex=False)
        .str.strip()
    )

    # Qaydalara uyğun dəyişiklik
    for key, value in rules.items():
        key_norm = normalize_text(key)
        mask = df[col_name].apply(normalize_text).str.contains(key_norm, na=False)
        df.loc[mask, col_name] = value

    # Bütün sətrlər kiçik hərflə
    df[col_name] = df[col_name].str.lower()
    
    return df
