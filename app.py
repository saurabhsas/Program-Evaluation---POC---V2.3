import streamlit as st
import pandas as pd

from core.data_loader import load_data
from core.filters import render_filter_ui, apply_filters_cached
from core.query_router import run_prompt
from core.insights_engine import generate_insights

from core.group_match_loader import load_group_match_data
from core.matching_engine import multi_caliper_matching
from core.matched_data_loader import load_matched_datasets

from visualization.chart_router import build_chart
from utils.constants import PROMPTS


st.set_page_config(layout="wide")
st.title("🏥 Matched Cohort Analytics Dashboard")


# -----------------------------------
# CACHE MATCHING
# -----------------------------------
@st.cache_data(show_spinner=False)
def get_matched():
    g1, g2 = load_group_match_data()
    return multi_caliper_matching(g1, g2)


# -----------------------------------
# LOAD DATA
# -----------------------------------
df = load_data()
matched = get_matched()


# -----------------------------------
# MATCHING QUALITY
# -----------------------------------
st.markdown("## 🎛 Matching Quality")

CALIPER_DESC = {
    "1e-05": "Very Strict (5 decimal)",
    "0.0001": "Strict (4 decimal)",
    "0.001": "Moderate (3 decimal)",
    "0.02": "Loose",
    "no_caliper": "Fallback (full coverage)"
}

available_calipers = sorted(matched["caliper_used"].unique())

selected_calipers = st.multiselect(
    "Select Matching Precision Levels",
    options=available_calipers,
    default=available_calipers
)

with st.expander("📘 Caliper Definitions"):
    for cal in available_calipers:
        st.markdown(f"**{cal}** — {CALIPER_DESC.get(cal, '')}")


filtered_matched = matched[
    matched["caliper_used"].isin(selected_calipers)
]


# -----------------------------------
# MATCH SUMMARY
# -----------------------------------
colA, colB, colC = st.columns(3)

colA.metric("Total Matches", len(filtered_matched))
colB.metric("Group1 Members", filtered_matched["G1_MEMBER_ID"].nunique())
colC.metric("Group2 Members", filtered_matched["G2_MEMBER_ID"].nunique())


# -----------------------------------
# LOAD MATCHED DATA
# -----------------------------------
g1_data, g2_data, _ = load_matched_datasets(df, filtered_matched)

combined = pd.concat([g1_data, g2_data])


# -----------------------------------
# FILTERS
# -----------------------------------
filters = render_filter_ui(combined)
filtered = apply_filters_cached(combined, filters)


# -----------------------------------
# KPI
# -----------------------------------
def compute_kpis(df):
    members = df["MEMBER_ID"].nunique()
    total = df["PAID"].sum()

    return {
        "Members": members,
        "Total Cost": total,
        "Medical Cost": df["MEDICAL_PAID"].sum(),
        "Pharmacy Cost": df["RX_PAID"].sum(),
    }


k1 = compute_kpis(filtered[filtered["GROUP"] == "Group1"])
k2 = compute_kpis(filtered[filtered["GROUP"] == "Group2"])


st.markdown("## 📊 Key Metrics Overview")

def render_kpis(title, kpis1, kpis2):
    st.markdown(f"### {title}")
    cols = st.columns(4)

    for i, key in enumerate(kpis1.keys()):
        v1 = kpis1[key]
        v2 = kpis2[key]

        pct = ((v1 - v2) / v2 * 100) if v2 else 0

        cols[i % 4].metric(
            key,
            f"${v1:,.0f}" if "Cost" in key else f"{int(v1)}",
            f"{pct:+.1f}%"
        )


render_kpis("Group1", k1, k2)
st.markdown("---")
render_kpis("Group2", k2, k1)


# -----------------------------------
# PROMPT
# -----------------------------------
st.markdown("## 📈 Analysis")

selected_prompt = st.selectbox("Select Analysis", PROMPTS)


# -----------------------------------
# CHART
# -----------------------------------
result = run_prompt(selected_prompt, filtered)

fig = build_chart(result, selected_prompt)
st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# INSIGHTS
# -----------------------------------
st.markdown("## 🧠 Insights")

for ins in generate_insights(selected_prompt, result):
    st.write("•", ins)


# -----------------------------------
# TABLE
# -----------------------------------
st.markdown("## 📄 Data Sample")

display_df = result.copy()

for col in display_df.columns:
    if display_df[col].dtype in ["int64", "float64"] and col != "MONTH":
        display_df[col] = display_df[col].apply(
            lambda x: f"${x:,.0f}" if pd.notnull(x) else x
        )

st.dataframe(display_df.head(50))
