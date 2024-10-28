import streamlit as st
import base64
import utils.Generate_text_to_img as Generate_text_to_img
import io

Product = st.selectbox(
        "Select the Product to design",
        ("Shoe", "Tshirt","fullHand-Tshirt","Oversized-Tshirt","shirt", "Other")        
    )
    
if Product == "Other":
    uploaded_image = st.file_uploader("Choose a image")

    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        st.image(io.BytesIO(bytes_data))     
else:
    uploaded_image = None
    base64_image = ""
if "prompt_input" not in st.session_state:
    st.session_state["prompt_input"] = ""
st.write(Product)

if "Product" in st.session_state:
    st.write(Product)
prompt_input = st.text_input("Input a text here", st.session_state["prompt_input"])
submit = st.button("Generate")

if submit:
    if (uploaded_image is None and Product != "Other") or (uploaded_image is not None and Product == "Other"):
        st.session_state["prompt_input"] = prompt_input
        st.write("You have entered: ", prompt_input)
        ImgGen = Generate_text_to_img.ImageGen()
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
        st.error("Upload the image for style")