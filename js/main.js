// Rez domom: zvýraznenie systému pri prechode myšou / fokuse (štítky, legenda, kategórie).
(function () {
  var rez = document.querySelector('.rez');
  if (rez) {
    var nastav = function (s) { rez.dataset.aktiv = s || ''; };
    rez.querySelectorAll('[data-sys]').forEach(function (el) {
      var s = el.getAttribute('data-sys');
      el.addEventListener('pointerenter', function () { nastav(s); });
      el.addEventListener('focusin', function () { nastav(s); });
    });
    rez.addEventListener('pointerleave', function () { nastav(''); });
    rez.addEventListener('focusout', function (e) { if (!rez.contains(e.relatedTarget)) nastav(''); });
  }
  // Menu na mobile
  var b = document.querySelector('.burger'), m = document.getElementById('menu');
  if (b && m) {
    b.addEventListener('click', function () {
      var o = m.classList.toggle('otvorene'); b.setAttribute('aria-expanded', o ? 'true' : 'false');
    });
    m.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { m.classList.remove('otvorene'); b.setAttribute('aria-expanded', 'false'); }); });
  }
  // Akciový pás: šípky
  var pas = document.querySelector('.pas');
  document.querySelectorAll('.sipka').forEach(function (s) {
    s.addEventListener('click', function () {
      var k = pas.querySelector('.produkt'); var w = k ? k.getBoundingClientRect().width + 16 : 280;
      pas.scrollBy({ left: w * 2 * Number(s.getAttribute('data-smer')), behavior: 'smooth' });
    });
  });
  // Formulár: v návrhu sa nič neodosiela
  document.querySelectorAll('form.formular').forEach(function (f) {
    var stav = f.querySelector('.formular-stav');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (f.querySelector('.past input').value) return;
      if (f.getAttribute('data-demo') === '1') { stav.textContent = 'Ukážka formulára: v návrhu sa nič neodosiela. Po spustení webu príde dopyt na obchod@pohodadomova.sk.'; return; }
      stav.textContent = 'Odosielam…';
      fetch(f.getAttribute('data-endpoint'), { method: 'POST', body: new FormData(f), headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); f.reset(); stav.textContent = 'Ďakujeme, dopyt sme prijali.'; })
        .catch(function () { stav.textContent = 'Odoslanie sa nepodarilo. Napíšte nám prosím e-mailom.'; });
    });
  });
})();
// Názov priloženého súboru
document.querySelectorAll('.subor input[type=file]').forEach(function (i) {
  i.addEventListener('change', function () { var m = i.parentNode.querySelector('.subor-meno'); if (m) m.textContent = i.files.length ? i.files[0].name : ''; });
});
