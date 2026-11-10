---
title: Amigos e a Network
area: fleet
summary: Adicione amigos pelo nome de usuário, encontre pessoas que você conhece que têm uma Machine e pareie uma Machine no seu próprio computador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
---
## Amigos

Adicione alguém pelo nome de usuário exato, na aba **Fleet**, em Amigos. Amigos podem perguntar quem conhece alguém, receber contexto de reuniões e apresentações calorosas, e ver quando você está ocupado (só os horários ocupados, nunca o quê). Remova ou bloqueie um amigo quando quiser.

## Encontre pessoas que você conhece

No painel da Network:

- "Verificar quais dos meus contatos têm uma Machine" sugere pessoas que você conhece.
- "Deixar quem tem meu e-mail me encontrar" permite que elas encontrem você.

Os dois vêm ligados por padrão, e desligados no nível de segurança Cuidadoso. Desligue qualquer um quando quiser; sua escolha fica. Podem encontrar você pelo e-mail de login e pelos endereços conectados, exceto os compartilhados como info@, que ficam desligados até você ligá-los.

Pessoas que você conhece e que estão na Network são sugeridas assim que você a ativa, e quando alguém entra depois. Uma sugestão vem com Conectar, Agora não ou **Nunca sugerir**. **Sair da Network** tira você dela.

As pessoas encontradas mostram **Tem uma Machine** na sua lista Pessoas. A verificação usa os endereços das suas mensagens e os que você adicionou a alguém com **Editar**: se alguém se cadastrou com outro endereço, adicione-o a essa pessoa. Na página de alguém encontrado, **Adicionar como amigo** envia o mesmo pedido que Conectar (**Adicionar como família** fica no menu ⋯).

Para quem não tem uma Machine, **Convidar para a The Machine** mostra o que a pessoa recebe, para **Copiar** ou **Abrir no seu e-mail**, sem enviar nada sozinha.

Números de telefone também contam: os das suas conversas no WhatsApp com pessoas para quem você escreveu ou com quem se encontrou, e os que você adicionou com **Editar**. Seu número do WhatsApp vinculado e os números em Sobre você fazem você ser encontrado, cada um com sua chave em **Pode ser encontrado por**. Um número só encontra alguém quando essa pessoa também procurou você, ou vocês são amigos, então ninguém pode testar números para ver quem tem uma Machine.

## Agendar com outras Machines

Quando alguém com uma Machine escreve "vamos nos ver semana que vem", sua Machine pede à dela os horários livres e acha um bom para os dois, dentro do seu horário de trabalho. Cada um recebe um só to-do, como "Reunião com Alex Example", com o horário embaixo. Toque em **Marcar**, **Outro horário** ou **Não precisa**. O convite só sai quando os dois tocaram em Marcar.

Só livre ou ocupado é enviado, com criptografia de ponta a ponta, para no máximo 14 dias e arredondado a 15 minutos. Eventos privados contam como ocupados. Uma Machine só pode perguntar se vocês trocaram emails nos dois sentidos. Configure no painel Network em **O que outras Machines podem perguntar à minha**: **Livre/ocupado para agendar** ou **Desativado**, com a duração, o intervalo e os horários preferidos. Cada pedido aparece em Atividade, em Calendário.

Sem Machine ou sem resposta: o rascunho do email recebe um link onde a outra pessoa escolhe um dos seus horários livres. A escolha vira um to-do com **Marcar**; nada é marcado antes de você tocar.

O link mostra só horários livres, pelas mesmas regras, e nada mais sobre você. Ele termina assim que a reunião é marcada, ou depois de 14 dias. No email, ele aparece como "Pick a time". Embaixo, a página diz que sua Machine encontrou estes horários, com "Get yours." e seu primeiro nome. Desligue isso em **Rodapé nos links de agendamento**. Cada link e escolha aparece em Atividade.

## Uma Machine no seu próprio computador

Para entrar na Network com uma Machine que você mesmo roda:

1. No painel da sua Machine, abra **Configurações** e toque em **Entrar na Network**.
2. Na página que abrir, entre (ou crie sua conta) e confirme. Sua Machine recebe sozinha, sem reiniciar.

O jeito com código continua funcionando: toque em **Parear uma Machine auto-hospedada** na sua página de conta em app.themachine.computer, depois rode `assistant fleet-pair` com o código no seu computador e reinicie. O código funciona uma vez, por 15 minutos.

Até 5 Machines por conta. Cada uma pode ser desconectada ali.
