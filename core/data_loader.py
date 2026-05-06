import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(path="data/Final_Monthly.csv"):

    df = pd.read_csv(path)

    # Standardize columns
    df.columns = df.columns.str.strip().str.upper()

    # Normalize naming
    if "MEMBERID" in df.columns:
        df.rename(columns={"MEMBERID": "MEMBER_ID"}, inplace=True)

    if "MEMBERUCI" in df.columns:
        df.rename(columns={"MEMBERUCI": "MEMBER_UCI"}, inplace=True)

    df["MEMBER_ID"] = df["MEMBER_ID"].astype(str)

    # Optimize memory
    for col in ["COUNTY", "LINEOFBUSINESS", "GENDER", "AGE_CATEGORY"]:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df