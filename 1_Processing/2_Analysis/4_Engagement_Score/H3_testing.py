from pathlib import Path
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col

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

def export_pooled_and_fdp_analysis(input_folder: Path):

    pooled_data = []
    fdp_data = []

    for csv_path in sorted(input_folder.glob("*.csv")):
        df = pd.read_csv(csv_path)

        if SENTIMENT_COL not in df.columns or Y_COL not in df.columns:
            continue

        d = df[[SENTIMENT_COL, Y_COL]].copy()
        d[SENTIMENT_COL] = pd.to_numeric(d[SENTIMENT_COL], errors="coerce")
        d[Y_COL] = pd.to_numeric(d[Y_COL], errors="coerce")
        d = d.dropna()

        if len(d) < 10:
            continue

        pooled_data.append(d)

        if "FDP" in csv_path.name.upper():
            fdp_data.append(d)

    pooled_df = pd.concat(pooled_data, ignore_index=True)

    if not fdp_data:
        raise ValueError("No FDP files found – filename must contain 'FDP'")
    fdp_df = pd.concat(fdp_data, ignore_index=True)

    Xp = sm.add_constant(pooled_df[SENTIMENT_COL])
    yp = pooled_df[Y_COL]
    pooled_model = sm.OLS(yp, Xp).fit(cov_type="HC3")

    Xf = sm.add_constant(fdp_df[SENTIMENT_COL])
    yf = fdp_df[Y_COL]
    fdp_model = sm.OLS(yf, Xf).fit(cov_type="HC3")

    # ---------- REGRESSION TABLE ----------
    table = summary_col(
        [pooled_model, fdp_model],
        model_names=["All Parties Pooled", "FDP"],
        stars=True,
        info_dict={
            "N": lambda x: f"{int(x.nobs)}",
            "R2": lambda x: f"{x.rsquared:.3f}"
        }
    )

    table_path = input_folder / "regression_table_pooled_vs_fdp.txt"
    with open(table_path, "w") as f:
        f.write(table.as_text())

    print("\n=== REGRESSION TABLE ===\n")
    print(table)

    # ---------- PLOT ----------
    plt.figure(figsize=(8, 5))

    plt.scatter(pooled_df[SENTIMENT_COL], pooled_df[Y_COL], alpha=0.2, label="All Parties")
    xs = pd.Series(sorted(pooled_df[SENTIMENT_COL]))
    plt.plot(xs, pooled_model.params["const"] + pooled_model.params[SENTIMENT_COL] * xs)

    plt.scatter(fdp_df[SENTIMENT_COL], fdp_df[Y_COL], alpha=0.4, label="FDP")
    xs_f = pd.Series(sorted(fdp_df[SENTIMENT_COL]))
    plt.plot(xs_f, fdp_model.params["const"] + fdp_model.params[SENTIMENT_COL] * xs_f)

    plt.xlabel("Sentiment")
    plt.ylabel("Engagement Score")
    plt.title("Sentiment vs Engagement – All Parties vs FDP")
    plt.legend()

    plot_path = input_folder / "sentiment_vs_engagement"


if __name__ == "__main__":
    results_df = run_folder(INPUT_FOLDER)

    out_path = INPUT_FOLDER / "sentiment_vs_engagement_ols_by_party_with_pooled.csv"
    results_df.to_csv(out_path, index=False)
    export_pooled_and_fdp_analysis(INPUT_FOLDER)


    print(results_df.to_string(index=False))
    print(f"\nSaved: {out_path}")
