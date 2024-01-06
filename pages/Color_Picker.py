import streamlit as st
import numpy as np
import pandas as pd
from skimage.color import rgb2lab, deltaE_cie76

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_lab(rgb_color):
    return rgb2lab(np.array([[rgb_color]]) / 255.0)[0, 0]

def calculate_color_difference(color1_lab, color2_lab):
    return deltaE_cie76(color1_lab, color2_lab)

def find_closest_points(color_lab, reference_points):
    distances = [(calculate_color_difference(color_lab, rgb_to_lab(hex_to_rgb(ref_color))), ref_value) for ref_color, ref_value in reference_points]
    distances.sort(key=lambda x: x[0])
    return distances[0], distances[1]

def interpolate_value(color_lab, reference_points):
    (dist1, val1), (dist2, val2) = find_closest_points(color_lab, reference_points)
    if dist1 < 1e-5:  # Very close to a reference point
        return val1
    elif dist1 == dist2:  # Avoid division by zero
        return (val1 + val2) / 2
    else:
        ratio = dist1 / (dist1 + dist2)
        return val1 * (1 - ratio) + val2 * ratio

def load_reference_points_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    return list(df.to_records(index=False))

# Streamlit interface setup
st.set_page_config(layout="wide")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("Ước Lượng Giá Trị Màu sắc Trên Bản Đồ Choropleth")

url = 'https://devpicker.com/image-color-picker'

st.subheader("Xác định mã màu tại đây")
with st.expander("Xác định màu"):
    st.write(url)
    st.components.v1.iframe(url, width=1300, height=1000)

csv_file_path = 'RefColor.csv'  # Update with the correct path
reference_points_from_csv = load_reference_points_from_csv(csv_file_path)

st.subheader("Thiết lập điểm tham chiếu")
with st.expander("Các điểm tham chiếu"):
    num_references = len(reference_points_from_csv)
    reference_points = []
    for i in range(num_references):
        col1, col2 = st.columns(2)
        with col1:
            ref_color = st.color_picker(f"Màu tham chiếu {i+1}", reference_points_from_csv[i][0])
        with col2:
            ref_value = st.number_input(f"Giá trị tham chiếu {i+1}", value=reference_points_from_csv[i][1])
        reference_points.append((ref_color, ref_value))

point_color = st.color_picker("Nhập giá trị màu sắc tại đây!", '#baf6f6')

if st.button('Ước lượng giá trị'):
    try:
        point_rgb = hex_to_rgb(point_color)
        point_lab = rgb_to_lab(point_rgb)
        value = interpolate_value(point_lab, reference_points)
        st.success(f"Giá trị ước lượng cho màu {point_color} là: {value:.2f}")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")
