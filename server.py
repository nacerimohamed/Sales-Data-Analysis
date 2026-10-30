
from flask import Flask, jsonify, render_template
import pandas as pd
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Sample - Superstore.csv"


def load_data():
    df = pd.read_csv(DATA_PATH, encoding="latin-1")

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

    return df


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# KPI OVERVIEW
# -----------------------------
@app.route("/api/overview")
def overview():
    df = load_data()

    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()

    return jsonify({
        "total_sales": round(float(total_sales), 2),
        "total_profit": round(float(df["Profit"].sum()), 2),
        "total_orders": int(total_orders),
        "total_customers": int(df["Customer ID"].nunique()),
        "total_quantity": int(df["Quantity"].sum()),
        "average_order_value": round(
            float(total_sales / total_orders), 2
        )
    })


# -----------------------------
# MONTHLY SALES TREND
# -----------------------------
@app.route("/api/monthly-sales")
def monthly_sales():
    df = load_data()

    monthly = (
        df.groupby("Month")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Month")
    )

    return jsonify({
        "labels": monthly["Month"].tolist(),
        "sales": monthly["sales"].round(2).tolist(),
        "profit": monthly["profit"].round(2).tolist()
    })


# -----------------------------
# SALES AND PROFIT BY CATEGORY
# -----------------------------
@app.route("/api/category-performance")
def category_performance():
    df = load_data()

    category = (
        df.groupby("Category")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        .reset_index()
    )

    return jsonify({
        "labels": category["Category"].tolist(),
        "sales": category["sales"].round(2).tolist(),
        "profit": category["profit"].round(2).tolist()
    })


# -----------------------------
# REGIONAL PERFORMANCE
# -----------------------------
@app.route("/api/region-performance")
def region_performance():
    df = load_data()

    region = (
        df.groupby("Region")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        .reset_index()
    )

    return jsonify({
        "labels": region["Region"].tolist(),
        "sales": region["sales"].round(2).tolist(),
        "profit": region["profit"].round(2).tolist()
    })


# -----------------------------
# TOP 10 CUSTOMERS
# -----------------------------
@app.route("/api/top-customers")
def top_customers():
    df = load_data()

    customers = (
        df.groupby("Customer Name")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("sales", ascending=False)
        .head(10)
    )

    return jsonify({
        "labels": customers["Customer Name"].tolist(),
        "sales": customers["sales"].round(2).tolist(),
        "profit": customers["profit"].round(2).tolist()
    })
  
@app.route("/api/filters")
def filters():
    df = load_data()

    return jsonify({
        "years": sorted(df["Year"].unique().tolist()),
        "regions": sorted(df["Region"].unique().tolist()),
        "categories": sorted(df["Category"].unique().tolist())
    })


@app.route("/api/dashboard-data")
def dashboard_data():
    from flask import request

    df = load_data()

    year = request.args.get("year", "all")
    region = request.args.get("region", "all")
    category = request.args.get("category", "all")

    if year != "all":
        df = df[df["Year"] == int(year)]

    if region != "all":
        df = df[df["Region"] == region]

    if category != "all":
        df = df[df["Category"] == category]

    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()

    monthly = (
        df.groupby("Month")
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Month")
    )

    categories_data = (
        df.groupby("Category")
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
    )

    regions_data = (
        df.groupby("Region")
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
    )

    customers_data = (
        df.groupby("Customer Name")
        .agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
        .reset_index()
        .sort_values("sales", ascending=False)
        .head(10)
    )

    return jsonify({
        "overview": {
            "total_sales": round(float(total_sales), 2),
            "total_profit": round(float(df["Profit"].sum()), 2),
            "total_orders": int(total_orders),
            "total_customers": int(df["Customer ID"].nunique()),
            "total_quantity": int(df["Quantity"].sum()),
            "average_order_value": round(
                float(total_sales / total_orders), 2
            ) if total_orders else 0
        },
        "monthly": {
            "labels": monthly["Month"].tolist(),
            "sales": monthly["sales"].round(2).tolist(),
            "profit": monthly["profit"].round(2).tolist()
        },
        "categories": {
            "labels": categories_data["Category"].tolist(),
            "sales": categories_data["sales"].round(2).tolist(),
            "profit": categories_data["profit"].round(2).tolist()
        },
        "regions": {
            "labels": regions_data["Region"].tolist(),
            "sales": regions_data["sales"].round(2).tolist(),
            "profit": regions_data["profit"].round(2).tolist()
        },
        "customers": {
            "labels": customers_data["Customer Name"].tolist(),
            "sales": customers_data["sales"].round(2).tolist(),
            "profit": customers_data["profit"].round(2).tolist()
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
