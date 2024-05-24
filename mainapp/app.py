import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

from dataservice import get_data
from sql import getuserData, init, saveCardData, saveData
from streamlit import data_editor


def main():
    if "firstrun" not in st.session_state:
        st.session_state.firstrun = True

    st.set_page_config(
        page_title="Bizcard Data Extraction", page_icon="📄", layout="wide"
    )

    st.subheader("⏩ Bizcard **Data Extraction** | _By Gopi_ ")

    if st.session_state.firstrun:
        # st.balloons()

        init()
        st.session_state.firstrun = False
    fl = st.file_uploader(
        label="Upload here",
    )
    tab1, tab2 = st.tabs(["Data Extraction", "Data modification"])
    with tab1:
        if fl:
            if "image" in fl.type:
                img1, img2 = st.columns([1, 1])
                img = Image.open(fl)
                with img1:
                    # Display the image
                    st.image(img, caption="Original Image")

                # Initialize the OCR reader
                reader = easyocr.Reader(["en"], gpu=False)

                # Perform OCR on the image
                text_read = reader.readtext(np.array(img))

                result = []
                for text in text_read:
                    result.append(text[1])

                result_image = draw_text(img, text_read)
                with img2:
                    st.image(result_image, caption="Processed Image")
                data = get_data(result)
                # Create dataframe
                data_df = pd.DataFrame(data)

                # Show dataframe
                saveCardData(data_df)

            else:
                st.warning("Please Provide a Valid Image!")
    with tab2:
        userDetailsdata = getuserData()
        userDetailsdata.index = userDetailsdata.index + 1
        uuid_mapping = userDetailsdata[["bizcardky"]].copy()
        display_data = userDetailsdata.drop(columns=["bizcardky"])
        edited_data = st.data_editor(display_data, key="my_key")
        if st.button("Save Data"):
            saveData(edited_data, uuid_mapping)


def draw_image(image):
    st.toast("calling draw image")
    plt.rcParams["figure.figsize"] = (15, 15)
    plt.imshow(image)
    plt.axis("off")  # Turn off axis
    return plt



def draw_text(image_with_boxes, text_read):
    image_with_text = np.array(image_with_boxes)
    color = (0, 255, 0)  # Green color for both text and bounding boxes
    width = 2  # Width of the bounding box lines
    text_colour = color  
    spacer = 100  

    for bound, text, prob in text_read:
        p0, p1, p2, p3 = bound

        p0 = (round(p0[0]), round(p0[1]))
        p1 = (round(p1[0]), round(p1[1]))
        p2 = (round(p2[0]), round(p2[1]))
        p3 = (round(p3[0]), round(p3[1]))

        cv2.line(image_with_text, tuple(p0), tuple(p1), color, width)
        cv2.line(image_with_text, tuple(p1), tuple(p2), color, width)
        cv2.line(image_with_text, tuple(p2), tuple(p3), color, width)
        cv2.line(image_with_text, tuple(p3), tuple(p0), color, width)

        # position (top-left corner of the bounding box)
        text_position = (p0[0], p2[1] - 1)

        #  image with the specified green color
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
