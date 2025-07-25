from agents import CVAgent

# Agent başlat
 
agent = CVAgent(analyzer)

# CV input alanı
st.subheader("📝 CV Metnini Girin")
cv_input = st.text_area("CV içeriğinizi buraya yapıştırın", height=300)

if st.button("Analiz Et") and cv_input.strip():
    with st.spinner("CV analiz ediliyor..."):
        result = agent.run("Lütfen bu CV'yi analiz et ve öneriler sun.", cv_input)
        if "error" in result:
            st.error("❌ Hata: " + result["error"])
        else:
            st.success("✅ Analiz tamamlandı!")

            st.subheader("✅ Güçlü Yönler")
            for item in result.get("strengths", []):
                st.markdown(f"- **{item.get('title', '')}**: {item.get('description', '')}")

            st.subheader("⚠️ Geliştirme Alanları")
            for item in result.get("weaknesses", []):
                st.markdown(f"- **{item.get('title', '')}**: {item.get('description', '')}")

            st.subheader("💼 Önerilen Kariyerler")
            for item in result.get("suggested_careers", []):
                st.markdown(f"- **{item.get('title', '')}**: {item.get('description', '')}")