import streamlit as st
import numpy as np
import pandas as pd


# Title of the application
st.title('Hello Streamlit')



df =  pd.DataFrame({
    'name' : ['pritesh','Akanksha','Prasad','arjun'],
    'age': [24,25,24,24],
    'city':['Aurangabad','Dumka','Banglore','Surat']    
})

st.write('here is my dataFrame')
st.write(df)


df = pd.DataFrame(
    np.random.randn(20,3), columns=['a','b','c']
)


st.line_chart(df)