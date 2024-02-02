import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
  page_title="Pergunta 2"
)


def main():
  fatos = pd.read_csv("dw/csv/fato.csv", sep=';')
  data = pd.read_csv("dw/csv/data.csv", sep=';', parse_dates=['dia_data'])
  loc = pd.read_csv("dw/csv/localizacao.csv", sep=';')
  orgaos = pd.read_csv("dw/csv/orgao.csv", sep=';')
  
  st.markdown("# Segunda pergunta:")
  st.markdown(" ## Dado um órgão, qual o valor total gasto em licitação por Estado?")
  st.write("\n")

  orgaosList = orgaos['nome_orgao'].copy()

  orgao = st.selectbox('Escolha um órgão', orgaosList)

  orgaoId = orgaos.loc[orgaos['nome_orgao'] == orgao]['id'].values[0]

  fatos = fatos[fatos['dim_localizacao_id'] != 838]

  facts = fatos.loc[fatos['dim_orgao_id'] == orgaoId]

  st.write("Escolha opções de filtros: ")

  dateEnabled = st.checkbox('Habilitar datas ? (Selecione um intervalo entre 01/01/2019-31/12/2020)')

  # Filtro por data
  initialDate = st.date_input("Data inicial")
  finalDate = st.date_input("Data final")
  initialDateId = data.loc[data['dia_data'] == initialDate.isoformat()]
  finalDateId = data.loc[data['dia_data'] == finalDate.isoformat()]

  if(dateEnabled == True):
    facts = fatos.loc[
      (fatos['dim_data_abertura_id'] >= initialDateId['id'].values[0]) &
      (fatos['dim_data_abertura_id'] <= finalDateId['id'].values[0])
    ]

  # Filtro por estado
  stateList = loc[loc['uf'] != '-3']['uf'].unique().tolist()
  selectedStates = st.multiselect('Escolha os Estados que deseja filtrar:', stateList)

  if(len(selectedStates) > 0):
    stateListId = loc[loc['uf'].isin(selectedStates)]['id'].tolist()
    facts = facts[facts['dim_localizacao_id'].isin(stateListId)]

  factValAndLoc = pd.DataFrame({
    'id': facts['dim_localizacao_id'], 
    'valor': facts['valor_licitacao']
  })
  factValAndLoc2 = pd.merge(factValAndLoc, loc, on='id')
  locId = facts['dim_localizacao_id'].unique()

  result = factValAndLoc2.groupby('uf')['valor'].sum().reset_index()

  fig = px.area(result, x='uf', y='valor', hover_name='uf',
                 title=f'Valor total gasto em licitação por Estado para o órgão: {orgao}',
                 labels={'uf': 'Estado', 'valor': 'Valor Total'},
                 )
  
  st.plotly_chart(fig)

if __name__ == '__main__':
  main()