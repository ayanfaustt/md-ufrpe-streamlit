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
  st.write("Selecione o perído desejado (selecione um período entre 01/01/2019 - 31/12/2020):")

  initialDate = st.date_input("Data inicial")
  finalDate = st.date_input("Data final")
  st.write('\n')

  stateList = municipios['uf'].unique().tolist()
  selectedStates = st.multiselect('Escolha os Estados que deseja filtrar:', stateList)

  initialDateId = data.loc[data['dia_data'] == initialDate.isoformat()]
  finalDateId = data.loc[data['dia_data'] == finalDate.isoformat()]


  selectedFate = fatos.loc[
    (fatos['dim_data_abertura_id'] >= initialDateId['id'].values[0]) &
    (fatos['dim_data_abertura_id'] <= finalDateId['id'].values[0])
  ]


  if(len(selectedStates) > 0):
    stateListId = municipios[municipios['uf'].isin(selectedStates)]['id'].tolist()
    selectedFate = selectedFate[selectedFate['dim_localizacao_id'].isin(stateListId)]

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

    optionView  =st.radio('Selecione o tipo de visualização: ', ['Paginação', 'Visualização única'])
    fig2 = None
    if(optionView == 'Paginação'):
      barPerPage = 5

      pageNumbers = len(result) // barPerPage + (len(result) % barPerPage > 0)

      selectedPage = st.number_input("select page", 1, pageNumbers)
      start = (selectedPage - 1) * barPerPage
      end = start + barPerPage

      currentPage = result.iloc[start:end]
      fig2 = px.bar(currentPage,
                    x=currentPage.index, 
                    y='valor', 
                    labels={'valor': 'Média em R$'},
                    title='Média por município em R$',
                    height=500)
    else:
      fig2 = px.bar(result,
                    x=result.index, 
                    y='valor', 
                    labels={'valor': 'Média em R$'},
                    title='Média por município em R$',
                    height=500)
  
    fig2.update_layout(xaxis_title='Município', yaxis_title='Média em R$')
    st.plotly_chart(fig2)



if __name__ == '__main__':
  main()