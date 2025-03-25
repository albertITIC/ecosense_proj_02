// --------------------------- OBJECTES --------------------------- 
const btnTornar = document.getElementById("tornar");

// --------------------------- EVENTS --------------------------- 
btnTornar.addEventListener("click", tornarIndex);

// --------------------------- FUNCIONS --------------------------- 
function tornarIndex() {
    window.location.href = "./index.html"; // Redirige a index.html
}
