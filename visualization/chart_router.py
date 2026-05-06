# visualization/chart_router.py

import plotly.express as px


def build_chart(df, prompt):

    if df is None or df.empty:
        return px.scatter(title="No data available")

    cols = df.columns.tolist()

    # -----------------------------------
    # MONTHLY TREND
    # -----------------------------------
    if "MONTH" in cols and "Value" in cols:

        df["MONTH"] = df["MONTH"].astype(str)

        fig = px.line(
            df,
            x="MONTH",
            y="Value",
            color="GROUP",
            markers=True,
            title="Monthly Cost Trend"
        )

        fig.update_xaxes(type="category")
        fig.update_yaxes(tickprefix="$", separatethousands=True)

        return fig

    # -----------------------------------
    # DIMENSION BASED
    # -----------------------------------
    if "Dimension" in cols and "Value" in cols:

        fig = px.bar(
            df,
            x="Dimension",
            y="Value",
            color="GROUP",
            barmode="group",
            title=prompt
        )

        fig.update_yaxes(tickprefix="$", separatethousands=True)

        return fig

    # -----------------------------------
    # MEMBER BASED
    # -----------------------------------
    if "MEMBER_ID" in cols:

        fig = px.bar(
            df,
            x="MEMBER_ID",
            y="PAID",
            color="GROUP",
            title=prompt
        )

        fig.update_yaxes(tickprefix="$", separatethousands=True)

        return fig

    # -----------------------------------
    # FALLBACK
    # -----------------------------------
    return px.bar(df)
