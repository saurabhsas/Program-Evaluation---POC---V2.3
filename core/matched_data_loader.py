import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_matched_datasets(df, matched):

    df = df.copy()
    df["MEMBER_ID"] = df["MEMBER_ID"].astype(str)

    matched = matched.copy()

    valid_ids = set(df["MEMBER_ID"])

    matched = matched[
        matched["G1_MEMBER_ID"].isin(valid_ids) &
        matched["G2_MEMBER_ID"].isin(valid_ids)
    ]

    g1 = df[df["MEMBER_ID"].isin(matched["G1_MEMBER_ID"])].copy()
    g2 = df[df["MEMBER_ID"].isin(matched["G2_MEMBER_ID"])].copy()

    g1["GROUP"] = "Group1"
    g2["GROUP"] = "Group2"

    return g1, g2, matched