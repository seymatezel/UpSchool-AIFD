""""import streamlit as st
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
            st.write("Uygun bir kariyer alanı tespit edilemedi.")"""

import streamlit as st
import re
from collections import Counter

class CVAnalyzer:
    def __init__(self):
        # Kariyer alanları ve gereken beceriler
        self.career_skills = {
            "Yazılım Geliştirici": {
                "skills": ["python", "javascript", "java", "c++", "html", "css", "sql", "git", "react", "node.js", "angular", "vue", "django", "flask", "spring"],
                "description": "Mobil ve web uygulamaları geliştirme",
                "roadmap": [
                    "1. Programlama dillerini öğrenin (Python, JavaScript)",
                    "2. Veritabanı yönetimi (SQL)",
                    "3. Web framework'leri (React, Django)",
                    "4. Version control (Git)",
                    "5. Proje portföyü oluşturun"
                ]
            },
            "Veri Analisti": {
                "skills": ["python", "sql", "excel", "tableau", "power bi", "statistics", "pandas", "numpy", "matplotlib", "seaborn", "jupyter", "r"],
                "description": "Büyük veri setlerini analiz etme ve raporlama",
                "roadmap": [
                    "1. İstatistik ve matematik temelleri",
                    "2. Python/R ile veri analizi",
                    "3. SQL ve veritabanı yönetimi",
                    "4. Görselleştirme araçları (Tableau, Power BI)",
                    "5. Makine öğrenmesi temellerini öğrenin"
                ]
            },
            "Dijital Pazarlama": {
                "skills": ["google analytics", "seo", "sem", "social media", "content marketing", "email marketing", "facebook ads", "google ads", "instagram", "linkedin"],
                "description": "Online platformlarda marka tanıtımı ve satış",
                "roadmap": [
                    "1. Dijital pazarlama temellerini öğrenin",
                    "2. Google Analytics sertifikası alın",
                    "3. SEO ve SEM stratejilerini öğrenin",
                    "4. Sosyal medya pazarlama",
                    "5. Content marketing ve email kampanyaları"
                ]
            },
            "Grafik Tasarım": {
                "skills": ["photoshop", "illustrator", "indesign", "figma", "sketch", "creative", "design", "ui", "ux", "adobe", "canva"],
                "description": "Görsel tasarım ve yaratıcı çözümler",
                "roadmap": [
                    "1. Tasarım temellerini öğrenin",
                    "2. Adobe Creative Suite (Photoshop, Illustrator)",
                    "3. UI/UX tasarım prensipleri",
                    "4. Portföy oluşturma",
                    "5. Müşteri projeleri üzerinde çalışın"
                ]
            },
            "Proje Yönetimi": {
                "skills": ["project management", "agile", "scrum", "leadership", "planning", "communication", "jira", "trello", "kanban", "pmp"],
                "description": "Projeleri planlamak ve yönetmek",
                "roadmap": [
                    "1. Proje yönetimi metodolojilerini öğrenin",
                    "2. Agile ve Scrum sertifikası alın",
                    "3. Liderlik becerilerini geliştirin",
                    "4. Proje yönetim araçlarını öğrenin",
                    "5. Gerçek projelerde deneyim kazanın"
                ]
            },
            "Siber Güvenlik": {
                "skills": ["cybersecurity", "penetration testing", "firewall", "network security", "encryption", "vulnerability", "security", "ethical hacking"],
                "description": "Bilgi güvenliği ve siber tehdit analizi",
                "roadmap": [
                    "1. Ağ güvenliği temellerini öğrenin",
                    "2. Penetration testing araçları",
                    "3. Siber güvenlik sertifikaları (CEH, CISSP)",
                    "4. Güvenlik açığı analizi",
                    "5. Incident response süreçleri"
                ]
            }
        }
    
    def extract_skills(self, text):
        """Metinden becerileri çıkarma"""
        text = text.lower()
        found_skills = []
        
        # Tüm kariyer alanlarındaki becerileri kontrol et
        all_skills = set()
        for career in self.career_skills.values():
            all_skills.update(career["skills"])
        
        for skill in all_skills:
            if skill in text:
                found_skills.append(skill)
        
        return found_skills
    
    def analyze_strengths_weaknesses(self, text, skills):
        """Güçlü ve zayıf yönleri analiz etme"""
        strengths = []
        weaknesses = []
        
        # Güçlü yönler
        if len(skills) >= 5:
            strengths.append("Çok çeşitli beceri setine sahipsiniz")
        if "experience" in text.lower() or "deneyim" in text.lower():
            strengths.append("İş deneyiminiz bulunuyor")
        if "project" in text.lower() or "proje" in text.lower():
            strengths.append("Proje deneyiminiz var")
        if "education" in text.lower() or "eğitim" in text.lower() or "university" in text.lower() or "üniversite" in text.lower():
            strengths.append("Eğitim geçmişiniz güçlü")
        if "certificate" in text.lower() or "sertifika" in text.lower():
            strengths.append("Sertifikalarınız mevcut")
        if "team" in text.lower() or "takım" in text.lower():
            strengths.append("Takım çalışması deneyiminiz var")
        
        # Zayıf yönler
        if len(skills) < 3:
            weaknesses.append("Daha fazla teknik beceri geliştirmeniz önerilir")
        if "certificate" not in text.lower() and "sertifika" not in text.lower():
            weaknesses.append("Sertifikalar CV'nizde belirtilmemiş")
        if len(text) < 200:
            weaknesses.append("CV'niz daha detaylı olabilir")
        if "language" not in text.lower() and "dil" not in text.lower():
            weaknesses.append("Yabancı dil becerilerinizi belirtmeyi unutmayın")
        
        return strengths, weaknesses
    
    def recommend_careers(self, skills):
        """Kariyer önerileri"""
        career_scores = {}
        
        for career, data in self.career_skills.items():
            score = 0
            matched_skills = []
            for skill in skills:
                if skill in data["skills"]:
                    score += 1
                    matched_skills.append(skill)
            career_scores[career] = {
                'score': score,
                'matched_skills': matched_skills,
                'total_skills': len(data["skills"])
            }
        
        # En yüksek skorlu kariyerleri öner
        sorted_careers = sorted(career_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        return sorted_careers
    
    def get_career_match_percentage(self, score, total_skills):
        """Kariyer uyum yüzdesini hesapla"""
        if total_skills == 0:
            return 0
        return min(100, round((score / total_skills) * 100))

def main():
    st.set_page_config(
        page_title="CV Analiz ve Kariyer Önerisi",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS stil
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
    }
    .skill-badge {
        background-color: #e1f5fe;
        color: #01579b;
        padding: 0.25rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .strength-item {
        color: #2e7d32;
        font-weight: bold;
    }
    .weakness-item {
        color: #d32f2f;
        font-weight: bold;
    }
    .career-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Ana başlık
    st.markdown('<h1 class="main-header">📋 CV Analiz ve Kariyer Önerisi</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Uygulama Bilgileri")
    st.sidebar.info("""
    Bu uygulama CV'nizを analiz ederek:
    - Becerilerinizi tespit eder
    - Güçlü/zayıf yönlerinizi değerlendirir  
    - Size uygun kariyer alanlarını önerir
    - Gelişim yol haritası sunar
    """)
    
    st.sidebar.success("💡 CV'nizi metin olarak girin ve analiz edin!")
    
    # Ana içerik
    analyzer = CVAnalyzer()
    
    # CV giriş alanı
    st.markdown('<div class="section-header">📝 CV Metninizi Girin</div>', unsafe_allow_html=True)
    
    # Örnek CV metni
    sample_cv = """Adım John Doe. Bilgisayar Mühendisliği mezunuyum. 
    
3 yıllık Python ve JavaScript deneyimim var. Web geliştirme projelerinde çalıştım. 
React, Django ve SQL biliyorum. Git kullanarak takım çalışması yaptım.

Üniversitede makine öğrenmesi projeleri geliştirdim. 
Excel ve Power BI ile veri analizi deneyimim var.

İngilizce C1 seviyesinde. Takım lideri olarak çalıştım. 
Agile metodolojilerine hakimim."""
    
    # Örnek CV butonu
    if st.button("📋 Örnek CV Metni Yükle"):
        st.session_state.cv_text = sample_cv
    
    # CV metin giriş alanı
    cv_text = st.text_area(
        "CV Metniniz (Türkçe veya İngilizce):",
        value=st.session_state.get('cv_text', ''),
        height=300,
        help="CV'nizdeki deneyimlerinizi, becerilerinizi ve eğitim bilgilerinizi buraya yazın."
    )
    
    # Analiz butonu
    if st.button("🔍 CV'mi Analiz Et", type="primary"):
        if cv_text.strip():
            # Analiz yap
            skills = analyzer.extract_skills(cv_text)
            strengths, weaknesses = analyzer.analyze_strengths_weaknesses(cv_text, skills)
            recommended_careers = analyzer.recommend_careers(skills)
            
            # Sonuçları göster
            st.markdown('<div class="section-header">🎯 Analiz Sonuçları</div>', unsafe_allow_html=True)
            
            # Üç sütunlu layout
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("💡 Tespit Edilen Beceriler")
                if skills:
                    skills_html = ""
                    for skill in skills:
                        skills_html += f'<span class="skill-badge">{skill.title()}</span> '
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.info("Belirgin beceri tespit edilemedi")
            
            with col2:
                st.subheader("✅ Güçlü Yönler")
                if strengths:
                    for strength in strengths:
                        st.markdown(f'<div class="strength-item">• {strength}</div>', unsafe_allow_html=True)
                else:
                    st.info("Güçlü yönler tespit edilemedi")
            
            with col3:
                st.subheader("⚠️ Geliştirilebilir Alanlar")
                if weaknesses:
                    for weakness in weaknesses:
                        st.markdown(f'<div class="weakness-item">• {weakness}</div>', unsafe_allow_html=True)
                else:
                    st.success("Belirgin zayıf yön tespit edilemedi")
            
            # Kariyer önerileri
            st.markdown('<div class="section-header">🎯 Size Uygun Kariyer Alanları</div>', unsafe_allow_html=True)
            
            if recommended_careers:
                # En iyi 3 kariyer önerisini göster
                top_careers = [career for career in recommended_careers if career[1]['score'] > 0][:3]
                
                if top_careers:
                    for i, (career, data) in enumerate(top_careers, 1):
                        match_percentage = analyzer.get_career_match_percentage(data['score'], data['total_skills'])
                        
                        st.markdown(f"""
                        <div class="career-card">
                            <h3>{i}. {career}</h3>
                            <p><strong>Açıklama:</strong> {analyzer.career_skills[career]['description']}</p>
                            <p><strong>Uyum Oranı:</strong> {match_percentage}% ({data['score']}/{data['total_skills']} beceri)</p>
                            <p><strong>Eşleşen Beceriler:</strong> {', '.join(data['matched_skills'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # En uygun kariyer için yol haritası
                    best_career = top_careers[0][0]
                    st.markdown(f'<div class="section-header">🗺️ {best_career} İçin Gelişim Yol Haritası</div>', unsafe_allow_html=True)
                    
                    roadmap = analyzer.career_skills[best_career]["roadmap"]
                    for step in roadmap:
                        st.markdown(f"**{step}**")
                    
                    # Motivasyon mesajı
                    st.success(f"🎉 {best_career} alanında güçlü bir potansiyeliniz var! Yukarıdaki adımları takip ederek kendinizi geliştirebilirsiniz.")
                else:
                    st.warning("Spesifik kariyer önerisi oluşturulamadı. CV'nize daha fazla teknik beceri eklemeyi deneyin.")
            else:
                st.error("Kariyer analizi yapılamadı.")
        else:
            st.error("Lütfen CV metninizi girin!")
    
    # Alt bilgi
    st.markdown("---")
    st.markdown("💡 **İpucu:** Daha iyi sonuçlar için CV'nizde teknik becerilerinizi, iş deneyimlerinizi ve projelerinizi detaylı olarak belirtin.")

if __name__ == "__main__":
    main()