import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
  page_title="Pergunta2"
)


def main():
  fatos = pd.read_csv("dw/csv/fato.csv", sep=';')
  orgaos = pd.read_csv("dw/csv/orgao.csv", sep=';')
  municipios = pd.read_csv("dw/csv/localizacao.csv", sep=';')
  
  st.markdown("# Segunda pergunta:")
  st.markdown("## Dado um município, quais as unidades gestora são responsáveis pela maior quantidade de licitações?")
  st.write("\n")

  municipio_selecionado = st.selectbox ("Selecione um município:", municipios.municipio)

  st.write("Você selecionou:", municipio_selecionado)

  # Criando um dicionário de mapeamento de municípios para IDs
  mapa_municipios_ids = dict(zip(municipios['municipio'], municipios['id']))

  # Obtendo o ID correspondente
  id_municipio = mapa_municipios_ids[municipio_selecionado]
  st.write(f"ID do município {municipio_selecionado}: {id_municipio}")

  linhas_filtradas = fatos[fatos['dim_localizacao_id'] == id_municipio]
  st.write(linhas_filtradas)

  nome_dos_ngc = orgaos[['nome_orgao', 'id']]
  dados_com_nomes_orgaos = pd.merge(nome_dos_ngc, linhas_filtradas, left_on='id', right_on='dim_orgao_id')

  contagem_por_orgao = dados_com_nomes_orgaos['nome_orgao'].value_counts()
  

  st.write("Contagem de licitações por orgao:")
  st.write(contagem_por_orgao)
  
if __name__ == '__main__':
  main()