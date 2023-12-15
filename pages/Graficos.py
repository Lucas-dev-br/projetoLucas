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
st.title("Analise de produto e preços")
st.subheader("Pré-visualização dos dados:")
st.write(df_product_prices.head())

# Interactive filter for selecting products
selected_product = st.selectbox("Selecione o produto:", df_product_prices['productname'].unique())

# Filter data for the selected product
filtered_data = df_product_prices[df_product_prices['productname'] == selected_product]

# Visualization options
visualization_option = st.radio("Selecione o tipo de visualização:", ["Gráfico de linha", "Gráfico de barras", "Gráfico de dispersão"])

# Interactive filter for selecting cities
selected_cities = st.multiselect("Selecionar as cidades:", filtered_data.columns[2:6])

# Plot selected visualization
st.subheader(f"{visualization_option} para {selected_product} nas cidades selecionadas:")
if visualization_option == "Gráfico de linha":
    fig = px.line(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")
elif visualization_option == "Gráfico de barras":
    fig = px.bar(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")
elif visualization_option == "Gráfico de dispersão":
    fig = px.scatter(filtered_data, x='date', y=selected_cities, title=f"{selected_product} Prices Over Time")

# Show the interactive chart
st.plotly_chart(fig)

# Summary statistics
st.subheader("Estatísticas resumidas:")
if selected_cities:
    st.write(filtered_data[selected_cities].describe())
else:
    st.warning("Porfavor selecione ao menos uma cidade para mostrar o grafico.")