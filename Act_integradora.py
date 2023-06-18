# Librerías 
import pandas as pd 
import streamlit as st 
import plotly.express as px

# Cargamos los datos 
crime = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

# Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard San Francisco Police",
    page_icon="🚓",
    layout="wide")
# Título del Dasboard 
st.title("Datos Departamento Policía San Francisco 👮🚓")
         
st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.")

# Modificaciones de tipos de dato 
crime["Incident Date"] = pd.to_datetime(crime["Incident Date"])
#crime
# Modificación de valores latitud y longuitud

mapa = pd.DataFrame()
# Cambios de nombres en las variables 

# Mapa 
mapa["Date"] = crime["Incident Date"]
mapa["Day"] = crime["Incident Day of Week"]
mapa["Police District"] = crime["Police District"]
mapa["lat"] = crime["Latitude"]
mapa["lon"] = crime["Longitude"]
mapa["Neighborhood"]= crime["Analysis Neighborhood"]
mapa["Incident Category"]= crime["Incident Category"]
mapa = mapa.dropna()
#st.map(subset_data)

# Procesamiento para gráficas
# Gráfica crímenes por distrito policial 
crime_district = crime.groupby("Police District").count().reset_index()
crime_district = crime_district.sort_values(by='Row ID', ascending=False)

# Gráfica crimenes por vecindario 
crime_nei = crime.groupby(["Analysis Neighborhood"]).count().reset_index()
crime_nei = crime_nei.sort_values(by='Row ID', ascending=False)
# Filtrar top crimenes por vecindario 
crime_nei_top = crime_nei[crime_nei["Row ID"] > 10000]

# Gráfica categoría de crimenes 
crime_cat = crime.groupby(["Incident Category"]).count().reset_index()
crime_cat = crime_cat.sort_values(by='Row ID', ascending=False)
# Filtrar por delitos con mayor conteo 
crime_cat_top = crime_cat[crime_cat["Row ID"] > 6000]

# Convertir la columna 'Incident_Datetime' a formato de fecha y hora
crime['Incident Datetime'] = pd.to_datetime(crime['Incident Datetime'], format='%Y/%m/%d %I:%M:%S %p')

# Crear una nueva columna que contenga solo la hora
crime['Incident_Hour'] = crime['Incident Datetime'].dt.hour
crime_per_hour = crime.groupby("Incident_Hour").count().reset_index()

# Crear columna Incident_Day

# Convertir la columna 'Incident_Datetime' a formato de fecha y hora
crime['Incident Datetime'] = pd.to_datetime(crime['Incident Datetime'], format='%Y/%m/%d %I:%M:%S %p')


# Crear una nueva columna que contenga solo la hora
crime['Incident_Day'] = crime['Incident Datetime'].dt.day
# Agrupo la información 

crime_per_day = crime.groupby("Incident_Day").count().reset_index()



# Mostrar el widget de entrada de fecha
start_date = pd.to_datetime(st.date_input("Start date:"))
end_date = pd.to_datetime(st.date_input("End date:"))

if start_date < end_date:
    # Filtrar el dataframe por el rango de fechas
    mask = (crime["Incident Date"] > start_date) & (crime["Incident Date"] <= end_date)
    fac_group = crime.loc[mask]


# Filtros de barras laterales 
subset_data2 = mapa
police_district_input = st.sidebar.multiselect(
'Police District',
mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1 = subset_data2
neighborhood_input = st.sidebar.multiselect(
'Neighborhood',
subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) > 0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]

subset_data = subset_data1
incident_input = st.sidebar.multiselect(
'Incident Category',
subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) > 0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]



# Creamos la estructura del Dashboard 
fig_col1, fig_col2, fig_col3 = st.columns(3, gap="large")
import streamlit as st
import pydeck as pdk

# Creamos la estructura del Dashboard 
fig_col1, fig_col2, fig_col3 = st.columns(3, gap="large")

with fig_col1:
    st.markdown("<h4 style='text-align: center'>Number of crimes per Police district</h4>", unsafe_allow_html=True)
    # Crear una nueva columna que indique si cada fila corresponde al valor máximo o no
    crime_district['Máximo'] = crime_district.apply(lambda row: row['Row ID'] == crime_district['Row ID'].max(), axis=1)

    # Crear la gráfica de barras y asignar el color utilizando la nueva columna
    fig1 = px.bar(crime_district, x="Police District", y="Row ID", hover_data=['Police District'], height=500, width=400, color="Máximo", color_discrete_map={True: '#8a0e1a', False: '#0e8a7e'})
    fig1.update_xaxes(title_text="Police District")
    fig1.update_yaxes(title_text="Number of crimes")
    st.write(fig1)


with fig_col2:
    st.markdown("<h4 style='text-align: center'>Incidents per crime category</h4>", unsafe_allow_html=True)
    # Crear una nueva columna que indique si cada fila corresponde al valor máximo o no
    crime_nei_top['Máximo'] = crime_nei_top.apply(lambda row: row['Row ID'] == crime_nei_top['Row ID'].max(), axis=1)

    # Crear la gráfica de barras y asignar el color utilizando la nueva columna
    fig2 = px.pie(crime_cat_top, values='Row ID', names='Incident Category', color='Incident Category', color_discrete_sequence=["#0e8a7e", "#006c6a", "#4ec8be", "#8efefe"],
              height=500, width=500)
    st.write(fig2)

with fig_col3:
    st.markdown("<h4 style='text-align: center'>Number of crimes per Neighborhood</h4>", unsafe_allow_html=True)
    # Crear una nueva columna que indique si cada fila corresponde al valor máximo o no
    crime_nei_top['Máximo'] = crime_nei_top.apply(lambda row: row['Row ID'] == crime_nei_top['Row ID'].max(), axis=1)

    # Crear la gráfica de barras y asignar el color utilizando la nueva columna
    fig3 = px.bar(crime_nei_top, x="Analysis Neighborhood", y="Row ID", hover_data=["Analysis Neighborhood"], height=600, width=400, color="Máximo", color_discrete_map={True: '#8a0e1a', False: '#0e8a7e'})
    fig3.update_xaxes(title_text="Neighborhood")
    fig3.update_yaxes(title_text="Number of crimes")
    st.write(fig3)

fig_col4, fig_col5, fig_col6 = st.columns(3, gap="large")

with fig_col4:
    st.markdown("<h4 style='text-align: center'>Crime ocurrence per hour </h4>", unsafe_allow_html=True)
    fig4 = px.line(crime_per_hour, x="Incident_Hour", y="Row ID", hover_data=['Incident_Hour'], height=300, width=1300)
    fig4.update_xaxes(title_text="Hour of the day")
    fig4.update_yaxes(title_text="Number of crimes")
    fig4.update_traces(line_color="#0e8a7e")
    fig4.update_traces(line_width=5)
    st.write(fig4)

fig_col7, fig_col8, fig_col9 = st.columns(3, gap="large")
with fig_col4:
    st.markdown("<h4 style='text-align: center'>Crime ocurrence per month day </h4>", unsafe_allow_html=True)
    fig5 = px.line(crime_per_day, x="Incident_Day", y="Row ID", hover_data=['Incident_Day'], height=300, width=1300)
    fig5.update_xaxes(title_text="Month day")
    fig5.update_yaxes(title_text="Number of crimes")
    fig5.update_traces(line_color="#0e8a7e")
    fig5.update_traces(line_width=5)
    st.write(fig5)


st.map(subset_data)

subset_data

st.markdown("It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.")
st.markdown("Crime locations in San Francisco")
