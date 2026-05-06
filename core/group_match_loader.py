import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_group_match_data():

    g1 = pd.read_csv("data/Group1.csv")
    g2 = pd.read_csv("data/Group2.csv")
    score = pd.read_csv("data/Member_match_score.csv")

    # Standardize
    for df in [g1, g2, score]:
        df.columns = df.columns.str.strip().str.upper()

    # Normalize naming
    for df in [g1, g2, score]:
        if "MEMBERID" in df.columns:
            df.rename(columns={"MEMBERID": "MEMBER_ID"}, inplace=True)
        if "MEMBERUCI" in df.columns:
            df.rename(columns={"MEMBERUCI": "MEMBER_UCI"}, inplace=True)

    # Convert RUN_YM
    score["RUN_YM"] = pd.to_numeric(score["RUN_YM"], errors="coerce")

    # Keep latest RUN_YM per MEMBER_UCI
    score = score.sort_values("RUN_YM", ascending=False)
    score = score.drop_duplicates(subset=["MEMBER_UCI"])

    # Join
    g1 = g1.merge(score, on="MEMBER_UCI", how="left")
    g2 = g2.merge(score, on="MEMBER_UCI", how="left")

    return g1, g2