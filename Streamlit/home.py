import streamlit as st

def main():

    st.set_page_config(
        layout="centered",
        page_title="Home",
        page_icon="🏠"
        )
    st.title("🏠 Data Warehouse Licitação")

    st.write("Este projeto tem como objetivo mostrar informações sobre as licitações realizadas no período de 01/01/2019 - 31/12/2020")

    st.subheader("Grupo 03 - Integrantes:")
    st.write("- Ayan Faustt")
    st.write("- Diego Diniz")
    st.write("- Diogo de Souza")
    st.write("- Querem Hapuque")
    st.write("- Lucas Lima")

if __name__ == '__main__':
    main()