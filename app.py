import streamlit as st 
import Generate
import io
st.title("Generative AI  for Dynamic Product Design and Virtual Representation")

with st.sidebar:
    Product = st.selectbox(
        "Select the Product to design",
        ("Shoe", "T-shirt", "Other")
    )

    uploaded_image = st.file_uploader("Choose a image")

    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        st.image(io.BytesIO(bytes_data))

if "prompt_input" not in st.session_state:
    st.session_state["prompt_input"] = ""

st.write(Product)

if "Product" in st.session_state:
    st.write(Product)

prompt_input = st.text_input("Input a text here", st.session_state["prompt_input"])
submit = st.button("Generate")

if submit:
    st.session_state["prompt_input"] = prompt_input
    st.write("You have entered: ", prompt_input)

    ImgGen = Generate.ImageGen()
    images = ImgGen.Genarate(prompt_input)
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