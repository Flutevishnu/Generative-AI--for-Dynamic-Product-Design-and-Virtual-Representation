import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageOps
import numpy as np

# Streamlit UI
st.title("Image Mask Creator for Stable Diffusion")

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Open the uploaded image
    img = Image.open(uploaded_image)
    img = ImageOps.contain(img, (512, 512))  # Resize image to fit in the canvas, maintaining aspect ratio

    # Create a canvas for drawing the mask
    st.markdown("Draw on the image to create a mask:")
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 1)",  # Drawing color (black)
        stroke_width=15,                # Stroke width
        stroke_color="rgba(0, 0, 0, 1)",  # Mask color
        background_image=img,           # Use the uploaded image as the background
        update_streamlit=True,
        height=512,
        width=512,
        drawing_mode="freedraw",        # Set to 'freedraw' to allow free drawing
        key="canvas",
    )

    # If drawing is done, extract the mask
    if canvas_result.image_data is not None:
        mask = canvas_result.image_data
        # Convert the alpha channel (4th channel) to a binary mask (255 for drawn, 0 for background)
        mask_binary = (mask[:, :, 3] > 0).astype(np.uint8) * 255  # Mask is white where drawn, black elsewhere

        # Create an image from the binary mask
        mask_img = Image.fromarray(mask_binary, mode="L")  # "L" mode is for grayscale images
        st.image(mask_img, caption="Generated Mask", use_column_width=True)

        # Provide download button for the mask
        mask_img.save("mask_image.png")
        with open("mask_image.png", "rb") as file:
            st.download_button(
                label="Download Mask",
                data=file,
                file_name="mask_image.png",
                mime="image/png",
            )
