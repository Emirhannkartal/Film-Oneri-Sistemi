Bu proje, kullanıcılara kişiselleştirilmiş ve çeşitlendirilmiş film önerileri sunmak amacıyla geliştirilmiştir. MovieLens 20M veri seti kullanılarak, kullanıcıların izleme geçmişi ve film türü tercihleri göz önünde bulundurularak öneriler sunulmaktadır. Sistem ayrıca popüler filmler ve birliktelik kurallarına (Apriori algoritması) dayalı öneriler sağlayarak kullanıcı deneyimini zenginleştirmeyi hedeflemektedir.

Özellikler

Popüler Film Önerileri: Kullanıcıya, genel olarak en çok beğenilen filmleri önerir.

Kişiselleştirilmiş Öneriler: Kullanıcının izleme geçmişine ve tercih ettiği türlere göre öneriler sunar.

Birliktelik Kuralları ile Öneriler: Apriori algoritması kullanılarak, kullanıcıların sıklıkla birlikte izlediği filmlere dayalı öneriler üretir.

Film Türünü ve Adına Göre Öneriler: Kullanıcının belirttiği film türünü veya adına göre öneriler sunar.

Grafik Kullanıcı Arayüzü (GUI): Tkinter ile oluşturulan kullanıcı dostu bir arayüz sağlar.
Kullanıcı-Film Matrisi:
   Kullanıcıların izleme geçmişi ve film puanlamalarına dayalı olarak kullanıcı-film matrisi oluşturulmuştur. Bu matris:
   - Satırlarda kullanıcıları, sütunlarda filmleri temsil eder.
   - Hücre değerleri, kullanıcının bir filmi izleyip izlemediğini veya verdiği puanı gösterir.
   - İzlenen filmler `1`, izlenmeyenler veya puanlanmayanlar `0` olarak işaretlenir.
   Kullanıcı-film matrisi, kişiselleştirilmiş önerilerin temelini oluşturur.

5. Ağaç Veri Yapısı:
   Birliktelik kurallarının uygulanmasında, sık öğe kümelerinin depolanması için ağaç veri yapısı (Trie) kullanılmıştır:
   - **Hızlı Arama ve Ekleme:** Trie, sık kullanılan film kümelerinin verimli bir şekilde saklanmasını sağlar.
   - **Bellek Verimliliği:** Belleği optimize ederek yalnızca gerekli düğümleri saklar.
   Örneğin, bir filmle ilişkili diğer filmler, ağacın ilgili düğümlerinde depolanarak hızlıca erişilebilir hale gelir.

Kullanılan Teknolojiler ve Araçlar

Bu projede aşağıdaki teknolojiler ve araçlar kullanılmıştır:

Programlama Dili

Python: Projenin temel işlevselliğini ve veri işlemeyi gerçekleştirmek için kullanıldı.

Veri İşleme ve Analiz

Pandas: Veri manipülasyonu ve temizleme işlemleri için kullanıldı.

MLxtend: Apriori algoritmasının uygulanması ve birliktelik kurallarının çıkarılması için tercih edildi.

Grafik Kullanıcı Arayüzü (GUI)

Tkinter: Kullanıcıların sistemle kolay etkileşim kurması için basit ve etkili bir grafik arayüz geliştirildi.

Veri Seti

MovieLens 20M Veri Seti: Kaggle platformundan alınmış, kullanıcı-izleme alışkanlıklarını içeren geniş bir veri seti.

Diğer Araçlar

Numpy: Matematiksel işlemler ve veri manipülasyonu için kullanıldı.

Matplotlib ve Seaborn: Veri analizi sonuçlarını görselleştirmek için kullanılan kütüpaneler.

KURULUMLAR
Python Yükleyin:
Python'un en güncel sürümünü Python Resmi Web Sitesi üzerinden yükleyin.

Gerekli Kütüpaneleri Yükleyin:
Aşağıdaki komutu kullanarak gerekli Python kütüpanelerini yükleyebilirsiniz:
pip install pandas mlxtend tkinter numpy matplotlib seaborn


