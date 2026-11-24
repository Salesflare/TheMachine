---
title: Notificações
area: settings
summary: Escolha o que você recebe, onde e quando. Só o que não pode esperar gera um alerta; o resto aparece em um único resumo pela manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: bdb4ecec9446aa5e
---
Quer receber menos notificações ou notificações diferentes? Em **Configurações**, na guia **Notificações**, escolha onde receber cada tipo:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, uma tarefa que precisa que você entre na sua conta ou uma pergunta do Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no seu celular ou computador), **Telegram** quando estiver configurado e **E-mail** em uma Machine hospedada ou em uma na The Machine Network. Todas estão ativadas, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma guia: dias de trabalho, horários em que as notificações podem ser enviadas, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, uma notificação no Telegram ou um e-mail só é enviado quando:

- uma tarefa vence hoje ou está marcada como urgente;
- uma resposta que alguém está esperando foi escrita e está pronta para enviar;
- uma tarefa precisa que você entre na sua conta;
- um item adiado volta no horário escolhido.

Todo o resto aparece sem alerta no painel (e silenciosamente no Telegram) e fica à espera do resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje gera um alerta. Você recebe no máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, você recebe apenas o resumo da manhã até voltar.

## Quando as notificações são enviadas

O sistema verifica se você está usando o painel, não apenas se ele está aberto:

- Se você estiver usando o painel (com ele em primeiro plano e depois de clicar, digitar ou rolar nos últimos 10 minutos), nada gera um alerta. As notificações no Telegram chegam silenciosamente. Só abrir ou recarregar o painel não conta.
- Se você estiver ausente (o painel estiver em segundo plano, fechado ou sem atividade por 10 minutos), uma notificação push é enviada um minuto depois que você sair, a menos que volte e veja a notificação.
- Se você ainda não tiver visto a notificação 15 minutos depois e ela não puder esperar, será enviado um e-mail, no máximo um por hora. O que você já resolveu não aparece no e-mail, e cada tarefa aparece uma única vez, com o status atual. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe atribuir uma tarefa a você e não houver um celular nem Telegram para entrar em contato, será enviado um e-mail com o título e um link, 15 minutos depois, caso você ainda não tenha visto a tarefa. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Fora do seu horário de trabalho, nada é enviado. O resumo da manhã inclui essas tarefas.
- Uma nova tarefa de trabalho em um dia de folga fica para o horário do resumo do próximo dia de trabalho. A tarefa mostra quando você vai recebê-la, por exemplo: Notificação seg., 2 de nov. · 08:30.

O progresso e as edições nunca geram notificações. Se houver um novo resultado em uma tarefa que você ainda não viu, ele atualiza a tarefa sem gerar outra notificação. Uma sequência de notificações gera um único alerta. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: Fazer, Adiar, Marcar como feito.
- Rascunho pronto: Abrir rascunho, Adiar, Marcar como feito.
- Resultado pronto: Abrir, Marcar como feito, Adiar.
- Precisa da sua resposta, está com um problema ou precisa que você entre na sua conta: Responder, Abrir ou Entrar, depois Adiar e Marcar como feito.
- Lembrete: Marcar como feito, Adiar, Abrir.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois desses botões. As perguntas do Fleet continuam com as opções Responder uma vez e Recusar.

Nada é enviado, pago ou entregue a partir de uma notificação. Um rascunho sempre é aberto primeiro, para você ver antes de enviar. Abrir rascunho mostra a tarefa na sua lista, com o rascunho completo. Fazer só inicia o trabalho em uma nova tarefa.

No app para celular, Adiar e Marcar como feito pedem que você desbloqueie o app primeiro. No navegador, os botões abrem o painel, onde a ação é realizada e a opção Desfazer aparece. Adiar faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para abrir as tarefas (e para adiar o que está à espera). Eles só abrem o painel.

Ao tocar em uma notificação, ou em Abrir no e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. A notificação nunca abre o chat. Se a página ainda não estiver atualizada, ela acompanha a tarefa assim que for.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário definido em **Resumo da manhã**, a menos que não haja nada para mostrar. Se esse horário for antes de **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega como notificação push e por e-mail, em um formato curto para você ler rapidamente:

- uma saudação com o que importa hoje, como "Bom dia, Sam, há 2 respostas prontas para enviar" ou, se houver uma tarefa, "Bom dia, Sam, aguardando sua aprovação: Enviar o formulário do pedido". Só contam como prontas as tarefas com um rascunho ou resultado para aprovar. Uma tarefa que precisa primeiro da sua resposta não conta;
- as tarefas incluídas na saudação, cada uma com um link Abrir, e o que vence hoje. Caso contrário, no máximo três coisas para fazer;
- até cinco tarefas que você adicionou e que estão à sua espera, independentemente do que a saudação inclui;
- quantas outras tarefas podem esperar e quanto tempo você levará para resolvê-las no seu ritmo, por exemplo: "Mais 12 podem esperar, leva cerca de 5 min para resolver". As tarefas que esperam sua resposta não entram nesse cálculo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou em que The Machine ainda está trabalhando, só é contada quando estiver à sua espera. O total corresponde às tarefas que estão à sua espera na lista;
- suas reuniões em uma linha.

Abrir mostra a tarefa destacada na sua lista, mesmo que esteja concluída ou adiada. Uma promessa abre a tarefa correspondente ou, se ainda não houver uma, a página da promessa.

A notificação push traz o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos meios escolhidos na opção acima. Ele só chega em um dia em que você esteve presente: usou o painel ou tomou uma decisão sobre uma tarefa nele, no Telegram, no chat ou por voz. Se não houver nenhuma tarefa concluída nem reunião realizada naquele dia, você não recebe o resumo.

O resumo começa com uma contagem do dia, como "Boa noite, Sam, 4 tarefas feitas hoje", seguida de uma seção **Trabalho** e outra **Pessoal**. Se uma seção não tiver nada, ela não aparece. Um alerta sobre a sua Machine não aparece em nenhuma das duas. Cada seção inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois "+12 mais" e as reuniões do dia, como "+3 reuniões: reunião sobre preços e mais 2";
- **Em aberto para amanhã** (ou para o próximo dia de trabalho, se for sexta-feira): as próximas reuniões e o que vence.

No fim, o resumo informa quantas tarefas ainda precisam da sua atenção. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com as opções **Copiar Trabalho** e **Copiar Pessoal**. Para parar de recebê-lo, desative a opção correspondente.

## Privacidade

As notificações push são enviadas diretamente da sua Machine para o dispositivo, com criptografia. Os e-mails passam pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando o modo [Cuidadosa](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para não recebê-lo por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma linha de texto simples pela Apple ou pelo Google e depois pede à sua Machine o título e a próxima etapa.
