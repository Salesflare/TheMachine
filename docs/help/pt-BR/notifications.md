---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar faz barulho. O resto vem em um resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3faac166e8f9fa3d
---
Quer receber menos notificações ou outras notificações? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, uma tarefa que precisa que você faça login ou uma pergunta do Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando, quando voltarem.
- **Resumo da manhã**: um resumo breve do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que continua em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no celular ou computador), **Telegram**, depois que estiver configurado, e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Todas estão ativadas, exceto os resumos no Telegram.

Seu **Horário de trabalho** também fica na mesma aba: dias de trabalho, quando as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Você recebe uma notificação push, um aviso no Telegram ou um e-mail apenas quando:

- uma tarefa vence hoje ou está marcada como urgente;
- alguém está esperando uma resposta que foi redigida e está pronta para enviar;
- uma tarefa precisa que você faça login;
- um item adiado volta no horário que você escolheu.

Todo o resto aparece discretamente no painel (e sem aviso no Telegram) e fica lá até o resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje faz barulho. Você recebe no máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, você recebe apenas o resumo da manhã, até voltar.

## Quando as notificações chegam

O sistema verifica se você está usando o painel, não apenas se ele está aberto:

- Se você está usando o painel (ele está em primeiro plano e você clicou, digitou ou rolou a página nos últimos 10 minutos), nada faz barulho. As notificações do Telegram chegam sem aviso. Só abrir ou recarregar o painel não conta.
- Se você saiu do painel (ele está em segundo plano, fechado ou sem atividade há 10 minutos), uma notificação push chega um minuto depois, a menos que você volte e veja a tarefa.
- Se a tarefa ainda não foi vista 15 minutos depois e não pode esperar, você recebe um e-mail sobre ela, no máximo um por hora. O que você já resolveu fica de fora, e cada tarefa aparece uma vez, com o status atual. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe atribuir uma tarefa a você e sua Machine não tiver um celular ou Telegram para entrar em contato, você recebe um e-mail com o título e um link, 15 minutos depois, se ainda não tiver visto a tarefa. Desative **E-mail** em **Resultados e perguntas** para desativar esse envio.
- Fora do seu horário de trabalho, nada chega. O resumo da manhã inclui essas tarefas.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo do próximo dia de trabalho. A tarefa mostra quando vai chegar até você, como em Notificação seg., 2 de nov. · 08:30.

Atualizações de progresso e edições nunca geram notificações. Um novo resultado em uma tarefa que você ainda não viu atualiza a tarefa sem gerar uma nova notificação. Vários avisos de uma vez geram uma única notificação. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Precisa da sua resposta, está bloqueada ou exige login: **Responder**, **Abrir** ou **Fazer login**, depois **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

No navegador e no Telegram, aparecem dois desses botões. Nas perguntas do Fleet, **Responder** e **Recusar** continuam disponíveis.

Nada é enviado, pago ou enviado para processamento a partir de uma notificação. Um rascunho sempre abre primeiro, para você ver antes de enviá-lo. **Abrir rascunho** mostra a tarefa na sua lista com o rascunho completo. **Fazer** só inicia o trabalho em uma nova tarefa.

No app para celular, **Adiar** e **Marcar como feito** pedem que você desbloqueie o celular primeiro. No navegador, eles abrem o painel, onde a ação é realizada e a opção **Desfazer** aparece. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para **Abrir** (e para **Adiar** no caso do que está esperando). Eles só abrem o painel.

Ao tocar em uma notificação ou em **Abrir** no e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja agora: **Feito agora**, **Feito**, **Volta mais tarde** ou em outra visualização. A notificação nunca abre o chat. Se a página ainda não tiver atualizado, ela acompanha a tarefa assim que isso acontecer.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para mostrar. Se esse horário for antes de **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário, para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega por notificação push e e-mail, e é curto o bastante para ler rapidamente:

- uma saudação com o que importa hoje, como "Bom dia, Sam, 2 respostas estão prontas para enviar" ou, se houver uma tarefa, "Bom dia, Sam, sua aprovação está pronta: Enviar o formulário do pedido". Só contam como prontas as tarefas com um rascunho ou resultado para aprovar. Uma tarefa que primeiro precisa da sua resposta não conta;
- as tarefas incluídas na saudação, cada uma com um link para **Abrir**, e o que vence hoje; caso contrário, no máximo três tarefas;
- até cinco tarefas que você mesmo adicionou e que estão esperando por você, independentemente do que a saudação inclui;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como "Mais 12 podem esperar, cerca de 5 min para resolver". As tarefas que esperam sua resposta não entram nesse tempo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou em que The Machine ainda está trabalhando, só é contada quando estiver esperando por você. A contagem corresponde às tarefas que estão esperando na sua lista;
- suas reuniões em uma linha.

**Abrir** mostra a tarefa destacada na sua lista, mesmo que esteja feita ou adiada. Uma promessa abre a tarefa correspondente ou, se ela ainda não existir, a página da própria promessa.

A notificação push diz o mesmo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão, 15 minutos antes de **Até**, pelos meios escolhidos na linha acima. Só chega em um dia em que você esteve presente: você usou o painel ou tomou uma decisão sobre uma tarefa nele, no Telegram, no chat ou por voz. Se você não concluiu nenhuma tarefa nem participou de uma reunião, não recebe o resumo.

O resumo começa com uma contagem do dia, como "Boa noite, Sam, 4 tarefas feitas hoje", e depois mostra uma seção de **Trabalho** e outra de **Pessoal**. Se uma seção não tiver nada, ela não aparece. Cada seção inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois "+12 mais" e as reuniões do dia, como "+3 reuniões: Conversa sobre preços e mais 2";
- **Em aberto para amanhã** (ou para o próximo dia de trabalho, se for sexta-feira): as próximas reuniões e o que vence.

No fim, o resumo mostra quantas tarefas ainda precisam da sua atenção. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com **Copiar Trabalho** e **Copiar Pessoal**. Para parar de receber o resumo, desative a opção correspondente.

## Privacidade

A notificação push vai diretamente da sua Machine para o dispositivo, com criptografia. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando [Com cuidado](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para que ele não seja enviado por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma linha simples pela Apple ou pelo Google e, em seguida, pede o título e a próxima etapa à sua Machine.
