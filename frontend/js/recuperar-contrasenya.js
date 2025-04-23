document.addEventListener("DOMContentLoaded", function () {
    // --------------------------- OBJECTES --------------------------- 
    const btnTorna = document.getElementById("tornar");

    // --------------------------- EVENTS --------------------------- 
    if (btnTorna) {
        btnTorna.addEventListener("click", tornarIndex);
    }

    // --------------------------- FUNCIONS --------------------------- 
    function tornarIndex() {
        window.location.href = "../pages/registrarse.html";
        console.log("Tornant a iniciar sessió...");
    }
});
