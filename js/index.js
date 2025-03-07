
// --------------------------------------------------------------- CONST ---------------------------------------------------------------
const btnScroll = document.getElementById("btn-scroll-top");

// --------------------------------------------------------------- EVENTS ---------------------------------------------------------------
btnScroll.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

// -------------------------------------------------------------- FUNCIONS --------------------------------------------------------------
// Funció per pujar de manera automàtica fins a dalt de la primera pàgina    
window.addEventListener("scroll", () => {
    const scrollHeight = document.documentElement.scrollHeight;
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const clientHeight = document.documentElement.clientHeight;

    if (scrollTop + clientHeight >= scrollHeight - 100) { 
        btnScroll.style.display = "block"; 
    } else { 
        btnScroll.style.display = "none"; 
    }
});
