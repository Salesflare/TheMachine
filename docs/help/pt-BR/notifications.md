---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar alerta. O resto vem em um resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 2146426abe3eaa50
---
Quer receber menos notificações ou outras notificações? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, uma tarefa que precisa de um acesso ou uma pergunta da Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando e que voltaram.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no celular ou computador), **Telegram** depois de configurado e **E-mail** em uma Machine hospedada ou em uma da The Machine Network. Todas ficam ativadas, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma aba: dias de trabalho, quando as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, um alerta do Telegram ou um e-mail só chega para:

- uma tarefa que vence hoje ou foi marcada como urgente;
- uma resposta que alguém está esperando, pronta para enviar;
- uma tarefa que precisa que você faça login;
- um adiamento que voltou no horário escolhido.

Todo o resto aparece discretamente no painel (e sem alerta no Telegram) e fica à espera do resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje gera um alerta. Você recebe no máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, você recebe apenas o resumo da manhã, até voltar.

## Quando as notificações chegam

O sistema verifica se você está usando o painel de verdade, não apenas se ele está aberto:

- Se você estiver usando (com o painel em primeiro plano e tiver clicado, digitado ou rolado nos últimos 10 minutos): nenhum alerta chega. As mensagens do Telegram chegam sem alerta. Só abrir ou recarregar o painel não conta.
- Se você estiver ausente (com o painel em segundo plano, fechado ou sem atividade há 10 minutos): uma notificação push chega um minuto depois que você sair, a menos que você volte e a veja.
- Se ainda não tiver sido vista 15 minutos depois e não puder esperar: você recebe um e-mail, no máximo um por hora. O que você já resolveu fica de fora. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe atribuir uma tarefa a você e sua Machine não tiver um telefone ou Telegram para entrar em contato: você recebe um e-mail com o título e um link, 15 minutos depois, se ainda não tiver visto a tarefa. Desative **E-mail** em **Resultados e perguntas** para não receber esse tipo de e-mail.
- Fora do seu horário de trabalho: nenhum alerta. A tarefa aparece no resumo da manhã.
- Uma nova tarefa de trabalho em um dia de folga fica à espera do horário do resumo do próximo dia de trabalho. A tarefa mostra quando será enviada, por exemplo: Notificação seg., 2 de nov. · 08:30.

Atualizações de progresso e edições nunca geram notificações. Se surgir um novo resultado em uma tarefa que você ainda não viu, ele a atualiza sem gerar outra notificação. Uma sequência de alertas gera apenas um. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Pergunta, tarefa bloqueada ou necessidade de fazer login: **Responder**, **Abrir** ou **Fazer login**, depois **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois desses botões. Nas perguntas da Fleet, as opções são **Responder uma vez** e **Recusar**.

Nada é enviado, pago ou enviado para avaliação a partir de uma notificação. Um rascunho sempre abre primeiro para você conferir antes de enviar. **Abrir rascunho** mostra a tarefa na sua lista, com o rascunho completo. **Fazer** só inicia o trabalho em uma nova tarefa.

No app para celular, **Adiar** e **Marcar como feito** pedem que você desbloqueie o aparelho primeiro. No navegador, eles abrem o painel, que conclui a ação e mostra **Desfazer**. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links **Abrir** (e **Adiar** para o que está à espera). Eles apenas abrem o painel.

Ao tocar em uma notificação ou em **Abrir** no e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja agora: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. O chat nunca é aberto. Se a página ainda não tiver atualizado, ela acompanha a tarefa assim que isso acontecer.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário definido em **Resumo da manhã**, a menos que não haja nada a informar. Se esse horário for antes de **Itens adiados voltam às**, ele espera até 5 minutos depois desse horário, para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega por notificação push e e-mail, e é curto o bastante para ler rapidamente:

- uma saudação com o que importa hoje, como “Bom dia, Sam, há 2 respostas prontas para enviar” ou, se houver uma tarefa, “Bom dia, Sam, aguardando sua aprovação: envie o formulário do pedido”;
- as tarefas incluídas na saudação, cada uma com um link **Abrir**, e o que vence hoje; caso contrário, até três coisas para fazer;
- até cinco tarefas que você mesmo adicionou e que dependem de você, independentemente do que a saudação incluir;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como “Mais 12 podem esperar, cerca de 5 min para resolver”. As tarefas que aguardam sua resposta não entram nesse tempo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou em que The Machine ainda está trabalhando, só entra na contagem quando depender de você. A contagem corresponde às tarefas que estão à espera na sua lista.
- suas reuniões em uma linha.

**Abrir** mostra a tarefa destacada na sua lista, mesmo que esteja concluída ou adiada. Uma promessa abre a tarefa correspondente ou, se ela ainda não tiver uma, a página da própria promessa.

A notificação push mostra o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos canais escolhidos na opção acima. Você não recebe um resumo em um dia sem tarefas concluídas ou reuniões realizadas. Ele começa com um resumo do dia em números, como “Boa noite, Sam, 4 tarefas feitas hoje”, seguido de uma parte de **Trabalho** e outra de **Pessoal**. As partes sem conteúdo não aparecem. Cada uma tem:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, seguidas de “+12 a mais” e pelas reuniões do dia, como “+3 reuniões: chamada sobre preços e mais 2”;
- **Em aberto para amanhã** (na sexta-feira, para o próximo dia de trabalho): as primeiras reuniões e o que vence.

No fim, ele mostra quantas tarefas ainda precisam de você. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com **Copiar Trabalho** e **Copiar Pessoal**. Para deixar de recebê-lo, desative essa opção.

## Privacidade

As notificações push vão direto da sua Machine para o seu dispositivo, criptografadas para ele. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para que ele não chegue por e-mail.

Ative as notificações push de um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) recebe uma notificação simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
