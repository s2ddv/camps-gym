const LOGOUT_URL = "http://127.0.0.1:8000/api/usuarios/logout/";

async function logout() {
    try {
        const response = await fetch(LOGOUT_URL, {
            method: "POST",
            credentials: "include"
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Erro ao deslogar!");
            return;
        }

        alert("Você saiu da sua conta!");
        window.location.href = "/frontend/src/pages/login.html";

    } catch (error) {
        console.error("Erro:", error);
        alert("Não foi possível conectar ao servidor.");
    }
}
