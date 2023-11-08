import numpy as np
import pandas as pd
import streamlit as st


def main():
    st.write("Hello World!")


name = st.sidebar.text_input("あなたの名前は？")
age = st.sidebar.slider("あなたの年齢は？", 0, 100, 10)

dataframe = pd.DataFrame(
    np.random.randn(10, 20), columns=("col %d" % i for i in range(20))
)

st.write("This is a area_chart.")
st.area_chart(dataframe)

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
)

st.map(df)

if __name__ == "__main__":
    main()
