
const charts = {};

const formatCurrency = value =>
    "$" + Number(value).toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

const formatNumber = value =>
    Number(value).toLocaleString("en-US");

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: "top",
            labels: {
                usePointStyle: true,
                padding: 20,
                font: {
                    family: "Inter",
                    size: 11
                }
            }
        }
    }
};

async function fetchData(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Request failed: ${url}`);
    }

    return response.json();
}

// -----------------------------
// LOAD FILTER OPTIONS
// -----------------------------
async function loadFilters() {
    const data = await fetchData("/api/filters");

    populateSelect("year-filter", data.years, "All Years");
    populateSelect("region-filter", data.regions, "All Regions");
    populateSelect("category-filter", data.categories, "All Categories");
}

function populateSelect(id, values, defaultLabel) {
    const select = document.getElementById(id);

    select.innerHTML = `<option value="all">${defaultLabel}</option>`;

    values.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}

// -----------------------------
// UPDATE KPI CARDS
// -----------------------------
function updateKPIs(data) {
    document.getElementById("total-sales").textContent =
        formatCurrency(data.total_sales);

    document.getElementById("total-profit").textContent =
        formatCurrency(data.total_profit);

    document.getElementById("total-orders").textContent =
        formatNumber(data.total_orders);

    document.getElementById("total-customers").textContent =
        formatNumber(data.total_customers);

    document.getElementById("total-quantity").textContent =
        formatNumber(data.total_quantity);

    document.getElementById("average-order-value").textContent =
        formatCurrency(data.average_order_value);
}

// -----------------------------
// CREATE OR UPDATE CHART
// -----------------------------
function updateChart(id, config) {
    const canvas = document.getElementById(id);

    if (!canvas) return;

    if (charts[id]) {
        charts[id].data = config.data;
        charts[id].options = config.options;
        charts[id].update();
    } else {
        charts[id] = new Chart(canvas, config);
    }
}

// -----------------------------
// MONTHLY SALES CHART
// -----------------------------
function renderMonthlyChart(data) {
    updateChart("monthlySalesChart", {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Sales",
                    data: data.sales,
                    borderColor: "#3978f6",
                    backgroundColor: "rgba(57,120,246,0.10)",
                    fill: true,
                    tension: 0.4
                },
                {
                    label: "Profit",
                    data: data.profit,
                    borderColor: "#16a36a",
                    backgroundColor: "transparent",
                    tension: 0.4
                }
            ]
        },
        options: {
            ...chartOptions,
            interaction: {
                intersect: false,
                mode: "index"
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => "$" + value.toLocaleString()
                    }
                }
            }
        }
    });
}

// -----------------------------
// CATEGORY CHART
// -----------------------------
function renderCategoryChart(data) {
    updateChart("categoryChart", {
        type: "doughnut",
        data: {
            labels: data.labels,
            datasets: [{
                data: data.sales,
                backgroundColor: ["#3978f6", "#16a36a", "#8256d0"],
                borderWidth: 0,
                hoverOffset: 8
            }]
        },
        options: {
            ...chartOptions,
            cutout: "68%"
        }
    });
}

// -----------------------------
// REGION CHART
// -----------------------------
function renderRegionChart(data) {
    updateChart("regionChart", {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Profit",
                data: data.profit,
                backgroundColor: "#3978f6",
                borderRadius: 6
            }]
        },
        options: {
            ...chartOptions,
            indexAxis: "y",
            plugins: {
                ...chartOptions.plugins,
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => "$" + value.toLocaleString()
                    }
                }
            }
        }
    });
}

// -----------------------------
// TOP CUSTOMERS CHART
// -----------------------------
function renderCustomersChart(data) {
    updateChart("customersChart", {
        type: "bar",
        data: {
            labels: data.labels,
            datasets: [{
                label: "Sales",
                data: data.sales,
                backgroundColor: "#3978f6",
                borderRadius: 5
            }]
        },
        options: {
            ...chartOptions,
            indexAxis: "y",
            plugins: {
                ...chartOptions.plugins,
                legend: { display: false }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => "$" + value.toLocaleString()
                    }
                }
            }
        }
    });
}

// -----------------------------
// APPLY FILTERS
// -----------------------------
async function applyFilters() {
    const year = document.getElementById("year-filter").value;
    const region = document.getElementById("region-filter").value;
    const category = document.getElementById("category-filter").value;

    const params = new URLSearchParams({
        year,
        region,
        category
    });

    try {
        const data = await fetchData(
            `/api/dashboard-data?${params.toString()}`
        );

        updateKPIs(data.overview);

        renderMonthlyChart(data.monthly);
        renderCategoryChart(data.categories);
        renderRegionChart(data.regions);
        renderCustomersChart(data.customers);

    } catch (error) {
        console.error("Dashboard update error:", error);
    }
}

// -----------------------------
// INITIALIZE DASHBOARD
// -----------------------------
async function initializeDashboard() {
    try {
        await loadFilters();

        document.getElementById("year-filter")
            .addEventListener("change", applyFilters);

        document.getElementById("region-filter")
            .addEventListener("change", applyFilters);

        document.getElementById("category-filter")
            .addEventListener("change", applyFilters);

        document.getElementById("reset-filters")
            .addEventListener("click", () => {
                document.getElementById("year-filter").value = "all";
                document.getElementById("region-filter").value = "all";
                document.getElementById("category-filter").value = "all";

                applyFilters();
            });

        await applyFilters();

    } catch (error) {
        console.error("Dashboard initialization error:", error);
    }
}

initializeDashboard();
