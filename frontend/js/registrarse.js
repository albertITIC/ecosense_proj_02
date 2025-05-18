// --------------------------- OBJECTES ---------------------------
const btnTornar = document.getElementById("tornar");
const form = document.querySelector("form");

// --------------------------- EVENTS ---------------------------
btnTornar.addEventListener("click", tornarIndex);
form.addEventListener("submit", loginUsuari);

// --------------------------- FUNCIONS ---------------------------
function tornarIndex() {
    window.location.href = "../index.html";
}

// Login
async function loginUsuari(e) {
    e.preventDefault(); // Evita que el formulari recarregui la pàgina

    const gmail = document.getElementById("email").value;
    const contrasenya = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                gmail: gmail,
                contrasenya: contrasenya
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert("Error: " + errorData.detail);
            return;
        }

        const data = await response.json();
        console.log("Login correcte:", data);

        // Guardem info de l'usuari per usar-la després (ex: id)
        if (data.usuari && data.usuari.id) {
            localStorage.setItem("usuari", JSON.stringify(data.usuari));
        }

        // Redirigir a plantes.html
        window.location.href = "../pages/plantes.html";

    } catch (error) {
        console.error("Error en el login:", error);
        alert("Hi ha hagut un error inesperat.");
    }
}
