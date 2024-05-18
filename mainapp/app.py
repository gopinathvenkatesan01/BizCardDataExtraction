import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np


def main():
    st.set_page_config(
        page_title="Bizcard Data Extraction", page_icon="📄", layout="wide"
    )

    st.subheader("⏩ Bizcard **Data Extraction** | _By Gopi_ ")

    fl = st.file_uploader(
        label="Upload here",
    )
    if fl:
        st.write(fl)
        if "image" in fl.type:
            img = Image.open(fl)
            # Display the image
            st.image(img, caption=fl.name)

            # Initialize the OCR reader
            reader = easyocr.Reader(["en"], gpu=False)

            # Perform OCR on the image
            text_read = reader.readtext(np.array(img))
            
            st.code(text_read)
            result = []
            for text in text_read:
                result.append(text[1])

            result_image = draw_text(img, text_read)

            st.image(result_image, caption="Captured text")

        else:
            st.warning("Please Provide a Valid Image!")


def draw_image(image):
    st.toast("calling draw image")
    plt.rcParams["figure.figsize"] = (15, 15)
    plt.imshow(image)
    plt.axis("off")  # Turn off axis
    return plt



def draw_text(image_with_boxes, text_read, color=(0, 255, 0), width=2):
    image_with_text = np.array(image_with_boxes)
    spacer = 100 
    text_colour =(97, 106, 107)
    for bound, text, prob in text_read:
        
        p0, p1, p2, p3 = bound
        
        p0 = (round(p0[0]), round(p0[1]))
        p1 = (round(p1[0]), round(p1[1]))
        p2 = (round(p2[0]), round(p2[1]))
        p3 = (round(p3[0]), round(p3[1]))

        
        # Draw bounding box
        cv2.line(image_with_text, tuple(p0), tuple(p1), color, width)
        cv2.line(image_with_text, tuple(p1), tuple(p2), color, width)
        cv2.line(image_with_text, tuple(p2), tuple(p3), color, width)
        cv2.line(image_with_text, tuple(p3), tuple(p0), color, width)

        # Calculate text position (top-left corner of the bounding box)
        text_position = (p0[0], p2[1] - 1)  # Adjust the offset as needed

        # Put text on the image
        cv2.putText(
            image_with_text,
            text,
            text_position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            text_colour,
            2,
        )
        spacer += 15
    return image_with_text


if __name__ == "__main__":
    main()
