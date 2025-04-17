
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

# Setup
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")
st.title("📊 Dashboard Analisis & Prediksi Penjualan")

# Upload data
uploaded_file = st.file_uploader("📤 Upload file penjualan (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['tanggal'])
    df = df.sort_values('tanggal')

    st.subheader("📌 Ringkasan Penjualan")
    total = df['total'].sum()
    daily_avg = df.groupby('tanggal')['total'].sum().mean()
    col1, col2 = st.columns(2)
    col1.metric("Total Penjualan", f"Rp {total:,.0f}")
    col2.metric("Rata-rata Harian", f"Rp {daily_avg:,.0f}")

    st.subheader("📆 Penjualan Harian")
    daily_sales = df.groupby('tanggal')['total'].sum()
    st.line_chart(daily_sales)

    st.subheader("📦 Penjualan per Kategori")
    fig_kat, ax_kat = plt.subplots()
    df.groupby('kategori')['total'].sum().plot(kind='bar', ax=ax_kat, color='skyblue')
    ax_kat.set_ylabel("Total Penjualan")
    st.pyplot(fig_kat)

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
