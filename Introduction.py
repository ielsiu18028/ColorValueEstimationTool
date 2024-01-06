import streamlit as st



# Streamlit interface setup
st.set_page_config(layout="wide")

documentation_text = """
# Tài Liệu: Công Cụ Ước Lượng Giá Trị Màu Sắc

## Tổng Quan
Ứng dụng Streamlit này được thiết kế để ước lượng giá trị dựa trên màu sắc đầu vào, chủ yếu dùng cho bản đồ choropleth. Công cụ này tính toán giá trị gần nhất tương ứng với màu do người dùng chọn bằng cách so sánh với các màu tham chiếu được định nghĩa trước và giá trị liên quan của chúng.

## Phương Pháp Tiếp Cận Kỹ Thuật

### 1. Chuyển Đổi Không Gian Màu (RGB sang CIELAB)
Để đạt được sự so sánh màu sắc dựa trên cảm nhận chính xác hơn, ứng dụng chuyển đổi màu sắc từ không gian màu RGB sang không gian màu CIELAB. CIELAB được thiết kế để gần với thị giác của con người và phù hợp hơn với cách mọi người cảm nhận sự khác biệt về màu sắc so với RGB.

- **Chuyển Đổi RGB sang CIELAB**: Công cụ chuyển đổi màu RGB (đầu vào và tham chiếu) sang màu CIELAB sử dụng hàm `rgb2lab` từ mô-đun `skimage.color`.

### 2. Tính Toán Sự Khác Biệt Màu Sắc
Sau khi chuyển đổi sang CIELAB, ứng dụng tính toán sự khác biệt màu sắc giữa màu đầu vào và mỗi màu tham chiếu.

- **Tính Delta E (CIE 1976)**: Sự khác biệt giữa hai màu trong không gian CIELAB được tính toán sử dụng hàm `deltaE_cie76`, thực hiện theo công thức tiêu chuẩn CIE 1976 cho sự khác biệt màu sắc.

### 3. Nội Suy Giá Trị
Sau đó, ứng dụng tìm hai màu tham chiếu gần nhất với màu đầu vào và nội suy giá trị dựa trên khoảng cách đến hai màu tham chiếu này.

- **Xác Định Điểm Gần Nhất**: Nó xác định hai màu tham chiếu gần nhất với màu đầu vào dựa trên khoảng cách màu đã tính toán.
- **Nội Suy Giá Trị**: Nếu màu đầu vào rất gần với một màu tham chiếu (khoảng cách < 1e-5), giá trị của màu tham chiếu đó sẽ được sử dụng trực tiếp. Nếu không, công cụ thực hiện nội suy tuyến tính để ước lượng giá trị, với khoảng cách đảo ngược trọng số đóng góp của mỗi giá trị tham chiếu.

## Giao Diện Người Dùng
Ứng dụng có giao diện người dùng đơn giản và trực quan:

- **Chọn Màu**: Người dùng có thể chọn màu mà họ muốn ước lượng giá trị. Điều này có thể được thực hiện bằng cách nhập mã màu hex hoặc sử dụng công cụ chọn màu.
- **Màu Tham Chiếu và Giá Trị**: Công cụ cho phép người dùng xem và điều chỉnh màu tham chiếu và giá trị liên quan của chúng. Ban đầu, chúng được tải từ một tệp CSV.
- **Ước Lượng Giá Trị**: Khi chọn màu và nhấp vào nút 'Ước Lượng Giá Trị', giá trị ước lượng cho màu được chọn sẽ được hiển thị.

## Cài Đặt và Phụ Thuộc
- **Streamlit**: Ứng dụng được xây dựng sử dụng khung Streamlit.
- **NumPy**: Sử dụng cho các phép toán số học.
- **Pandas**: Dùng để tải và xử lý dữ liệu từ tệp CSV.
- **Scikit-Image**: Cần thiết cho việc chuyển đổi không gian màu và tính toán sự khác biệt màu sắc.

"""

st.markdown(documentation_text)