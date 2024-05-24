# BizCardX-Extracting Business Card Data by using easyOCR (Optical Character Recognition)

<p align="center">
  <img src="https://github.com/gopinathvenkatesan01/BizCardDataExtraction/assets/162252390/7f89dceb-fa2f-49ad-a25a-1d71441abed0" alt="Project WorkFlow" width="690" height="390">
 </p>

## Introduction

* In today's fast-paced business environment, efficiently managing and organizing contact information is crucial for successful networking and communication. With the advent of digital tools and technologies, manual entry of business card details into a database can be time-consuming and prone to errors. To overcome these challenges, developers can leverage the power of optical character recognition (OCR) and databases to automate the process of extracting relevant information from business cards and storing it for easy access.

* One powerful OCR library that facilitates the extraction of text from images is EasyOCR. EasyOCR is an open-source Python library that utilizes deep learning models to accurately recognize and extract text from various languages. By integrating EasyOCR with a MySQL database, developers can streamline the process of capturing business card data and storing it in a structured and organized manner.

## Developer Guide

### 1. Tools Install

* Python 3.11.0 or higher.
* PostgresSQL.

### 2. Requirement Libraries to Install

* pip install pandas easyocr numpy Pillow opencv-python-headless os re sqlalchemy psycopg2 streamlit 

### 3.Import Libraries

#### Scanning library

* import easyocr # (Optical Character Recognition)
* import numpy as np
* from PIL
* from PIL import Image, ImageDraw
* import cv2
* import os
* import re

#### Data frame libraries

* import pandas as pd

#### Database Library

* import sqlalchemy
* import psycopg2
* from sqlalchemy import (
    create_engine,
    Table,
    Column,
    MetaData,
    select,
    String,
    Text,
    update,
    delete,
    )from sqlalchemy import create_engine, inspect

#### Dashboard library

* import streamlit as st

### 4. E T L Process

#### a) Extract data

* Extract relevant information from business cards by using the easyOCR library

#### b) Process and Transform the data

* After the extraction process, process the extracted data based on Company name, Card Holder, Designation, Mobile Number, Email, Website, Area, City, State, and Pincode is converted into a data frame.

#### c) Load data

* After the transformation process, the data is stored in the MySQL database.

## User Guide

#### Step 1. Data collection zone
* Click the **'Browse Files'** button and select an image

#### Step 2. Data upload
* Click the **'Upload Data'** button to upload the data to the Mysql database

#### Step 3. Modification zone
* In this **'Data Modification'** you can able to modify the information also you can delete the previous data

## Video link

**Contributing**

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request.

**License**

This project is licensed under the MIT License. Please review the LICENSE file for more details.

**Contact**

📧 Email: gopinathvenakatesan01@gmail.com

🌐 LinkedIn: [linkedin.com/in/gopinath-venkatesan-9707022a7](https://www.linkedin.com/in/gopinath-venkatesan-9707022a7/)

