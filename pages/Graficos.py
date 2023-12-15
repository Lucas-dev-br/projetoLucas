import pandas as pd
import streamlit as st
import plotly.express as px

# Load data from CSV
file_path = "produto.csv"  # Replace with the actual file path
try:
    df_product_prices = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"File not found: {file_path}")
    st.stop()

# Display the data
st.title("Product and Price Analysis")
st.subheader("Preview of the Data:")
st.write(df_product_prices.head())

# Interactive filter for selecting products
selected_product = st.selectbox("Select a Product:", df_product_prices['productname'].unique())

# Filter data for the selected product
filtered_data = df_product_prices[df_product_prices['productname'] == selected_product]

# Visualization options
visualization_option = st.radio("Select Visualization Type:", ["Line Chart", "Bar Chart", "Scatter Plot"])

# Interactive filter for selecting cities
selected_cities = st.multiselect("Select Cities:", filtered_data.columns[2:6])

# Plot selected visualization
st.subheader(f"{visualization_option} for {selected_product} in Selected Cities:")
if visualization_option == "Line Chart":
    fig = px.line(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")
elif visualization_option == "Bar Chart":
    fig = px.bar(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")
elif visualization_option == "Scatter Plot":
    fig = px.scatter(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")

# Show the interactive chart
st.plotly_chart(fig)

# Summary statistics
st.subheader("Summary Statistics:")
if selected_cities:
    st.write(filtered_data[selected_cities].describe())
else:
    st.warning("Please select at least one city for summary statistics.")