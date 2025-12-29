from pathlib import Path
import pandas as pd
import statsmodels.api as sm

# -------- CONFIG -------- #
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INPUT_FOLDER = PROJECT_ROOT / "A_Data" / "2_Instagram" / "2_CLEAN" #change per platform. For Tiktok: 1_Tiktok

SENTIMENT_COL = "sentiment_rulebased"
Y_COL = "engagement_score"


# -------- PARTY REGRESSION -------- #
def run_party_regression(df: pd.DataFrame, x_col: str, y_col: str):
    d = df[[x_col, y_col]].copy()
    d[x_col] = pd.to_numeric(d[x_col], errors="coerce")
    d[y_col] = pd.to_numeric(d[y_col], errors="coerce")
    d = d.dropna()

    if len(d) < 10:
        return None, d

    X = sm.add_constant(d[x_col])
    y = d[y_col]

    model = sm.OLS(y, X).fit(cov_type="HC3")

    return {
        "n": int(model.nobs),
        "beta_sentiment": float(model.params[x_col]),
        "se_hc3": float(model.bse[x_col]),
        "t_hc3": float(model.tvalues[x_col]),
        "p_hc3": float(model.pvalues[x_col]),
        "r2": float(model.rsquared),
        "intercept": float(model.params["const"]),
    }, d


# -------- RUN FOLDER -------- #
def run_folder(input_folder: Path) -> pd.DataFrame:
    rows = []
    pooled_rows = []

    for csv_path in sorted(input_folder.glob("*.csv")):
        df = pd.read_csv(csv_path)

        if SENTIMENT_COL not in df.columns or Y_COL not in df.columns:
            rows.append({"party_file": csv_path.name, "status": "missing_columns"})
            continue

        res, cleaned = run_party_regression(df, SENTIMENT_COL, Y_COL)

        if res is None:
            rows.append({"party_file": csv_path.name, "status": "too_few_rows"})
            continue

        rows.append({"party_file": csv_path.name, "status": "ok", **res})

        # collect for pooled regression
        cleaned["party_file"] = csv_path.name
        pooled_rows.append(cleaned)

    results_df = pd.DataFrame(rows)

    # -------- POOLED REGRESSION -------- #
    if pooled_rows:
        pooled_df = pd.concat(pooled_rows, ignore_index=True)

        Xp = sm.add_constant(pooled_df[SENTIMENT_COL])
        yp = pooled_df[Y_COL]

        pooled_model = sm.OLS(yp, Xp).fit(cov_type="HC3")

        pooled_row = {
            "party_file": "ALL_PARTIES_POOLED",
            "status": "ok",
            "n": int(pooled_model.nobs),
            "beta_sentiment": float(pooled_model.params[SENTIMENT_COL]),
            "se_hc3": float(pooled_model.bse[SENTIMENT_COL]),
            "t_hc3": float(pooled_model.tvalues[SENTIMENT_COL]),
            "p_hc3": float(pooled_model.pvalues[SENTIMENT_COL]),
            "r2": float(pooled_model.rsquared),
            "intercept": float(pooled_model.params["const"]),
        }

        results_df = pd.concat([results_df, pd.DataFrame([pooled_row])], ignore_index=True)

    return results_df


if __name__ == "__main__":
    results_df = run_folder(INPUT_FOLDER)

    out_path = INPUT_FOLDER / "sentiment_vs_engagement_ols_by_party_with_pooled.csv"
    results_df.to_csv(out_path, index=False)

    print(results_df.to_string(index=False))
    print(f"\nSaved: {out_path}")
