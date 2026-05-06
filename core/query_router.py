# core/query_router.py

import pandas as pd


def run_prompt(prompt, df):

    df = df.copy()

    # -----------------------------------
    # MONTH FORMATTING (YYYYMM)
    # -----------------------------------
    if "ELIGIBILITYYEARANDMONTH" in df.columns:
        df["MONTH"] = df["ELIGIBILITYYEARANDMONTH"].astype(str)

    # -----------------------------------
    # MONTHLY TREND
    # -----------------------------------
    if prompt == "Monthly Total Cost Trend":
        result = (
            df.groupby(["MONTH", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .rename(columns={"PAID": "Value"})
        )

        return result.sort_values("MONTH")

    # -----------------------------------
    # LOB
    # -----------------------------------
    if prompt == "Total Cost by Line of Business":
        return (
            df.groupby(["LINEOFBUSINESS", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .rename(columns={
                "LINEOFBUSINESS": "Dimension",
                "PAID": "Value"
            })
        )

    # -----------------------------------
    # COUNTY
    # -----------------------------------
    if prompt == "Total Cost by County":
        return (
            df.groupby(["COUNTY", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .rename(columns={
                "COUNTY": "Dimension",
                "PAID": "Value"
            })
        )

    # -----------------------------------
    # AGE CATEGORY
    # -----------------------------------
    if prompt == "Total Cost by Age Category":
        return (
            df.groupby(["AGE_CATEGORY", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .rename(columns={
                "AGE_CATEGORY": "Dimension",
                "PAID": "Value"
            })
        )

    # -----------------------------------
    # GENDER
    # -----------------------------------
    if prompt == "Total Cost by Gender":
        return (
            df.groupby(["GENDER", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .rename(columns={
                "GENDER": "Dimension",
                "PAID": "Value"
            })
        )

    # -----------------------------------
    # TOP MEMBERS
    # -----------------------------------
    if prompt == "Top 10 High Cost Members":
        return (
            df.groupby(["MEMBER_ID", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .sort_values("PAID", ascending=False)
            .head(10)
        )

    # -----------------------------------
    # PARETO
    # -----------------------------------
    if prompt == "Pareto Cost Analysis (Top 5%)":
        agg = (
            df.groupby(["MEMBER_ID", "GROUP"])["PAID"]
            .sum()
            .reset_index()
            .sort_values("PAID", ascending=False)
        )

        cutoff = max(1, int(len(agg) * 0.05))
        return agg.head(cutoff)

    return df
