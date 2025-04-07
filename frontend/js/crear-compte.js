// --------------------------- OBJECTES --------------------------- 
const btnTornar = document.getElementById("tornar");
// console.log(btnTornar)

// --------------------------- EVENTS --------------------------- 
btnTornar.addEventListener("click", tornarIndex);

// --------------------------- FUNCIONS --------------------------- 
function tornarIndex() {
    window.location.href = "../pages/registrarse.html";
    console.log("Tornant a iniciar sessió...")
}
