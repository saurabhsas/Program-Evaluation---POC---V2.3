# visualization/chart_router.py

import plotly.express as px


def build_chart(df, prompt):

    if df is None or df.empty:
        return px.scatter(title="No data available")

    # -----------------------------------
    if prompt == "Monthly Total Cost Trend":
        fig = px.line(
            df,
            x="MONTH",
            y="Value",
            color="GROUP",
            markers=True,
            title="Monthly Cost Trend"
        )
        fig.update_xaxes(type="category")
        return fig

    # -----------------------------------
    if prompt == "Medical vs Pharmacy Cost Split":
        return px.bar(
            df,
            x="Dimension",
            y="Value",
            color="GROUP",
            barmode="group",
            title="Medical vs Pharmacy Cost"
        )

    # -----------------------------------
    if "Line of Business" in prompt:
        return px.bar(
            df,
            x="Dimension",
            y="Value",
            color="GROUP",
            barmode="group",
            title="Cost by Line of Business"
        )

    # -----------------------------------
    if "County" in prompt:
        return px.bar(
            df,
            x="Dimension",
            y="Value",
            color="GROUP",
            title="Cost by County"
        )

    # -----------------------------------
    if "Age Category" in prompt or "Gender" in prompt:
        return px.bar(
            df,
            x="Dimension",
            y="Value",
            color="GROUP",
            barmode="group"
        )

    # -----------------------------------
    if "Top 10" in prompt or "High Utilization" in prompt:
        return px.bar(
            df,
            x="Dimension",
            y="Value",
            color="GROUP",
            title="Top Members"
        )

    # -----------------------------------
    if "Pareto" in prompt:
        return px.bar(
            df,
            x="MEMBER_ID",
            y="PAID",
            color="GROUP",
            title="Top 5% Members Cost"
        )

    # -----------------------------------
    return px.bar(df)