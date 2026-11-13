---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só notifica o que não pode esperar, o resto vai num único resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
---
Em **Configurações**, **Notificações**, escolha por tipo onde cada coisa chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou algo urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, um login que uma tarefa precisa, uma pergunta do Fleet.
- **Lembretes**: itens adiados e esperas que voltam.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que fica em aberto para amanhã. Veja abaixo.

Cada um tem um botão para **Push** (o app no seu celular ou computador), **Telegram** quando estiver configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Todos ficam ativados, menos os resumos no Telegram.

O **Horário de trabalho** fica na mesma aba: os seus dias de trabalho, as horas em que as notificações podem sair, quando os itens adiados voltam, o horário do resumo e o seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Um push, um aviso no Telegram ou um e-mail só sai para:

- uma tarefa que vence hoje, ou marcada como urgente;
- uma resposta que alguém está esperando, escrita e pronta para enviar;
- uma tarefa que precisa que você entre na sua conta;
- algo adiado que volta no horário que você escolheu.

Todo o resto chega em silêncio no painel (e sem som no Telegram) e espera o resumo da manhã. Num dia de folga, só notifica o que é urgente ou vence hoje. No máximo 8 push por dia. Depois de 3 dias sem abrir o painel, só chega o resumo da manhã, até você voltar.

## Quando ele notifica

Como o Slack, ele vê se você está usando o painel, não só se ele está aberto:

- Em uso: o painel está na sua frente, em foco, e você clicou, digitou, rolou ou tocou nele nos últimos 10 minutos. Nada vibra. O Telegram chega sem som.
- Longe: o painel está em segundo plano, minimizado, fechado ou parado há 10 minutos. Um push sai um minuto depois que você deixou o painel, a menos que você volte e veja antes.
- Ainda não visto 15 minutos depois, e não pode esperar: um e-mail para isso, no máximo um por hora. O que você já resolveu fica de fora. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Fora do seu horário de trabalho: nada. O resumo da manhã traz o que chegou.
- Uma nova tarefa de trabalho que chega num dia de folga espera o horário do resumo do seu próximo dia útil. A tarefa mostra onde e quando vai chegar até você, como Notificação seg, 2 nov · 08:30, conforme a linha **Novas tarefas**. Com Push e Telegram desligados ali, não mostra nada.

Só notifica o que precisa de você. Andamento e edições não. Um resultado mais novo numa tarefa que você ainda não viu a atualiza sem uma nova notificação. Várias de uma vez vibram uma vez só. O ícone do app mostra quantas tarefas precisam de você.

## Botões nas notificações

Cada notificação tem botões para o próximo passo. No app do celular:

- Nova tarefa: Fazer, Adiar, Marcar como feita.
- Rascunho pronto: Abrir rascunho, Adiar, Marcar como feita.
- Resultado pronto: Abrir, Marcar como feita, Adiar.
- Pergunta, travada ou login necessário: Responder, Abrir ou Entrar, depois Adiar e Marcar como feita.
- Lembrete: Marcar como feita, Adiar, Abrir.
- Resumo da manhã: toque para abrir.

Um navegador e o Telegram mostram dois deles. As perguntas do Fleet mantêm Responder uma vez e Recusar.

Nada é enviado, pago ou enviado para aprovação a partir de uma notificação. Um rascunho sempre abre primeiro, para você ver antes de sair. Abrir rascunho mostra a tarefa na sua lista com o rascunho completo. Fazer só começa o trabalho em uma tarefa nova.

No app, Adiar e Marcar como feita pedem para desbloquear primeiro. No navegador, eles abrem o painel, que faz isso e mostra Desfazer. Adiar traz a tarefa de volta em duas horas, ou amanhã de manhã em um lembrete.

Os e-mails com o que espera por você têm links Abrir e Adiar. Eles só abrem o painel.

Tocar em uma notificação, ou em Abrir em um e-mail ou no Telegram, mostra a tarefa destacada na sua lista. Se ela estiver feita, adiada ou em outra visão, abre o chat dela.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário do **Resumo da manhã**, a menos que não haja nada a dizer. Se for antes de **Itens adiados voltam às**, ele espera até 5 minutos depois, para incluir as tarefas que voltam naquela manhã. **Prévia**, na linha dele, mostra sem enviar. Por padrão é um push e um e-mail, curtos para ler de relance:

- um bom-dia com o que importa hoje, como "Bom dia, Sam: 2 respostas prontas para enviar" ou, para uma tarefa, "Bom dia, Sam. Para revisar: Enviar o formulário de pedido";
- as tarefas que o bom-dia conta, cada uma com um link Abrir, e o que vence hoje; senão, no máximo três coisas a fazer;
- quantas mais podem esperar e quanto tempo levam no seu ritmo, como "Mais 12 podem esperar, cerca de 5 min para resolver." As tarefas que esperam a sua resposta não entram nesse tempo.
- suas reuniões numa linha.

Abrir mostra a tarefa destacada na sua lista. Se ela estiver feita, adiada ou em outra visão, abre o chat dela. Uma promessa abre a tarefa dela, ou a própria página se ainda não tiver uma.

O push diz o mesmo sem links. Toque nele, ou no link no fim do e-mail, para ler este resumo de novo em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho no horário dele em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos meios que você escolher na linha dele acima. Um dia sem tarefa feita nem reunião realizada não recebe nenhum. Ele começa com o seu dia em um número, como "Boa noite, Sam: 4 tarefas feitas hoje", e depois uma parte **Trabalho** e uma parte **Pessoal**. Uma parte vazia fica de fora. Cada uma tem:

- **Feito hoje**: até três tarefas que você ou sua Machine terminaram, depois "+12 mais" e as reuniões do dia, como "+3 reuniões: Ligação de preços e mais 2";
- **Em aberto para amanhã** (numa sexta, seu próximo dia de trabalho): as primeiras reuniões e o que vence.

Ele termina com quantas tarefas ainda precisam de você. Toque na notificação push, ou no link no fim do e-mail, para ler de novo, com **Copiar Trabalho** e **Copiar Pessoal**. Para não receber, desative a linha dele.

## Privacidade

O push vai da sua Machine direto para o seu dispositivo, criptografado para esse dispositivo. O plano de controle nunca vê. O e-mail é enviado pelo servidor de e-mail da The Machine para o endereço da sua conta, então o texto passa por ele e pelo provedor de e-mail. Quando o modo [Cuidadoso](security-levels.md) esconde o texto das tarefas nas notificações, os e-mails só trazem números. Desative **E-mail** para um tipo para deixá-lo totalmente fora do e-mail.

Ative o push para um dispositivo em **Este dispositivo**, ou veja [Instalar o app](phone-app.md).
