from django.db import models
from .ilan import Ilan # <<< BAĞIMLILIK
from .musteri import Musteri # <<< BAĞIMLILIK

# --- RANDEVU MODELİ ---
class Randevu(models.Model):
    DURUM_SECENEKLERI = [
        ('Planlandı', 'Planlandı'),
        ('Tamamlandı', 'Tamamlandı'),
        ('İptal Edildi', 'İptal Edildi'),
    ]
    
    tarih_saat = models.DateTimeField()
    # ForeignKey alanları diğer dosyalardaki modellere bakar
    ilgili_musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE, related_name='randevular')
    ilan = models.ForeignKey(Ilan, on_delete=models.SET_NULL, null=True, blank=True, related_name='randevular')
    notlar = models.TextField(blank=True, null=True)
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='Planlandı')
    
    def __str__(self):
        return f"Randevu: {self.tarih_saat.strftime('%Y-%m-%d %H:%M')} - Müşteri: {self.ilgili_musteri.ad_soyad}"

    class Meta:
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"