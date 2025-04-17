
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

# Setup
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")
st.title("📊 Dashboard Analisis & Prediksi Penjualan")

# Upload data
uploaded_file = st.file_uploader("📤 Upload file penjualan (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Tanggal'])
    df = df.sort_values('Tanggal')

    st.subheader("📌 Ringkasan Penjualan")
    total = df['Total'].sum()
    daily_avg = df.groupby('Tanggal')['Total'].sum().mean()
    col1, col2 = st.columns(2)
    col1.metric("Total Penjualan", f"Rp {total:,.0f}")
    col2.metric("Rata-rata Harian", f"Rp {daily_avg:,.0f}")

    st.subheader("📆 Penjualan Harian")
    daily_sales = df.groupby('Tanggal')['Total'].sum()
    st.line_chart(daily_sales)

    st.subheader("📦 Penjualan per Kategori")
    df_grouped = df.groupby("Kategori")["Total"].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=df_grouped, x="Kategori", y="Total", ax=ax, color='skyblue')

    # Format sumbu-y agar tidak dalam notasi ilmiah
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    ax.set_xlabel("Kategori")
    ax.set_ylabel("Total Penjualan")
    ax.set_title("Total Penjualan per Kategori")

    st.pyplot(fig)
  
    # col1, _ = st.columns([1, 1])  # Grafik setengah layar

    # with col1:
    #     st.subheader("📦 Penjualan per Kategori")

    #     df_grouped = df.groupby("Kategori")["Total"].sum().reset_index()

    #     fig, ax = plt.subplots(figsize=(4, 3))
    #     sns.barplot(data=df_grouped, x="Kategori", y="Total", ax=ax, color='skyblue')

    #     ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    #     ax.set_xlabel("Kategori", fontsize=8)
    #     ax.set_ylabel("Total Penjualan", fontsize=8)
    #     ax.set_title("Total per Kategori", fontsize=10)

    #     st.pyplot(fig)


    st.subheader("📉 Dekomposisi Tren & Musiman")
    period = st.slider("Pilih Periode Musiman", min_value=2, max_value=14, value=7)
    decomposed = seasonal_decompose(daily_sales, model='additive', period=period)
    fig_dec, axes = plt.subplots(4, 1, figsize=(10, 6), sharex=True)
    decomposed.observed.plot(ax=axes[0], title='Observed')
    decomposed.trend.plot(ax=axes[1], title='Trend')
    decomposed.seasonal.plot(ax=axes[2], title='Seasonal')
    decomposed.resid.plot(ax=axes[3], title='Residual')
    plt.tight_layout()
    st.pyplot(fig_dec)

    st.subheader("📈 Prediksi Penjualan (7 Hari ke Depan)")
    model_opt = st.selectbox("Pilih Model Prediksi", ["Simple Exponential Smoothing", "Holt-Winters"])
    forecast_horizon = 7

    if model_opt == "Simple Exponential Smoothing":
        ses_model = SimpleExpSmoothing(daily_sales, initialization_method="estimated").fit()
        forecast = ses_model.forecast(forecast_horizon)
    else:
        hw_model = ExponentialSmoothing(daily_sales, trend='add', seasonal='add',
                                         seasonal_periods=period, initialization_method="estimated").fit()
        forecast = hw_model.forecast(forecast_horizon)

    combined = pd.concat([daily_sales, forecast])
    fig_forecast, ax_forecast = plt.subplots()
    daily_sales.plot(ax=ax_forecast, label="Aktual")
    forecast.plot(ax=ax_forecast, label="Forecast", linestyle="--")
    ax_forecast.legend()
    st.pyplot(fig_forecast)

    st.download_button("📥 Download Forecast CSV", forecast.to_csv().encode(), file_name="forecast.csv", mime="text/csv")

else:
    st.info("Silakan upload file CSV dengan kolom: tanggal, produk, kategori, total")
