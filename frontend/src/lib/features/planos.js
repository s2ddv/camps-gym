const numeroWhatsApp = "5599999999999"; 

const botoesEscolher = document.querySelectorAll(".plano-card button");

botoesEscolher.forEach(botao => {
    botao.addEventListener("click", () => {
    const plano = botao.parentElement.querySelector("h2").innerText
    const mensagem = `Olá! Tenho interesse no ${plano}. Pode me dar mais informações?`;
    const linkWhatsApp = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(mensagem)}`;
    window.open(linkWhatsApp, "_blank");
    });
});