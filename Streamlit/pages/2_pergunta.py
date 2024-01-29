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
  loc = pd.read_csv("dw/csv/localizacao.csv", sep=';')
  orgaos = pd.read_csv("dw/csv/orgao.csv", sep=';')
  
  st.markdown("# Segunda pergunta:")
  st.markdown(" ## Dado um órgão, qual o valor total gasto em licitação por Estado?")
  st.write("\n")

  orgaosList = orgaos['nome_orgao'].copy()

  orgao = st.selectbox('Escolha um órgão', orgaosList)

  orgaoId = orgaos.loc[orgaos['nome_orgao'] == orgao]['id'].values[0]

  facts = fatos.loc[fatos['dim_orgao_id'] == orgaoId]
  factValAndLoc = pd.DataFrame({
    'id': facts['dim_localizacao_id'], 
    'valor': facts['valor_licitacao']
  })
  factValAndLoc2 = pd.merge(factValAndLoc, loc, on='id')
  locId = facts['dim_localizacao_id'].unique()

  result = factValAndLoc2.groupby('uf')['valor'].sum().reset_index()

  st.dataframe(result)
  st.write(locId)
  st.write(facts.count())


  st.write(orgao)
  st.write(orgaoId)




if __name__ == '__main__':
  main()