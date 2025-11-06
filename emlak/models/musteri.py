# emlak/models/musteri.py

from django.db import models
from django.utils import timezone # olusturulma_tarihi için eklendi

# --- MÜŞTERİ MODELİ ---
class Musteri(models.Model):
    ROL_SECENEKLERI = [
        ('Satici', 'Satıcı / Mülk Sahibi'),
        ('Alici', 'Alıcı / Potansiyel Alıcı'),
        ('Kiraci', 'Kiracı'),
        ('Kiralayan', 'Kiralayan / Kiraya Veren'),
        ('Genel', 'Genel İlgilenen'),
    ]
    
    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    talep_ozeti = models.TextField(verbose_name="Talep Özeti")
    rol = models.CharField(max_length=20, choices=ROL_SECENEKLERI, default='Genel', verbose_name="Müşteri Rolü")
    kayit_tarihi = models.DateTimeField(auto_now_add=True)
    olusturulma_tarihi = models.DateTimeField(default=timezone.now, verbose_name="Oluşturulma Tarihi")
    
    # ----------------------------------------------------
    # KRİTİK DÜZELTME: Bu metodun sınıf içinde, girintili olması gerekir!
    # ----------------------------------------------------
    def __str__(self):
        # Admin panelinde ve ilişkilerde bu format görünür
        return f"{self.ad_soyad} ({self.get_rol_display()})"
    
    # ----------------------------------------------------
    # KRİTİK DÜZELTME: Meta sınıfı da sınıf içinde olmalıdır.
    # ----------------------------------------------------
    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"