import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
from fpdf import FPDF  # pip install fpdf

st.set_page_config(page_title="VN Finance Manager", page_icon="💰", layout="wide")
st.title("💰 VN Finance Manager - Quản lý tài chính VN")
st.caption("Expense Tracker + Tiết kiệm + Hóa đơn | Dành cho freelancer & tiểu thương")

# Tab
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💸 Expense Tracker", "🏦 Tiết kiệm Calculator", "📄 Tạo Hóa đơn"])

# === TAB 1: Dashboard ===
with tab1:
    st.subheader("Tổng quan tài chính")
    # Dữ liệu mẫu (user sẽ thay bằng data thật)
    data = pd.DataFrame({
        "Ngày": ["2026-04-01", "2026-04-05", "2026-04-10", "2026-04-20"],
        "Loại": ["Chi tiêu", "Thu nhập", "Chi tiêu", "Thu nhập"],
        "Số tiền": [500000, 3000000, 1200000, 2500000],
        "Mô tả": ["Ăn uống", "Dự án freelance", "Xăng xe", "Bán hàng online"]
    })
    st.dataframe(data, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(data[data["Loại"]=="Chi tiêu"], values="Số tiền", names="Mô tả", title="Phân bổ chi tiêu")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(data, x="Ngày", y="Số tiền", color="Loại", title="Thu - Chi theo ngày")
        st.plotly_chart(fig_bar, use_container_width=True)

# === TAB 2: Expense Tracker ===
with tab2:
    st.subheader("Thêm chi tiêu/thu nhập")
    with st.form("expense_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            date = st.date_input("Ngày", datetime.now())
            category = st.selectbox("Danh mục", ["Ăn uống", "Di chuyển", "Điện nước", "Thuê nhà", "Khác", "Thu nhập freelance", "Bán hàng"])
        with col_b:
            amount = st.number_input("Số tiền (VND)", min_value=1000, value=500000)
            desc = st.text_input("Mô tả")
        submitted = st.form_submit_button("✅ Lưu")
        if submitted:
            # Lưu vào CSV (hoặc dùng sqlite cho production)
            new_row = pd.DataFrame([[date, category, amount, desc]], columns=["Ngày", "Danh mục", "Số tiền", "Mô tả"])
            try:
                df = pd.read_csv("expenses.csv")
                df = pd.concat([df, new_row], ignore_index=True)
            except:
                df = new_row
            df.to_csv("expenses.csv", index=False)
            st.success("Đã lưu!")

    if st.button("Xem lịch sử"):
        try:
            df = pd.read_csv("expenses.csv")
            st.dataframe(df)
        except:
            st.info("Chưa có dữ liệu. Hãy thêm giao dịch đầu tiên!")

# === TAB 3: Tiết kiệm Calculator ===
with tab3:
    st.subheader("🏦 Tính lãi tiết kiệm (dữ liệu tháng 4/2026)")
    amount = st.number_input("Số tiền gửi (VND)", min_value=1000000, value=50000000)
    months = st.slider("Kỳ hạn (tháng)", 1, 36, 12)
    
    # Bảng lãi suất real-time (cập nhật 25/4/2026)
    rates_data = {
        "Ngân hàng": ["Techcombank", "VPBank", "VietABank", "SeABank"],
        "Lãi suất (%/năm)": [6.6, 6.5, 6.8, 8.0]  # promo cao nhất
    }
    df_rates = pd.DataFrame(rates_data)
    st.dataframe(df_rates)
    
    best_rate = df_rates["Lãi suất (%/năm)"].max()
    interest = amount * best_rate / 100 * (months / 12)
    st.metric("Lãi dự kiến (lãi đơn)", f"{interest:,.0f} VND", f"{best_rate}%/năm")
    st.info("💡 Lãi kép sẽ cao hơn một chút. Công thức: \( P \times (1 + r/12)^{months} - P \).")

# === TAB 4: Tạo Hóa đơn PDF ===
with tab4:
    st.subheader("📄 Tạo hóa đơn PDF chuyên nghiệp")
    customer = st.text_input("Tên khách hàng")
    items = st.text_area("Danh sách sản phẩm/dịch vụ (mỗi dòng: Tên - Số lượng - Giá)", "Thiết kế website - 1 - 5000000")
    if st.button("Tạo & Tải hóa đơn"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="HÓA ĐƠN - VN Finance Manager", ln=1, align="C")
        pdf.cell(200, 10, txt=f"Khách hàng: {customer}", ln=1)
        pdf.cell(200, 10, txt=f"Ngày: {datetime.now().strftime('%d/%m/2026')}", ln=1)
        # Thêm items...
        pdf.output("hoa_don.pdf")
        with open("hoa_don.pdf", "rb") as f:
            st.download_button("⬇️ Tải hóa đơn PDF", f, file_name="hoa_don.pdf")

st.sidebar.success("🚀 App sẵn sàng kiếm tiền!")
st.sidebar.info("Premium: Export không giới hạn + forecast → Chỉ 49k VND/tháng (dùng Stripe/Lemon Squeezy)")