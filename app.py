import streamlit as st 
import Generate
import io
st.title("Generative AI  for Dynamic Product Design and Virtual Representation")

st.sidebar.success("Select a page above")

if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Generate")

if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)

ImgGen = Generate.ImageGen()
images = ImgGen.Genarate("shoe")
for nodeid in  images:
    for image_data in images[nodeid]:
        st.image(io.BytesIO(image_data))
