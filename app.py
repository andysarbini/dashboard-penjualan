
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

# Setup
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")
st.title("📊 Dashboard Analisis_5 & Prediksi Penjualan")

# Upload data
uploaded_file = st.file_uploader("📤 Upload file penjualan (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Tanggal'])
    df = df.sort_values('Tanggal')

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📦 Penjualan per Kategori", "📅 Tren Harian", "📁 Data Mentah"])

    # ========================
    # Tab 1: Penjualan per Kategori
    # ========================
    with tab1:
        col1, _ = st.columns([1, 1])  # Grafik setengah layar

        with col1:
            st.subheader("📦 Penjualan per Kategori")

            df_grouped = df.groupby("Kategori")["Total"].sum().reset_index()

            fig, ax = plt.subplots(figsize=(4, 3))
            sns.barplot(data=df_grouped, x="Kategori", y="Total", ax=ax, color='skyblue')

            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
            ax.set_xlabel("Kategori", fontsize=8)
            ax.set_ylabel("Total Penjualan", fontsize=8)
            ax.set_title("Total per Kategori", fontsize=10)

            st.pyplot(fig)

    # ========================
    # Tab 2: Tren Penjualan Harian
    # ========================
    with tab2:
        col1, _ = st.columns([1, 1])  # Grafik setengah layar

        with col1:
            st.subheader("📅 Tren Penjualan Harian")

            df_daily = df.groupby("Tanggal")["Total"].sum().reset_index()

            fig2, ax2 = plt.subplots(figsize=(4, 3))
            ax2.plot(df_daily["Tanggal"], df_daily["Total"], marker='o', linestyle='-')

            ax2.set_xlabel("Tanggal", fontsize=8)
            ax2.set_ylabel("Total Penjualan", fontsize=8)
            ax2.set_title("Tren Harian", fontsize=10)
            ax2.tick_params(axis='x', rotation=45)
            ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

            st.pyplot(fig2)

    # ========================
    # Tab 3: Data Mentah
    # ========================
    with tab3:
        st.subheader("📁 Data Penjualan Mentah")
        st.dataframe(df)
else:
    st.info("Silakan upload file CSV dengan kolom: tanggal, produk, kategori, total")
