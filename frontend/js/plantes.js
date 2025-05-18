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

//Botó hamburguesa
document.addEventListener("DOMContentLoaded", function () {
    const btnHamburguesa = document.querySelector(".menu-toggle"); 
    const linksMenu = document.querySelector(".links");

    btnHamburguesa.addEventListener("click", function () {
        linksMenu.classList.toggle("mostrar");
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.querySelector(".menu-toggle");
    const links = document.querySelector(".links");

    toggleBtn.addEventListener("click", () => {
        links.classList.toggle("show");
    });
});

// 1. Agafem l'usuari del localStorage
const usuariJSON = localStorage.getItem("usuari");

// 2. Comprovem si l'usuari existeix
if (!usuariJSON) {
    alert("No has iniciat sessió.");
    window.location.href = "../pages/registrarse.html";
}

// 3. Convertim el JSON a objecte
const usuari = JSON.parse(usuariJSON);

// 4. Agafem el seu ID
const usuariId = usuari.id;
fetch(`http://localhost:8000/plantes/${usuariId}`)
    .then(res => {
        if (!res.ok) {
            throw new Error("Error en carregar les plantes.");
        }
        return res.json();
    })
    .then(data => {
        console.log("Plantes rebudes:", data);
        mostrarPlantes(data); // Cridem funció que mostrarà les plantes
    })
    .catch(error => {
        console.error("Error:", error);
        alert("No s'han pogut carregar les plantes.");
    });

    
// Creació del div per la planta
function mostrarPlantes(plantes) {
    const container = document.getElementById("llista-plantes");

    if (!plantes.length) {
        container.innerHTML = "<p>No tens cap planta registrada.</p>";
        return;
    }

    plantes.forEach(planta => {
        const card = document.createElement("div");
        card.classList.add("planta-card");

        card.innerHTML = `
            <h3>${planta.nom}</h3>
            <p>Tipus: ${planta.tipus}</p>
            <p>Humitat mínima: ${planta.humitat_min}</p>
            <p>Humitat màxima: ${planta.humitat_max}</p>
        `;

        container.appendChild(card);
    });
}
