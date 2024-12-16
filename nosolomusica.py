import streamlit as st
import pandas as pd
from matplotlib.colors import hsv_to_rgb
import base64
import io
df = pd.read_csv('musica_miercoles1.csv')

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            color: black;
        }}
        .stTitle, .stHeader, .stSubheader {{
            color: ##566573;
        }}
        .stButton {{
            background-color: #f0a500;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }}
        .stButton:hover {{
            background-color: #ff7f32;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Imagen de fondo (puedes cambiar esta ruta a la imagen de fondo que prefieras)
background_image_path = "foto.png"
set_background(background_image_path)

# Título de la aplicación
st.title("¡Transforma tu música en arte visual!")

# Presentación de la app
st.header("¿Qué es esta app?")
st.write("""
Esta app está diseñada para:
1. Empresas innovadoras que crean productos con forma de onda, materializando la voz diciendo una frase o simplemente, una canción. 
   El objetivo de la app es generar una experiencia única para el cliente, permitiéndoles transformar canciones o frases en piezas artísticas  personalizadas.
2. Diseñadores de portadas de albums.
3. Coloristas de videoclips.
4. Cualquier usuario que busque la esencia de una canción o sonido.

¡Haz que cada palabra o canción cobre vida! 
""")



# Título de la aplicación
st.title("Selector de Canciones")

# Sección 1: Cargar una canción
st.header("Carga una canción por ruta")
ruta_cancion = st.text_input("Introduce la ruta de la canción:")
if st.button("Subir"):
    if ruta_cancion:
        st.success(f"Ruta seleccionada: {ruta_cancion}")
    else:
        st.error("Por favor, introduce una ruta válida.")

# Sección 2: Filtros por género y subgénero
st.header("Filtrar canciones por género y subgénero")
generos = ["Rock", "Electronica"]
genero_seleccionado = st.selectbox("Selecciona un género:", generos)

# Subgéneros dependiendo del género seleccionado
if genero_seleccionado == "Rock":
    subgeneros = ["Rock Baladas", "Rock en Español", "Dark Wave"]
elif genero_seleccionado == "Electronica":
    subgeneros = ["Dance", "Remember", "Techno"]

subgenero_seleccionado = st.selectbox("Selecciona un subgénero:", subgeneros)

# Filtrar canciones
canciones_filtradas = df[df.subgenero==subgenero_seleccionado][['titulo','artista','año']]

# Elige una cancion
cancion_elegida = st.selectbox("Elige una cancion:", canciones_filtradas)

path = canciones_filtradas[canciones_filtradas.titulo==cancion_elegida]
titulo_elegido = path.iloc[0]["titulo"]
artista_elegido = path.iloc[0]["artista"]
año_elegido = str(path.iloc[0]["año"])

st.write(f"Subgénero: {subgenero_seleccionado}")
st.write(f"Título: {titulo_elegido}")
st.write(f"Artista: {artista_elegido}")
st.write(f"Género: {genero_seleccionado}")
st.write(f"Año: {año_elegido}")

if st.button("PLAY"):
    ruta = f'/Users/nosolomusica/Desktop/Análisis de Datos/Semana 8/FINAL_PROYECT/Streamlit/{subgenero_seleccionado}/{artista_elegido}_{titulo_elegido}_{genero_seleccionado}_{subgenero_seleccionado}_{año_elegido}.mp3'
    st.audio(ruta, format='audio/mp3')

df = pd.read_csv('musica_miercoles1.csv')

# Seleccionamos las columnas relevantes
features = ['zero_crossing_rate', 'rolloff', 'spectral_centroid', 'spectral_bandwidth']

# Normalizamos las columnas seleccionadas
for feature in features:
    df[feature] = df[feature].apply(lambda x: x.replace(',','.'))
    df[feature] = df[feature].astype(float)
    df[feature + '_norm'] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())

df['tempo_norm'] = (df['tempo'] - df['tempo'].min()) / (df['tempo'].max() - df['tempo'].min())
# Asignamos colores basados en las características
def assign_color(row):
    # Usamos las características normalizadas para definir Hue, Saturation, Lightness
    hue = row.iloc[0]['tempo_norm']  # Relacionamos el tempo con el matiz
    st.write("Matiz: ", hue)
    saturation = row.iloc[0]['rolloff_norm']  # Relacionamos el rolloff con la saturación
    st.write("Saturación: ", saturation)
    lightness = 1 - row.iloc[0]['zero_crossing_rate_norm']  # Relacionamos el zero crossing con la luminosidad
    st.write("Brillo ", lightness)
    # Convertimos HSL a RGB
    rgb = hsv_to_rgb([hue, saturation, lightness])
    # Convertimos a formato hexadecimal para usar en visualizaciones
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

fila_elegida = df[df.titulo == titulo_elegido]

color_elegido = assign_color(fila_elegida)
color = st.color_picker("Tenemos tu color", color_elegido)
st.write(color_elegido)


# Fondo de la app (si es necesario)
background_image_path = "foto.png"

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background(background_image_path)

import streamlit as st
from PIL import Image, ImageEnhance
import io

# Título
st.title("Transforma una imagen según parámetros de la canción")

# Parámetros constantes de transformación
hue = 0.5  # Hue fijo (puedes cambiarlo según necesites)
saturation = 1.5  # Saturación fija
lightness = 1.2  # Luminosidad fija

# Subir imagen
uploaded_image = st.file_uploader("Sube una imagen para transformarla", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Cargar imagen
    image = Image.open(uploaded_image).convert('RGB')

    # Aplicar transformaciones
    enhancer = ImageEnhance.Color(image)
    transformed_image = enhancer.enhance(saturation)  # Aplicar saturación

    # Ajuste de luminosidad
    enhancer = ImageEnhance.Brightness(transformed_image)
    transformed_image = enhancer.enhance(lightness)  # Aplicar luminosidad

    # Convertir la imagen para ajustar el tono
    hsv_image = transformed_image.convert("HSV")
    hsv_data = hsv_image.getdata()

    # Aplicar el valor de 'hue' a cada píxel (ajuste el matiz)
    new_hsv_data = []
    for pixel in hsv_data:
        h, s, v = pixel
        new_pixel = (int(hue * 255), s, v)  # Ajuste el matiz multiplicando por hue
        new_hsv_data.append(new_pixel)

    # Convertir de nuevo a imagen
    hsv_image.putdata(new_hsv_data)
    final_image = hsv_image.convert("RGB")

    # Mostrar imagen transformada
    st.image(final_image, caption="Imagen transformada", use_column_width=True)

    # Descargar imagen transformada
    buf = io.BytesIO()
    final_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Descargar imagen transformada",
        data=byte_im,
        file_name="imagen_transformada.png",
        mime="image/png",
    )
