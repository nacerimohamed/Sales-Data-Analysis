# Sales Data Analysis & Interactive Dashboard

An end-to-end data analysis project using Python to explore sales performance, identify business trends, and build an interactive dashboard.

## Project Overview

This project analyzes the Sample Superstore dataset to understand sales performance, profitability, customer behavior, and regional trends.

An interactive dashboard was developed using Streamlit and Plotly to make the analysis easier to explore through dynamic filters and visualizations.

## Technologies Used

- **Python** – Data analysis and processing
- **Pandas & NumPy** – Data manipulation
- **Matplotlib & Seaborn** – Data visualization
- **Plotly** – Interactive charts
- **Streamlit** – Interactive dashboard
- **Jupyter Notebook** – Exploratory Data Analysis

## Dataset

The project uses the Sample Superstore dataset, containing 9,994 records and 21 columns related to orders, customers, products, sales, and profits.

## Key Performance Indicators

- Total Sales: $2,297,200.86
- Total Profit: $286,397.02
- Total Orders: 5,009
- Total Customers: 793
- Total Quantity Sold: 37,873

## Analysis & Insights

The analysis explores:

- Sales and profit performance by category and sub-category
- Regional sales and profitability
- Monthly and yearly sales trends
- Customer purchasing behavior
- Discount impact on profitability
- Top-performing customers
- Products and sub-categories generating losses

## Dashboard Features

- Interactive filters by year, region, and category
- Dynamic KPI cards
- Monthly sales trend visualization
- Category and regional performance charts
- Top 10 customers analysis
- Discount impact analysis
- Filtered data explorer

## Project Structure

```text
Sales-Data-Analysis/
│
├── data/
│   └── Sample - Superstore.csv
│
├── images/
│   └── profit_by_category.png
│
├── notebooks/
│
├── sales_analysis.ipynb
├── app.py
├── requirements.txt
└── README.md
```

## Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/nacerimohamed/Sales-Data-Analysis.git
```

2. Navigate to the project directory:

```bash
cd Sales-Data-Analysis
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Run the dashboard:

```bash
streamlit run app.py
```

## Author

**Mohamed Naceri**

Full Stack Developer | Data Analysis Enthusiast