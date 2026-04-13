//=====// Uhr //=================================================================================//
function updateDateTime() {
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

    document.getElementById('date').textContent = date;
    document.getElementById('time').textContent = time;
}

updateDateTime();
setInterval(updateDateTime, 1000);


//=====// Scroll-Fortschritt speichern //========================================================//
const box = document.getElementById("content-scroller");

box.addEventListener("scroll", () => {
    localStorage.setItem("scrollPos", box.scrollTop);
});

window.addEventListener("load", () => {
    const saved = localStorage.getItem("scrollPos");
    if (saved !== null) {
        box.scrollTop = parseInt(saved, 10);
    }
});


//=====// Ticker //==============================================================================//
document.addEventListener("DOMContentLoaded", () => {
    
    const initTickers = () => {
        document.querySelectorAll(".ticker-wrapper").forEach((wrapper) => {
            const ticker = wrapper.querySelector(".ticker");
            if (!ticker) return;

            // 1. Originaltext speichern, damit wir bei einem Resize nicht den generierten HTML-Code nochmal einlesen
            if (!ticker.dataset.originalText) {
                ticker.dataset.originalText = ticker.innerHTML.trim();
            }
            const text = ticker.dataset.originalText;

            // 2. Ein einzelnes Element temporär einsetzen, um dessen exakte Breite zu messen
            ticker.innerHTML = `<span class="ticker-item">${text}</span>`;
            const singleItem = ticker.querySelector(".ticker-item");
            
            const itemWidth = singleItem.getBoundingClientRect().width;
            const wrapperWidth = wrapper.getBoundingClientRect().width;

            // 3. Wie viele Elemente brauchen wir, um den sichtbaren Bereich 1x komplett zu füllen? (Mindestens 1)
            const itemsNeeded = Math.max(1, Math.ceil(wrapperWidth / itemWidth));

            // 4. Verdoppeln, damit der CSS Transform-Trick (translateX(-50%)) mathematisch nahtlos aufgeht
            const totalItems = itemsNeeded * 2;

            // 5. HTML mit der berechneten Anzahl aufbauen
            let newHTML = '';
            for (let i = 0; i < totalItems; i++) {
                // Screenreader sollen den Text nicht tausendmal vorlesen, daher verstecken wir Duplikate
                const aria = i >= itemsNeeded ? ' aria-hidden="true"' : '';
                newHTML += `<span class="ticker-item"${aria}>${text}</span>`;
            }
            
            ticker.innerHTML = newHTML;

            // 6. Animations-Geschwindigkeit berechnen
            // Die Distanz für 50% der Animation ist exakt (itemsNeeded * itemWidth)
            const distance = itemsNeeded * itemWidth;
            const speed = 120; // Pixel pro Sekunde
            ticker.style.setProperty("--duration", `${Math.max(distance / speed, 5)}s`);
        });
    };

    // Beim Start einmal ausführen
    initTickers();
    
    // Neu berechnen, falls sich die Fenstergröße ändert (Debounced, um Performance zu sparen)
    window.addEventListener('resize', () => {
        clearTimeout(window.tickerResizeTimer);
        window.tickerResizeTimer = setTimeout(initTickers, 200);
    });
});