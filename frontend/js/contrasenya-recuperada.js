// --------------------------- OBJECTES --------------------------- 
const btnTornar = document.getElementById("tornar");
// console.log(btnTornar)

// --------------------------- EVENTS --------------------------- 
btnTornar.addEventListener("click", tornarIndex);

// --------------------------- FUNCIONS --------------------------- 
function tornarIndex() {
    window.location.href = "../pages/contrasenya-recuperada.html";
    console.log("Tornant al inici...")
}
