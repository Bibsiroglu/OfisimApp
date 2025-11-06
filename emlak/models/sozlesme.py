# emlak/models/sozlesme.py
from django.db import models
from .ilan import Ilan 
from .musteri import Musteri 

# --- SÖZLEŞME MODELİ (SON HALİ) ---
class Sozlesme(models.Model):
    SOZLESME_TIPI_SECENEKLERI = [
        ('Satis', 'Satış Sözleşmesi'),
        ('Kira', 'Kira Sözleşmesi'),
        ('Hizmet', 'Hizmet Sözleşmesi'),
        ('Portfoy', 'Portföy Yetki Sözleşmesi'),
    ]

    DURUM_SECENEKLERI = [
        ('Aktif', 'Aktif'),
        ('Bitti', 'Süresi Bitti'),
        ('Iptal', 'İptal Edildi'),
    ]

    sozlesme_no = models.CharField(max_length=50, unique=True, verbose_name="Sözleşme No")
    sozlesme_tipi = models.CharField(max_length=20, choices=SOZLESME_TIPI_SECENEKLERI, verbose_name="Tip")
    
    # -----------------------------------------------------------
    # İLİŞKİLER (YENİ YAPILANDIRMA: İki Tarafı Tutma)
    # -----------------------------------------------------------
    
    # İlan: Hangi mülkle ilgili olduğu
    ilgili_ilan = models.ForeignKey(Ilan, on_delete=models.SET_NULL, null=True, blank=True, related_name='sozlesmeler', verbose_name="İlgili İlan")
    
    # Taraf 1: Mülk Sahibi/Kiraya Veren/Hizmeti Alan
    sahip_musteri = models.ForeignKey(
        Musteri, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='sahip_oldugu_sozlesmeler', 
        verbose_name="Mülk Sahibi/Ana Taraf"
    )
    
    # Taraf 2: Alıcı/Kiracı/Hizmeti Veren
    karsi_taraf_musteri = models.ForeignKey(
        Musteri, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='karsi_taraf_sozlesmeleri', 
        verbose_name="Alıcı/Kiracı/Karşı Taraf"
    )
    
    # -----------------------------------------------------------
    # FİNANSAL VE SÜRE BİLGİLERİ
    # -----------------------------------------------------------
    baslangic_tarihi = models.DateField(verbose_name="Başlangıç Tarihi")
    bitis_tarihi = models.DateField(null=True, blank=True, verbose_name="Bitiş Tarihi (Kira/Portföy)")
    
    # Finansal Alanlar
    komisyon_orani = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Komisyon Oranı (%)")
    komisyon_tutari = models.BigIntegerField(null=True, blank=True, verbose_name="Komisyon Tutarı (TL)")
    depozito_tutari = models.BigIntegerField(null=True, blank=True, verbose_name="Depozito Tutarı (TL)")
    
    # Genel Durum ve Belge Takibi
    durum = models.CharField(max_length=10, choices=DURUM_SECENEKLERI, default='Aktif')
    
    # dosya_yolu yerine FileField kullanıyoruz:
    dosya = models.FileField(
        upload_to='sozlesme_belgeleri/', # Yüklenecek dosyanın MEDIA_ROOT altındaki klasörü
        null=True, 
        blank=True, 
        verbose_name="Sözleşme Dosyası (PDF/DOCX)"
    )
    aciklama = models.TextField(blank=True, verbose_name="Ek Açıklamalar")
    
    def __str__(self):
        return f"{self.get_sozlesme_tipi_display()} - No: {self.sozlesme_no}"

    class Meta:
        verbose_name = "Sözleşme"
        verbose_name_plural = "Sözleşmeler"