from django.db import models

from emlak.models.musteri import Musteri

# --- SABİT SEÇENEK LİSTELERİ ---
DURUM_SECENEKLERI = [
    ('Aktif','Aktif'),
    ('Satıldı','Satıldı'),
    ('Kiralandı','Kiralandı'),
    ('Yayından Kaldırıldı', 'Yayından Kaldırıldı')
]

EMLAK_TIPI_SECENEKLERI = [
    # Satılık Mülkler
    ('Satilik Daire', 'Satılık Daire'),
    ('Satilik Villa', 'Satılık Villa'),
    ('Satilik Arsa', 'Satılık Arsa'),
    ('Satilik İşyeri', 'Satılık İşyeri'),
    
    # Kiralık Mülkler (YENİ EKLENENLER)
    ('Kiralik Daire', 'Kiralık Daire'),
    ('Kiralik Villa', 'Kiralık Villa'),
    ('Kiralik İşyeri', 'Kiralık İşyeri'),
]
BINA_YASI_SECENEKLERI = [
    ('0-5', '0-5 Yaşında'),
    ('6-10', '6-10 Yaşında'),
    ('11-15', '11-15 Yaşında'),
    ('16+', '16 Yaş ve Üzeri'),
]
TAPU_DURUMU_SECENEKLERI = [
    ('Kat Mülkiyeti', 'Kat Mülkiyeti'),
    ('Kat İrtifaklı', 'Kat İrtifaklı'),
    ('Hisseli', 'Hisseli'),
]

# --- İLAN MODELİ ---
class Ilan(models.Model):
    ilan_no = models.CharField(max_length=20, unique=True, verbose_name="İlan No", blank=True, null=True)
    baslik = models.CharField(max_length=150, verbose_name="İlan Başlığı")
    emlak_tipi = models.CharField(max_length=20, choices=EMLAK_TIPI_SECENEKLERI, verbose_name="Emlak Tipi")
    il = models.CharField(max_length=50)
    ilce = models.CharField(max_length=50)
    mahalle = models.CharField(max_length=100, verbose_name="Mahalle/Semt")
    oda_sayisi = models.CharField(max_length=10, verbose_name="Oda Sayısı")
    brut_alan = models.DecimalField(max_digits=6, decimal_places=1, verbose_name="Brüt Alan (m²)")
    net_alan = models.DecimalField(max_digits=6, decimal_places=1, verbose_name="Net Alan (m²)")
    bina_yasi = models.CharField(max_length=10, choices=BINA_YASI_SECENEKLERI, verbose_name="Bina Yaşı")
    bulundugu_kat = models.IntegerField(verbose_name="Bulunduğu Kat")
    kat_sayisi = models.IntegerField(verbose_name="Toplam Kat Sayısı")
    banyo_sayisi = models.IntegerField(default=1, verbose_name="Banyo Sayısı")
    mutfak = models.CharField(max_length=50, default='Ayrı', verbose_name="Mutfak Tipi")
    krediye_uygun = models.BooleanField(default=False, verbose_name="Krediye Uygun")
    site_icerisinde = models.BooleanField(default=False, verbose_name="Site İçerisinde")
    site_adi = models.CharField(max_length=100, blank=True, null=True)
    otopark = models.CharField(max_length=50, default='Yok', verbose_name="Otopark Tipi")
    asansor = models.BooleanField(default=False)
    balkon = models.BooleanField(default=False)
    esyali = models.BooleanField(default=False, verbose_name="Eşyalı")
    kullanım_durumu = models.CharField(max_length=20, default='Boş', verbose_name="Kullanım Durumu")
    takas = models.BooleanField(default=False)
    aidat_tl = models.IntegerField(null=True, blank=True, verbose_name="Aidat (TL)")
    fiyat = models.BigIntegerField()
    durum = models.CharField(max_length=25, default='Aktif', choices=DURUM_SECENEKLERI)
    tapu_durumu = models.CharField(max_length=30, choices=TAPU_DURUMU_SECENEKLERI, verbose_name="Tapu Durumu")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="İlana Koyulma Tarihi")
    son_guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    yayindan_kaldirma_tarihi = models.DateTimeField(null=True, blank=True, verbose_name="Yayından Kaldırma Tarihi") 
    mulk_sahibi = models.ForeignKey(
        Musteri,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ilanlarim',
        verbose_name='Mülk Sahibi'
    )
    
    def __str__(self):
        return f"ID:{self.id} | {self.il}/{self.ilce} {self.oda_sayisi} Satılık Daire ({self.fiyat:,.0f} TL)"

    class Meta:
        verbose_name = "İlan"
        verbose_name_plural = "İlanlar"