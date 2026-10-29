---
title: Follow-ups
area: graph
summary: Faz follow-up sozinha quando alguém não responde, para um quadro inteiro ou um só projeto. Pergunta antes, a menos que você diga o contrário.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 4
---
Quando alguém de um quadro para de responder, sua Machine escreve o follow-up para você, no seu tom e na mesma conversa. Fica desligado até você ativar.

## Ativar

**⋯** em um quadro, depois **Follow-ups…**, e marque **Fazer follow-up quando não houver resposta**. Vale para todos os projetos desse quadro. Ou toque em **Follow-ups desativados** abaixo do nome do quadro, ou em **Fazer follow-up** em uma etapa com projetos sem resposta há mais de 10 dias.

Para um projeto só, **Follow-ups…** no **⋯** do cartão dele ou na página dele. **Para este projeto** escolhe **Ativado**, **Desligada** ou a configuração do quadro. A configuração do próprio projeto vale mais que a do quadro.

## Configurações

- Espere de 3 a 7 dias sem resposta. Depois da espera mais curta, um follow-up é escrito. A mais longa é o prazo máximo para ele sair, mesmo com o seu uso apertado.
- Faça follow-up no mínimo 1 e no máximo 3 vezes. O mínimo sempre sai. Entre os dois, ela lê a conversa e o projeto e só faz follow-up quando ainda faz sentido. Nunca mais que o máximo.
- **Etapas**: **Todas as etapas abertas**, ou seja, nem a última etapa do quadro nem Parado ou recusado. **Personalizar** liga ou desliga etapas e dá a uma etapa sua própria espera.
- **Canais**: os conectados que podem enviar. Um follow-up sai pelo mesmo canal da última mensagem. **Trocar de canal se não houver resposta** tenta o próximo permitido.
- **Mover para Parado ou recusado depois do último**: ligado quando o quadro tem essa linha.

## Perguntar ou enviar sozinha

**Perguntar antes de enviar** é o padrão: os rascunhos esperam nas suas tarefas. **Enviar sem perguntar** é um sim permanente para aquele quadro ou projeto. O que for fora do comum continua esperando por você, assim como o que falhar. Com o modo Cuidadoso ativo, ela sempre pergunta. Um follow-up nunca sai duas vezes.

Logo antes do envio, a conversa é verificada de novo, e se alguém escreveu depois do rascunho, ele não sai: "Não enviado: nova mensagem na conversa".

## Revisar

Os follow-ups de um quadro chegam como uma tarefa só, nunca uma por e-mail. Enquanto são escritos aparece “Escrevendo 3 follow-ups…”, depois “8 follow-ups prontos para Alpha testers”.

**Revisar** mostra todos completos, um embaixo do outro, para você ler tudo rolando uma vez só. **Enviar**, **Editar** e **Pular** aparecem no atual. No teclado, j e k (ou as setas) navegam, Enter envia, e edita e s pula. **Enviar todos os marcados** envia os que continuam marcados. O follow-up de um único projeto é uma tarefa normal.

Quando vários saem em sequência, também com Enviar sem perguntar, cada caixa de e-mail envia um a cada 30 a 45 segundos, e a tarefa mostra o andamento: “Enviando 3 de 8…”.

## E-mails enviados antes da sua Machine

E-mails que você enviou de outro app, antes de a sua Machine ler essa caixa, também contam. Ela lê a conversa (ou, quando não dá, os e-mails anteriores citados no seu último), então três e-mails sem resposta contam como três, e “Sem resposta há” conta a partir do primeiro. Se você já chegou ao máximo, ela não escreve outro.

## Quando para

Os follow-ups param quando a pessoa responde, quando o projeto é ganho, perdido, arquivado ou movido para uma etapa fechada, e quando você adia ou pula um. Antes de escrever, sua Machine confere se há algo mais novo na conversa, para não insistir com quem já respondeu em outro lugar.

Depois do último follow-up sem resposta, o projeto mostra “Sem resposta após 3 follow-ups” e passa para Parado ou recusado, se isso estiver ligado.

## Onde você vê

O cabeçalho do quadro diz “Follow-ups ativados, o próximo Qui”. O cartão de um projeto mostra o próximo follow-up, ou que há um pronto. A página do projeto lista o que foi enviado, inclusive o que saiu automaticamente.

Os follow-ups esperam enquanto sua Machine está ocupada com suas tarefas ou perto do limite de uso, e depois se atualizam. Em um quadro compartilhado, só a Machine do dono do projeto faz follow-up.
