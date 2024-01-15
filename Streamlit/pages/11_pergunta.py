import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
  page_title="Test"
)


def main():
  fatos = pd.read_csv("dw/csv/fato.csv", sep=';')
  data = pd.read_csv("dw/csv/data.csv", sep=';', parse_dates=['dia_data'])
  municipios = pd.read_csv("dw/csv/localizacao.csv", sep=';')
  
  st.markdown("# Primeira pergunta:")
  st.markdown("## Quais Municípios efetuaram um maior gasto em licitações em uma janela de tempo e qual o valor do montante ?")
  st.write("\n")
  st.write("Seleciona o perído desejado:")

  initialDate = st.date_input("Data inicial")
  finalDate = st.date_input("Data final")
  st.write('\n')

  initialDateId = data.loc[data['dia_data'] == initialDate.isoformat()]
  finalDateId = data.loc[data['dia_data'] == finalDate.isoformat()]

  selectedFate = fatos.loc[
    (fatos['dim_data_abertura_id'] >= initialDateId['id'].min()) &
    (fatos['dim_data_abertura_id'] <= finalDateId['id'].max())
  ]


  cities = municipios[municipios['id'].isin(selectedFate['dim_localizacao_id'])]
  coastForCitie = selectedFate.groupby('dim_localizacao_id')['valor_licitacao'].sum().sort_values(ascending=False)

  barPerPage = 5

  pageNumbers = len(coastForCitie) // barPerPage + (len(coastForCitie) % barPerPage > 0)

  selectedPage = st.number_input("select page", 1, pageNumbers)
  start = (selectedPage - 1) * barPerPage
  end = start + barPerPage

  currentPage = coastForCitie.iloc[start:end]

  st.dataframe(coastForCitie)

  st.dataframe(cities)

  st.dataframe(selectedFate)

  if(selectedFate is not None) :
    fig, ax = plt.subplots(figsize=(10, 6))
    currentPage.plot(kind='barh', color='blue', ax=ax)
    ax.set_title('Test')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

  # if(selectedFate is not None) :
  #   fig = go.Figure(go.Bar(
  #     x = coastForCitie,
  #     orientation='h'
  #   ))
  #   coastForCitie.T.plot(kind='bar', color='blue', ax=ax)
  #   ax.set_title('Test')
  #   plt.xticks(rotation=45, ha='right')
  #   st.pyplot(fig)



if __name__ == '__main__':
  main()