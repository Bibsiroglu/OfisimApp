// emlak/static/emlak/js/ilan_form_dinamik.js (İş Yeri ve Konut Optimizasyonu)

(function ($) {
    $(document).ready(function () {

        var $emlakTipiSelect = $('#id_emlak_tipi');

        // --- 1. SADECE KİŞİSEL KONUT ALANLARI (İş Yeri seçilirse gizlenecekler) ---
        var kisiselKonutAlanlari = [
            '#id_banyo_sayisi',
            '#id_mutfak',
            '#id_balkon',
            '#id_esyali',
        ];

        // --- 2. ORTAK MÜLK ALANLARI (Arsa dışındaki her şeyde görünür) ---
        var ortakMulkAlanlari = [
            '#id_oda_sayisi',
            '#id_brut_alan',
            '#id_net_alan',
            '#id_bina_yasi',
            '#id_bulundugu_kat',
            '#id_kat_sayisi',
            '#id_isitma',
            '#id_kullanım_durumu',
            '#id_aidat_tl'
        ];

        // --- 3. ARSA ÖZEL ALANLARI (Konut/İşyeri seçilirse gizlenecekler) ---
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

            // ----------------------------------------------------
            // GİZLEME MANTIĞI
            // ----------------------------------------------------

            if (tip.includes('arsa')) {
                // ARSA seçildi: Tüm Konut/İşyeri alanlarını gizle
                $kisiselKonutAlanlari.hide();
                $ortakMulkAlanlari.hide();
                $arsaAlanlari.show();

            } else if (tip.includes('isyeri')) {
                // İŞ YERİ seçildi:
                $arsaAlanlari.hide(); // Arsa alanları gizlenir
                $kisiselKonutAlanlari.hide(); // Banyo, Mutfak, Balkon, Eşyalı gizlenir
                $ortakMulkAlanlari.show(); // Oda, Isıtma, Bina Yaşı KALIR

            } else {
                // DAİRE VEYA VİLLA (KONUT): Sadece Arsa gizlenir, diğer her şey gösterilir
                $arsaAlanlari.hide();
                $kisiselKonutAlanlari.show();
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