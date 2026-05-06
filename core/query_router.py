import pandas as pd


def run_prompt(prompt, df):

    if "ELIGIBILITYYEARANDMONTH" in df.columns:
        df["MONTH"] = df["ELIGIBILITYYEARANDMONTH"].astype(str)

    if prompt == "Monthly Total Cost Trend":
        return (
            df.groupby(["MONTH", "GROUP"])["PAID"]
            .sum().reset_index()
            .rename(columns={"PAID": "Value"})
        )

    if prompt == "Total Cost by Line of Business":
        return (
            df.groupby(["LINEOFBUSINESS", "GROUP"])["PAID"]
            .sum().reset_index()
            .rename(columns={"LINEOFBUSINESS": "Dimension", "PAID": "Value"})
        )

    if prompt == "Pareto Cost Analysis (Top 5%)":
        agg = (
            df.groupby(["MEMBER_ID", "GROUP"])["PAID"]
            .sum().reset_index()
            .sort_values("PAID", ascending=False)
        )
        cutoff = int(len(agg) * 0.05)
        return agg.head(max(1, cutoff))

    return df