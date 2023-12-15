import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Carregar o DataFrame
try:
    df_product_prices = pd.read_csv("produto.csv", thousands=",")
except FileNotFoundError:
    st.error("Arquivo não encontrado. Certifique-se de que o arquivo 'produto.csv' está no diretório correto.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("O arquivo 'produto.csv' está vazio.")
    st.stop()
except pd.errors.ParserError:
    st.error("Erro ao ler o arquivo 'produto.csv'. Verifique se o formato do arquivo está correto.")
    st.stop()

# Verificar se as colunas necessárias estão presentes
required_columns = ["productname", "date", "farmprice", "atlantaretail", "chicagoretail", "losangelesretail", "newyorkretail", "averagespread"]
missing_columns = set(required_columns) - set(df_product_prices.columns)

if missing_columns:
    st.error(f"As seguintes colunas estão faltando no arquivo: {', '.join(missing_columns)}")
    st.stop()

# Lista de colunas de preço
price_columns = ["farmprice", "atlantaretail", "chicagoretail", "losangelesretail", "newyorkretail"]

# Remover símbolo de dólar e vírgulas, substituir valores em branco por NaN e converter para float
df_product_prices[price_columns + ["averagespread"]] = df_product_prices[price_columns + ["averagespread"]].replace('[\$,]', '', regex=True).replace('', np.nan).apply(pd.to_numeric, errors='coerce')

# Utilizar a função melt para transformar colunas de cidade em uma única coluna
df_product_prices_melted = pd.melt(df_product_prices, id_vars=["productname", "date", "averagespread"], value_vars=price_columns, var_name="city", value_name="price")

# Filtros interativos
selected_product = st.selectbox("Selecione um produto:", df_product_prices_melted["productname"].unique())
selected_city_options = df_product_prices_melted[df_product_prices_melted["productname"] == selected_product]["city"].unique()
selected_city = st.selectbox("Selecione uma cidade:", selected_city_options)

# Adicionar print para verificar os dados antes de aplicar filtros
print("Dados antes de aplicar filtros:")
print(df_product_prices_melted)

# Aplicar filtros
filtered_data = df_product_prices_melted[(df_product_prices_melted["productname"] == selected_product) & (df_product_prices_melted["city"] == selected_city)]

# Adicionar print para verificar os dados após aplicar filtros
print("Dados após aplicar filtros:")
print(filtered_data)

if filtered_data.empty:
    st.warning(f"Nenhum dado encontrado para {selected_product} em {selected_city}. Tente selecionar outras opções.")
    st.stop()

# Adicionar print para verificar os dados antes de calcular a média
print("Dados antes de calcular a média:")
print(filtered_data)

# Calcular a média de lucro em cada cidade
df_avg_profit = filtered_data.groupby("city")["averagespread"].mean()

# Calcular a diferença em porcentagem
df_avg_profit_diff = df_avg_profit.sub(df_avg_profit[selected_city]).div(df_avg_profit[selected_city]).mul(100)

# Adicionar print para verificar os dados após calcular a média
print("Dados após calcular a média:")
print(df_avg_profit_diff)

# Criar gráfico de barra para a diferença de valores em porcentagem
fig_avg_profit_diff = px.bar(
    x=df_avg_profit_diff.index,
    y="averagespread",
    data_frame=df_avg_profit_diff.reset_index(),
    labels={"averagespread": "Diferença Percentual (%)"},
    title=f"Diferença Percentual da Média de Lucro em Relação a {selected_city} ({selected_product} - {selected_city})"
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig_avg_profit_diff)

# Adicionar gráfico de linhas interativo para o histórico de preço
fig_price_history = px.line(
    filtered_data,
    x="date",
    y="price",
    color="city",
    markers=True,
    title=f"Histórico de Preço do Produto em Cada Cidade ao Longo do Tempo ({selected_product} - {selected_city})",
    labels={"price": "Preço", "date": "Data"},
)

# Mostrar o gráfico de linhas no Streamlit
st.plotly_chart(fig_price_history)

print("Colunas em df_product_prices_melted:")
print(df_product_prices_melted.columns)


# Calcular o percentual de lucro para cada linha
df_product_prices_melted["pct_lucro"] = ((df_product_prices_melted["price"] - df_product_prices_melted["farmprice"]) / df_product_prices_melted["farmprice"]) * 100

# Adicionar print para verificar os dados antes de aplicar filtros
print("Dados antes de aplicar filtros:")
print(df_product_prices_melted)

# Restante do seu código para filtros interativos e gráficos...

# Calcular a média do percentual de lucro agrupado por produto e cidade
df_avg_pct_lucro = df_product_prices_melted.groupby(["productname", "city"])["pct_lucro"].mean().reset_index()

# Adicionar print para verificar os dados antes de criar o gráfico
print("Dados antes de criar o gráfico de barras do percentual de lucro:")
print(df_avg_pct_lucro)

# Criar gráfico de barras para o percentual de lucro médio
fig_avg_pct_lucro = px.bar(
    df_avg_pct_lucro,
    x="city",
    y="pct_lucro",
    color="productname",
    title="Percentual Médio de Lucro por Produto em Cada Cidade",
    labels={"pct_lucro": "Percentual de Lucro Médio (%)", "city": "Cidade"}
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig_avg_pct_lucro)