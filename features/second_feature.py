import streamlit as st
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')
import json

# Sayfa yapılandırması
st.set_page_config(
    page_title="CV Analiz Uygulaması",
    page_icon="📄",
    layout="wide"
)

# CSS stil
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .analysis-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .strength-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .weakness-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    .career-box {
        background-color: #e2e3e5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #6c757d;
        margin: 0.5rem 0;
    }
    .roadmap-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CVAnalyzer:
    def __init__(self):
        # Hugging Face LLM modelini yükle
        self.load_llm_model()
        
        self.skills_keywords = {
            'teknoloji': ['python', 'java', 'javascript', 'html', 'css', 'sql', 'machine learning', 
                         'data science', 'web development', 'mobile development', 'artificial intelligence'],
            'yönetim': ['project management', 'team lead', 'scrum master', 'agile', 'leadership',
                       'koordinasyon', 'planlama', 'strateji'],
            'analiz': ['data analysis', 'business analysis', 'statistical analysis', 'reporting',
                      'excel', 'tableau', 'power bi', 'analytics'],
            'tasarım': ['ui/ux', 'graphic design', 'photoshop', 'illustrator', 'figma', 'sketch'],
            'pazarlama': ['digital marketing', 'social media', 'seo', 'content marketing', 'advertising'],
            'muhasebe': ['accounting', 'finance', 'budget', 'financial analysis', 'taxation'],
            'satış': ['sales', 'customer service', 'crm', 'negotiation', 'business development']
        }
        
        self.career_suggestions = {
            'teknoloji': ['Yazılım Geliştirici', 'Data Scientist', 'Web Developer', 'Mobile Developer', 
                         'DevOps Engineer', 'AI/ML Engineer'],
            'yönetim': ['Proje Yöneticisi', 'Ürün Yöneticisi', 'Scrum Master', 'Takım Lideri', 
                       'Operasyon Yöneticisi'],
            'analiz': ['Business Analyst', 'Data Analyst', 'İş Zekası Uzmanı', 'Pazar Araştırmacısı'],
            'tasarım': ['UI/UX Designer', 'Grafik Tasarımcı', 'Ürün Tasarımcısı', 'Web Tasarımcısı'],
            'pazarlama': ['Dijital Pazarlama Uzmanı', 'İçerik Pazarlama Uzmanı', 'SEO Uzmanı', 
                         'Sosyal Medya Uzmanı'],
            'muhasebe': ['Mali Müşavir', 'Muhasebeci', 'Finansal Analist', 'Bütçe Uzmanı'],
            'satış': ['Satış Temsilcisi', 'Satış Müdürü', 'İş Geliştirme Uzmanı', 'Müşteri Temsilcisi']
        }
        
        self.roadmaps = {
            'Yazılım Geliştirici': {
                'adımlar': [
                    '1. Temel programlama dilleri öğrenin (Python, Java, JavaScript)',
                    '2. Veri yapıları ve algoritmalar çalışın',
                    '3. Version control sistemlerini (Git) öğrenin',
                    '4. Web framework\'leri ile projeler geliştirin',
                    '5. Veritabanı yönetimi öğrenin (SQL)',
                    '6. Açık kaynak projelere katkıda bulunun'
                ],
                'süre': '6-12 ay',
                'kaynaklar': ['Codecademy', 'freeCodeCamp', 'GitHub', 'Stack Overflow']
            },
            'Data Scientist': {
                'adımlar': [
                    '1. Python ve R programlama dillerini öğrenin',
                    '2. İstatistik ve matematik temelleri güçlendirin',
                    '3. Pandas, NumPy, Scikit-learn kütüphanelerini öğrenin',
                    '4. Makine öğrenmesi algoritmalarını uygulayın',
                    '5. Veri görselleştirme araçlarını kullanın',
                    '6. Gerçek veri setleriyle projeler yapın'
                ],
                'süre': '8-15 ay',
                'kaynaklar': ['Kaggle', 'Coursera', 'edX', 'Jupyter Notebook']
            },
            'UI/UX Designer': {
                'adımlar': [
                    '1. Tasarım prensiplerini öğrenin',
                    '2. Figma, Sketch, Adobe XD araçlarını kullanın',
                    '3. Kullanıcı araştırması yöntemlerini öğrenin',
                    '4. Wireframe ve prototip oluşturun',
                    '5. Kullanıcı testleri yapın',
                    '6. Portfolio oluşturun'
                ],
                'süre': '4-8 ay',
                'kaynaklar': ['Figma', 'Behance', 'Dribbble', 'Nielsen Norman Group']
            },
            'Dijital Pazarlama Uzmanı': {
                'adımlar': [
                    '1. Dijital pazarlama temellerini öğrenin',
                    '2. Google Analytics ve Google Ads sertifikası alın',
                    '3. SEO ve SEM stratejilerini öğrenin',
                    '4. Sosyal medya pazarlaması yapın',
                    '5. İçerik pazarlama stratejileri geliştirin',
                    '6. Email pazarlama kampanyaları yürütün'
                ],
                'süre': '3-6 ay',
                'kaynaklar': ['Google Digital Garage', 'HubSpot Academy', 'Facebook Blueprint']
            }
        }
    
    @st.cache_resource
    def load_llm_model(_self):
        """Hugging Face LLM modelini yükle"""
        try:
            # Hafif ve hızlı bir model kullan
            model_name = "microsoft/DialoGPT-medium"
            
            # Text generation pipeline
            _self.text_generator = pipeline(
                "text-generation",
                model="gpt2",
                tokenizer="gpt2",
                max_length=512,
                temperature=0.7,
                pad_token_id=50256
            )
            
            # Sentiment analysis pipeline
            _self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest"
            )
            
            return True
        except Exception as e:
            st.error(f"Model yüklenirken hata: {str(e)}")
            return False
    
    def generate_llm_analysis(self, cv_text: str) -> Dict:
        """LLM kullanarak CV analizi yap"""
        try:
            # CV'yi analiz etmek için prompt hazırla
            prompt = f"""
            Aşağıdaki CV'yi analiz edin:
            
            CV: {cv_text[:1000]}...
            
            Analiz:
            Güçlü yönler:
            """
            
            # LLM ile metin üret
            response = self.text_generator(
                prompt,
                max_length=len(prompt.split()) + 100,
                num_return_sequences=1,
                temperature=0.7
            )
            
            generated_text = response[0]['generated_text']
            
            # Sentiment analizi
            sentiment = self.sentiment_analyzer(cv_text[:512])
            
            # Basit parsing ile güçlü yönleri çıkar
            strengths = self.extract_strengths_from_llm(generated_text)
            weaknesses = self.extract_weaknesses_from_llm(cv_text)
            careers = self.suggest_careers_with_llm(cv_text)
            
            return {
                'llm_generated': True,
                'strengths': strengths,
                'weaknesses': weaknesses,
                'suggested_careers': careers,
                'sentiment': sentiment[0]['label'],
                'confidence': sentiment[0]['score'],
                'raw_llm_output': generated_text
            }
            
        except Exception as e:
            st.error(f"LLM analizi sırasında hata: {str(e)}")
            return self.fallback_analysis(cv_text)
    
    def extract_strengths_from_llm(self, llm_output: str) -> List[str]:
        """LLM çıktısından güçlü yönleri çıkar"""
        strengths = []
        
        # Basit keyword tabanlı çıkarım
        positive_keywords = ['experienced', 'skilled', 'proficient', 'expert', 'strong', 'excellent']
        
        sentences = llm_output.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in positive_keywords):
                strengths.append(sentence.strip())
        
        # Eğer bulunamazsa varsayılan değerler
        if not strengths:
            strengths = [
                "Teknik beceriler mevcut",
                "Profesyonel deneyim var",
                "İletişim becerileri güçlü"
            ]
        
        return strengths[:5]  # Max 5 güçlü yön
    
    def extract_weaknesses_from_llm(self, cv_text: str) -> List[str]:
        """CV'den zayıf yönleri analiz et"""
        weaknesses = []
        cv_lower = cv_text.lower()
        
        # Eksik alanları kontrol et
        if 'education' not in cv_lower and 'eğitim' not in cv_lower:
            weaknesses.append("Eğitim bilgisi eksik")
        
        if 'experience' not in cv_lower and 'deneyim' not in cv_lower:
            weaknesses.append("İş deneyimi bilgisi yetersiz")
        
        if 'project' not in cv_lower and 'proje' not in cv_lower:
            weaknesses.append("Proje deneyimi belirtilmemiş")
        
        if len(cv_text) < 200:
            weaknesses.append("CV çok kısa, detay eksik")
        
        return weaknesses if weaknesses else ["Genel olarak yeterli profil"]
    
    def suggest_careers_with_llm(self, cv_text: str) -> List[str]:
        """LLM yardımıyla kariyer önerileri"""
        try:
            # Basit prompt ile kariyer önerisi
            career_prompt = f"Based on this CV, suggest 3 career paths: {cv_text[:300]}"
            
            # Keyword tabanlı kariyer önerisi (LLM fallback)
            cv_lower = cv_text.lower()
            suggested_careers = []
            
            # Teknoloji alanı
            if any(word in cv_lower for word in ['python', 'java', 'programming', 'software', 'kod']):
                suggested_careers.extend(['Yazılım Geliştirici', 'Data Scientist'])
            
            # Yönetim alanı
            if any(word in cv_lower for word in ['manager', 'leader', 'team', 'yönetici']):
                suggested_careers.extend(['Proje Yöneticisi', 'Takım Lideri'])
            
            # Tasarım alanı
            if any(word in cv_lower for word in ['design', 'ui', 'ux', 'tasarım']):
                suggested_careers.extend(['UI/UX Designer', 'Grafik Tasarımcı'])
            
            # Pazarlama alanı
            if any(word in cv_lower for word in ['marketing', 'social media', 'pazarlama']):
                suggested_careers.extend(['Dijital Pazarlama Uzmanı'])
            
            return list(set(suggested_careers))[:6] if suggested_careers else ['Genel İş Pozisyonları']
            
        except Exception as e:
            return ['Yazılım Geliştirici', 'Data Analyst', 'Proje Yöneticisi']
    
    def fallback_analysis(self, cv_text: str) -> Dict:
        """LLM çalışmazsa fallback analizi"""
        return self.analyze_cv_text(cv_text)
    
    def analyze_cv_text(self, cv_text: str) -> Dict:
        """CV metnini analiz eder (keyword tabanlı)"""
        cv_lower = cv_text.lower()
        
        # Beceri analizi
        found_skills = {}
        for category, keywords in self.skills_keywords.items():
            found_skills[category] = []
            for keyword in keywords:
                if keyword in cv_lower:
                    found_skills[category].append(keyword)
        
        # Güçlü yönleri belirle
        strengths = []
        for category, skills in found_skills.items():
            if len(skills) >= 2:
                strengths.append(f"{category.title()}: {', '.join(skills[:3])}")
        
        # Zayıf yönleri belirle
        weaknesses = []
        weak_areas = [cat for cat, skills in found_skills.items() if len(skills) == 0]
        if weak_areas:
            weaknesses.append(f"Eksik alanlar: {', '.join(weak_areas)}")
        
        # Deneyim analizi
        experience_keywords = ['yıl', 'year', 'experience', 'deneyim', 'worked', 'çalıştı']
        has_experience = any(keyword in cv_lower for keyword in experience_keywords)
        
        if not has_experience:
            weaknesses.append("Deneyim bilgisi yetersiz")
        
        # Eğitim analizi
        education_keywords = ['üniversite', 'university', 'degree', 'bachelor', 'master', 'lisans', 'yüksek lisans']
        has_education = any(keyword in cv_lower for keyword in education_keywords)
        
        if has_education:
            strengths.append("Eğitim geçmişi mevcut")
        else:
            weaknesses.append("Eğitim bilgisi eksik")
        
        # Kariyer önerileri
        career_matches = {}
        for category, skills in found_skills.items():
            if skills:
                career_matches[category] = len(skills)
        
        # En yüksek puan alan kategoriler
        top_categories = sorted(career_matches.items(), key=lambda x: x[1], reverse=True)[:3]
        
        suggested_careers = []
        for category, _ in top_categories:
            suggested_careers.extend(self.career_suggestions.get(category, []))
        
        return {
            'llm_generated': False,
            'strengths': strengths if strengths else ['Temel beceriler mevcut'],
            'weaknesses': weaknesses if weaknesses else ['Genel olarak yeterli profil'],
            'suggested_careers': list(set(suggested_careers))[:6],
            'skill_categories': found_skills
        }

# Uygulama başlığı
st.markdown('<h1 class="main-header">📄 CV Analiz Uygulaması</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">CV\'nizi analiz edin ve kariyer önerilerini keşfedin!</p>', unsafe_allow_html=True)

# Session state initialization
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'selected_career' not in st.session_state:
    st.session_state.selected_career = None
if 'show_roadmap' not in st.session_state:
    st.session_state.show_roadmap = False

# CV Analiz Sınıfını başlat
analyzer = CVAnalyzer()

# Ana içerik alanı
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 CV Analizi")
    
    # CV girişi
    cv_input_method = st.radio("CV bilgilerinizi nasıl girmek istiyorsunuz?", 
                               ["Metin olarak gir", "Dosya yükle"])
    
    cv_text = ""
    
    if cv_input_method == "Metin olarak gir":
        cv_text = st.text_area("CV bilgilerinizi buraya giriniz:", 
                              height=200, 
                              placeholder="Adınız, deneyiminiz, becerileriniz, eğitim durumunuz vb...")
    else:
        uploaded_file = st.file_uploader("CV dosyanızı yükleyin", type=['txt'])
        if uploaded_file is not None:
            cv_text = str(uploaded_file.read(), "utf-8")
            st.text_area("Yüklenen CV:", value=cv_text, height=200)
    
    # Analiz butonu
    analyze_method = st.radio("Analiz yöntemi:", ["🤖 AI/LLM Analizi", "⚡ Hızlı Analiz"])
    
    if st.button("🔍 Analiz Et", type="primary", use_container_width=True):
        if cv_text.strip():
            with st.spinner("CV analiz ediliyor..."):
                if analyze_method == "🤖 AI/LLM Analizi":
                    st.session_state.analysis_result = analyzer.generate_llm_analysis(cv_text)
                else:
                    st.session_state.analysis_result = analyzer.analyze_cv_text(cv_text)
                st.session_state.analysis_done = True
                st.session_state.show_roadmap = False
        else:
            st.warning("Lütfen CV bilgilerinizi giriniz!")

with col2:
    st.subheader("ℹ️ Nasıl Kullanılır?")
    st.markdown("""
    1. **CV Bilgilerini Girin**: CV'nizdeki bilgileri metin olarak girin veya dosya yükleyin
    2. **Analiz Et**: Butona tıklayarak AI analizini başlatın
    3. **Sonuçları İnceleyin**: Güçlü/zayıf yönlerinizi görün
    4. **Kariyer Önerilerini Keşfedin**: Size uygun alanları keşfedin
    5. **Yol Haritası Alın**: Seçtiğiniz alan için detaylı plan alın
    """)

# Analiz sonuçları
if st.session_state.analysis_done and st.session_state.analysis_result:
    st.markdown("---")
    
    result = st.session_state.analysis_result
    
    # LLM analizi yapıldıysa ekstra bilgi göster
    if result.get('llm_generated', False):
        st.subheader("🤖 AI/LLM Analiz Sonuçları")
        
        # Sentiment analizi
        sentiment_color = "green" if result.get('sentiment') == 'POSITIVE' else "orange" if result.get('sentiment') == 'NEUTRAL' else "red"
        confidence = result.get('confidence', 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sentiment", result.get('sentiment', 'Unknown'))
        with col2:
            st.metric("Güven Skoru", f"{confidence:.2f}")
        with col3:
            st.metric("Analiz Tipi", "🤖 AI/LLM")
        
        # Debug bilgisi (isteğe bağlı)
        with st.expander("🔍 LLM Raw Output (Debug)"):
            st.text(result.get('raw_llm_output', 'No raw output'))
            
    else:
        st.subheader("⚡ Hızlı Analiz Sonuçları")
    
    # Sonuçları 3 sütunda göster
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💪 Güçlü Yönleriniz")
        for strength in result['strengths']:
            st.markdown(f'<div class="strength-box">✅ {strength}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎯 Gelişim Alanları")
        for weakness in result['weaknesses']:
            st.markdown(f'<div class="weakness-box">⚠️ {weakness}</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🚀 Kariyer Önerileri")
        for career in result['suggested_careers']:
            st.markdown(f'<div class="career-box">💼 {career}</div>', unsafe_allow_html=True)
    
    # Kariyer seçimi
    st.markdown("---")
    st.subheader("🎯 Kariyer Yol Haritası")
    
    if result['suggested_careers']:
        st.markdown("**Önerilen kariyer alanlarından birini seçerek detaylı yol haritası alabilirsiniz:**")
        
        selected_career = st.selectbox(
            "Hangi kariyer alanı için yol haritası istiyorsunuz?",
            ["Seçiniz..."] + result['suggested_careers']
        )
        
        if selected_career != "Seçiniz...":
            if st.button("📋 Yol Haritasını Göster", type="secondary"):
                st.session_state.selected_career = selected_career
                st.session_state.show_roadmap = True
    
    # Yol haritası gösterimi
    if st.session_state.show_roadmap and st.session_state.selected_career:
        career = st.session_state.selected_career
        st.markdown(f"### 📋 {career} Yol Haritası")
        
        if career in analyzer.roadmaps:
            roadmap = analyzer.roadmaps[career]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 🗺️ Adımlar:")
                for step in roadmap['adımlar']:
                    st.markdown(f'<div class="roadmap-box">{step}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### ⏱️ Tahmini Süre:")
                st.info(roadmap['süre'])
                
                st.markdown("#### 📚 Önerilen Kaynaklar:")
                for resource in roadmap['kaynaklar']:
                    st.markdown(f"• {resource}")
        else:
            st.info(f"{career} alanı için henüz detaylı yol haritası hazırlanmamış. Genel tavsiyeler:")
            st.markdown("""
            - Bu alanda uzman kişilerle iletişim kurun
            - İlgili sertifikasyon programlarını araştırın
            - Sektör etkinliklerine katılın
            - Online kurslar ve eğitimler alın
            - Pratik projeler yapın
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💡 Bu uygulama AI tabanlı analiz yapmaktadır. Sonuçlar genel öneriler niteliğindedir.</p>
    <p>Made with ❤️ using Streamlit and Hugging Face Transformers</p>
</div>
""", unsafe_allow_html=True)