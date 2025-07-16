# AIFD-CapstoneProject
# 📄 CV Analiz Uygulaması

Bu uygulama, kullanıcıların CV (özgeçmiş) metinlerini analiz ederek güçlü ve zayıf yönlerini çıkarmak, potansiyel kariyer yollarını önermek ve seçilen kariyer için detaylı bir gelişim yol haritası sunmak amacıyla geliştirilmiştir. Streamlit arayüzü ile kullanıcı dostudur ve Hugging Face Transformers modellerini kullanarak AI destekli analizler gerçekleştirir.

---

## Özellikler

-  CV bilgisi metin olarak girilebilir ya da `.txt` dosyası olarak yüklenebilir
-  Hugging Face modelleri ile AI/LLM (Large Language Model) tabanlı analiz
-  Anahtar kelime tabanlı hızlı analiz alternatifi
-  Güçlü yönler ve  gelişim alanlarını analiz etme
-  Potansiyel kariyer önerileri
- Kariyer yol haritası (tahmini süre + kaynaklarla birlikte)

---

##  Gereksinimler

Python 3.8 veya üzeri bir sürüm yüklü olmalıdır.

---

##  Kurulum

1. **Projeyi klonlayın veya dosyaları indirin:**

```bash
git clone https://github.com/kullanici-adi/cv-analiz-app.git
cd cv-analiz-app
```

2. **Sanal ortam oluşturun ve aktif edin (opsiyonel ama önerilir):**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Gerekli kütüphaneleri yükleyin:**

```bash
pip install -r requirements.txt
```

Eğer `requirements.txt` yoksa, aşağıdaki komutla bağımlılıkları manuel kurabilirsiniz:

```bash
pip install streamlit transformers torch
```

---

##  Uygulamayı Başlat

```bash
streamlit run app.py
```

> Not: Dosya adın farklıysa örneğin `cv_analiz.py` gibi, o adı kullanmalısın.

Uygulama tarayıcınızda otomatik olarak açılmazsa şu adrese gidin:  
📍 [http://localhost:8501](http://localhost:8501)

---

##  Kullanılan Modeller

- `gpt2` – Metin üretimi (text generation)
- `cardiffnlp/twitter-roberta-base-sentiment-latest` – Duygu analizi (sentiment analysis)

Bu modeller ilk çalıştırmada Hugging Face üzerinden indirilecektir. İnternet bağlantısı gerektiğini unutmayın.

---

##  Kullanım Adımları

1. **CV Bilgisi Girin:**  
   Metin kutusuna CV metni yazın veya `.txt` uzantılı dosya yükleyin.

2. **Analiz Yöntemini Seçin:**  
   - AI/LLM (gelişmiş, yorumlu analiz)  
   - Hızlı analiz (anahtar kelime tabanlı)

3. **Analizi Başlatın:**  
   "🔍 Analiz Et" butonuna tıklayın.

4. **Sonuçları Görüntüleyin:**  
   - Güçlü yönler
   - Gelişim alanları
   - Önerilen kariyer yolları

5. **Yol Haritası Seçin:**  
   İlginizi çeken kariyer alanını seçerek o alanda ilerlemek için önerilen adımları, süreyi ve kaynakları görün.

---

## Not

> Bu proje eğitim ve kariyer gelişimi amaçlı hazırlanmıştır. AI tabanlı analiz çıktıları öneri niteliğindedir ve profesyonel kararlar için destekleyici olarak değerlendirilmelidir.

Made with by Şeyma Tezel  
 Streamlit + Hugging Face Transformers kullanılarak geliştirilmiştir.

