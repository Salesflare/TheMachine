---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar dispara uma notificação. O resto fica em um único resumo pela manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 334224e0b479ef47
---
Quer receber menos notificações ou outras? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, um acesso que uma tarefa precisa ou uma pergunta da Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando, quando voltarem.
- **Resumo da manhã**: um resumo breve do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no seu celular ou computador), **Telegram** depois de configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Todas ficam ativadas, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma guia: dias de trabalho, quando as notificações podem ser enviadas, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, uma notificação do Telegram ou um e-mail só é enviado quando há:

- uma tarefa que vence hoje ou foi marcada como urgente;
- uma resposta que alguém está esperando, preparada e pronta para enviar;
- uma tarefa que precisa que você faça login;
- um item adiado que voltou no horário que você escolheu.

Todo o resto aparece sem alarde no painel (e silenciosamente no Telegram) e espera pelo resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje dispara uma notificação. Você recebe no máximo 8 notificações push por dia. Se você não abrir o painel por 3 dias, só receberá o resumo da manhã até voltar.

## Quando as notificações são enviadas

O app verifica se você está usando o painel de verdade, não apenas se ele está aberto:

- Em uso (em primeiro plano, e você clicou, digitou ou rolou a página nos últimos 10 minutos): nenhuma notificação dispara. As notificações do Telegram chegam silenciosamente.
- Ausente (em segundo plano, fechado ou sem atividade há 10 minutos): uma notificação push é enviada um minuto depois que você sai, a menos que você volte e a veja.
- Se ainda não for vista 15 minutos depois e não puder esperar: você recebe um e-mail sobre ela, no máximo um por hora. O que você já resolveu fica de fora. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe atribuir uma tarefa a você e sua Machine não tiver um celular nem Telegram para entrar em contato: você recebe um e-mail com o título e um link, 15 minutos depois, se ainda não tiver visto a tarefa. Desative **E-mail** em **Resultados e perguntas** para não receber esses e-mails.
- Fora do seu horário de trabalho: nada. O resumo da manhã inclui o que aconteceu.
- Uma nova tarefa de trabalho em um dia de folga fica aguardando até o horário do resumo no próximo dia de trabalho. A tarefa mostra quando será enviada, por exemplo, Notificação seg., 2 de nov. · 08:30.

O progresso e as edições nunca geram notificações. Um novo resultado em uma tarefa que você ainda não viu atualiza a tarefa sem enviar outra notificação. Várias notificações de uma vez geram um único alerta. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Pergunta, tarefa bloqueada ou pedido de login: **Responder**, **Abrir** ou **Fazer login** e, depois, **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois desses botões. Nas perguntas da Fleet, **Responder** e **Recusar** continuam disponíveis.

Nada é enviado, pago ou enviado para análise por uma notificação. Um rascunho sempre abre primeiro, para você ver antes de ser enviado. **Abrir rascunho** mostra a tarefa na sua lista com o rascunho completo. **Fazer** só inicia o trabalho em uma nova tarefa.

No app para celular, **Adiar** e **Marcar como feito** pedem que você desbloqueie o aparelho primeiro. No navegador, eles abrem o painel, que executa a ação e mostra **Desfazer**. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para **Abrir** (e **Adiar** para o que está aguardando). Eles só abrem o painel.

Ao tocar em uma notificação ou em **Abrir** em um e-mail ou no Telegram, a tarefa aparece destacada na sua lista. Se ela já estiver feita, adiada ou em outra visualização, o chat dela será aberto.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário definido em **Resumo da manhã**, a menos que não haja nada para informar. Se esse horário for anterior a **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário, para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega como notificação push e e-mail, e é curto o bastante para você ler de relance:

- uma saudação com o que importa hoje, como “Bom dia, Sam, 2 respostas estão prontas para enviar” ou, se houver uma única tarefa, “Bom dia, Sam, está pronta para sua aprovação: enviar o formulário do pedido”;
- as tarefas mencionadas na saudação, cada uma com um link **Abrir**, e o que vence hoje; caso contrário, no máximo três tarefas;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como “Mais 12 podem esperar, cerca de 5 min para resolver”. O tempo não inclui tarefas que estão esperando sua resposta.
- suas reuniões em uma linha.

**Abrir** mostra a tarefa destacada na sua lista. Se ela já estiver feita, adiada ou em outra visualização, o chat dela será aberto. Uma promessa abre a tarefa correspondente ou, se ainda não houver uma, a página da promessa.

A notificação push mostra a mesma coisa, sem links. Toque nela ou no link no fim do e-mail para ler este resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos canais escolhidos na linha acima. Se você não tiver concluído nenhuma tarefa nem participado de nenhuma reunião naquele dia, não receberá o resumo. Ele começa com uma contagem do dia, como “Boa noite, Sam, 4 tarefas feitas hoje”, e depois mostra uma seção de **Trabalho** e outra de **Pessoal**. As seções sem conteúdo não aparecem. Cada uma inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, seguidas de “+12 mais” e das reuniões do dia, como “+3 reuniões: chamada sobre preços e mais 2”;
- **Em aberto para amanhã** (na sexta-feira, para o próximo dia de trabalho): as primeiras reuniões e o que vence.

O resumo termina informando quantas tarefas ainda precisam da sua atenção. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com **Copiar Trabalho** e **Copiar Pessoal**. Para parar de receber o resumo, desative a opção na linha correspondente.

## Privacidade

As notificações push vão diretamente da sua Machine para o dispositivo, criptografadas para ele. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando [Modo cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para que ele não seja enviado por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma linha sem formatação pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
