import math
import re
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, UnidentifiedImageError

from constants import URL_PATTERN

st.write("# Find the perfect art piece! :art:")
# Data Input
st.write("## Choose your image")
link = st.text_input("Enter URL:")
st.write(
    "### <div align='center'>:point_up: or :point_down:</div>", unsafe_allow_html=True
)
file = st.file_uploader("Upload image file:")

# Process Input
query_image = None

if link and re.match(URL_PATTERN, link) is None:
    st.warning("Invalid URL, please provide a new one!")
    st.stop()
elif link:
    try:
        r = requests.get(link)
        query_image = Image.open(BytesIO(r.content))
    except:
        st.warning("Error downloading the image!")
        st.stop()

if file:
    try:
        query_image = Image.open(file)
    except UnidentifiedImageError:
        st.warning("Unable to open image!")
        st.stop()

# Get Results
if query_image:
    with st.beta_expander("See chosen image"):
        st.image(query_image, use_column_width=True)
    query = [
        {
            "title": "YOU ARE HERE!",
            "price": 550.00,
            "image_url": "https://d3rf6j5nx5r04a.cloudfront.net/unpdgdMhfwBFhXVnZZliirrvQZs=/1120x1434/product/6/d/6661b64d0871455ead041a6dd36b2dc9_opt.jpg",
            "url": "https://www.artfinder.com/art/sort-best_match/paginate-60/product_category-painting/#/quick-view/you-are-here-4c065",
            "style": "Acrylic painting",
            "palette_embedding": [1, 2, 3, 4, 5, 1, 23, 12, 31, 31, 23],
        },
        {
            "title": "AUTUMN BIRCHES",
            "price": 300.00,
            "image_url": "https://d3rf6j5nx5r04a.cloudfront.net/xIufPNcQ7xf7BgE0DsQe5Z3_PSc=/1120x1296/product/1/2/a8c65e49eb184d1a94c3a81d025c6aff_opt.jpg",
            "url": "https://www.artfinder.com/art/sort-best_match/paginate-60/product_category-painting/#/quick-view/autumn-birches-e34fe",
            "style": "Oil painting",
            "palette_embedding": [1, 2, 3, 4, 5, 1, 23, 12, 31, 31, 23],
        },
        {
            "title": "Garden in spring - modern floral",
            "price": 1094.00,
            "image_url": "https://d3rf6j5nx5r04a.cloudfront.net/M4Bs2uNgD8v9FMx4jEN1IvMirBc=/1120x1590/product/d/1/78c4e791e2ad4747899785291647309b_opt.jpg",
            "url": "https://www.artfinder.com/art/sort-best_match/paginate-60/product_category-painting/#/quick-view/garden-in-spring-modern-floral",
            "style": "Acrylic painting",
            "palette_embedding": [1, 2, 3, 4, 5, 1, 23, 12, 31, 31, 23],
        },
    ]
    st.write("# Here is what we found! :tada:")
    num_cols = 2
    for i in range(math.ceil(len(query) / num_cols)):
        cols = st.beta_columns(num_cols)
        for result, col in zip(query[i * num_cols :], cols):
            with col:
                st.write(f"### [{result['title']}]({result['url']})")
                try:
                    img_r = requests.get(result["image_url"])
                    img = Image.open(BytesIO(img_r.content))
                    st.image(img, use_column_width=True)
                except:
                    st.write("Image not found :sad:")
                st.write(f"#### U$S {result['price']} - {result['style']}")
