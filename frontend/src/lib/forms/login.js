const form = document.querySelector("form");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    login();
});

function login() {
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();

    if (!email || !senha) {
        alert("Preencha todos os campos!");
        return;
    }

    const usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];

    const usuario = usuarios.find(
        user => user.email === email && user.senha === senha
    );

    if (!usuario) {
        alert("Email ou senha incorretos!");
        return;
    }

    localStorage.setItem("usuarioLogado", JSON.stringify(usuario));

    alert(`Bem-vindo, ${usuario.nome}!`);

    window.location.href = "/frontend/src/pages/index.html";
}

function togglePassword() {
    const input = document.getElementById("senha");

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}
