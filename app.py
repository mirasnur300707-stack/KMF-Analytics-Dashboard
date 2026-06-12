import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="KMF Bank Analytics", layout="wide")

st.title("KMF Bank - Loan Analytics Dashboard")
st.markdown("**Prototype analytical dashboard for microloan monitoring | Industrial Practice**")
st.info("This dashboard uses synthetic demo data only and does not contain real bank customer information.")

# Test data
@st.cache_data
def load_data():
    data = {
        "client_id": range(1001, 1101),
        "region": ["Almaty"] * 25 + ["Astana"] * 25 + ["Shymkent"] * 20 + ["Karaganda"] * 15 + ["Aktobe"] * 15,
        "loan_amount": [50000, 80000, 120000, 200000, 350000] * 20,
        "loan_date": pd.date_range(start="2026-06-01", periods=100, freq="D"),
        "status": ["Active"] * 50 + ["Closed"] * 35 + ["Overdue"] * 15,
        "interest_rate": [18, 22, 25, 28] * 25,
        "days_overdue": [0] * 70 + [7, 14, 30, 45] * 7 + [0] * 2,
        "product_type": ["Microloan", "Business loan", "Consumer loan", "SME loan"] * 25,
        "channel": ["Branch", "Mobile App", "Website", "Call Center"] * 25
    }

    df = pd.DataFrame(data)
    df["loan_date"] = pd.to_datetime(df["loan_date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

all_regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect(
    "Select Region",
    all_regions,
    default=all_regions
)

all_statuses = sorted(df["status"].unique())
selected_statuses = st.sidebar.multiselect(
    "Select Loan Status",
    all_statuses,
    default=all_statuses
)

all_products = sorted(df["product_type"].unique())
selected_products = st.sidebar.multiselect(
    "Select Product Type",
    all_products,
    default=all_products
)

filtered_df = df[
    (df["region"].isin(selected_regions)) &
    (df["status"].isin(selected_statuses)) &
    (df["product_type"].isin(selected_products))
]

# KPI Metrics
total_loans = len(filtered_df)
total_amount = filtered_df["loan_amount"].sum()
overdue_loans = (filtered_df["days_overdue"] > 0).sum()
average_interest = filtered_df["interest_rate"].mean() if total_loans > 0 else 0
overdue_rate = (overdue_loans / total_loans * 100) if total_loans > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Loans", total_loans)
col2.metric("Total Amount Issued", f"{total_amount:,.0f} ₸")
col3.metric("Overdue Loans", overdue_loans)
col4.metric("Overdue Rate", f"{overdue_rate:.1f}%")
col5.metric("Average Interest Rate", f"{average_interest:.1f}%")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Clients", "Loans", "Analytics"])

with tab1:
    st.subheader("Loan Status Distribution")

    fig_status = px.pie(
        filtered_df,
        names="status",
        title="Loan Status Distribution"
    )
    st.plotly_chart(fig_status, use_container_width=True)

    st.subheader("Loans by Region")

    region_summary = filtered_df.groupby("region")["loan_amount"].sum().reset_index()

    fig_region = px.bar(
        region_summary,
        x="region",
        y="loan_amount",
        title="Total Loan Amount by Region",
        labels={"region": "Region", "loan_amount": "Total Loan Amount"}
    )
    st.plotly_chart(fig_region, use_container_width=True)

with tab2:
    st.subheader("Clients Data")
    st.dataframe(filtered_df, use_container_width=True)

with tab3:
    st.subheader("Issued Loans")

    sorted_loans = filtered_df.sort_values("loan_date", ascending=False)
    st.dataframe(sorted_loans, use_container_width=True)

with tab4:
    st.subheader("Loans Issuance Dynamics")

    daily = filtered_df.groupby("loan_date")["loan_amount"].sum().reset_index()

    fig_daily = px.line(
        daily,
        x="loan_date",
        y="loan_amount",
        title="Daily Loan Issuance",
        markers=True
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.subheader("Interest Rate Distribution")

    fig_interest = px.histogram(
        filtered_df,
        x="interest_rate",
        title="Interest Rate Distribution",
        nbins=10
    )
    st.plotly_chart(fig_interest, use_container_width=True)

    st.subheader("Loan Products Distribution")

    fig_product = px.bar(
        filtered_df,
        x="product_type",
        title="Number of Loans by Product Type"
    )
    st.plotly_chart(fig_product, use_container_width=True)

st.caption("Developed by a 2nd-year Computer Science student during Industrial Practice at KMF Bank • June 2026")