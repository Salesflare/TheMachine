---
title: Follow-ups
area: graph
summary: Faça follow-up automaticamente quando alguém não responder, em um quadro inteiro ou em um projeto específico. Sua confirmação é solicitada antes, a menos que você escolha outra opção.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 0e7bdfb2c9b2deb5
---
Quando alguém em um quadro para de responder, sua Machine prepara um rascunho de follow-up para você, com a sua voz e na mesma conversa. O recurso fica desativado até você ativá-lo. Se uma das suas habilidades for adequada ao quadro, os rascunhos vão seguir essa habilidade, inclusive na ordem das informações no e-mail.

## Ativar

No quadro, toque em **⋯** e depois em **Follow-ups…**. Marque **Fazer follow-up quando não houver resposta**. Isso vale para todos os projetos do quadro. Você também pode tocar em **Follow-ups desativados** abaixo do nome do quadro ou em **Fazer follow-up** em uma etapa com projetos sem resposta há mais de 10 dias.

Para um único projeto, toque em **Follow-ups…** no menu **⋯** do projeto no quadro ou na página dele. Em **Para este projeto**, escolha **Ativado**, **Desligada** ou a configuração do quadro. A configuração do projeto tem prioridade sobre a do quadro.

## Configurações

- Por padrão, aguarde de 3 a 7 dias sem resposta. Um follow-up é preparado como rascunho depois do menor prazo e enviado até o fim do maior, mesmo quando seu uso está perto do limite.
- **Só em dias de trabalho**: nada é preparado ou enviado nos seus dias de folga (em **Configurações** > **Notificações** > **Horário de trabalho**). O que vencer nesse período fica para a manhã seguinte em que você trabalhar. Ativado para Trabalho e desativado para Pessoal.
- Por padrão, faça de 1 a 3 follow-ups. O mínimo é sempre enviado, e os demais ficam como rascunhos. Quando sua Machine achar melhor parar, o rascunho explica o motivo ("A Machine pararia por aqui: 9 e-mails sem resposta desde agosto") e fica desmarcado. Você pode enviá-lo, pulá-lo ou escolher **Parar os follow-ups aqui**. O máximo nunca é ultrapassado.
- **Etapas**: por padrão, **Todas as etapas abertas**, exceto a última etapa do quadro e Parado ou recusado. Em **Personalizar**, você pode ativar ou desativar etapas e definir um tempo de espera para cada uma.
- **Canais**: os canais conectados que podem enviar mensagens. O follow-up é enviado pelo mesmo canal da última mensagem. **Trocar de canal se não houver resposta** tenta usar o próximo canal permitido.
- **Mover para Parado ou recusado depois do último**: ativado quando o quadro tem essa coluna.

## Pedir confirmação ou enviar automaticamente

**Perguntar antes de enviar** é a opção padrão: os rascunhos ficam nas suas tarefas. **Enviar sem perguntar** permite o envio automático para aquele quadro ou projeto. O que for incomum ou apresentar erro ainda fica aguardando sua confirmação, e o nível Cauteloso sempre pede sua confirmação. Um follow-up nunca é enviado duas vezes. Você nunca recebe notificações de follow-ups, por push ou e-mail: os rascunhos ficam na sua lista e no resumo da manhã.

Logo antes do envio, a conversa é verificada novamente. Se alguém tiver escrito desde que o rascunho foi preparado, ele não será enviado: "Não enviado: há uma nova mensagem na conversa". A tarefa mostra a mensagem, quem a escreveu e quando, além das opções **Ler** e **Refazer para esta mensagem**, que pede um novo rascunho levando a mensagem em conta.

## Revisar os follow-ups

Os follow-ups de um quadro aparecem em uma única tarefa, nunca em uma tarefa por e-mail. Enquanto os rascunhos são preparados, aparece "Escrevendo 3 follow-ups…" e, depois, "8 follow-ups prontos para Alpha testers".

Em **Revisar**, os rascunhos aparecem um abaixo do outro, na íntegra, para você ler todos rolando a tela. **Enviar**, **Editar** e **Pular** aparecem no rascunho atual. No teclado, j e k (ou as setas) navegam pelos rascunhos; Enter envia, e edita, s pula (pressione de novo para desfazer), x marca ou desmarca, e c pede mudanças. **Enviar todos os marcados** envia os que ainda estiverem marcados.

Todo follow-up inclui um rascunho. Se não for possível escrever um, aparece o que falta primeiro ("Sem rascunho. Falta informar quem vai receber.") e ele fica desmarcado. **Escrever** ainda permite pedir o rascunho. Se houver mais de um destinatário possível, aparece "Quem recebe: escolha ao enviar", e **Enviar** pede que você escolha.

**Pular** desmarca o rascunho e o move para o fim da lista, com a indicação "Ignorado" e a opção **Desfazer**. Ele é ignorado definitivamente quando você fecha a revisão. Um rascunho ignorado pode voltar pela opção **Trazer de volta** nos follow-ups do projeto ou na tarefa em **Feito**, desde que nenhum follow-up mais recente tenha chegado. O follow-up de um projeto individual é uma tarefa normal.

**Pedir mudanças…** reescreve todos os rascunhos marcados ou apenas o atual, conforme você pedir. Nada é enviado, e **Desfazer alteração** restaura o texto anterior. Enquanto a caixa de texto estiver aberta ou a reescrita estiver em andamento, nada pode ser enviado. Se um rascunho mudar, ele será mostrado novamente antes do envio.

Quando vários follow-ups são enviados em sequência, inclusive com **Enviar sem perguntar**, cada caixa de e-mail envia um a cada 30 a 45 segundos. A tarefa mostra o andamento: "Enviando 3 de 8…". **Parar o envio** interrompe os demais. O que já estiver a caminho ainda será enviado, e os outros voltam para a revisão como rascunhos, para serem enviados depois ("Envio interrompido. 1 enviado, 11 mantidos como rascunhos.").

## E-mails enviados antes de sua Machine

E-mails enviados por você em outro app, antes de sua Machine acessar aquela caixa de e-mail, também são contabilizados. Ela lê a conversa (ou, quando não consegue, os e-mails anteriores citados na sua última mensagem). Assim, três e-mails sem resposta contam como três, e o prazo de "Sem resposta há" começa no primeiro. Se você já tiver atingido o máximo, nenhum outro follow-up será preparado.

## Quando os follow-ups param

Os follow-ups param quando a pessoa responde, quando o projeto é ganho, perdido, arquivado ou movido para uma etapa fechada, e quando você adia ou pula um deles. Antes de preparar um rascunho, sua Machine verifica se há algo mais recente na conversa, para não insistir com alguém que já respondeu em outro lugar.

**Pausar**, em **Follow-ups…**, pausa um quadro ou projeto sem desativar os follow-ups: nada é preparado nem enviado, nenhuma sequência é encerrada e as tarefas de follow-up abertas continuam abertas. Escolha um dia para retomar ou toque em **Retomar** quando quiser. O tempo de espera continua de onde parou, e o que estiver vencido será retomado um item de cada vez. Enquanto isso, aparece **Pausado**.

Depois do último follow-up sem resposta, aparece "Sem resposta após 3 follow-ups" no projeto, que é movido para Parado ou recusado se essa opção estiver ativada. Se os follow-ups forem interrompidos antes de qualquer envio, aparece "Follow-ups interrompidos" e o projeto continua na mesma etapa.

Se o e-mail da pessoa não for entregue e ela tiver outro endereço, o follow-up será enviado para esse endereço ("E-mail não entregue, agora para <address>"). Se o endereço de um rascunho não puder receber mensagens antes do envio, ele ficará retido: "Não enviado: <address> não recebeu o e-mail". Em seguida, será direcionado para o outro endereço da pessoa e aguardará até você tocar em **Enviar**.

Se não houver outro endereço, os follow-ups passam para LinkedIn ou WhatsApp quando isso for permitido e você conversar com a pessoa por lá. Caso contrário, eles param com a mensagem "E-mail não entregue". Se o projeto for importante, você recebe uma tarefa para encontrar um novo endereço.

## Onde ver os follow-ups

O cabeçalho do quadro mostra "Follow-ups ativados, próximo: qui.". No quadro, cada projeto mostra o próximo follow-up ou se ele já está pronto. A página do projeto lista o que foi enviado, inclusive os envios automáticos.

Os follow-ups ficam aguardando enquanto sua Machine está ocupada ou perto do limite de uso e são retomados depois. Em um quadro compartilhado, apenas a Machine da pessoa responsável pelo projeto faz follow-up.
