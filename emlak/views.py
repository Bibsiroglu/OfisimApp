from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Ilan, Musteri, Randevu, Sozlesme
from datetime import date, timedelta
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q 
from django.db.models import Sum 
import json 
import operator

# --- TEMEL VIEWS ---

@login_required
def ana_sayfa(request):
    """Dashboard'u gösterir: Özet veriler, bugünün/yaklaşan randevular, sözleşme bitişleri."""
    
    bugun = date.today()
    simdi = timezone.now()
    
    otuz_gun_sonra = bugun + timedelta(days=30)
    otuz_gun_once = simdi - timedelta(days=30)
    yedi_gun_once = simdi - timedelta(days=7)
    
    # Model seçeneklerini alıyoruz (HTML filtreleri için)
    emlak_tipi_secenekleri = Ilan._meta.get_field('emlak_tipi').choices
    oda_sayisi_secenekleri = Ilan._meta.get_field('oda_sayisi').choices 
    
    # ------------------------------------------------------------------
    # Veri Çekme (Dashboard Metrikleri)
    # ------------------------------------------------------------------
    
    aktif_ilan_sayisi = Ilan.objects.filter(durum='Aktif').count()
    pasif_ilan_sayisi = Ilan.objects.exclude(durum='Aktif').count()
    toplam_musteri_sayisi = Musteri.objects.count()
    son_30_gun_yeni_musteri_sayisi = Musteri.objects.filter(kayit_tarihi__gte=otuz_gun_once).count()
    
    pasif_durum_sayilari = Ilan.objects.filter(
        durum__in=['Satildi', 'Kiralandi', 'Yayindan_kaldirildi']
    ).values('durum').annotate(sayi=Count('durum')).order_by('durum')

    durum_cevirisi = dict(Ilan._meta.get_field('durum').choices)

    pasif_durum_basliklari = [durum_cevirisi.get(item['durum'], item['durum']) for item in pasif_durum_sayilari]
    pasif_durum_verileri = [item['sayi'] for item in pasif_durum_sayilari]

    aktif_tip_sayilari = Ilan.objects.filter(durum='Aktif').values('emlak_tipi').annotate(sayi=Count('emlak_tipi')).order_by('-sayi')

    # Emlak tipi seçeneklerinden Türkçe isimleri almak için sözlük oluşturulur
    tip_cevirisi = dict(Ilan._meta.get_field('emlak_tipi').choices)

    aktif_tip_basliklari = []
    aktif_tip_verileri = []

    for item in aktif_tip_sayilari:
        turkce_baslik = tip_cevirisi.get(item['emlak_tipi'], item['emlak_tipi'])
        aktif_tip_basliklari.append(turkce_baslik)
        aktif_tip_verileri.append(item['sayi'])

    # JSON formatına çevirme
    aktif_tip_basliklari_json = json.dumps(aktif_tip_basliklari)
    aktif_tip_verileri_json = json.dumps(aktif_tip_verileri)

    # Randevu ve Sözleşme Takibi
    bugunun_randevulari = Randevu.objects.filter(
        tarih_saat__date=bugun, 
        durum='Planlandı'
    ).select_related('ilgili_musteri', 'ilan').order_by('tarih_saat')

    son_bir_hafta_randevulari = Randevu.objects.filter(
        tarih_saat__range=(yedi_gun_once, simdi)
    ).select_related('ilgili_musteri', 'ilan').order_by('-tarih_saat')
    
    yaklasan_sozlesmeler = Sozlesme.objects.filter(
        bitis_tarihi__gte=bugun, 
        bitis_tarihi__lte=otuz_gun_sonra,
        durum='Aktif'
    ).select_related('sahip_musteri', 'karsi_taraf_musteri', 'ilgili_ilan').order_by('bitis_tarihi')
    
    # GRAFİK VERİSİ HAZIRLAMA (Randevu Sıklığı)
    ilan_randevu_performansi = Randevu.objects.filter(
        ilan__isnull=False, ilan__durum='Aktif', 
    ).values('ilan').annotate(randevu_sayisi=Count('ilan')).order_by('-randevu_sayisi')[:10]

    ilan_basliklari = []
    ilan_verileri = []
    for item in ilan_randevu_performansi:
        try:
            ilan_obj = Ilan.objects.get(pk=item['ilan'])
            ilan_basliklari.append(ilan_obj.baslik if ilan_obj.baslik else f"No: {ilan_obj.ilan_no}") 
        except Ilan.DoesNotExist:
             ilan_basliklari.append("Bilinmeyen İlan")
             
        ilan_verileri.append(item['randevu_sayisi'])
    
    ilan_grafigi_basliklari_json = json.dumps(ilan_basliklari)
    ilan_grafigi_verileri_json = json.dumps(ilan_verileri)

    # ------------------------------------------------------------------
    # CONTEXT TANIMLAMASI (Tüm veriler burada birleştirilir)
    # ------------------------------------------------------------------
    context = {
        'pasif_durum_basliklari_json': json.dumps(pasif_durum_basliklari),
        'pasif_durum_verileri_json': json.dumps(pasif_durum_verileri),
        'aktif_tip_basliklari_json': aktif_tip_basliklari_json,
        'aktif_tip_verileri_json': aktif_tip_verileri_json,
        'aktif_ilan_sayisi': aktif_ilan_sayisi,
        'pasif_ilan_sayisi': pasif_ilan_sayisi,
        'toplam_musteri_sayisi': toplam_musteri_sayisi,
        'son_30_gun_yeni_musteri_sayisi': son_30_gun_yeni_musteri_sayisi,
        'bugunun_randevulari': bugunun_randevulari,
        'yaklasan_sozlesmeler': yaklasan_sozlesmeler,
        'son_bir_hafta_randevulari': son_bir_hafta_randevulari,
        'ilan_grafigi_basliklari_json': ilan_grafigi_basliklari_json,
        'ilan_grafigi_verileri_json': ilan_grafigi_verileri_json,
        'emlak_tipi_secenekleri': emlak_tipi_secenekleri, 
        'oda_sayisi_secenekleri': oda_sayisi_secenekleri,
    }
    
    return render(request, 'ana_sayfa.html', context)


@login_required
def ilan_listesi(request):
    """Tüm (Aktif/Pasif) ilanları listeler ve GET filtrelerini uygular."""
    
    tum_ilanlar = Ilan.objects.all().select_related('mulk_sahibi').order_by('-kayit_tarihi')
    
    # GET parametrelerini alma
    durum_filtresi = request.GET.get('durum')
    il_filtresi = request.GET.get('il')
    oda_filtresi = request.GET.get('oda_sayisi')
    tip_filtresi = request.GET.get('emlak_tipi')
    
    # 3. FİLTRELEME MANTIĞI
    if durum_filtresi and durum_filtresi != '':
        tum_ilanlar = tum_ilanlar.filter(durum=durum_filtresi)
    
    if il_filtresi and il_filtresi != '':
        tum_ilanlar = tum_ilanlar.filter(il__icontains=il_filtresi)
    
    if oda_filtresi and oda_filtresi != 'HEPSI' and oda_filtresi != '':
        tum_ilanlar = tum_ilanlar.filter(oda_sayisi=oda_filtresi)
    
    if tip_filtresi and tip_filtresi != '':
        tum_ilanlar = tum_ilanlar.filter(emlak_tipi=tip_filtresi)
        
    context = {'tum_ilanlar': tum_ilanlar}
    
    return render(request, 'ilan_listesi.html', context)

@login_required
def ilan_detay(request, pk):
    """Tek bir ilanın detayını gösterir."""
    ilan = get_object_or_404(Ilan, pk=pk)
    
    # İlişkili randevuları ve sözleşmeleri çekelim
    ilgili_randevular = ilan.randevular.all().order_by('-tarih_saat')
    ilgili_sozlesmeler = ilan.sozlesmeler.all().order_by('-baslangic_tarihi')
    
    # İLGİLENEN MÜŞTERİLERİ ÇEKME MANTIĞI
    ilgilenen_musteri_idler = ilgili_randevular.values_list('ilgili_musteri__id', flat=True).distinct()
    ilgilenen_musteriler = Musteri.objects.filter(id__in=ilgilenen_musteri_idler)
    
    context = {
        'ilan': ilan,
        'ilgili_randevular': ilgili_randevular,
        'ilgili_sozlesmeler': ilgili_sozlesmeler,
        'ilgilenen_musteriler': ilgilenen_musteriler,
    }
    # NOT: Dosya taşıma işlemi sonrası path'i sadece dosya adı olarak kullanıyoruz.
    return render(request, 'ilan_detay.html', context)

@login_required
def musteri_listesi(request):
    """Tüm müşterileri listeler (En yeniden eskiye)."""
    
    # Tüm müşterileri çeker ve sıralar
    tum_musteriler = Musteri.objects.all().order_by('-kayit_tarihi')
    
    context = {
        'tum_musteriler': tum_musteriler,
    }
    
    # Dosya taşıma işlemi sonrası path'i sadece dosya adı olarak kullanıyoruz.
    return render(request, 'musteri_listesi.html', context)

@login_required
def musteri_detay(request, pk):
    """Müşteriye ait tüm geçmiş işlemleri (Sözleşme, Randevu, İlanlar) gösterir."""
    musteri = get_object_or_404(Musteri, pk=pk)
    
    # Sözleşmeler:
    sahip_sozlesmeler = Sozlesme.objects.filter(sahip_musteri=musteri)
    karsi_sozlesmeler = Sozlesme.objects.filter(karsi_taraf_musteri=musteri)
    musteri_sozlesmeleri = (sahip_sozlesmeler | karsi_sozlesmeler).distinct().order_by('-baslangic_tarihi')
    
    # Randevular:
    musteri_randevulari = Randevu.objects.filter(ilgili_musteri=musteri).select_related('ilan').order_by('-tarih_saat')
    
    # İlgilenilen İlanlar (Randevu veya Sözleşme ile ilişkili olanlar)
    randevu_ilan_idleri = musteri_randevulari.values_list('ilan__id', flat=True).distinct()
    sozlesme_ilan_idleri = musteri_sozlesmeleri.values_list('ilgili_ilan__id', flat=True).distinct()
    
    tum_ilgili_ilan_idler = set(list(randevu_ilan_idleri) + list(sozlesme_ilan_idleri))
    ilgilenilen_ilanlar = Ilan.objects.filter(pk__in=tum_ilgili_ilan_idler).distinct()

    context = {
        'musteri': musteri,
        'randevular': musteri_randevulari,
        'sozlesmeler': musteri_sozlesmeleri,
        'ilgilenilen_ilanlar': ilgilenilen_ilanlar,
    }
    
    return render(request, 'musteri_detay.html', context)

@login_required
def gelismis_arama(request):
    """Müşteri ve İlanlar için tek bir sayfada gelişmiş arama yapar."""
    
    sorgu = request.GET.get('q', None) 
    
    ilan_sonuclari = Ilan.objects.none()
    musteri_sonuclari = Musteri.objects.none()
    
    if sorgu:
        from django.db.models import Q 

        # --- İLAN ARAMA ---
        ilan_sonuclari = Ilan.objects.filter(
            Q(ilan_no__icontains=sorgu) | 
            Q(il__icontains=sorgu) | 
            Q(ilce__icontains=sorgu) 
        ).distinct()
        
        # --- MÜŞTERİ ARAMA ---
        musteri_sonuclari = Musteri.objects.filter(
            Q(ad_soyad__icontains=sorgu) | 
            Q(telefon__icontains=sorgu) | 
            Q(talep_ozeti__icontains=sorgu) 
        ).distinct()

    context = {
        'sorgu': sorgu,
        'ilan_sonuclari': ilan_sonuclari,
        'musteri_sonuclari': musteri_sonuclari,
    }
    
    # Not: Dosya taşıma işlemi sonrası path'i sadece dosya adı olarak kullanıyoruz.
    return render(request, 'gelismis_arama.html', context)
# ... (Diğer view fonksiyonları aynı kalır: ilan_detay, musteri_detay, sozlesme_listesi, gelismis_arama)
# (Bu fonksiyonların da kodunuzun devamında eksiksiz olduğundan emin olun.)