import streamlit as st

def main():

    st.set_page_config(
        layout="centered",
        page_title="Home",
        page_icon="🏠"
        )
    st.title("🏠 Data Warehouse Licitação")


    st.write("Este projeto tem como objetivo mostrat informações sobre as licitações realizadas no período de 01/01/2019 - 31/12/2020")

if __name__ == '__main__':
    main()