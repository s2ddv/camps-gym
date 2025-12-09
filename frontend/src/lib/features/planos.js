const numeroWhatsApp = "15996744027"; 

const botoesEscolher = document.querySelectorAll(".plano-card button");

botoesEscolher.forEach(botao => {
    botao.addEventListener("click", () => {
    const plano = botao.parentElement.querySelector("h3").innerText
    const mensagem = `Olá! Tenho interesse no ${plano}. Pode me dar mais informações?`;
    const linkWhatsApp = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(mensagem)}`;
    window.open(linkWhatsApp, "_blank");
    });
});