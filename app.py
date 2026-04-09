from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import plotly.express as px

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    df = pd.read_csv("tourism_data.csv")

    years_cols = {
        "2017": "Number of Arrivals-2017",
        "2018": "Number of Arrivals-2018",
        "2019": "Number of Arrivals-2019",
        "2020": "Number of Arrivals-2020",
        "2021": "Number of Arrivals-2021"
    }

    # Convert to numeric
    for col in years_cols.values():
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Default year
    selected_year = request.form.get("year", "2019")

    # KPI
    total = df[years_cols[selected_year]].sum()

    # Growth calculation
    prev_year = str(int(selected_year) - 1)
    if prev_year in years_cols:
        prev_total = df[years_cols[prev_year]].sum()
        growth = ((total - prev_total) / prev_total) * 100
    else:
        growth = 0

    # 📊 Bar chart (Top countries)
    top_df = df[['Country of Nationality', years_cols[selected_year]]].dropna()
    top_df = top_df.sort_values(by=years_cols[selected_year], ascending=False).head(10)

    fig = px.bar(
        top_df,
        x='Country of Nationality',
        y=years_cols[selected_year],
        title=f"Top 10 Countries - {selected_year}",
        color=years_cols[selected_year],
        color_continuous_scale='blues'
    )

    chart_html = fig.to_html(full_html=False)

    return render_template(
        "index.html",
        chart=chart_html,
        total=int(total),
        growth=round(growth, 2),
        selected_year=selected_year
    )

if __name__ == "__main__":
    app.run(debug=True)
