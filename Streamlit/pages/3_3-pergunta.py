import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os


st.set_page_config(
  page_title="Pergunta 3"
)


def main():
  fatos = pd.read_csv("dw/csv/fato.csv", sep=';')
  orgaos = pd.read_csv("dw/csv/orgao.csv", sep=';')
  data = pd.read_csv("dw/csv/data.csv", sep=';', parse_dates=['dia_data'])
  municipios = pd.read_csv("dw/csv/localizacao.csv", sep=';')
  
  st.markdown("# Terceira pergunta:")
  st.markdown("## Qual a média dos valores das licitações ?")
  st.write("\n")

  stateList = municipios['uf'].unique().tolist()
  orgaosList = orgaos['nome_orgao'].unique().tolist()

  
  selectYear = st.selectbox ("Selecione o ano", [2019, 2020])

  selectedStates = st.multiselect('Filtre por Estado', stateList)
  orgao = st.multiselect('Filtre por Órgão', orgaosList)
  rangeDate = data.loc[data['ano'] == selectYear]

  fatos = fatos[fatos['dim_localizacao_id'] != 838]

  merged_df = pd.merge(rangeDate, fatos, left_on='id', right_on='dim_data_abertura_id')

  # filtro por estado
  if(len(selectedStates) > 0):
    stateListId = municipios[municipios['uf'].isin(selectedStates)]['id'].tolist()
    merged_df = merged_df[merged_df['dim_localizacao_id'].isin(stateListId)]
  
  # filtro por orgão
  if(len(orgao) > 0):
    st.write(orgao)
    orgaoId = orgaos.loc[orgaos['nome_orgao'].isin(orgao)]['id'].values
    merged_df = merged_df.loc[merged_df['dim_orgao_id'].isin(orgaoId)]

  # average_by_month = merged_df.groupby(merged_df['dia_data'].dt.month)['valor_licitacao'].mean().reset_index()

  merged_df = pd.merge(merged_df, municipios, left_on='dim_localizacao_id', right_on='id', suffixes=('', '_municipio'))
  
  average_by_month_location = merged_df.groupby([merged_df['dia_data'].dt.month, 'uf'])['valor_licitacao'].mean().reset_index()

  # average_by_month_location = merged_df.groupby([merged_df['dia_data'].dt.month, 'uf'])['valor_licitacao'].mean().reset_index()
  average_by_month_location['dia_data'] = average_by_month_location['dia_data'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))


  fig = px.line(average_by_month_location, x='dia_data', y='valor_licitacao', color='uf',
                  labels={'valor_licitacao': 'Média dos Valores de Licitação'},
                  title='Média dos Valores de Licitação por Mês e por Estado')
    
    # Adiciona o formato de data ao eixo x
  fig.update_xaxes(type='category')
  
  # Exibe o gráfico
  st.plotly_chart(fig)

if __name__ == '__main__':
  main()