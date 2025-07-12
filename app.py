import streamlit as st
import re

# CV analiz fonksiyonu
def analyze_cv(cv_text):
    strengths = []
    weaknesses = []

    # Basit kurallar
    if "takım" in cv_text.lower():
        strengths.append("Takım çalışmasına yatkın")
    if "python" in cv_text.lower():
        strengths.append("Python bilgisi var")
    if "veri" in cv_text.lower():
        strengths.append("Veri analizi deneyimi var")
    if "lider" in cv_text.lower():
        strengths.append("Liderlik deneyimi olabilir")
    if "yönetim" in cv_text.lower():
        strengths.append("Yönetim becerisine sahip")

    if len(cv_text.split()) < 50:
        weaknesses.append("CV çok kısa olabilir, detay eksikliği")
    if not re.search(r"\d{4}", cv_text):
        weaknesses.append("Tarih bilgisi eksik olabilir (eğitim/deneyim yılı)")

    # Kariyer önerileri (örnek mantık)
    suggestions = []
    if "python" in cv_text.lower() or "veri" in cv_text.lower():
        suggestions.append("Veri Analisti")
    if "takım" in cv_text.lower() or "yönetim" in cv_text.lower():
        suggestions.append("Proje Yöneticisi")
    if "lider" in cv_text.lower():
        suggestions.append("Topluluk Lideri")

    return strengths, weaknesses, suggestions

# Streamlit Arayüzü
st.set_page_config(page_title="CV Analiz Aracı", page_icon="📄")
st.title("📄 CV'den Güçlü/Zayıf Yön Analizi ve Kariyer Önerileri")

cv_input = st.text_area("CV metninizi buraya yapıştırın:", height=300)

if st.button("Analiz Et"):
    if cv_input.strip() == "":
        st.warning("Lütfen CV metnini girin.")
    else:
        strengths, weaknesses, suggestions = analyze_cv(cv_input)
        st.subheader("🟩 Güçlü Yönler")
        if strengths:
            st.write("- " + "\n- ".join(strengths))
        else:
            st.write("Güçlü yön tespit edilemedi.")

        st.subheader("🟥 Zayıf Yönler")
        if weaknesses:
            st.write("- " + "\n- ".join(weaknesses))
        else:
            st.write("Zayıf yön tespit edilemedi.")

        st.subheader("🎯 Uygun Kariyer Alanları")
        if suggestions:
            st.write("- " + "\n- ".join(suggestions))
        else:
            st.write("Uygun bir kariyer alanı tespit edilemedi.")