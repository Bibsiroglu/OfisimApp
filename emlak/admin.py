from django.contrib import admin
from .models import Ilan, Musteri, Randevu, Sozlesme
from django.contrib import admin

class IlanAdmin(admin.ModelAdmin):

    list_display = (
        'ilan_no', 
        'baslik', 
        'mulk_sahibi', 
        'emlak_tipi', 
        'oda_sayisi', 
        'fiyat', 
        'isitma',
        'esyali',
        'durum'
    )

    list_filter = (
        'durum', 
        'emlak_tipi', 
        'isitma',
        'otopark',
        'mutfak',
        'il', 
        'ilce', 
        'krediye_uygun',
        'esyali'
    )
    search_fields = ('ilan_no', 'baslik', 'il', 'ilce', 'mahalle', 'mulk_sahibi__ad_soyad')

    autocomplete_fields = ('mulk_sahibi',)
    
    readonly_fields = ('son_guncelleme_tarihi',) 

    fieldsets = (
        ('TEMEL BİLGİLER VE KONUM', {
            'fields': (
                ('ilan_no', 'mulk_sahibi'), 
                'baslik', 
                'emlak_tipi', 
                ('il', 'ilce', 'mahalle', 'tam_adres'), 
                ('fiyat', 'durum')
            )
        }),
        ('FİZİKSEL VE TEKNİK ÖZELLİKLER', {
            'fields': (
                ('oda_sayisi', 'brut_alan', 'net_alan'), 
                ('bina_yasi', 'bulundugu_kat', 'kat_sayisi'),
                ('banyo_sayisi', 'mutfak'),
                ('isitma', 'otopark'),
                ('krediye_uygun', 'tapu_durumu')
            )
        }),
        ('TARİHÇE VE YÖNETİM', {
            'fields': ('kayit_tarihi', 'son_guncelleme_tarihi', 'yayindan_kaldirma_tarihi'),
            'classes': ('collapse',)
        }),
    )
    
# --- 2. MÜŞTERİ YÖNETİMİ ---
class MusteriAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'telefon', 'rol', 'email', 'kayit_tarihi')
    search_fields = ('ad_soyad', 'telefon', 'email')
    list_filter = ('rol', 'kayit_tarihi') 

# --- 3. RANDEVU YÖNETİMİ ---
class RandevuAdmin(admin.ModelAdmin):
    # list_display'e yeni metot 'musteri_telefonu' eklendi
    list_display = ('tarih_saat', 'ilgili_musteri', 'musteri_telefonu', 'ilan', 'durum')
    list_filter = ('durum', 'tarih_saat')
    autocomplete_fields = ('ilgili_musteri', 'ilan') 
    search_fields = ('ilgili_musteri__ad_soyad', 'ilan__ilan_no') 

    # YENİ METOT: Müşteri nesnesindeki telefon bilgisini çeker
    def musteri_telefonu(self, obj):
        # Randevu objesi (obj) üzerinden ilişkili müşterinin telefonunu çek
        return obj.ilgili_musteri.telefon
    
    musteri_telefonu.short_description = 'Müşteri Telefonu'

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