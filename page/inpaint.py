import streamlit as st
import base64
import io
import utils.Generate_inpaint as Generate_inpaint
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np

Product = st.selectbox(
        "Select the Product to design",
        ("Shoe", "Tshirt","fullHand-Tshirt","Oversized-Tshirt","shirt", "Other")        
    )
st.title(Product)

uploaded_image = st.file_uploader("Upload image")
uploaded_mask = st.file_uploader("Upload Mask image")
if uploaded_image is not None and uploaded_mask is not None:
    bytes_image, bytes_mask = uploaded_image.getvalue(), uploaded_mask.getvalue()
    base64_image = base64.b64encode(bytes_image).decode('utf-8')
    base64_mask = base64.b64encode(bytes_mask).decode('utf-8')
        
if "prompt_input" not in st.session_state:
    st.session_state["prompt_input"] = ""

prompt_input = st.text_input("Input a text here", st.session_state["prompt_input"])
submit = st.button("Generate")

if submit:
    if uploaded_image is not None and uploaded_mask is not None:
        st.session_state["prompt_input"] = prompt_input
        st.write("You have entered: ", prompt_input)
        ImgGen = Generate_inpaint.ImageGen()
        images = ImgGen.Generate(prompt_input, Product, base64_image, base64_mask)
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