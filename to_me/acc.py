import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd

st.set_page_config(page_title="ALEM - Undertone Finder", layout="centered")
st.title("ALEM: skin undertone identification")
st.write("Upload your photo and discover the best accessory color for your skin tone!")

uploaded_file = st.file_uploader("Upload photo of your wrist or your face...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    st.image(img_rgb, caption='Uploaded photo', use_column_width=True)
    
    if st.button('undertone identification'):
        with st.spinner('...'):
            h, w, _ = img.shape
            cx, cy = w // 2, h // 2
            sample = img[cy-50:cy+50, cx-50:cx+50]
            
            avg_color_per_row = np.average(sample, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            b, g, r = avg_color
            
        
            
            if r > b + 10:
                result = "Warm"
                advice = "Gold, yellow, and warm colors look beautiful on you."
                color_hex = "#FFD700"
            elif b > r + 2:
                result = "Cool"
                advice = "Silver, white gold, and cool colors (blue, violet) are recommended for you."
                color_hex = "#C0C0C0"
            else:
                result = "Neutral"
                advice = "You can wear any color with confidence—gold and silver both look great on you!"
                color_hex = "#E5AA70"

            
            st.success(f"your undertone is፡ {result} !")
            st.info(f"Advice፡ {advice}")
            
            chart_data = pd.DataFrame({
                'Color Channels': ['Red (ቀይ)', 'Green (አረንጓዴ)', 'Blue (ሰማያዊ)'],
                'Intensity': [r, g, b]
            })
            st.bar_chart(chart_data.set_index('Color Channels'))
            
            st.write("Recommended color samples for your skin:")

            st.markdown(f'<div style="background-color:{color_hex}; width:100%; height:50px; border-radius:10px;"></div>', unsafe_allow_case=True)

else:
    st.info("To get started please upload your photo in the box above")

st.markdown("---")
st.caption("ALEM - በኢትዮጵያዊት ስታይሊስት 👩🏾‍💻")