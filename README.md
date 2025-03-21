# MetroSimulation
Proje Başlığı ve Kısa Açıklama

Bu proje, bir metro simülasyonu oluşturarak, farklı algoritmalar kullanarak en kısa yolu ve en etkili rota planlamasını belirlemeyi amaçlamaktadır. BFS (Breadth-First Search) ve A* (A-Star) algoritmaları kullanılarak farklı senaryolar için rota planlaması yapılmaktadır.

2. Kullanılan Teknolojiler ve Kütüphaneler
Proje Python dili kullanılarak geliştirilmiştir ve aşağıdaki kütüphaneler kullanılmıştır:
heapq: Öncelikli kuyruk veri yapısı için kullanılmıştır.
collections: Kuyruk veri yapısını yönetmek için deque kullanılmıştır.
random: Rastgele senaryolar oluşturmak için kullanılmıştır.
time: Algoritmaların performansını ölçmek için kullanılmıştır.

3. Algoritmaların Çalışma Mantığı
BFS Algoritması
BFS, bir graf veya ağaç yapısında en kısa yolu bulmak için kullanılan bir arama algoritmasıdır. FIFO (First In First Out) mantığıyla çalışır ve başlangıç noktasından itibaren tüm komşuları sırayla ziyaret ederek hedef noktaya ulaşmaya çalışır.

Nasıl Çalışır?
Başlangıç noktası kuyruğa eklenir.
Kuyruğun ilk elemanı alınır ve ziyaret edilmemiş komşular kuyruğa eklenir.
Hedef noktaya ulaşıldığında algoritma sonlanır.

A* Algoritması
A* algoritması, en kısa yolu bulmak için kullanılan sezgisel bir arama algoritmasıdır. BFS'den farklı olarak, heuristic (sezgisel fonksiyon) kullanarak en uygun yolu tahmin etmeye çalışır.

Nasıl Çalışır?
Açık listeye (priority queue) başlangıç noktası eklenir.
En düşük maliyetli düğüm seçilir ve genişletilir.
Her komşu için yeni maliyet hesaplanır ve en düşük maliyetli yol tercih edilir.
Hedefe ulaşıldığında algoritma durur.

Neden Bu Algoritmaları Kullandık?
BFS, engellerin olmadığı ve her kenarın aynı ağırlıkta olduğu durumlarda en iyi sonucu verir.
A* algoritması, ağırlıklı graf yapılarında ve daha büyük ölçekli haritalarda optimal bir çözüm sunar.
İki algoritma karşılaştırılarak, metro simülasyonunun farklı senaryolarda nasıl çalıştığı gözlemlenmiştir.

Örnek Kullanım ve Test Sonuçları
Kullanım Örneği
Proje şu şekilde çalıştırılabilir:

python YigitAlpSen_MetroSimulation.py

Test Sonuçları
BFS algoritması, küçük ölçekli haritalarda hızlı ve etkili bir çözüm sunmuştur.
A* algoritması, büyük haritalarda BFS'ye göre daha az düğüm genişleterek daha verimli çalışmıştır.
Algoritmaların karşılaştırmalı performans analizi için time kütüphanesi kullanılmıştır.

5. Projeyi Geliştirme Fikirleri
Daha Gerçekçi Bir Simülasyon: Farklı metro hatlarını ve aktarma istasyonlarını içeren daha karmaşık bir harita eklenebilir.
GUI (Grafiksel Arayüz): Kullanıcıların metro haritasını görsel olarak takip edebileceği bir arayüz eklenebilir.
Gerçek Zamanlı Trafik Verisi: Simülasyona anlık trafik yoğunluğu ve gecikmeler eklenerek daha gerçekçi bir model oluşturulabilir.
Geniş Ölçekli Bir Simülasyon: Ülke genelindeki şehirler arası ulaşım araçlarının zaman ve yerleri girilerek daha geniş ölçekte bir simülasyon elde edilebilir.

