---
title: Regras de compartilhamento
area: fleet
summary: O que sua Machine pode responder em cada Fleet e para cada tipo de pergunta. Você escolhe entre Perguntar antes, Sempre ou Nunca e decide se os nomes podem ser incluídos.
covers:
code: fleet.py, dashboard.html
order: 2
keywords: share, sharing, colleagues, teammates, team, what others see, answer for me
translated: 1ae445260f88518d
---
## Configure as regras

Decida o que sua Machine conta para seu Fleet. Na aba **Fleet**, abra **Compartilhamento**. Cada tipo de pergunta tem uma regra:

- **Perguntar antes**: você vê cada pergunta e decide.
- **Sempre**: sua Machine responde por conta própria.
- **Nunca**: sua Machine recusa.
- **Nomes**: define se a resposta pode dizer quem é alguém, como o nome de uma pessoa convidada, ou se deve omitir os nomes.

Sua Machine nunca compartilha o conteúdo dos seus e-mails nem o assunto das suas reuniões. Com **Diferente para alguém? Adicione uma exceção**, você define uma regra para uma pessoa.

As regras só podem ser alteradas no painel, nunca por mensagem.

## Em um Fleet de Trabalho

Em um Fleet de Trabalho Padrão, as regras para quem conhece quem, o contexto das reuniões e quem cuida dos e-mails compartilhados têm apenas as opções **Sempre** e **Nunca**. Com **Sempre**, sua Machine responde usando apenas o que o [Graph da equipe](team-graph.md) já compartilha com sua equipe, e só menciona pessoas que ele compartilha. Uma regra salva como **Perguntar antes** funciona como **Sempre**.

Enquanto o Graph da equipe não estiver compartilhando, as opções **Perguntar antes** também continuam disponíveis para quem conhece quem e para o contexto das reuniões. O mesmo vale para um Fleet no nível Cuidadoso. Consulte [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).

## Na primeira vez que alguém perguntar

Uma pergunta que precisa da sua aprovação chega como uma tarefa, com as opções **Compartilhar uma vez**, **Sempre compartilhar**, **Recusar** ou **Nunca compartilhar**.
