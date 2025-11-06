from django.contrib import admin
from .models import Ilan, Musteri, Randevu, Sozlesme

# --- 1. İLAN YÖNETİMİ ---
class IlanAdmin(admin.ModelAdmin):
    # list_display'e 'mulk_sahibi' eklendi
    list_display = ('ilan_no', 'mulk_sahibi', 'il', 'ilce', 'oda_sayisi', 'fiyat', 'durum', 'kayit_tarihi')
    
    # list_filter ve search_fields'e mulk sahibi eklendi
    list_filter = ('durum', 'emlak_tipi', 'il', 'ilce', 'krediye_uygun', 'esyali')
    search_fields = ('ilan_no', 'il', 'ilce', 'mahalle', 'mulk_sahibi__ad_soyad') # Mülk sahibi adına göre arama

    # Otomatik arama kutusu ekleyelim
    autocomplete_fields = ('mulk_sahibi',)
    
# --- 2. MÜŞTERİ YÖNETİMİ ---
class MusteriAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'telefon', 'rol', 'email', 'kayit_tarihi')
    search_fields = ('ad_soyad', 'telefon', 'email')
    list_filter = ('rol', 'kayit_tarihi') 

# --- 3. RANDEVU YÖNETİMİ ---
class RandevuAdmin(admin.ModelAdmin):
    list_display = ('tarih_saat', 'ilgili_musteri', 'ilan', 'durum')
    list_filter = ('durum', 'tarih_saat')
    search_fields = ('ilgili_musteri__ad_soyad', 'ilan__ilan_no') 

# --- 4. SÖZLEŞME YÖNETİMİ ---
class SozlesmeAdmin(admin.ModelAdmin):
    list_display = ('sozlesme_no', 'sozlesme_tipi', 'sahip_musteri', 'karsi_taraf_musteri', 'komisyon_tutari', 'bitis_tarihi', 'durum')
    list_filter = ('sozlesme_tipi', 'durum', 'baslangic_tarihi')
    
    # 1. ARANABİLİR ALANLAR: Autocomplete'in ilanlar içinde hangi alanlara göre arama yapacağını söyler.
    search_fields = (
        'sozlesme_no', 
        'sahip_musteri__ad_soyad', 
        'karsi_taraf_musteri__ad_soyad',
        # İlan No, il ve ilçe alanlarına göre arama yapar. Bu KRİTİKTİR.
        'ilgili_ilan__ilan_no',  
        'ilgili_ilan__il',      
        'ilgili_ilan__ilce',      
    )
    
    # 2. OTOMATİK TAMAMLAMA: Bu alanda arama kutusunu etkinleştirir.
    autocomplete_fields = ('ilgili_ilan', 'sahip_musteri', 'karsi_taraf_musteri')
    
# KRİTİK KISIM: Modelleri Admin paneline kayıt etme
admin.site.register(Ilan, IlanAdmin)
admin.site.register(Musteri, MusteriAdmin)
admin.site.register(Randevu, RandevuAdmin)
admin.site.register(Sozlesme, SozlesmeAdmin)