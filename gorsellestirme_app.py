import streamlit as st
import pandas as pd
import plotly.express as px
import io

# --- Sayfa Ayarları (Geniş ekran modu daha iyi grafikler sunar) ---
st.set_page_config(page_title="Parametre Görselleştirme", layout="wide")

st.title("📈 Anlık Parametre Görselleştirme Aracı")
st.write("Lütfen `topluexcel.py` ile oluşturduğunuz 'Parametre Tarihçesi' Excel dosyasını (.xlsx) yükleyin.")

# --- 1. Dosya Yükleme Arayüzü ---
uploaded_file = st.file_uploader(
    "Görselleştirmek için bir Excel dosyası yükleyin", 
    type=["xlsx"]
)

# Dosya yüklendiyse devam et
if uploaded_file is not None:
    try:
        # 2. Yüklenen Excel'i Oku
        st.success(f"'{uploaded_file.name}' dosyası başarıyla okundu. İşleniyor...")
        
        # 'Parametreler.csv' dosyasını okurken, bunun aslında bir Excel olduğunu varsayıyorum
        # (Yüklediğin dosya adı .xlsx içeriyordu)
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        st.subheader("Veri Önizlemesi (İlk 5 Satır)")
        st.dataframe(df.head()) # Verinin ilk 5 satırını göster
        
        # --- 3. Otomatik Grafikler ---
        
        # Grafiklerin X ekseni olarak kullanılacak ana sütun
        x_axis_col = "Zaman (Kümülatif)"
        
        # Gerekli sütunlar dosyada var mı diye kontrol et
        if x_axis_col not in df.columns:
            st.error(f"HATA: Dosyada '{x_axis_col}' sütunu bulunamadı! Lütfen doğru dosyayı yükleyin.")
        else:
            st.header("İstenen Parametre Grafikleri")
            
            # --- Grafik 1: Ortalama Kuvvet ---
            # (Görsel: image_a07af4.png)
            if "Ortalama Kuvvet (N)" in df.columns:
                st.subheader("Ortalama Kuvvet Grafiği")
                fig1 = px.line(
                    df, 
                    x=x_axis_col, 
                    y="Ortalama Kuvvet (N)",
                    title="Ortalama Kuvvet vs. Zaman",
                    markers=True # Her bir ölçüm noktasını göster
                )
                fig1.update_layout(xaxis_title="Geçen Toplam Süre", yaxis_title="Ortalama Kuvvet (N)")
                st.plotly_chart(fig1, use_container_width=True)
            
            # --- Grafik 2: Anlık Eğim ---
            # (Görsel: image_a07af9.png)
            if "Anlik_Eğim (O anki)" in df.columns:
                st.subheader("Anlık Eğim Grafiği")
                fig2 = px.line(
                    df, 
                    x=x_axis_col, 
                    y="Anlik_Eğim (O anki)",
                    title="Anlık Eğim vs. Zaman",
                    markers=True,
                    color_discrete_sequence=['red']
                )
                fig2.update_layout(xaxis_title="Geçen Toplam Süre", yaxis_title="Anlık Eğim")
                st.plotly_chart(fig2, use_container_width=True)

            # --- Grafik 3: Ortalama Eğim ---
            if "Ortalama Eğim (N/s)" in df.columns:
                st.subheader("Ortalama Eğim Grafiği")
                fig3 = px.line(
                    df, 
                    x=x_axis_col, 
                    y="Ortalama Eğim (N/s)",
                    title="Ortalama Eğim vs. Zaman",
                    markers=True,
                    color_discrete_sequence=['green']
                )
                fig3.update_layout(xaxis_title="Geçen Toplam Süre", yaxis_title="Ortalama Eğim (N/s)")
                st.plotly_chart(fig3, use_container_width=True)

            # --- Grafik 4: Alan Altında Kalan Değer (Toplam İş) ---
            # (Görsel: image_a07b33.png)
            if "Toplam İş (J) [K-Y Alanı]" in df.columns:
                st.subheader("Alan Altında Kalan Değer Grafiği (Toplam İş)")
                fig4 = px.line(
                    df,
                    x=x_axis_col,
                    y="Toplam İş (J) [K-Y Alanı]",
                    title="Toplam İş (Kümülatif Enerji) vs. Zaman",
                    markers=True,
                    color_discrete_sequence=['purple']
                )
                fig4.update_layout(xaxis_title="Geçen Toplam Süre", yaxis_title="Toplam İş (Joule)")
                st.plotly_chart(fig4, use_container_width=True)

            # --- 5. Özel Grafik Oluşturucu ---
            st.header("Kendi Grafiğini Oluştur")
            
            # Y ekseni için ÇOKLU sütun seçimi
            y_axes = st.multiselect(
                "Y-Eksen(ler)i Seçin:", 
                df.columns, 
                # Varsayılan olarak ikisini birden seçelim
                default=["Anlik_Eğim (O anki)", "Ortalama Eğim (N/s)"] 
            )
            
            if y_axes:
                st.subheader(f"Özel Grafik: {', '.join(y_axes)} vs. {x_axis_col}")
                fig_custom = px.line(df, x=x_axis_col, y=y_axes, markers=True)
                st.plotly_chart(fig_custom, use_container_width=True)
            
    except Exception as e:
        st.error(f"Dosya okunurken veya grafik çizilirken bir hata oluştu: {e}")
        st.exception(e) # Hatanın detayını ekrana yazdır

else:
    st.info("Başlamak için lütfen bir Excel dosyası yükleyin.")