---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar gera um alerta. O resto fica em um resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4f777fac22dba7c0
---
Quer receber menos notificações ou outras notificações? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, um acesso que uma tarefa exige ou uma pergunta da Fleet.
- **Lembretes**: tarefas adiadas e respostas pelas quais você está esperando, quando voltarem.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no celular ou computador), **Telegram** depois de configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Tudo fica ativado, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma aba: dias de trabalho, horários em que as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, um alerta no Telegram ou um e-mail só é enviado quando:

- uma tarefa vence hoje ou está marcada como urgente;
- alguém está esperando uma resposta que foi preparada e está pronta para enviar;
- uma tarefa precisa que você faça login;
- uma tarefa adiada volta no horário escolhido.

Todo o resto aparece em silêncio no painel (e silenciosamente no Telegram) e fica à espera do resumo da manhã. Em um dia de folga, só o que for urgente ou vencer hoje gera um alerta. São enviados no máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, você recebe apenas o resumo da manhã, até voltar.

## Quando as notificações chegam

O sistema verifica se você está usando o painel de verdade, não apenas se ele está aberto:

- Em uso (na tela, e você clicou, digitou ou rolou nos últimos 10 minutos): nada gera um alerta. As mensagens do Telegram chegam silenciosamente. Só abrir ou recarregar o painel não conta.
- Ausente (em segundo plano, fechado ou sem atividade por 10 minutos): uma notificação push chega um minuto depois que você sai, a menos que volte e veja a notificação.
- Se ainda não tiver sido vista 15 minutos depois e não puder esperar, você recebe um e-mail sobre ela, no máximo um por hora. O que você já resolveu fica de fora. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se uma pessoa da equipe atribuir uma tarefa a você e sua Machine não tiver um celular ou Telegram para entrar em contato, você recebe um e-mail com o título e um link, 15 minutos depois, se ainda não tiver visto a tarefa. Desative **E-mail** em **Resultados e perguntas** para desativar isso.
- Fora do seu horário de trabalho: nada. O resumo da manhã inclui o que ficou pendente.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo do próximo dia de trabalho. A tarefa mostra quando será enviada, por exemplo: Notificação seg., 2 de nov. · 08:30.

O progresso e as edições nunca geram notificações. Se surgir um novo resultado para uma tarefa que você ainda não viu, ele é atualizado sem uma nova notificação. Vários alertas de uma vez geram apenas uma notificação. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Pergunta, tarefa bloqueada ou pedido para fazer login: **Responder**, **Abrir** ou **Entrar**, depois **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois desses botões. Nas perguntas da Fleet, continuam disponíveis **Responder uma vez** e **Recusar**.

Nada é enviado, pago ou submetido por uma notificação. Um rascunho sempre abre primeiro, para você conferir antes do envio. **Abrir rascunho** mostra a tarefa na sua lista com o rascunho completo. **Fazer** só inicia o trabalho em uma tarefa nova.

No app para celular, é preciso desbloquear o dispositivo antes de **Adiar** ou **Marcar como feito**. No navegador, essas opções abrem o painel, que executa a ação e mostra **Desfazer**. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para **Abrir** (e **Adiar** para o que está pendente). Eles apenas abrem o painel.

Ao tocar em uma notificação, ou em **Abrir** em um e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. O chat nunca é aberto. Se a página ainda não estiver atualizada, ela acompanha a tarefa assim que estiver.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para informar. Se esse horário for anterior a **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário, para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega como notificação push e e-mail, curto o bastante para ler de relance:

- uma saudação com o que importa hoje, como “Bom dia, Sam, há 2 respostas prontas para enviar” ou, para uma tarefa, “Bom dia, Sam, aguarda sua aprovação: enviar o formulário de pedido”;
- as tarefas mencionadas na saudação, cada uma com um link para abrir, e o que vence hoje; se não houver nada disso, até três tarefas;
- tarefas que você mesmo adicionou e que dependem de você, até cinco, independentemente do que a saudação menciona;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como “Mais 12 podem esperar, cerca de 5 min para resolver.” Tarefas que esperam uma resposta sua não entram nesse cálculo, e uma tarefa adiada que vence hoje só é contada quando voltar.
- suas reuniões, em uma linha.

**Abrir** mostra a tarefa destacada na sua lista, inclusive se estiver concluída ou adiada. Uma promessa abre a tarefa correspondente ou, se ela ainda não existir, a página da própria promessa.

A notificação push mostra o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos meios escolhidos na opção acima. Se você não tiver concluído nenhuma tarefa nem participado de uma reunião naquele dia, não recebe o resumo. Ele começa com uma contagem do dia, como “Boa noite, Sam, 4 tarefas concluídas hoje”, seguida de uma seção de **Trabalho** e outra de **Pessoal**. Se uma seção não tiver conteúdo, ela não aparece. Cada uma inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois “+12 outras” e as reuniões do dia, como “+3 reuniões: ligação sobre preços e mais 2”;
- **Em aberto para amanhã** (na sexta-feira, para o próximo dia de trabalho): as primeiras reuniões e o que vence.

No fim, aparece quantas tarefas ainda precisam da sua atenção. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com **Copiar Trabalho** e **Copiar Pessoal**. Para parar de receber, desative essa opção.

## Privacidade

As notificações push vão da sua Machine diretamente para o dispositivo, criptografadas para ele. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para não recebê-lo por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou consulte [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma linha de texto simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
