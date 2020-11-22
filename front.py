import math
import re
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, UnidentifiedImageError

from api import elastic_client, query_object
from constants import INDEX_NAME, URL_PATTERN
from palette_generator import embedding_from_palette, palette_from_image


@st.cache
def get_images(response):
    for result in response:
        img_r = requests.get(result["image_url"])
        img = Image.open(BytesIO(img_r.content))
        result["image"] = img
    return response


def get_recommendations(file, gte, lte):
    palette = palette_from_image(file)
    algorithm_entry = "-".join(palette)

    embedded_palette = embedding_from_palette(algorithm_entry)
    elastic_response = elastic_client.search(
        index=INDEX_NAME, body=query_object(embedded_palette, gte=gte, lte=lte)
    )["hits"]["hits"]

    final_response = []
    for response in elastic_response:
        final_response.append(response["_source"])
    final_response = get_images(final_response)
    return final_response


st.write("# Find the perfect art piece! :art:")

# Data Input
st.write("## Choose your image")
link = st.text_input("Enter URL:")
st.write(
    "### <div align='center'>:point_up: or :point_down:</div>", unsafe_allow_html=True
)
uploaded_file = st.file_uploader("Upload image file:")

# Process Input
query_image = None

if link and re.match(URL_PATTERN, link) is None:
    st.warning("Invalid URL, please provide a new one!")
    st.stop()
elif link:
    try:
        img_r = requests.get(link)
        query_image = Image.open(BytesIO(img_r.content))
    except:
        st.warning("Error downloading the image!")
        st.stop()

if uploaded_file:
    try:
        query_image = Image.open(uploaded_file)
    except UnidentifiedImageError:
        st.warning("Unable to open image!")
        st.stop()

# Filters
st.sidebar.write("## Apply filters")
gte, lte = st.sidebar.slider(
    "Select a price range (U$S)", 0, 50000, (0, 50000), step=10
)

# Visualization options
st.sidebar.write("## Visualization options")
num_cols = st.sidebar.slider("columns", min_value=1, max_value=5, value=2, step=1)

# Get Results
if query_image:
    buffer = BytesIO()
    query_image = query_image.convert("RGB")
    query_image.save(buffer, format="JPEG")
    query_file = buffer.getvalue()

    with st.beta_expander("See chosen image"):
        st.image(query_file, use_column_width=True)

    query = get_recommendations(query_image, gte, lte)
    st.write("# Here is what we found! :tada:")
    for i in range(math.ceil(len(query) / num_cols)):
        cols = st.beta_columns(num_cols)
        for result, col in zip(query[i * num_cols :], cols):
            with col:
                st.write(f"### {result['title']}")
                try:
                    st.image(result["image"], use_column_width=True)
                except:
                    st.write("Image not found :sad:")
                st.write(f"#### U$S {result['price']}")
                st.write(
                    f"<form action='{result['url']}'>"
                    "     <input type='submit' value='Buy it!' />"
                    " </form>",
                    unsafe_allow_html=True,
                )
