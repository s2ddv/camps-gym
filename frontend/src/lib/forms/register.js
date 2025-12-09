document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("Form enviado");

    const email = document.getElementById("email").value;
    const firstName = document.getElementById("first_name").value;
    const lastName = document.getElementById("last_name").value;
    const username = `${firstName}${lastName}`.replace(/\s+/g, '').toLowerCase(); 

    const data = {
        username: username, 
        first_name: firstName,
        last_name: lastName,
        email: email,
        senha: document.getElementById("password").value,

        data_de_nascimento: document.getElementById("data_de_nascimento").value,
        telefone: document.getElementById("telefone").value,
        objetivo: document.getElementById("foco").value,
        altura: document.getElementById("altura").value,
        peso: document.getElementById("peso").value,
    };

    console.log("Dados enviados:", data);

    try {
        const response = await fetch("http://127.0.0.1:8000/api/usuarios/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        console.log("Status da resposta:", response.status);

        const responseData = await response.json();
        console.log("Dados da resposta:", responseData);

        if (response.ok) {
            console.log("Sucesso! Redirecionando...");
            window.location.href = "./index.html";
            alert("Usuário registrado com sucesso!");
        } else {
            console.log("Erro na resposta:", responseData);
            alert("Erro ao registrar usuário:\n\n" + JSON.stringify(responseData));
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro de conexão: " + error.message);
    }
});