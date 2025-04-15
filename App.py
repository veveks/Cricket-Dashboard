import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("2025-04-03-17-12-05.csv")

st.title("🏏 Prem CC selection Dashboard")

# Filters
batsman = st.selectbox("Select Batsman", sorted(df['batsman'].unique()))
bowler = st.selectbox("Select Bowler", sorted(df['bowler'].unique()))

# Filtered data
filtered_df = df[(df['batsman'] == batsman) & (df['bowler'] == bowler)]

# Simple chart
st.subheader(f"Performance of {batsman} vs {bowler}")
fig = px.bar(filtered_df, x="over", y="runs", title="Runs per Over")
st.plotly_chart(fig)

# Show raw data
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df)