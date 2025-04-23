document.addEventListener("DOMContentLoaded", function () {
    const btnRegister = document.getElementById("registrarse");

    if (btnRegister) {
        btnRegister.addEventListener("click", function () {
            // Aquí pots posar validació de correu, si vols
            window.location.href = "../pages/contrasenya-recuperada.html";
            console.log("Redirigint a contrasenya recuperada...");
        });
    }
});
