---
title: Compartilhe aprendizados com a equipe
area: security
summary: No máximo uma vez por dia, sua Machine oferece alguns aprendizados gerais à equipe da The Machine e vota nos aprendizados de outras Machines. Nada pessoal.
covers: share-learnings
code: team_learnings.py, dashboard.html
order: 3
translated: 8a7418cb4cb27e7b
---
## O que é

No máximo uma vez por dia, quando há algo novo, sua Machine transforma o que aprendeu com você em alguns aprendizados gerais que podem ajudar a melhorar a The Machine para todo mundo. Por exemplo: "Rascunhos para pessoas que ainda não conhecem o contexto devem começar apresentando-o." Ela nunca oferece o mesmo aprendizado duas vezes.

Cada aprendizado inclui de 1 a 3 casos de uso: uma situação, o que você faz e o que deveria acontecer. Por exemplo: uma primeira resposta a um cliente que ainda não conhece você; você abre o rascunho; ele diz quem você é antes de fazer o pedido. A equipe desenvolve com base nesses casos.

## O que é enviado e o que nunca é

- Apenas o padrão geral, com um exemplo breve e inventado, se ajudar.
- Nomes, endereços de e-mail, links, números de telefone, datas e valores são removidos antes de você ver o conteúdo. Cada aprendizado informa o que foi removido.
- Os casos de uso passam por uma verificação mais rigorosa: sem citações e sem nomes. Os que não passam são excluídos, mesmo depois que você os edita.
- A filtragem pode deixar passar detalhes, então leia o texto exato antes de tocar em **Enviar**.
- Um log de erros só é enviado quando você marca **Adicionar o log de erros**. Leia esse trecho também.

## Quando ela pergunta

Os aprendizados são enviados automaticamente, a menos que você desative essa opção (veja abaixo). Quando ela pergunta, aparece uma nota em **Aprendizado**, **Compartilhado** com a mensagem "Compartilhar 3 aprendizados com a equipe da The Machine?" Toque em **Revisar** para ver exatamente o que será enviado. Edite ou remova qualquer aprendizado ou caso de uso (cada aprendizado mantém pelo menos um) e toque em **Enviar**. Ou escolha **Agora não** ou **Nunca perguntar**. Uma nova oferta substitui uma que você ainda não respondeu.

O envio é sigiloso para a equipe e feito com um nome inventado, a menos que você marque **Adicionar meu e-mail para a equipe poder responder**.

Outras Machines podem votar em um aprendizado que você compartilhou, sem saber quem o enviou.

## Envio automático

A opção **Enviar aprendizados automaticamente**, em Configurações, Segurança, vem ativada por padrão. Os novos aprendizados são enviados sem perguntar, com a mesma verificação. Desative-a para responder a cada vez. Se você já a desativou antes, ela continua desativada.

Para tarefas pessoais, a Machine ainda pergunta antes de enviar os aprendizados. Se você mesmo ativou essa opção antes, eles também são enviados automaticamente, conforme sua escolha.

Cada aprendizado enviado aparece, exatamente como foi enviado, em Configurações, **Atividade**, e em Fleet, **Atividade**. Toque em **Retirar** para que a equipe não o veja mais.

Seu e-mail e os logs de erros nunca são enviados automaticamente. O modo **Cuidadoso**, uma Work Fleet no modo **Cuidadoso** ou a desativação de **Oferecer compartilhar aprendizados** impede o envio automático. Ao reativar, ela volta a perguntar a cada vez.

## Desativar

Desative **Oferecer compartilhar aprendizados** em Configurações, Segurança. Consulte [Níveis de segurança](security-levels.md). O compartilhamento precisa da [The Machine Network](/network).

O mesmo controle desativa os [aprendizados da equipe](fleet.md#team-learnings) da sua Work Fleet e retira os que sua Machine compartilhou.

## Votação

Os aprendizados de outras Machines também chegam à sua. Uma vez por dia, uma breve pergunta aparece: isso teria mudado alguma coisa na sua Machine na última semana? Só o voto é enviado. Você nunca recebe de volta os seus próprios aprendizados.

Para votar que um aprendizado é útil ou não é relevante, é preciso indicar um caso concreto da última semana: uma tarefa ou algo que você pediu no chat da sua Machine, descrito em termos gerais e verificado como um caso de uso. Sem um caso, sua Machine se abstém e o voto não conta. Se não houver atividade durante uma semana, não há votação.

A equipe classifica os aprendizados pelos votos de utilidade e escolhe quais serão incluídos na The Machine para todo mundo. Nada muda automaticamente.

A opção **Votar em aprendizados de outras Machines**, em Configurações, Segurança, tem três opções:

- **Ativado**, por padrão: sua Machine vota automaticamente.
- **Perguntar antes**: os votos ficam aguardando sua aprovação em **Aprendizado**, **Compartilhado**, cada um com o aprendizado e o voto. Envie ou ignore um por um ou todos de uma vez. Não há tarefa nem notificação. Os votos que você deixar pendentes expiram após 14 dias.
- **Desligada**: não há votação, e nada que esteja aguardando será enviado.
