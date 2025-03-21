from collections import defaultdict, deque
import heapq
from itertools import count
from typing import Dict, List, Tuple, Optional


class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

    def __hash__(self):
        return hash(self.idx)

    def __eq__(self, other):
        return isinstance(other, Istasyon) and self.idx == other.idx


class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        # Dikkat: 'id' yerine 'idx' kontrolü yapıyoruz
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur.
        Eğer rota bulunamazsa None, bulunursa Istasyon listesi döndürür.
        Test senaryolarımızdaki istasyon isimlerine (örneğin, Kızılay, Ulus, Demetevler, OSB vs.) göre çalışacaktır.
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        queue = deque([(baslangic, [baslangic])])
        visited = set([baslangic])

        while queue:
            current, path = queue.popleft()
            if current == hedef:
                return path
            for neighbor, _ in current.komsular:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def heuristic(self, a: Istasyon, b: Istasyon) -> int:
        """Heuristik fonksiyon: Test senaryolarımızdaki istasyon isimlerine göre örnek tahmini süre değerleri.
        Bu değerler örnektir; gerçek veriler girilebilir.
        """
        heuristic_map = {
            "Kızılay": {"Ulus": 4, "Demetevler": 6, "OSB": 10, "AŞTİ": 7, "Sıhhiye": 3, "Gar": 8, "Batıkent": 12,
                        "Keçiören": 15},
            "Ulus": {"Kızılay": 4, "Demetevler": 5, "OSB": 9, "AŞTİ": 8, "Sıhhiye": 4, "Gar": 7, "Batıkent": 11,
                     "Keçiören": 14},
            "Demetevler": {"Kızılay": 6, "Ulus": 5, "OSB": 8, "AŞTİ": 6, "Sıhhiye": 4, "Gar": 5, "Batıkent": 10,
                           "Keçiören": 9},
            "OSB": {"Kızılay": 10, "Ulus": 9, "Demetevler": 8, "AŞTİ": 12, "Sıhhiye": 10, "Gar": 6, "Batıkent": 15,
                    "Keçiören": 12},
            "AŞTİ": {"Kızılay": 7, "Ulus": 8, "Demetevler": 6, "OSB": 12, "Sıhhiye": 4, "Gar": 7, "Batıkent": 10,
                     "Keçiören": 13},
            "Sıhhiye": {"Kızılay": 3, "Ulus": 4, "Demetevler": 4, "OSB": 10, "AŞTİ": 4, "Gar": 5, "Batıkent": 8,
                        "Keçiören": 11},
            "Gar": {"Kızılay": 8, "Ulus": 7, "Demetevler": 5, "OSB": 6, "AŞTİ": 7, "Sıhhiye": 5, "Batıkent": 9,
                    "Keçiören": 4},
            "Batıkent": {"Kızılay": 12, "Ulus": 11, "Demetevler": 10, "OSB": 15, "AŞTİ": 10, "Sıhhiye": 8, "Gar": 9,
                         "Keçiören": 5},
            "Keçiören": {"Kızılay": 15, "Ulus": 14, "Demetevler": 9, "OSB": 12, "AŞTİ": 13, "Sıhhiye": 11, "Gar": 4,
                         "Batıkent": 5}
        }
        return heuristic_map.get(a.ad, {}).get(b.ad, 0)

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı ve toplam süreyi bulur.
        Eğer rota bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) döndürür.
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        open_set = []
        tie_breaker = count()  # Benzersiz sayaç (tie-breaker)
        # Heap'e (f_score, tie_breaker, current, path, g_score) şeklinde eleman ekliyoruz
        heapq.heappush(open_set, (0, next(tie_breaker), baslangic, [baslangic], 0))
        visited = {baslangic: 0}

        while open_set:
            f, _, current, path, g = heapq.heappop(open_set)
            if current == hedef:
                return path, g
            for neighbor, cost in current.komsular:
                tentative_g = g + cost
                if neighbor not in visited or tentative_g < visited[neighbor]:
                    visited[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, hedef)
                    heapq.heappush(open_set, (f_score, next(tie_breaker), neighbor, path + [neighbor], tentative_g))
        return None


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()

    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")

    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")

    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")

    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB

    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar

    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören

    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma

    # Test senaryoları
    print("\n=== Test Senaryoları ===")

    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
