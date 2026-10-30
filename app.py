
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 100%);
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1E3A8A 100%);
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #172554 !important;
}

[data-testid="stSidebar"] input {
    color: #172554 !important;
}

/* Header */
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #172554;
    letter-spacing: -1px;
    animation: fadeDown 0.8s ease;
}

.subtitle {
    color: #64748B;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 25px;
    animation: fadeUp 1s ease;
}

.section-title {
    color: #172554;
    font-size: 20px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* KPI Cards */
.kpi-card {
    position: relative;
    overflow: hidden;
    background: #FFFFFF;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 5px 18px rgba(15,23,42,0.05);
    min-height: 150px;
    transition: all 0.35s ease;
    animation: fadeUp 0.8s ease both;
}

.kpi-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 14px 30px rgba(37,99,235,0.13);
    border-color: #93C5FD;
}

.kpi-card::after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    background: rgba(59,130,246,0.06);
    border-radius: 50%;
    right: -35px;
    top: -35px;
    transition: transform 0.4s ease;
}

.kpi-card:hover::after {
    transform: scale(1.7);
}

.kpi-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 46px;
    height: 46px;
    background: #EFF6FF;
    border-radius: 13px;
    margin-bottom: 14px;
    color: #2563EB;
    transition: all 0.3s ease;
}

.kpi-card:hover .kpi-icon {
    background: #2563EB;
    color: #FFFFFF;
    transform: scale(1.1) rotate(-5deg);
}

.kpi-icon svg {
    width: 24px;
    height: 24px;
    stroke: currentColor;
    fill: none;
    stroke-width: 1.8;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.kpi-label {
    color: #64748B;
    font-size: 13px;
    font-weight: 600;
}

.kpi-value {
    color: #172554;
    font-size: 24px;
    font-weight: 800;
    margin-top: 7px;
    letter-spacing: -0.5px;
}

/* Charts */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 10px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 15px rgba(15,23,42,0.04);
    transition: all 0.3s ease;
    animation: fadeUp 0.9s ease;
}

div[data-testid="stPlotlyChart"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(15,23,42,0.08);
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    border: none;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(59,130,246,0.2);
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 13px;
    padding: 30px 0 15px;
}

/* Animations */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SVG ICONS
# =====================================================
ICONS = {
    "wallet": """
        <rect x="3" y="6" width="18" height="15" rx="2"/>
        <path d="M3 10h18"/>
        <path d="M16 15h2"/>
        <path d="M7 6V4h13v2"/>
    """,

    "trending-up": """
        <path d="m22 7-8.5 8.5-5-5L2 17"/>
        <path d="M16 7h6v6"/>
    """,

    "shopping-cart": """
        <circle cx="9" cy="21" r="1"/>
        <circle cx="20" cy="21" r="1"/>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
    """,

    "users": """
        <path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
        <circle cx="10" cy="7" r="4"/>
        <path d="M20 21v-2a4 4 0 0 0-3-3.87"/>
        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    """,

    "target": """
        <circle cx="12" cy="12" r="10"/>
        <circle cx="12" cy="12" r="6"/>
        <circle cx="12" cy="12" r="2"/>
    """,

    "credit-card": """
        <rect x="2" y="5" width="20" height="14" rx="2"/>
        <path d="M2 10h20"/>
        <path d="M6 15h4"/>
    """
}


def render_icon(name):
    return f"""
    <svg viewBox="0 0 24 24" aria-hidden="true">
        {ICONS[name]}
    </svg>
    """


# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    data = pd.read_csv(
        "data/Sample - Superstore.csv",
        encoding="latin-1"
    )

    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Ship Date"] = pd.to_datetime(data["Ship Date"])

    data["Year"] = data["Order Date"].dt.year
    data["Month"] = data["Order Date"].dt.to_period("M").astype(str)

    return data


df = load_data()


# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.markdown("## SALES ANALYTICS")
st.sidebar.caption("Dashboard Control Panel")
st.sidebar.divider()

years = sorted(df["Year"].unique().tolist())
regions = sorted(df["Region"].unique().tolist())
categories = sorted(df["Category"].unique().tolist())

if st.sidebar.button("Reset All Filters", use_container_width=True):
    st.session_state["years_filter"] = years
    st.session_state["regions_filter"] = regions
    st.session_state["categories_filter"] = categories

st.sidebar.markdown("### Time Period")

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=years,
    default=years,
    key="years_filter"
)

st.sidebar.markdown("### Geography")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions,
    key="regions_filter"
)

st.sidebar.markdown("### Product Category")

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories,
    key="categories_filter"
)

st.sidebar.divider()
st.sidebar.caption("Python | Pandas | Plotly | Streamlit")


# =====================================================
# FILTER DATA
# =====================================================
filtered_df = df[
    (df["Year"].isin(selected_years))
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
]

if filtered_df.empty:
    st.warning("No data found. Please change your filters.")
    st.stop()


# =====================================================
# HEADER
# =====================================================
st.markdown(
    '<div class="main-title">Sales Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Monitor sales performance, profitability, '
    'customers and business trends.</div>',
    unsafe_allow_html=True
)


# =====================================================
# KPI CALCULATIONS
# =====================================================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

average_order_value = (
    total_sales / total_orders
    if total_orders != 0 else 0
)

# =====================================================
# KPI CARDS
# =====================================================
st.markdown(
    '<div class="section-title">Business Overview</div>',
    unsafe_allow_html=True
)

kpi_data = [
    ("wallet", "Total Sales", f"${total_sales:,.2f}"),
    ("trending-up", "Total Profit", f"${total_profit:,.2f}"),
    ("shopping-cart", "Total Orders", f"{total_orders:,}"),
    ("users", "Total Customers", f"{total_customers:,}"),
    ("target", "Profit Margin", f"{profit_margin:.2f}%"),
    ("credit-card", "Average Order Value", f"${average_order_value:,.2f}")
]

for row_start in range(0, len(kpi_data), 3):
    cols = st.columns(3)

    for col, item in zip(cols, kpi_data[row_start:row_start + 3]):
        icon_name, label, value = item

        html = f"""
        <html>
        <head>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
            }}

            .kpi-card {{
                background: white;
                padding: 22px;
                border-radius: 18px;
                border: 1px solid #E2E8F0;
                box-shadow: 0 5px 18px rgba(15,23,42,0.05);
                min-height: 150px;
                box-sizing: border-box;
                transition: all 0.3s ease;
            }}

            .kpi-card:hover {{
                transform: translateY(-6px);
                box-shadow: 0 14px 30px rgba(37,99,235,0.13);
                border-color: #93C5FD;
            }}

            .kpi-icon {{
                display: flex;
                align-items: center;
                justify-content: center;
                width: 46px;
                height: 46px;
                background: #EFF6FF;
                color: #2563EB;
                border-radius: 13px;
                margin-bottom: 14px;
                transition: all 0.3s ease;
            }}

            .kpi-card:hover .kpi-icon {{
                background: #2563EB;
                color: white;
                transform: scale(1.1) rotate(-5deg);
            }}

            .kpi-icon svg {{
                width: 24px;
                height: 24px;
                stroke: currentColor;
                fill: none;
                stroke-width: 1.8;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}

            .kpi-label {{
                color: #64748B;
                font-size: 13px;
                font-weight: 600;
            }}

            .kpi-value {{
                color: #172554;
                font-size: 23px;
                font-weight: 800;
                margin-top: 7px;
            }}
        </style>
        </head>

        <body>
            <div class="kpi-card">
                <div class="kpi-icon">
                    {render_icon(icon_name)}
                </div>

                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
        </body>
        </html>
        """

        with col:
            components.html(html, height=175, scrolling=False)
# =====================================================
# MONTHLY SALES TREND
# =====================================================
st.markdown(
    '<div class="section-title">Sales Performance Over Time</div>',
    unsafe_allow_html=True
)

monthly_sales = (
    filtered_df.groupby("Month", as_index=False)["Sales"]
    .sum()
    .sort_values("Month")
)

fig_monthly = px.area(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    color_discrete_sequence=["#2563EB"],
    template="plotly_white",
    title="Monthly Sales Trend"
)

fig_monthly.update_traces(
    line=dict(width=3),
    fillcolor="rgba(37,99,235,0.12)"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales ($)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=55, b=20)
)

st.plotly_chart(fig_monthly, use_container_width=True)


# =====================================================
# CATEGORY ANALYSIS
# =====================================================
st.markdown(
    '<div class="section-title">Product Category Analysis</div>',
    unsafe_allow_html=True
)

category_data = (
    filtered_df.groupby("Category", as_index=False)
    .agg({
        "Sales": "sum",
        "Profit": "sum"
    })
)

col1, col2 = st.columns(2)

with col1:
    fig_category_sales = px.bar(
        category_data,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s",
        title="Sales by Category",
        template="plotly_white",
        color_discrete_sequence=["#2563EB", "#0D9488", "#F59E0B"]
    )

    fig_category_sales.update_layout(
        showlegend=False,
        margin=dict(l=15, r=15, t=55, b=15)
    )

    st.plotly_chart(fig_category_sales, use_container_width=True)

with col2:
    fig_category_profit = px.bar(
        category_data,
        x="Category",
        y="Profit",
        color="Category",
        text_auto=".2s",
        title="Profit by Category",
        template="plotly_white",
        color_discrete_sequence=["#2563EB", "#0D9488", "#F59E0B"]
    )

    fig_category_profit.update_layout(
        showlegend=False,
        margin=dict(l=15, r=15, t=55, b=15)
    )

    st.plotly_chart(fig_category_profit, use_container_width=True)


# =====================================================
# REGIONAL ANALYSIS
# =====================================================
st.markdown(
    '<div class="section-title">Regional Performance</div>',
    unsafe_allow_html=True
)

region_data = (
    filtered_df.groupby("Region", as_index=False)
    .agg({
        "Sales": "sum",
        "Profit": "sum"
    })
)

col1, col2 = st.columns(2)

with col1:
    fig_region_sales = px.bar(
        region_data,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region",
        template="plotly_white",
        text_auto=".2s"
    )

    fig_region_sales.update_layout(
        showlegend=False,
        margin=dict(l=15, r=15, t=55, b=15)
    )

    st.plotly_chart(fig_region_sales, use_container_width=True)

with col2:
    fig_region_profit = px.bar(
        region_data.sort_values("Profit"),
        x="Profit",
        y="Region",
        orientation="h",
        color="Profit",
        color_continuous_scale="RdYlGn",
        title="Profit by Region",
        template="plotly_white"
    )

    fig_region_profit.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=15, r=15, t=55, b=15)
    )

    st.plotly_chart(fig_region_profit, use_container_width=True)


# =====================================================
# TOP 10 CUSTOMERS
# =====================================================
st.markdown(
    '<div class="section-title">Top 10 Customers</div>',
    unsafe_allow_html=True
)

top_customers = (
    filtered_df.groupby("Customer Name", as_index=False)
    .agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique"
    })
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_customers = px.bar(
    top_customers.sort_values("Sales"),
    x="Sales",
    y="Customer Name",
    orientation="h",
    color="Sales",
    color_continuous_scale="Blues",
    title="Top Customers by Sales",
    hover_data=["Profit", "Order ID"],
    template="plotly_white"
)

fig_customers.update_layout(
    xaxis_title="Sales ($)",
    yaxis_title="Customer",
    coloraxis_showscale=False,
    margin=dict(l=15, r=15, t=55, b=15)
)

st.plotly_chart(fig_customers, use_container_width=True)


# =====================================================
# DISCOUNT ANALYSIS
# =====================================================
st.markdown(
    '<div class="section-title">Discount Impact Analysis</div>',
    unsafe_allow_html=True
)

discount_data = (
    filtered_df.groupby("Discount", as_index=False)
    .agg({
        "Profit": "mean",
        "Sales": "mean"
    })
    .sort_values("Discount")
)

fig_discount = px.scatter(
    discount_data,
    x="Discount",
    y="Profit",
    size="Sales",
    color="Profit",
    color_continuous_scale="RdYlGn",
    title="Average Profit vs Discount",
    labels={
        "Discount": "Discount Rate",
        "Profit": "Average Profit ($)",
        "Sales": "Average Sales ($)"
    },
    template="plotly_white"
)

fig_discount.update_layout(
    margin=dict(l=15, r=15, t=55, b=15)
)

st.plotly_chart(fig_discount, use_container_width=True)


# =====================================================
# DATA EXPLORER
# =====================================================
with st.expander("Explore Filtered Dataset"):
    st.write(f"Showing {len(filtered_df):,} records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# FOOTER
# =====================================================
st.divider()

st.markdown("""
<div class="footer">
    <strong>Sales Analytics Dashboard</strong><br>
    Developed with Python · Pandas · Plotly · Streamlit<br>
    Data Analytics Portfolio Project
</div>
""", unsafe_allow_html=True)
