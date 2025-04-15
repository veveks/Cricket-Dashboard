import streamlit as st
import pandas as pd

# Load the CSV data
df = pd.read_csv("F:\\dataScience\\TNCA Dashboard\\2025-04-03-17-12-05.csv", on_bad_lines='skip')

# Clean data if necessary (e.g., strip whitespaces)
df.columns = df.columns.str.strip()

# Sidebar for Batsman Input
st.sidebar.header("Filters")

# Batsman input - allows typing in name
batsman_input = st.sidebar.text_input("Enter Batsman Name", "")

# Filter batsmen based on the input
if batsman_input:
    matching_batsmen = df[df['StrikerName'].str.contains(batsman_input, case=False, na=False)]['StrikerName'].unique()
    if len(matching_batsmen) > 0:
        batsman_name = st.sidebar.selectbox("Select Batsman", matching_batsmen)
    else:
        st.sidebar.write("No matching batsman found.")
else:
    batsman_name = None

# If a batsman is selected
if batsman_name:
    # Filter the dataframe based on the batsman selected
    filtered_batsman_df = df[df['StrikerName'] == batsman_name]
    
    # Dynamically filter available grounds based on selected batsman
    grounds = filtered_batsman_df['GroundName'].unique()
    selected_grounds = st.sidebar.multiselect("Select Grounds", grounds)

    # Multiple Bowler Type Filter
    bowler_types = df['BowlerType'].unique()
    selected_bowler_types = st.sidebar.multiselect("Select Bowler Types", bowler_types, default=bowler_types)

    # Filter the dataframe based on selected grounds and bowler types
    filtered_df = filtered_batsman_df[(filtered_batsman_df['GroundName'].isin(selected_grounds)) & 
                                      (filtered_batsman_df['BowlerType'].isin(selected_bowler_types))]

    # Calculate average runs and strike rate per match
    filtered_df['BallRuns'] = pd.to_numeric(filtered_df['BallRuns'], errors='coerce')  # Convert BallRuns to numeric

    # Average Runs per Match
    average_runs = filtered_df.groupby('MatchId')['BallRuns'].sum().mean()

    # Strike Rate per Match
    total_balls = filtered_df.groupby('MatchId')['BallNumber'].max()
    total_runs = filtered_df.groupby('MatchId')['BallRuns'].sum()
    strike_rate = (total_runs / total_balls) * 100

    # Display results
    st.title("Cricket Performance Dashboard")

    # Show average runs and strike rate
    st.subheader(f"Average Runs for {batsman_name}: {average_runs:.2f}")
    st.subheader(f"Strike Rate for {batsman_name}: {strike_rate.mean():.2f}")

    # Show the filtered data
    st.subheader("Filtered Ball-by-Ball Data")
    st.dataframe(filtered_df)

else:
    st.write("Please enter a batsman name to get the data.")
