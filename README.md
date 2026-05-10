# Devre Duyarlılık Analizi Projesi

Bu proje, bir DC direnç devresindeki parametre değişimlerinin (direnç değerleri ve kaynak akımları) düğüm gerilimleri üzerindeki etkisini inceleyen bir **Duyarlılık Analizi** aracıdır. Hesaplamalar sembolik ve sayısal yöntemler birleştirilerek yapılmıştır.

## 🛠 Özellikler
- **Sembolik Hesaplama:** `SymPy` kütüphanesi kullanılarak devrenin düğüm denklemleri otomatik olarak türetilir.
- **Sayısal Değerlendirme:** `NumPy` ile belirli parametre değerleri atanarak hassasiyet katsayıları hesaplanır.
- **Görselleştirme:** Analiz sonuçları, `Matplotlib` aracılığıyla yüksek çözünürlüklü bar grafikleri olarak sunulur.

## 📊 Metot
Proje, devreyi temsil eden $G \cdot V = I$ matris denklemini çözer:
- **G:** İletkenlik (Admitans) Matrisi
- **V:** Düğüm Gerilimleri Vektörü
- **I:** Kaynak Vektörü

Duyarlılıklar, normalize edilmiş türev formülü kullanılarak hesaplanır: $S_p^V = \frac{\partial V}{\partial p} \cdot \frac{p}{V}$
