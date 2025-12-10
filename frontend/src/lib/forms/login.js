const API_URL = "http://127.0.0.1:8000/api/usuarios/login/";

const form = document.querySelector("form");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");

form.addEventListener("submit", async (event) => {
    event.preventDefault(); 

    const username = emailInput.value.trim();
    const password = senhaInput.value.trim();

    if (!username || !password) {
        alert("Preencha todos os campos!");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            credentials: "include", 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Erro ao fazer login!");
            return;
        }

        alert("Login realizado com sucesso!");

        window.location.href = "/frontend/src/pages/index.html";

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível conectar ao servidor.");
    }
});


function togglePassword() {
    const input = document.getElementById("senha");
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}
