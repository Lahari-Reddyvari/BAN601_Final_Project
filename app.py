import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    page_icon="📊"
)

# --- Apply Blue Theme ---
st.markdown(
    """
    <style>
    .css-1d391kg h1 {color: #008080;}
    .css-1v3fvcr h2 {color: #008080;}
    .stMetricLabel {color: #008080;}
    .css-18e3th9 {background-color: #e6ffff;}
    </style>
    """,
    unsafe_allow_html=True
)
#Title
st.title("Sales Performance Dashboard for Accessories")
#Loading dataset
df = pd.read_csv("sales_data.csv")
#View dataset
df.head()

#creating a select box for year and product
st.sidebar.header("Filter Options")
year = st.sidebar.selectbox("Select Year", df["Year"].unique())
product = st.sidebar.selectbox("Select Product", ["Handbags_Sales", "Wallets_Sales"])
filtered_df = df[df["Year"] == year]

fig, ax = plt.subplots(figsize=(5, 3))

#plot
colors = {
    "Handbags_Sales": "blue",
    "Wallets_Sales": "green"
}

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
ax.set_title(f"{product.replace('_', ' ')} Trend in {year}", fontsize=8, color="#333333")
ax.set_xlabel("Month", fontsize=8)
ax.set_ylabel("Sales", fontsize=8)
ax.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig)

st.pyplot(fig)
#Cumulative Sales
filtered_df["Cumulative_Sales"] = filtered_df[product].cumsum()
st.subheader(f"Cumulative {product.replace('_', ' ')} Trend")
fig2, ax2 = plt.subplots(figsize=(5, 3))
sns.lineplot(
    data=filtered_df,
    x="Month",
    y="Cumulative_Sales",
    marker="o",
    color="orange",
    ax=ax2
)
ax2.set_title(f"Cumulative {product.replace('_', ' ')} in {year}", fontsize=8)
ax2.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)
st.pyplot(fig2)

with col2:
    st.pyplot(fig2)

#Summary statistics
st.subheader("Summary Statistics")
st.write(df[["Handbags_Sales","Wallets_Sales"]].describe().round(2))

#Total Sales
total_sales = filtered_df[product].sum()
st.metric(label=f"Total {product.replace('_', ' ')} in {year}", value=total_sales)


