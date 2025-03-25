// --------------------------------------------------------------- CONST ---------------------------------------------------------------
const btnScroll = document.getElementById("btn-scroll-top");

// --------------------------------------------------------------- EVENTS ---------------------------------------------------------------
btnScroll.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

// -------------------------------------------------------------- FUNCIONS --------------------------------------------------------------
// Funció per mostrar el botó abans de la meitat de la pàgina
window.addEventListener("scroll", () => {
    const scrollHeight = document.documentElement.scrollHeight;
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;

    if (scrollTop >= scrollHeight * 0.3) {  // Ara apareixerà al 30% de scroll
        btnScroll.classList.add("mostrar");
    } else { 
        btnScroll.classList.remove("mostrar");
    }
});