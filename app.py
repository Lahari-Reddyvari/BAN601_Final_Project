import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

#Page layout
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    page_icon="🛍️"
)
st.markdown(
 """
    <style>
    /* Remove top white space */
    .block-container {
        padding-top: 1rem !important;
    }
    /* Soft navy sidebar with dark text */
    [data-testid="stSidebar"] {
        background-color: #eceff4;
    }
    [data-testid="stSidebar"] * {
        color: #1a1a2e !important;
    }
    h2, h3 {
    color: #3d5a99 !important;
    }
    .stMetricLabel {color: #3d5a99;}
    </style>
    """,
    unsafe_allow_html=True
)
#Title
st.title("Sales Performance Dashboard for Accessories")

#Loading dataset
df = pd.read_csv("sales_data.csv")
df["Year"] = df["Year"].astype(int)

#Creating a select box for Year and Product
st.sidebar.header("Filter Options")
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
product = st.sidebar.selectbox("Select Product", ["Handbags_Sales", "Wallets_Sales"])
filtered_df = df[df["Year"] == year].copy()
filtered_df["Cumulative_Sales"] = filtered_df[product].cumsum()

colors = {
    "Handbags_Sales": "pink",
    "Wallets_Sales": "green"
}

#LinePlot
plt.rcParams['font.size'] = 8
fig1, ax = plt.subplots(figsize=(5, 3))
fig1.patch.set_facecolor("#eceff4")
ax.set_facecolor("#eceff4")
sns.lineplot(
    data=filtered_df,
    x="Month",
    y=product,
    marker="o",
    linewidth=2,
    markersize=5,
    color=colors[product],
    ax=ax
)
ax.set_title(f"{product.replace('_', ' ')} Trend in {year}", fontsize=10, color="#333333")
ax.set_xlabel("Month", fontsize=10)
ax.set_ylabel("Sales", fontsize=10)
ax.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)

#Cummulative Sales
fig2, ax2 = plt.subplots(figsize=(5, 3))
fig2.patch.set_facecolor("#eceff4")
ax2.set_facecolor("#eceff4")
sns.lineplot(
    data=filtered_df,
    x="Month",
    y="Cumulative_Sales",
    marker="o",
    color="orange",
    ax=ax2
)
ax2.set_title(f"Cumulative {product.replace('_', ' ')} in {year}", fontsize=10)
ax2.set_xlabel("Month", fontsize=10)
ax2.set_ylabel("Sales", fontsize=10)
ax2.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{product.replace('_', ' ')} Trend")
    st.pyplot(fig1)

with col2:
    st.subheader(f"Cumulative {product.replace('_', ' ')} Trend")
    st.pyplot(fig2)

#Summary statistics
st.subheader("Summary Statistics")
st.write(df[["Handbags_Sales","Wallets_Sales"]].describe().round(2))

#Total Sales
total_sales = filtered_df[product].sum()
st.metric(label=f"Total {product.replace('_', ' ')} in {year}", value=f"{total_sales:,}")
