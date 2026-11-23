---
title: Notificações
area: settings
summary: Escolha o que chega até você, por onde e quando. Só o que não pode esperar gera um alerta; o resto fica em um resumo pela manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: febea6f9eb2c331a
---
Quer receber menos notificações ou mudar quais recebe? Em **Configurações**, **Notificações**, escolha por onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, uma tarefa que precisa que você entre em uma conta ou uma pergunta do Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando, quando voltarem.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no celular ou computador), **Telegram** depois de configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Tudo vem ativado, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma aba: dias de trabalho, quando as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, um alerta no Telegram ou um e-mail só chega para:

- uma tarefa que vence hoje ou foi marcada como urgente;
- uma resposta que alguém está esperando, escrita e pronta para enviar;
- uma tarefa que precisa que você entre em uma conta;
- um item adiado que voltou no horário escolhido.

Todo o resto aparece discretamente no painel (e sem alerta no Telegram) e espera pelo resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje gera um alerta. São no máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, você só recebe o resumo da manhã até voltar.

## Quando as notificações chegam

O app verifica se você está usando o painel, não apenas se ele está aberto:

- Em uso (na tela, e você clicou, digitou ou rolou nos últimos 10 minutos): nada gera alerta. As mensagens do Telegram chegam sem alerta. Só abrir ou recarregar o painel não conta.
- Ausente (em segundo plano, fechado ou sem atividade por 10 minutos): uma notificação push chega um minuto depois que você sai, a menos que volte e a veja.
- Se ainda não tiver sido vista 15 minutos depois e não puder esperar: chega um e-mail, no máximo um por hora. O que você já resolveu fica de fora, e cada tarefa aparece uma única vez, com o estado atual. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe atribuir uma tarefa a você e sua Machine não tiver um celular ou Telegram para entrar em contato: chega um e-mail com o título e um link, 15 minutos depois, se a tarefa ainda não tiver sido vista. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Fora do seu horário de trabalho: nada. O resumo da manhã inclui esses itens.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo no próximo dia de trabalho. A tarefa mostra quando chegará até você, por exemplo: Notificação seg., 2 de nov. · 08:30.

Atualizações de progresso e edições nunca geram notificações. Se houver um novo resultado em uma tarefa que você ainda não viu, ele será atualizado sem uma nova notificação. Um grupo de notificações chega como um único alerta. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Pergunta, tarefa bloqueada ou necessidade de entrar em uma conta: **Responder**, **Abrir** ou **Entrar**, depois **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque nele para abrir.

O navegador e o Telegram mostram dois desses botões. Nas perguntas do Fleet, sempre aparecem **Responder** e **Recusar**.

Nenhuma notificação envia, paga ou envia algo para análise. Um rascunho sempre abre primeiro, para você conferir antes do envio. **Abrir rascunho** mostra a tarefa na sua lista, com o rascunho completo. **Fazer** só inicia o trabalho em uma tarefa nova.

No app para celular, **Adiar** e **Marcar como feito** pedem que você desbloqueie o aparelho primeiro. No navegador, eles abrem o painel, que executa a ação e mostra **Desfazer**. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para **Abrir** e, no caso do que está aguardando, para **Adiar**. Eles só abrem o painel.

Ao tocar em uma notificação ou em **Abrir** no e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja agora: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. O chat nunca abre. Se a página ainda não estiver atualizada, ela acompanha a tarefa assim que estiver.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para dizer. Se esse horário for antes de **Itens adiados voltam às**, o resumo espera até 5 minutos depois, para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega como notificação push e por e-mail, e é curto o bastante para ler rapidamente:

- uma saudação com o que importa hoje, como “Bom dia, Sam. 2 respostas estão prontas para enviar” ou, para uma tarefa, “Bom dia, Sam. Pronta para sua aprovação: enviar o formulário do pedido”. Só contam como prontas as tarefas com um rascunho ou resultado para aprovar. Uma tarefa que primeiro precisa da sua resposta não conta;
- as tarefas incluídas na saudação, cada uma com um link para **Abrir**, e o que vence hoje; caso contrário, no máximo três coisas para fazer;
- até cinco tarefas que você mesmo adicionou e que estão esperando por você, independentemente do que a saudação contabiliza;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como “Mais 12 podem esperar, cerca de 5 min para resolver”. As tarefas que aguardam sua resposta não entram nesse tempo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou que The Machine ainda está resolvendo, só entra na contagem quando estiver esperando por você. A contagem corresponde às tarefas que estão esperando na sua lista.
- seus compromissos, em uma linha.

**Abrir** mostra a tarefa destacada na sua lista, mesmo que esteja concluída ou adiada. Uma promessa abre a tarefa correspondente ou, se ainda não houver uma, a página da própria promessa.

A notificação push traz o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**. Por padrão, chega 15 minutos antes de **Até**, pelos meios escolhidos na linha acima. Só chega em um dia em que você esteve por lá: usou o painel ou tomou uma decisão sobre uma tarefa no painel, no Telegram, no chat ou por voz. Se não concluiu nenhuma tarefa nem teve reuniões, não recebe o resumo.

Ele começa com um resumo do dia em números, como “Boa noite, Sam. 4 tarefas feitas hoje”, seguido de uma seção **Trabalho** e outra **Pessoal**. Se uma seção não tiver conteúdo, ela não aparece. Cada uma inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois “+12 outras” e as reuniões do dia, como “+3 reuniões: conversa sobre preços e mais 2”;
- **Em aberto para amanhã** (ou para o próximo dia de trabalho, se for sexta-feira): as primeiras reuniões e o que vence.

No fim, mostra quantas tarefas ainda precisam de você. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com **Copiar Trabalho** e **Copiar Pessoal**. Para parar de receber, desative a opção correspondente.

## Privacidade

As notificações push vão da sua Machine direto para o dispositivo, com criptografia. Os e-mails passam pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para que ele não chegue por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) recebe uma notificação simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
