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

## Agendar com outras Machines

Quando alguém com uma Machine escreve "vamos nos ver semana que vem", sua Machine pede à dela os horários livres e acha um bom para os dois, dentro do seu horário de trabalho. Cada um recebe um só to-do, como "Reunião com Alex Example", com o horário embaixo. Toque em **Marcar**, **Outro horário** ou **Não precisa**. O convite só sai quando os dois tocaram em Marcar. Sem Machine ou sem resposta: o to-do mantém o rascunho de email com horários.

Só livre ou ocupado é enviado, com criptografia de ponta a ponta, para no máximo 14 dias e arredondado a 15 minutos. Eventos privados contam como ocupados. Uma Machine só pode perguntar se vocês trocaram emails nos dois sentidos. Configure no painel Network em **O que outras Machines podem perguntar à minha**: **Livre/ocupado para agendar** ou **Desativado**, com a duração, o intervalo e os horários preferidos. Cada pedido aparece em Atividade, em Calendário.

## Uma Machine no seu próprio computador

Para entrar na Network com uma Machine que você mesmo roda:

1. Na sua página de conta em app.themachine.computer, toque em **Parear uma Machine auto-hospedada**. O código funciona uma vez, por 15 minutos.
2. No seu computador, rode `assistant fleet-pair` com o código e reinicie.

Até 5 Machines por conta. Cada uma pode ser desconectada ali.
