// product_slider.js
(function () {
  // Busca todos los sliders en la página y los inicializa uno a uno.
  const carousels = document.querySelectorAll('.custom-carousel');
  if (!carousels.length) return;

  carousels.forEach(initCarousel);

  function initCarousel(carousel) {
    const track = carousel.querySelector('.track');
    if (!track) return;

    const cards = Array.from(track.children);
    const prevBtn = carousel.querySelector('.nav.prev');
    const nextBtn = carousel.querySelector('.nav.next');
    const viewport = track.parentElement; // .viewport

    // Safety defaults
    let index = 0;
    let slideTimer = null;

    function sizes() {
      const style = getComputedStyle(track);
      const gap = parseFloat(style.getPropertyValue('gap')) || parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--gap')) || 28;
      const cardRect = cards[0].getBoundingClientRect();
      return { gap, cardWidth: cardRect.width, viewportWidth: viewport.getBoundingClientRect().width };
    }

    // Obtiene translateX actual (puede venir como matrix)
    function currentTranslate() {
      const st = getComputedStyle(track).transform;
      if (st && st !== 'none') {
        const m = st.match(/matrix.*\((.+)\)/);
        if (m) {
          const vals = m[1].split(',').map(Number);
          return vals[4] || 0; // translateX
        }
      }
      return 0;
    }

    // Centrar la tarjeta con índice `index`
    function update(animate = true) {
      if (!animate) track.style.transition = 'none';
      else track.style.transition = '';

      const { gap, cardWidth, viewportWidth } = sizes();
      index = Math.max(0, Math.min(index, cards.length - 1));
      const offset = index * (cardWidth + gap) - (viewportWidth - cardWidth) / 2;
      const tx = Math.max(0, offset);
      track.style.transform = `translateX(-${tx}px)`;

      cards.forEach((c, i) => c.classList.toggle('active', i === index));

      if (!animate) requestAnimationFrame(() => requestAnimationFrame(() => track.style.transition = ''));
    }

    // Navegación
    if (prevBtn) prevBtn.addEventListener('click', () => { index = Math.max(0, index - 1); update(); resetAuto(); });
    if (nextBtn) nextBtn.addEventListener('click', () => { index = Math.min(cards.length - 1, index + 1); update(); resetAuto(); });

    // Teclado
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { index = Math.max(0, index - 1); update(); resetAuto(); }
      if (e.key === 'ArrowRight') { index = Math.min(cards.length - 1, index + 1); update(); resetAuto(); }
    });

    // Resize -> recalcula sin animación
    window.addEventListener('resize', () => update(false));

    // Inicializa
    window.addEventListener('load', () => update(false));

    // ARRRASTE (pointer) / SWIPE
    let pointerDown = false;
    let startX = 0;
    let startTransform = 0;
    let dragDelta = 0;

    // Aseguramos touch-action para que no bloquee el swipe
    viewport.style.touchAction = viewport.style.touchAction || 'pan-y';

    viewport.addEventListener('pointerdown', (e) => {
      pointerDown = true;
      startX = e.clientX;
      startTransform = -currentTranslate(); // valor positivo usado anteriormente
      track.style.transition = 'none';
      viewport.setPointerCapture && viewport.setPointerCapture(e.pointerId);
    });

    viewport.addEventListener('pointermove', (e) => {
      if (!pointerDown) return;
      const dx = e.clientX - startX;
      dragDelta = dx;
      const tentative = startTransform - dx;
      track.style.transform = `translateX(-${Math.max(0, tentative)}px)`;
    });

    function settleAfterDrag() {
      const { gap, cardWidth, viewportWidth } = sizes();
      if (Math.abs(dragDelta) > cardWidth * 0.22) {
        // swipe suficientemente grande -> mover índice
        if (dragDelta < 0) index = Math.min(cards.length - 1, index + 1);
        else index = Math.max(0, index - 1);
      } else {
        // snap al índice más cercano
        const translateX = -currentTranslate();
        const approxIndex = Math.round((translateX + (viewportWidth - cardWidth) / 2) / (cardWidth + gap));
        index = Math.max(0, Math.min(cards.length - 1, approxIndex));
      }
      dragDelta = 0;
      update();
    }

    viewport.addEventListener('pointerup', (e) => {
      if (!pointerDown) return;
      pointerDown = false;
      try { viewport.releasePointerCapture && viewport.releasePointerCapture(e.pointerId); } catch (err) {}
      track.style.transition = '';
      settleAfterDrag();
      resetAuto();
    });

    viewport.addEventListener('pointercancel', () => {
      pointerDown = false;
      dragDelta = 0;
      update();
    });

    // Click en tarjeta -> centrarla
    cards.forEach((c, i) => {
      c.addEventListener('click', (ev) => {
        // evita centrar si el click es sobre un botón interno
        const tag = ev.target.tagName.toLowerCase();
        if (tag === 'button' || tag === 'a') return;
        if (i !== index) {
          index = i;
          update();
          resetAuto();
        }
      });
    });

    // Auto-play (opcional). Puedes comentar si no quieres autoplay.
    function startAuto() {
      stopAuto();
      slideTimer = setInterval(() => { index = Math.min(cards.length - 1, index + 1); if (index === cards.length - 1) index = 0; update(); }, 5000);
    }
    function stopAuto() { if (slideTimer) { clearInterval(slideTimer); slideTimer = null; } }
    function resetAuto() { stopAuto(); startAuto(); }

    // Start autoplay by default
    startAuto();

    // expose update for debugging
    carousel._sliderUpdate = update;
  }
})();
