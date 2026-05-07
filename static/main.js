const config = window.cfg || {};

// ===== Uhr ==========================================================
function updateDateTime() {
    const dateEl = document.getElementById('date');
    const timeEl = document.getElementById('time');
    if (!dateEl || !timeEl) return;

    const now = new Date();

    const date = now.toLocaleDateString('de-DE', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    const time = now.toLocaleTimeString('de-DE', {
        hour: '2-digit',
        minute: '2-digit'
    });

    dateEl.textContent = date;
    timeEl.textContent = time;
}

function startClock() {
    updateDateTime();
    setInterval(updateDateTime, 10000);
}

// ===== Auto-Scroller ===============================================
function initAutoScroller(root = document) {
    const container = root.querySelector('#content-scroller');
    if (!container) return;

    if (container.dataset.autoscrollerInit === '1') return;
    container.dataset.autoscrollerInit = '1';

    if (config.dev) return;

    const scrollspeed = config.content?.scrollspeed ?? 1;
    let isScrolling = true;

    setInterval(() => {
        if (!isScrolling) return;

        container.scrollTop += 1;

        if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
            isScrolling = false;

            setTimeout(() => {
                container.scrollTop = 0;

                setTimeout(() => {
                    isScrolling = true;
                }, 3000);
            }, 3000);
        }
    }, scrollspeed * 1000);
}

// ===== Ticker =======================================================
function initTickers(root = document) {
    root.querySelectorAll(".ticker-wrapper").forEach((wrapper) => {
        if (wrapper.dataset.tickerInit === '1') return;
        wrapper.dataset.tickerInit = '1';

        const ticker = wrapper.querySelector(".ticker");
        if (!ticker) return;

        if (!ticker.dataset.originalText) {
            ticker.dataset.originalText = ticker.innerHTML.trim();
        }

        const text = ticker.dataset.originalText;

        ticker.innerHTML = `<span class="ticker-item">${text}</span>`;
        const singleItem = ticker.querySelector(".ticker-item");
        if (!singleItem) return;

        const itemWidth = singleItem.getBoundingClientRect().width;
        const wrapperWidth = wrapper.getBoundingClientRect().width;
        if (!itemWidth || !wrapperWidth) return;

        const itemsNeeded = Math.max(1, Math.ceil(wrapperWidth / itemWidth));
        const totalItems = itemsNeeded * 2;

        let newHTML = '';
        for (let i = 0; i < totalItems; i++) {
            const aria = i >= itemsNeeded ? ' aria-hidden="true"' : '';
            newHTML += `<span class="ticker-item"${aria}>${text}</span>`;
        }

        ticker.innerHTML = newHTML;

        const distance = itemsNeeded * itemWidth;
        const speed = 120;
        ticker.style.setProperty("--duration", `${Math.max(distance / speed, 5)}s`);
    });
}

// ===== Gemeinsamer Initializer ======================================
function initPage(root = document) {
    initAutoScroller(root);
    initTickers(root);
}

document.addEventListener("DOMContentLoaded", () => {
    startClock();
    initPage(document);
});

// HTMX: nach jedem nachgeladenen Fragment erneut initialisieren
document.body.addEventListener("htmx:load", (evt) => {
    initPage(evt.detail.elt);
});