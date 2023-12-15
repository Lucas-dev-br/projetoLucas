import streamlit as st
import pandas as pd

# Link para o conjunto de dados no Kaggle
dataset_link = "https://www.kaggle.com/datasets/everydaycodings/produce-prices-dataset/"

df_product_prices = pd.read_csv('produto.csv')

st.title("Análise de Produtos e Preços")
st.write(
    "Esta análise utiliza dados sobre produtos e preços. "
    "Os dados contêm informações sobre o nome do produto, data, preço na fazenda, preço no varejo em diferentes cidades, e informações sobre os preços médios."
)

total_produto_precos = df_product_prices.shape[0]
total_colunas_produto_precos = df_product_prices.shape[1]
st.subheader(f"Total de Produtos e Preços")
st.write(f"Total de produtos e preços: {total_produto_precos}")
st.write(f"Total de colunas na tabela: {total_colunas_produto_precos}")

st.header("Dados Completos de Produtos e Preços")
st.write(df_product_prices)

st.header("Análise de Preços por Produto")
produtos = df_product_prices['productname'].unique()
produto_selecionado = st.selectbox("Selecione um produto:", produtos)

df_produto_selecionado = df_product_prices[df_product_prices['productname'] == produto_selecionado]

st.subheader(f"Informações sobre {produto_selecionado}")
st.write(df_produto_selecionado)

st.subheader("Informações sobre as Colunas")
st.write("""
- productname: Nome do produto.
- date: Data do registro.
- farmprice: Preço na fazenda.
- atlantaretail: Preço no varejo em Atlanta.
- chicagoretail: Preço no varejo em Chicago.
- losangelesretail: Preço no varejo em Los Angeles.
- newyorkretail: Preço no varejo em Nova York.
- averagespread: Média dos preços no varejo.
""")

total_colunas_produto_precos = df_product_prices.shape[1]
total_linhas_produto_precos = df_product_prices.shape[0]

st.subheader("Total de Colunas, Linhas e Tabelas")
st.write(f"Total de colunas na tabela: {total_colunas_produto_precos}")
st.write(f"Total de linhas na tabela: {total_linhas_produto_precos}")

# Adicionando um pouco sobre a história do comércio
st.header("História do Comércio:")
st.write(
    "O comércio é uma parte fundamental da história da humanidade, remontando aos tempos mais antigos. "
    "Desde as rotas comerciais da Antiguidade até os modernos mercados globais, o comércio desempenhou um papel vital "
    "no intercâmbio de bens e culturas entre diferentes regiões. "
    "No contexto dos dados analisados, observamos a dinâmica dos preços de diferentes produtos em várias cidades, "
    "capturando uma pequena parte da complexa história do comércio."
)

# Adicionando link para o Kaggle
st.subheader("Conjunto de Dados no Kaggle:")
st.write(f"O conjunto de dados foi obtido no Kaggle. Você pode acessá-lo [aqui]({dataset_link}).")