document.addEventListener("DOMContentLoaded", function () {
    // Seleccionem tots els botons d'eliminar
    const botonsEliminar = document.querySelectorAll(".btn-eliminar");

    botonsEliminar.forEach(boto => {
        boto.addEventListener("click", function () {
            // Confirmació abans d'eliminar
            const confirmacio = confirm("Estàs segur que vols eliminar aquesta planta?");
            if (confirmacio) {
                // Busquem el contenidor més proper de la planta i l'amaguem
                const planta = this.closest(".container-planta");
                if (planta) {
                    planta.style.display = "none"; // Amaga visualment la planta
                }
            }
        });
    });
});
                        