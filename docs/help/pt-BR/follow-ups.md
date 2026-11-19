---
title: Follow-ups
area: graph
summary: Faça follow-up automaticamente quando alguém não responder, em um quadro inteiro ou em um projeto. Sua Machine pede sua aprovação antes de enviar, a menos que você escolha outra opção.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 76bea8f586963be1
---
Quando alguém em um quadro para de responder, sua Machine prepara um follow-up para você, com a sua voz e na mesma conversa. O recurso fica desativado até você ativá-lo. Quando uma das suas habilidades combina com o quadro, os rascunhos seguem essa habilidade, inclusive a ordem do conteúdo no e-mail.

## Ativar

No quadro, toque em **⋯**, depois em **Follow-ups…** e marque **Fazer follow-up quando não houver resposta**. Isso vale para todos os projetos do quadro. Você também pode tocar em **Follow-ups desativados** abaixo do nome do quadro ou em **Fazer follow-up** em uma etapa com projetos sem resposta há mais de 10 dias.

Para um único projeto, toque em **⋯** no quadro ou na página do projeto e escolha **Follow-ups…**. Em **Para este projeto**, escolha **Ativado**, **Desligada** ou a configuração do quadro. A configuração do projeto prevalece sobre a do quadro.

## Configurações

- Por padrão, aguarda de 3 a 7 dias sem resposta. O follow-up é preparado depois do menor prazo e enviado até o prazo mais longo, mesmo quando seu limite de uso está próximo.
- **Só em dias de trabalho**: nada é preparado nem enviado nos seus dias de folga, definidos em **Configurações** > **Notificações** > **Horário de trabalho**. O que vencer nesse período espera até a próxima manhã de trabalho. Fica ativado para Trabalho e desativado para Pessoal.
- Por padrão, faz de 1 a 3 tentativas. Sempre envia o número mínimo e deixa as demais como rascunho. Quando acha melhor parar, o rascunho explica o motivo (“A Machine pararia por aqui: 9 e-mails sem resposta desde agosto”) e não vem marcado. Você pode enviar, pular ou escolher **Parar os follow-ups aqui**. O limite máximo nunca é ultrapassado.
- **Etapas**: por padrão, **Todas as etapas abertas**, exceto a última etapa do quadro e Parado ou recusado. Com **Personalizar**, você ativa ou desativa etapas e define um prazo específico para cada uma.
- **Canais**: os canais conectados que podem enviar mensagens. O follow-up sai pelo mesmo canal da última mensagem. **Trocar de canal se não houver resposta** tenta o próximo canal permitido.
- **Mover para Parado ou recusado depois do último**: fica ativado quando o quadro tem essa etapa.

## Pedir aprovação ou enviar automaticamente

**Perguntar antes de enviar** é a opção padrão: os rascunhos ficam nas suas tarefas. **Enviar sem perguntar** autoriza o envio automaticamente para aquele quadro ou projeto. O que for incomum ou der erro ainda espera por você, e o nível Cuidadoso sempre pede aprovação. Um follow-up nunca é enviado duas vezes. Os follow-ups não enviam notificações push nem por e-mail: os rascunhos ficam na sua lista e no resumo da manhã.

Logo antes do envio, a conversa é verificada novamente. Se alguém tiver escrito depois que o rascunho foi criado, ele não será enviado: “Não enviado: há uma nova mensagem na conversa”. A tarefa mostra a mensagem, quem escreveu e quando, com as opções **Ler** e **Refazer para esta mensagem**. Esta última pede um novo rascunho que leve a mensagem em conta.

## Revisar os follow-ups

Os follow-ups de um quadro aparecem em uma única tarefa, nunca em uma tarefa por e-mail. Enquanto estão sendo preparados, ela mostra “Escrevendo 3 follow-ups…”, depois “8 follow-ups prontos para a equipe de testes Alpha”.

**Revisar** mostra todos em sequência e na íntegra, para você ler tudo rolando a tela. **Enviar**, **Editar** e **Pular** aparecem no follow-up atual. No teclado, j e k (ou as setas) passam de um para outro; Enter envia; e edita; s pula (e desfaz a ação se pressionado novamente); x marca ou desmarca; e c pede mudanças. **Enviar todos os selecionados** envia os que ainda estão marcados.

Todo follow-up vem com um rascunho. Quando não é possível escrever um, aparece o que falta primeiro (“Sem rascunho. Falta primeiro: saber para quem vai.”) e ele não vem marcado. **Escrever** pede um rascunho mesmo assim. Quando há mais de um possível destinatário, aparece “Quem recebe: escolha ao enviar”, e **Enviar** pede que você escolha.

**Pular** desmarca o rascunho e o move para o fim da lista, com o status “Ignorado” e a opção **Desfazer**. Ele só é ignorado de vez quando você fecha a revisão. Um follow-up ignorado volta com **Trazer de volta** nos follow-ups do projeto ou na tarefa em Feito, desde que nenhum follow-up mais recente tenha chegado. O follow-up de um único projeto é uma tarefa normal.

**Pedir mudanças…** reescreve todos os rascunhos marcados ou só o atual, conforme suas instruções. Nada é enviado, e **Desfazer alteração** restaura o texto anterior. Enquanto a caixa de texto está aberta ou a reescrita está em andamento, nada pode ser enviado. Se um rascunho mudar, ele será mostrado novamente antes do envio.

Quando vários follow-ups são enviados em sequência, inclusive com Enviar sem perguntar, cada caixa de e-mail envia um a cada 30 a 45 segundos. A tarefa mostra o andamento: “Enviando 3 de 8…”. **Parar o envio** interrompe os demais. O que já estiver a caminho ainda será enviado, e os outros voltam para a revisão como rascunhos, para serem enviados depois (“Envio interrompido. 1 enviado, 11 mantidos como rascunhos.”).

## E-mails enviados antes de a sua Machine acessar a caixa de e-mail

E-mails enviados por você em outro app, antes de a sua Machine acessar a caixa de e-mail, também contam. Ela lê a própria conversa ou, quando não consegue, os e-mails anteriores citados na sua última mensagem. Assim, três e-mails sem resposta contam como três, e o período em “Sem resposta há” começa no primeiro. Se você já atingiu o limite máximo, ela não prepara outro follow-up.

## Quando os follow-ups param

Os follow-ups param quando a pessoa responde, quando o projeto é ganho, perdido, arquivado ou movido para uma etapa fechada, e quando você adia ou pula um follow-up. Antes de preparar um rascunho, sua Machine verifica se há algo mais recente na conversa para não insistir com alguém que já respondeu por outro canal.

Um follow-up também é encerrado quando alguém já respondeu naquela mesma conversa. Um follow-up de outro projeto nunca conta. Quando sua Machine acha que não é preciso enviar um follow-up por outro motivo, a tarefa continua aberta e explica por quê. Você decide o que fazer.

**Pausar**, em **Follow-ups…**, pausa um quadro ou projeto sem desativar os follow-ups: nada é preparado nem enviado, nenhuma rodada termina e as tarefas de follow-up abertas continuam abertas. Escolha em que dia retomar ou toque em **Retomar** quando quiser. A contagem do prazo continua de onde parou, e o que estiver vencido chega aos poucos. Enquanto isso, aparece o status **Pausado**.

Depois do último follow-up sem resposta, o projeto mostra “Sem resposta após 3 follow-ups” e é movido para Parado ou recusado, se essa opção estiver ativada. Se os follow-ups forem interrompidos antes de qualquer envio, aparece “Follow-ups interrompidos”, e o projeto continua na mesma etapa.

Se o e-mail da pessoa voltar e ela tiver outro endereço, o follow-up será enviado para esse endereço (“E-mail devolvido, novo destinatário: <address>”). Se o endereço de um rascunho devolver o e-mail antes do envio, ele fica retido: “Não enviado: <address> devolveu o e-mail”. O follow-up passa para o outro endereço e espera você enviar.

Se não houver outro endereço, os follow-ups passam para LinkedIn ou WhatsApp quando esses canais forem permitidos e vocês conversarem por lá. Caso contrário, param com o aviso “E-mail devolvido”. Se o projeto for importante, você recebe uma tarefa para encontrar um novo endereço.

## Onde encontrar os follow-ups

No cabeçalho do quadro aparece “Follow-ups ativados, próximo: qui.”. No quadro, cada projeto mostra o próximo follow-up ou indica **Para revisar**. A página do projeto lista o que foi enviado, inclusive as mensagens enviadas automaticamente.

Os follow-ups ficam esperando enquanto sua Machine está ocupada ou perto do limite de uso e são retomados mais tarde. Em um quadro compartilhado, só a Machine de quem é dono do projeto faz follow-up.
