import streamlit as st
import base64
import io
import utils.Generate_img_to_img as Generate_img_to_img
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
from io import StringIO

Product = st.selectbox(
        "Select the Product to design",
        ("Shoe", "Tshirt","fullHand-Tshirt","Oversized-Tshirt","shirt", "Other")        
    )
st.title(Product)

uploaded_image = st.file_uploader("Upload image")

if uploaded_image is not None  :
    bytes_image = uploaded_image.getvalue()
    st.image(bytes_image)
    print(type(bytes_image))
    base64_image = base64.b64encode(bytes_image).decode('utf-8') 
 
        
if "prompt_input" not in st.session_state:
    st.session_state["prompt_input"] = ""

prompt_input = st.text_input("Input a text here", st.session_state["prompt_input"])
submit = st.button("Generate")

if submit:
    if uploaded_image is not None:
        st.session_state["prompt_input"] = prompt_input
        st.write("You have entered: ", prompt_input) 
        ImgGen = Generate_img_to_img.ImageGen()
        images = ImgGen.Generate(prompt_input, Product, base64_image)
        for nodeid in  images:
            for image_data in images[nodeid]:
                st.image(io.BytesIO(image_data))
                img_down = st.download_button(
                                        label = "Download Image",
                                        data = io.BytesIO(image_data),
                                        file_name = prompt_input+".png",
                                        mime = "image/png"
                                    )
        st.snow()
    else:
        st.error("Upload the image and mask")