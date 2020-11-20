import math
import re
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, UnidentifiedImageError

from constants import BACKEND_URL, URL_PATTERN


def get_recommendations(query_file):
    r = requests.post(
        BACKEND_URL + "/recommendations/",
        files={"file": query_file},
    )
    query = r.json()
    for result in query:
        img_r = requests.get(result["image_url"])
        img = Image.open(BytesIO(img_r.content))
        result["image"] = img
    return query


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

    query = get_recommendations(query_file)

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
                # if st.button("asd", key=result["url"]):
                st.write(
                    f"<form action='{result['url']}'>"
                    "     <input type='submit' value='Buy it!' />"
                    " </form>",
                    unsafe_allow_html=True,
                )
