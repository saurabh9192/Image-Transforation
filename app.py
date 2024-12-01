import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Function to perform translation
def translate_image(img, tx, ty):
    rows, cols, _ = img.shape
    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(img, translation_matrix, (cols, rows))

# Function to perform rotation
def rotate_image(img, angle, center=None, scale=1.0):
    rows, cols, _ = img.shape
    if center is None:
        center = (cols // 2, rows // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(img, rotation_matrix, (cols, rows))

# Function to perform scaling
def scale_image(img, fx, fy):
    return cv2.resize(img, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

# Function to perform shearing
def shear_image(img, shear_factor_x, shear_factor_y):
    rows, cols, _ = img.shape
    shear_matrix = np.float32([[1, shear_factor_x, 0], [shear_factor_y, 1, 0]])
    return cv2.warpAffine(img, shear_matrix, (cols + int(shear_factor_x * rows), rows + int(shear_factor_y * cols)))

# Streamlit App
st.title("Image Transformation App")
st.write("Upload an image and choose a transformation to apply.")

# Upload Image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_array = np.array(img)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Choose Transformation
    st.sidebar.title("Transformation Options")
    transformation = st.sidebar.radio(
        "Choose a Transformation:",
        ("Translated Image", "Rotated Image", "Scaled Image", "Sheared Image")
    )

    transformed_img = None

    # Apply Transformation Based on User Input
    if transformation == "Translated Image":
        tx = st.sidebar.slider("Translate X (pixels):", -200, 200, 50)
        ty = st.sidebar.slider("Translate Y (pixels):", -200, 200, 50)
        transformed_img = translate_image(img_array, tx, ty)

    elif transformation == "Rotated Image":
        angle = st.sidebar.slider("Rotation Angle (degrees):", -180, 180, 45)
        scale = st.sidebar.slider("Scale:", 0.1, 3.0, 1.0)
        transformed_img = rotate_image(img_array, angle, scale=scale)

    elif transformation == "Scaled Image":
        fx = st.sidebar.slider("Scale Factor X:", 0.1, 3.0, 1.5)
        fy = st.sidebar.slider("Scale Factor Y:", 0.1, 3.0, 1.5)
        transformed_img = scale_image(img_array, fx, fy)

    elif transformation == "Sheared Image":
        shear_factor_x = st.sidebar.slider("Shear Factor X:", -1.0, 1.0, 0.2)
        shear_factor_y = st.sidebar.slider("Shear Factor Y:", -1.0, 1.0, 0.2)
        transformed_img = shear_image(img_array, shear_factor_x, shear_factor_y)

    # Display Transformed Image
    if transformed_img is not None:
        st.image(transformed_img, caption="Transformed Image", use_column_width=True)

        # Download Button
        st.sidebar.title("Download Transformed Image")
        is_download = st.sidebar.button("Download Image")
        if is_download:
            img_download = Image.fromarray(transformed_img)
            buf = io.BytesIO()
            img_download.save(buf, format="JPEG")
            byte_im = buf.getvalue()
            st.sidebar.download_button(
                label="Download Transformed Image",
                data=byte_im,
                file_name="transformed_image.jpg",
                mime="image/jpeg"
            )
