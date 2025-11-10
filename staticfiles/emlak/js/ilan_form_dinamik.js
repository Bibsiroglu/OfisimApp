// emlak/static/emlak/js/ilan_form_dinamik.js (Nihai ve Çözümlenmiş Sürüm)

(function ($) {
    $(document).ready(function () {

        var $emlakTipiSelect = $('#id_emlak_tipi');

        // --- 1. SADECE KİŞİSEL KONUT VE GEREKSİZ ALANLAR (İş Yeri ve Arsa seçilirse gizlenecekler) ---
        var kisiselKonutAlanlari = [
            '#id_banyo_sayisi',
            '#id_mutfak',
            '#id_balkon',
            '#id_esyali',
            '#id_brut_alan', // <<< BRÜT ALAN BURADA KESİN GİZLENİR
        ];

        // --- 2. ORTAK MÜLK ALANLARI (NET ALAN DAHİL, GÖRÜNÜR KALMALI) ---
        var ortakMulkAlanlari = [
            '#id_oda_sayisi',
            '#id_net_alan',       // <<< NET ALAN BURADA KALIR
            '#id_bina_yasi',
            '#id_bulundugu_kat',
            '#id_kat_sayisi',
            '#id_isitma',
            '#id_kullanım_durumu',
            '#id_aidat_tl'
        ];

        // --- 3. ARSA ÖZEL ALANLARI ---
        var arsaOzelAlanlari = [
            '#id_imar_durumu', '#id_ada_no', '#id_parsel_no', '#id_pafta_no', '#id_kaks_emsal', '#id_gabari'
        ];

        // Alanları Admin Formunda yer aldığı kapsayıcı DIV'leri buluyoruz
        var $kisiselKonutAlanlari = $(kisiselKonutAlanlari.join(', ')).closest('.form-row, fieldset');
        var $ortakMulkAlanlari = $(ortakMulkAlanlari.join(', ')).closest('.form-row, fieldset');
        var $arsaAlanlari = $(arsaOzelAlanlari.join(', ')).closest('.form-row, fieldset');


        function toggleFields(secilenTip) {

            var tip = secilenTip.toLowerCase();

            // Başlangıçta tüm alanları göster
            $kisiselKonutAlanlari.show();
            $ortakMulkAlanlari.show();
            $arsaAlanlari.show();


            if (tip.includes('arsa')) {
                // ARSA seçildi
                $kisiselKonutAlanlari.hide();
                $ortakMulkAlanlari.hide();
                $arsaAlanlari.show();

            } else if (tip.includes('isyeri')) {
                // İŞ YERİ seçildi
                $arsaAlanlari.hide();
                $kisiselKonutAlanlari.hide();   // BRÜT ALAN gizlenir
                $ortakMulkAlanlari.show();      // NET ALAN gösterilir

            } else {
                // DAİRE VEYA VİLLA (KONUT)
                $arsaAlanlari.hide();
                $kisiselKonutAlanlari.show();   // BRÜT ALAN gösterilir
                $ortakMulkAlanlari.show();
            }
        }

        // Sayfa yüklendiğinde bir kere çalıştır
        toggleFields($emlakTipiSelect.val());

        // Seçim değiştiğinde çalıştır
        $emlakTipiSelect.on('change', function () {
            toggleFields($(this).val());
        });
    });
})(django.jQuery);