/* City Fête Events — site behaviour */

/* ---------- Homepage gallery ---------- */
(function () {
  const root = document.querySelector("[data-gallery]");
  if (!root) return;

  const slides = Array.from(root.querySelectorAll(".gallery-stage img"));
  const thumbs = Array.from(root.querySelectorAll(".gallery-thumbs button"));
  const caption = root.querySelector(".gallery-caption");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let index = 0;
  let timer = null;

  function show(next) {
    index = (next + slides.length) % slides.length;
    slides.forEach(function (img, i) {
      const active = i === index;
      img.classList.toggle("is-active", active);
      if (active && img.dataset.src) {
        img.src = img.dataset.src;
        img.removeAttribute("data-src");
      }
    });
    const upcoming = slides[(index + 1) % slides.length];
    if (upcoming && upcoming.dataset.src) {
      upcoming.src = upcoming.dataset.src;
      upcoming.removeAttribute("data-src");
    }
    thumbs.forEach(function (btn, i) {
      btn.setAttribute("aria-current", i === index ? "true" : "false");
    });
    caption.textContent = slides[index].dataset.credit || "";
  }

  function start() {
    if (reduceMotion) return;
    stop();
    timer = window.setInterval(function () { show(index + 1); }, 4500);
  }

  function stop() {
    if (timer) window.clearInterval(timer);
    timer = null;
  }

  root.querySelector(".prev").addEventListener("click", function () { show(index - 1); start(); });
  root.querySelector(".next").addEventListener("click", function () { show(index + 1); start(); });
  thumbs.forEach(function (btn, i) {
    btn.addEventListener("click", function () { show(i); start(); });
  });
  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  root.addEventListener("focusin", stop);
  root.addEventListener("focusout", start);

  show(0);
  start();
})();
