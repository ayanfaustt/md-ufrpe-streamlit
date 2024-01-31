import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
  page_title="Pergunta 1"
)


def main():
  fatos = pd.read_csv("dw/csv/fato.csv", sep=';')
  data = pd.read_csv("dw/csv/data.csv", sep=';', parse_dates=['dia_data'])
  municipios = pd.read_csv("dw/csv/localizacao.csv", sep=';')
  
  st.markdown("# Primeira pergunta:")
  st.markdown("## Qual a média gasta em licitações por municipio dada uma janela de tempo ?")
  st.write("\n")
  st.write("Seleciona o perído desejado (selecione um período entre 01/01/2019 - 31/12/2020):")

  initialDate = st.date_input("Data inicial")
  finalDate = st.date_input("Data final")
  st.write('\n')

  initialDateId = data.loc[data['dia_data'] == initialDate.isoformat()]
  finalDateId = data.loc[data['dia_data'] == finalDate.isoformat()]

  selectedFate = fatos.loc[
    (fatos['dim_data_abertura_id'] >= initialDateId['id'].values[0]) &
    (fatos['dim_data_abertura_id'] <= finalDateId['id'].values[0])
  ]

  if(len(selectedFate) > 0) :
    cities = municipios[municipios['id'].isin(selectedFate['dim_localizacao_id'])]
    cityIdWithValue = pd.DataFrame({
      'id': selectedFate['dim_localizacao_id'],
      'valor': selectedFate['valor_licitacao']
    })
    factAndCities = pd.merge(cityIdWithValue, cities, on='id')
    cityAndValue = pd.DataFrame({
      'municipio': factAndCities['municipio'],
      'valor': factAndCities['valor']
    })

    result = cityAndValue.groupby('municipio')['valor'].mean().sort_values(ascending=True)

    barPerPage = 5

    pageNumbers = len(result) // barPerPage + (len(result) % barPerPage > 0)

    selectedPage = st.number_input("select page", 1, pageNumbers)
    start = (selectedPage - 1) * barPerPage
    end = start + barPerPage

    currentPage = result.iloc[start:end]

    fig, ax = plt.subplots(figsize=(10, 6))
    currentPage.plot(kind='barh', color='blue', ax=ax)
    ax.set_title('Média por município em R$')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)



if __name__ == '__main__':
  main()