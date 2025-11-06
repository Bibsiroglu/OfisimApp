from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Ilan, Musteri, Randevu, Sozlesme
from datetime import date, timedelta
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q 

# --- TEMEL VIEWS ---
@login_required
def ana_sayfa(request):
    """Dashboard'u gösterir: Özet veriler, bugünün/yaklaşan randevular, sözleşme bitişleri."""
    bugun = date.today()
    otuz_gun_sonra = bugun + timedelta(days=30)
    otuz_gun_once = timezone.now() - timedelta(days=30)
    
    # ------------------------------------------------------------------
    # Veri Çekme (Dashboard Metrikleri)
    # ------------------------------------------------------------------
    aktif_ilan_sayisi = Ilan.objects.filter(durum='Aktif').count()
    
    # PASİF İLAN SAYISI
    pasif_ilan_sayisi = Ilan.objects.exclude(durum='Aktif').count()
    
    # Müşteri Metrikleri
    toplam_musteri_sayisi = Musteri.objects.count()
    son_30_gun_yeni_musteri_sayisi = Musteri.objects.filter(
        kayit_tarihi__gte=otuz_gun_once
    ).count()
    
    # Randevu ve Sözleşme Takibi
    bugunun_randevulari = Randevu.objects.filter(
        tarih_saat__date=bugun, 
        durum='Planlandı'
    ).select_related('ilgili_musteri', 'ilan').order_by('tarih_saat')
    
    yaklasan_sozlesmeler = Sozlesme.objects.filter(
        bitis_tarihi__gte=bugun, 
        bitis_tarihi__lte=otuz_gun_sonra,
        durum='Aktif'
    ).select_related('sahip_musteri', 'karsi_taraf_musteri', 'ilgili_ilan').order_by('bitis_tarihi')
    
    context = {
        'aktif_ilan_sayisi': aktif_ilan_sayisi,
        'pasif_ilan_sayisi': pasif_ilan_sayisi,
        'toplam_musteri_sayisi': toplam_musteri_sayisi,
        'son_30_gun_yeni_musteri_sayisi': son_30_gun_yeni_musteri_sayisi,
        'bugunun_randevulari': bugunun_randevulari,
        'yaklasan_sozlesmeler': yaklasan_sozlesmeler,
    }
    
    return render(request, 'emlak/ana_sayfa.html', context)

@login_required
def ilan_listesi(request):
    """Aktif ilanların listesini gösterir."""
    aktif_ilanlar = Ilan.objects.filter(durum='Aktif').order_by('-fiyat')
    context = {'aktif_ilanlar': aktif_ilanlar}
    return render(request, 'emlak/ilan_listesi.html', context)

@login_required
def ilan_detay(request, pk):
    """Tek bir ilanın detayını gösterir."""
    ilan = get_object_or_404(Ilan, pk=pk)
    
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
    return render(request, 'emlak/ilan_detay.html', context)


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
    
    return render(request, 'emlak/musteri_detay.html', context)

@login_required
def musteri_listesi(request):
    """Tüm müşterileri listeler (En yeniden eskiye)."""
    
    tum_musteriler = Musteri.objects.all().order_by('-kayit_tarihi')
    
    context = {
        'tum_musteriler': tum_musteriler,
    }
    
    return render(request, 'emlak/musteri_listesi.html', context)

@login_required
def gelismis_arama(request):
    """Müşteri ve İlanlar için tek bir sayfada gelişmiş arama yapar."""
    
    sorgu = request.GET.get('q', None) 
    
    ilan_sonuclari = Ilan.objects.none()
    musteri_sonuclari = Musteri.objects.none()
    
    if sorgu:
        from django.db.models import Q 

        # --- İLAN ARAMA ---
        ilan_sonuclari = Ilan.objects.filter