# How to Run this App:
# cd api_file_uploader
# pipenv run streamlit run app.py

import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
