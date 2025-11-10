
(function ($) {
    $(document).ready(function () {

        var $emlakTipiSelect = $('#id_emlak_tipi');

        // 1. KONUT / MÜLK İÇİ ALANLAR (Arsa seçilirse gizlenecekler)
        var konutMulkAlanlari = [
            '#id_oda_sayisi',
            '#id_bina_yasi',
            '#id_bulundugu_kat',
            '#id_kat_sayisi',
            '#id_banyo_sayisi',
            '#id_mutfak',
            '#id_isitma',              // Yeni eklediğiniz Isıtma
            '#id_kullanım_durumu',
            '#id_balkon',
            '#id_esyali'
        ];

        // 2. ARSA ÖZEL ALANLARI (Konut/İşyeri seçilirse gizlenecekler)
        var arsaOzelAlanlari = [
            '#id_imar_durumu',
            '#id_ada_no',
            '#id_parsel_no',
            '#id_pafta_no',
            '#id_kaks_emsal',
            '#id_gabari'
        ];

        // Alanları form-row kapsayıcısı ile bulur
        var $konutAlanlari = $(konutMulkAlanlari.join(', ')).closest('.form-row, fieldset');
        var $arsaAlanlari = $(arsaOzelAlanlari.join(', ')).closest('.form-row, fieldset');


        function toggleFields(secilenTip) {

            $konutAlanlari.show();
            $arsaAlanlari.show();

            // Seçilen tipin DB'deki kısa kodunu kontrol ediyoruz
            var tip = secilenTip.toLowerCase();

            if (tip.includes('arsa')) {
                // ARSA seçildi: Konut özelliklerini gizle, Arsa özelliklerini göster
                $konutAlanlari.hide();
                $arsaAlanlari.show();

            } else if (tip.includes('daire') || tip.includes('villa') || tip.includes('isyeri')) {
                // KONUT veya İŞYERİ seçildi: Arsa özelliklerini gizle, Konut/Mülk özelliklerini göster
                $arsaAlanlari.hide();
                $konutAlanlari.show();

            } else {
                // Diğer durumlarda hepsini göster (Güvenlik için)
                $konutAlanlari.show();
                $arsaAlanlari.show();
            }
        }

        // 1. Sayfa yüklendiğinde bir kere çalıştır (Düzenleme ekranı için KRİTİK!)
        toggleFields($emlakTipiSelect.val());

        // 2. Seçim değiştiğinde çalıştır
        $emlakTipiSelect.on('change', function () {
            toggleFields($(this).val());
        });
    });
})(django.jQuery);