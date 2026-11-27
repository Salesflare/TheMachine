---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar faz barulho. O resto fica em um resumo pela manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: dc56a77907df5da0
---
Quer receber menos notificações ou de outro tipo? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, uma tarefa que precisa que você entre na conta ou uma pergunta do Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando, quando voltam.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no celular ou computador), **Telegram** depois de configurar e **E-mail** em uma Machine hospedada ou em uma na The Machine Network. Tudo fica ativado, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma aba: dias de trabalho, quando as notificações podem ser enviadas, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Você recebe uma notificação push, um alerta no Telegram ou um e-mail somente quando:

- uma tarefa vence hoje ou está marcada como urgente;
- há uma resposta que alguém está esperando, já escrita e pronta para enviar;
- uma tarefa precisa que você entre na conta;
- um item adiado volta no horário que você escolheu.

Todo o resto aparece sem alarde no painel (e silenciosamente no Telegram) e espera pelo resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje faz barulho. Você recebe no máximo 8 notificações push por dia. Se você ficar 3 dias sem abrir o painel, recebe apenas o resumo da manhã até voltar.

## Quando as notificações chegam

O app verifica se você está usando o painel, não apenas se ele está aberto:

- Se você estiver usando (com o painel em primeiro plano e tiver clicado, digitado ou rolado a página nos últimos 10 minutos), nada faz barulho. As mensagens do Telegram chegam silenciosamente. Só abrir ou recarregar o painel não conta.
- Se você estiver ausente (com o painel em segundo plano, fechado ou sem atividade por 10 minutos), uma notificação push chega um minuto depois que você sair, a menos que você volte e veja a notificação.
- Se nada chegar até você em 15 minutos e não puder esperar, você recebe um e-mail, no máximo um por hora. O que você viu ou resolveu fica de fora, e cada tarefa aparece uma vez, no estado atual. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Consideramos que uma notificação chegou quando ela aparece no celular ou no navegador, ou quando o Telegram recebe a mensagem. Um celular desligado, sem conexão ou com as notificações desativadas não conta. O mesmo vale para o Telegram enquanto o painel está em uso. Se a notificação apareceu apenas no computador, o que for urgente ou vencer hoje ainda será enviado por e-mail: talvez você não esteja por perto.
- Sem app para celular, notificações do navegador ou Telegram? Você recebe por e-mail tudo o que foi mencionado acima.
- Se não for possível acessar o Telegram, a notificação push será enviada mesmo assim, uma vez, e o app tentará enviar pelo Telegram novamente.
- Se alguém da equipe passar uma tarefa para você e sua Machine não tiver um celular ou Telegram para avisar você, chega um e-mail com o título e um link, 15 minutos depois, se você ainda não tiver visto. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Se sua sessão do Claude expirar em até 3 dias ou já tiver expirado, você recebe um e-mail com **Entrar de novo**, uma vez por sessão. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Fora do seu horário de trabalho, nada chega. O resumo da manhã inclui esses itens.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo no seu próximo dia de trabalho. A tarefa mostra quando vai chegar até você, como em Notificação seg., 2 nov. · 08:30.

Atualizações de andamento e edições nunca geram notificações. Um resultado mais recente em uma tarefa que você ainda não viu atualiza a notificação existente, sem criar outra. Várias notificações em sequência geram um único alerta. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Precisa da sua resposta, está parada ou precisa que você entre na conta: **Responder**, **Abrir** ou **Entrar**, depois **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois botões. Nas perguntas do Fleet, **Responder** e **Recusar** continuam disponíveis.

Nenhuma notificação envia, paga ou envia algo para análise. Um rascunho sempre abre primeiro, para você ver antes de ser enviado. **Abrir rascunho** mostra a tarefa na sua lista com o rascunho completo. **Fazer** apenas inicia o trabalho em uma tarefa nova.

No app para celular, **Adiar** e **Marcar como feito** pedem que você desbloqueie o aparelho primeiro. No navegador, eles abrem o painel, onde a ação é feita e a opção de desfazer aparece. **Adiar** faz a tarefa voltar em duas horas ou, se for um lembrete, na manhã seguinte.

Os e-mails têm links para **Abrir** (e para **Adiar** quando algo está esperando). Eles apenas abrem o painel.

Se você tocar em uma notificação ou em **Abrir** em um e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja agora: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. O chat nunca abre. Se a página ainda não estiver atualizada, ela acompanha a tarefa assim que estiver.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para informar. Se esse horário for anterior a **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário, para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega por push e por e-mail, em um formato curto para ler rapidamente:

- uma saudação com o que importa hoje, como "Bom dia, Sam, há 2 respostas prontas para enviar" ou, se houver uma tarefa, "Bom dia, Sam, aguardando sua aprovação: Enviar o formulário do pedido". Só contam como prontas as tarefas com um rascunho ou resultado para aprovar. Uma tarefa que primeiro precisa da sua resposta não conta;
- as tarefas incluídas na saudação, cada uma com um link para **Abrir**, e o que vence hoje. Caso contrário, no máximo três coisas para fazer;
- até cinco tarefas que você mesmo adicionou e que estão esperando por você, independentemente do que a saudação inclui;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como em "Mais 12 podem esperar, cerca de 5 min para resolver." Tarefas que esperam sua resposta não entram nesse tempo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou em que The Machine ainda está trabalhando, só é contada quando estiver esperando por você. A quantidade corresponde às tarefas que estão esperando na sua lista;
- suas reuniões em uma linha.

**Abrir** mostra a tarefa destacada na sua lista, mesmo que esteja concluída ou adiada. Uma promessa abre a tarefa correspondente ou, se ainda não houver uma, a página da própria promessa.

A notificação push mostra o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos meios escolhidos na linha acima. Só chega em um dia em que você esteve presente: você usou o painel ou tomou uma decisão sobre uma tarefa nele, no Telegram, no chat ou por voz. Se não houver uma tarefa concluída nem uma reunião realizada nesse dia, você não recebe o resumo.

Ele começa com um resumo do dia, como "Boa noite, Sam, 4 tarefas concluídas hoje", seguido de uma parte de **Trabalho** e outra de **Pessoal**. Partes sem conteúdo não aparecem. Um alerta sobre sua Machine não entra em nenhuma das duas. Cada parte inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, seguidas de "+12 mais" e das reuniões do dia, como "+3 reuniões: reunião sobre preços e mais 2";
- **Em aberto para amanhã** (ou para o próximo dia de trabalho, se for sexta-feira): as primeiras reuniões e o que vence.

No fim, aparece quantas tarefas ainda precisam da sua atenção. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente e ver **Copiar Trabalho** e **Copiar Pessoal**. Para parar de receber esse resumo, desative a opção correspondente.

## Privacidade

As notificações push vão diretamente da sua Machine para o dispositivo, criptografadas para ele. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando o modo [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as quantidades. Desative **E-mail** em um tipo de notificação para não receber esse tipo por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma linha simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
