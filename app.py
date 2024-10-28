import streamlit as st 
import utils.Generate_text_to_img as Generate_text_to_img
import io
import base64


page_1 = st.Page("page/Home.py", title="Home", default=True)
page_2 = st.Page("page/text_to_design.py", title="Text-To-Image")
page_3 = st.Page("page/inpaint.py", title="Inpaint")
page_4 = st.Page("page/sketch_to_design.py", title="Sketch-To-Design")
pg = st.navigation({"Options": [page_1, page_2, page_3, page_4]})
pg.run()