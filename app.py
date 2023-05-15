import pandas as pd #pip install pandas openpyxL
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Alianzas", page_icon=":bar_chart:", layout="wide")

df = pd.read_excel (
    io='bd_23.xlsx', 
    engine='openpyxl', 
    sheet_name='alumnos',
    skiprows=0,
    usecols='A:O',
    nrows=663,

)

df['year'] = df['year'].astype(str).str.replace('.', '')

# -- Barra lateral --

st.sidebar.header("filtra la información aquí: ")

país = st.sidebar.multiselect(
"Seleciona el País: ", 
options=df["País"].unique(),
default=df["País"].unique()
)

año = st.sidebar.multiselect(
"Seleciona el Año: ", 
options=df["year"].unique(),
default=df["year"].unique()

)

sexo = st.sidebar.multiselect(
"Seleciona el Sexo: ", 
options=df["Sexo"].unique(),
default=df["Sexo"].unique()

)


carrera = st.sidebar.multiselect(
"Seleciona la Carrera: ", 
options=df["Carrera"].unique(),
default=df["Carrera"].unique()

)

movilidad = st.sidebar.multiselect(
"Seleciona la Movilidad saliente o entrante: ", 
options=df["Movilidad"].unique(),
default=df["Movilidad"].unique()

)


df_selection = df.query(

    "País == @país & Sexo == @sexo & year == @año & Movilidad == @movilidad & Carrera == @carrera" 
)


# -- pagina principal --

st.title(":bar_chart: Datos de Alianzas Internacionales FIUDEC" )
st.markdown('##')

#Top KPI's

Movilidad_Total = int(df_selection["cantidad"].sum())

alumnos_entrantes = df_selection[df["Movilidad"] == "Entrante"]

alumnos_salientes = df_selection[df["Movilidad"] == "Saliente"]

foreign_students = len(alumnos_entrantes.value_counts())

international_internships = len(df_selection[df["kpi2030"] == "International internships"].value_counts())

students_abroad = len(df_selection[df["kpi2030"] == "Student’s abroad"].value_counts())

uno, dos, tres, cuatro = st.columns(4)
with uno: 
    st.subheader("Estudiantes con movilidad internacional fiudec:")
    st.subheader(Movilidad_Total)
with dos:
    st.subheader("foreign students:")
    st.subheader(foreign_students)
with tres:
    st.subheader("International internships:")
    st.subheader(international_internships)
with cuatro:
    st.subheader("Student’s abroad:")
    st.subheader(students_abroad)

st.markdown("---")

#grafico cantidad por sexo

fig_sexo = px.histogram(
    
    df, 
    x=df_selection["Sexo"], 
    y=df_selection["cantidad"], 
    color=df_selection["Movilidad"], 
    barmode="group",
    title="Cantidad de estudiantes entrantes y salientes por género"
    
    
    )


st.plotly_chart(fig_sexo, use_container_width=True)

#grafico cantidad por carrera

fig_carrera = px.bar(
    
    df,
    y=df_selection["Carrera"], 
    x=df_selection["cantidad"], 
    color=df_selection["Movilidad"], 
    barmode="group",
    title="Cantidad de estudiantes entrantes y salientes por carrera",
    
    )

st.plotly_chart(fig_carrera, use_container_width=True)

#grafico cantidad por año


fig_año = px.bar(
    
    df,
    y=df_selection["year"], 
    x=df_selection["cantidad"], 
    color=df_selection["Movilidad"], 
    barmode="group",
    title="Cantidad de estudiantes entrantes y salientes por año",
    height=700
    
    )

st.plotly_chart(fig_año, use_container_width=True)

#grafico cantidad por país

fig_pais = px.bar(
    
    df, 
    y=df_selection["País"], 
    x=df_selection["cantidad"], 
    color=df_selection["Movilidad"], 
    barmode="group",
    title="Cantidad de estudiantes entrantes y salientes por país",
    
    )

st.plotly_chart(fig_pais, use_container_width=True)

#grafico cantidad por Universidad

fig_universidad = px.bar(
    
    df, 
    y=df_selection["Universidad"], 
    x=df_selection["cantidad"], 
    color=df_selection["Movilidad"], 
    barmode="group",
    title="Cantidad de estudiantes entrantes y salientes por Universidad",
    height=1000
        
    )

st.plotly_chart(fig_universidad, use_container_width=True)

#grafico tipo de movilidad

fig_tipo_de_movilidad = px.bar(
    
    df, 
    y=df_selection["Actividad"], 
    x=df_selection["cantidad"], 
    color=df_selection["Movilidad"], 
    barmode="group",
    title="Tipo de actividad realizada por los estudiantes",
        
    )

st.plotly_chart(fig_tipo_de_movilidad, use_container_width=True)

# entregar las top 5 universidades de los alumnos entrantes en un peridoo

conteo_universidades_entrantes = alumnos_entrantes.groupby(df_selection["Universidad"])["País"].value_counts()

top_universidades_entrantes = conteo_universidades_entrantes.sort_values(ascending=False).head(5)

conteo_universidades_salientes = alumnos_salientes.groupby(df_selection["Universidad"])["País"].value_counts()

top_universidades_salientes = conteo_universidades_salientes.sort_values(ascending=False).head(5)

st.write('Top 5 universidades de origen extranjeros:')
st.dataframe(top_universidades_entrantes, use_container_width=True)
st.write('Top 5 universidades de destino alumnos fiudec:')
st.dataframe(top_universidades_salientes, use_container_width=True)

