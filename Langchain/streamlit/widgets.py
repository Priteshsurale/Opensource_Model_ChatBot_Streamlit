import pandas as pd
import streamlit as st
 
 

st.write('Stramlit text input')
 
name = st.text_input('Enter Your Name:')
st.write(f'Hello {name}')


age = st.slider('Select Your Age:', 0,100,25,25)
st.write(f'Your age is  {age}')


options = ['Java','Python', 'Javascript', 'C++']
choice = st.selectbox("chose your favorite language:", options)
st.write(f'You selected {choice}')


upload_file = st.file_uploader("choose a CSV file:", type='csv')

if upload_file is not None:
    df= pd.read_csv(upload_file)
    st.write(df)




  