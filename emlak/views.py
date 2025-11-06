from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Ilan, Musteri, Randevu, Sozlesme # Modelleri toplu import ediyoruz
from datetime import date, timedelta
from django.db.models import Count

# --- TEMEL VIEWS ---
@login_required
def ana_sayfa(request):
    """Dashboard'u gösterir: Özet veriler, bugünün/yaklaşan randevular, sözleşme bitişleri."""
    bugun = date.today()
    otuz_gun_sonra = bugun + timedelta(days=30)
    
    # Veri Çekme
    aktif_ilan_sayisi = Ilan.objects.filter(durum='Aktif').count()
    
    bugunun_randevulari = Randevu.objects.filter(
        tarih_saat__date=bugun, 
        durum='Planlandı'
    ).select_related('ilgili_musteri', 'ilan').order_by('tarih_saat') # select_related performansı artırır
    
    yaklasan_sozlesmeler = Sozlesme.objects.filter(
        bitis_tarihi__gte=bugun, 
        bitis_tarihi__lte=otuz_gun_sonra,
        durum='Aktif'
    ).select_related('sahip_musteri', 'karsi_taraf_musteri', 'ilgili_ilan').order_by('bitis_tarihi')
    
    context = {
        'aktif_ilan_sayisi': aktif_ilan_sayisi,
        'bugunun_randevulari': bugunun_randevulari,
        'yaklasan_sozlesmeler': yaklasan_sozlesmeler,
        # İlan listesi ve detay view'leri için gerekli olanlar aşağıda tanımlanmıştır
    }
    
    return render(request, 'emlak/ana_sayfa.html', context)

@login_required
def ilan_listesi(request):
    """Aktif ilanların listesini gösterir."""
    # Henüz HTML kodunu yazmadık, sadece temel mantık
    aktif_ilanlar = Ilan.objects.filter(durum='Aktif').order_by('-fiyat')
    context = {'aktif_ilanlar': aktif_ilanlar}
    return render(request, 'emlak/ilan_listesi.html', context)

@login_required
def ilan_detay(request, pk):
    """Tek bir ilanın detayını gösterir."""
    ilan = get_object_or_404(Ilan, pk=pk)
    # İlişkili randevuları ve sözleşmeleri çekelim
    ilgili_randevular = ilan.randevular.all().order_by('-tarih_saat')
    ilgili_sozlesmeler = ilan.sozlesmeler.all().order_by('-baslangic_tarihi')
    
    context = {
        'ilan': ilan,
        'ilgili_randevular': ilgili_randevular,
        'ilgili_sozlesmeler': ilgili_sozlesmeler,
    }
    return render(request, 'emlak/ilan_detay.html', context)


# YENİ EKLENDİ: Müşteri Detay (CRM Geçmişi)
@login_required
def musteri_detay(request, pk):
    """Müşteriye ait tüm geçmiş işlemleri (Sözleşme, Randevu, İlanlar) gösterir."""
    musteri = get_object_or_404(Musteri, pk=pk)
    
    # Müşterinin Musteri modelindeki property'leri (randevu_gecmisi, sozlesme_gecmisi vb.) kullanarak kolayca çekiyoruz.
    # NOT: Bu property'ler Musteri modelinizde tanımlı olmalıdır.
    
    # Sözleşmeler: Musteri modelindeki related_name='yaptigi_sozlesmeler' kullanılır
    musteri_sozlesmeleri = musteri.yaptigi_sozlesmeler.all().select_related('ilgili_ilan').order_by('-baslangic_tarihi')
    
    # Randevular: Musteri modelindeki related_name='randevular' kullanılır
    musteri_randevulari = musteri.randevular.all().select_related('ilan').order_by('-tarih_saat')
    
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
    
    # Müşterileri kayıt tarihine göre tersten sırala
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
        # Bu kısım sadece arama yapıldığında çalışır
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
    
    return render(request, 'emlak/gelismis_arama.html', context)