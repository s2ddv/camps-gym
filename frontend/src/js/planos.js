  const numeroWhatsApp = "5599999999999"; // Exemplo: 55 + DDD + número

  const botoesEscolher = document.querySelectorAll(".plano-card button");

  botoesEscolher.forEach(botao => {
    botao.addEventListener("click", () => {
      // Pega o nome do plano (o texto do <h2> dentro do mesmo card)
      const plano = botao.parentElement.querySelector("h2").innerText;

      // Mensagem que será enviada
      const mensagem = `Olá! Tenho interesse no ${plano}. Pode me dar mais informações?`;

      // Cria o link do WhatsApp
      const linkWhatsApp = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(mensagem)}`;

      // Abre o WhatsApp em nova aba
      window.open(linkWhatsApp, "_blank");
    });
  });
