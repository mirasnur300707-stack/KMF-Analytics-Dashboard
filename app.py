import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="KMF Bank Analytics", layout="wide")
st.title("🚀 KMF Bank - Analytics Dashboard")
st.markdown("**Prototype of the analytical dashboard for microloans | Industrial Practice**")

# Sidebar filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Select Region",
                                 ["Almaty", "Astana", "Shymkent", "Karaganda", "Aktobe", "All Regions"],
                                 default=["All Regions"])

# Test data
@st.cache_data
def load_data():
    data = {
        'client_id': range(1001, 1101),
        'region': ['Almaty']*25 + ['Astana']*25 + ['Shymkent']*20 + ['Karaganda']*15 + ['Aktobe']*15,
        'loan_amount': [50000, 80000, 120000, 200000, 350000] * 20,
        'loan_date': pd.date_range(start='2025-01-01', periods=100, freq='D'),
        'status': ['Active']*50 + ['Closed']*35 + ['Overdue']*15,
        'interest_rate': [18, 22, 25, 28] * 25,
        'days_overdue': [0]*70 + [7, 14, 30, 45] * 7 + [0]*2
    }
    df = pd.DataFrame(data)
    df['loan_date'] = pd.to_datetime(df['loan_date'])
    return df

df = load_data()

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Loans", len(df))
col2.metric("Total Amount Issued", f"{df['loan_amount'].sum():,} ₸")
col3.metric("Overdue Loans", f"{(df['days_overdue'] > 0).sum()}")
col4.metric("Average Interest Rate", f"{df['interest_rate'].mean():.1f}%")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 Clients", "💰 Loans", "📈 Analytics"])

with tab1:
    st.subheader("Loan Status Distribution")
    fig = px.pie(df, names='status', title="Loan Status")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Clients Data")
    filtered_df = df if "All Regions" in regions else df[df['region'].isin(regions)]
    st.dataframe(filtered_df, use_container_width=True)

with tab3:
    st.subheader("Issued Loans")
    st.dataframe(df.sort_values('loan_date', ascending=False), use_container_width=True)

with tab4:
    st.subheader("Loans Issuance Dynamics")
    daily = df.groupby('loan_date')['loan_amount'].sum().reset_index()
    fig2 = px.line(daily, x='loan_date', y='loan_amount', title="Daily Loan Issuance")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(df, x='interest_rate', title="Interest Rate Distribution")
    st.plotly_chart(fig3, use_container_width=True)

st.caption("Developed by 2nd year Computer Science student during Industrial Practice at KMF Bank • June 2026")