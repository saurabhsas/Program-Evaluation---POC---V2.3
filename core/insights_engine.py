def generate_insights(prompt, df):
    
    if df is None or df.empty:
        return ["No insights available"]

    insights = []

    if "Monthly" in prompt:
        insights.append("Trend shows variation across months.")

    elif "Line of Business" in prompt:
        top = df.sort_values("Value", ascending=False).iloc[0]
        insights.append(f"Top LOB: {top['Dimension']}")

    elif "Pareto" in prompt:
        insights.append("Top 5% members contribute majority cost.")

    else:
        insights.append("Compare Group1 vs Group2.")

    return insights