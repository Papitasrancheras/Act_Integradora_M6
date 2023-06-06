# Librerías 
import pandas as pd 
import streamlit as st 

# Cargamos los datos 
crime = pd.read_csv("https://drive.google.com/file/d/11oLcKiW8SgCOp3tGiQCYuRG7pLL_J-Zf/view?usp=drive_link")
st.title("Datos Departamento Policía San Francisco")
st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.")

mapa = pd.DataFrame()
mapa = mapa.dropna()
st.map(mapa.astype(int))

