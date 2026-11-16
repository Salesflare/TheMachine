---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar gera um alerta. O resto fica em um único resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: ee3ba81a8441704f
---
Quer receber menos notificações ou de outro tipo? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, uma tarefa que precisa que você entre em uma conta ou uma pergunta da Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando e voltaram.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no seu celular ou computador), **Telegram** depois de configurado e **E-mail** em uma Machine hospedada ou em uma Machine na The Machine Network. Todas ficam ativadas, exceto os resumos no Telegram.

Seu **Horário de trabalho** também fica na mesma aba: dias de trabalho, quando as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, um alerta no Telegram ou um e-mail só chega quando há:

- uma tarefa com vencimento hoje ou marcada como urgente;
- uma resposta que alguém está esperando, preparada e pronta para enviar;
- uma tarefa que precisa que você entre em uma conta;
- um item adiado que voltou no horário escolhido.

Todo o resto aparece discretamente no painel e sem alertas no Telegram, aguardando o resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje gera um alerta. São no máximo 8 notificações push por dia. Se você passar 3 dias sem abrir o painel, só receberá o resumo da manhã até voltar.

## Quando as notificações chegam

O app verifica se você está usando o painel de verdade, não apenas se ele está aberto:

- Em uso (em primeiro plano, e você clicou, digitou ou rolou a página nos últimos 10 minutos): nada gera alertas. As mensagens do Telegram chegam sem som.
- Ausente (em segundo plano, fechado ou sem atividade por 10 minutos): uma notificação push chega um minuto depois que você sai, a menos que volte e veja a notificação.
- Se ainda não tiver sido vista depois de 15 minutos e não puder esperar, você recebe um e-mail, no máximo um por hora. O que você já resolveu não aparece. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe atribuir uma tarefa a você e sua Machine não tiver um celular ou Telegram para entrar em contato, você recebe um e-mail com o título da tarefa e um link, 15 minutos depois, se ainda não tiver sido vista. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Fora do seu horário de trabalho: nada. O resumo da manhã inclui esses itens.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo do seu próximo dia de trabalho. A tarefa mostra quando será enviada, por exemplo: Notificação seg., 2 de nov. · 08:30.

O progresso e as edições nunca geram notificações. Se surgir um novo resultado em uma tarefa que você ainda não viu, ele atualiza a tarefa sem gerar outra notificação. Uma série de atualizações gera apenas um alerta. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Feito**.
- Resultado pronto: **Abrir**, **Feito**, **Adiar**.
- Pergunta, problema ou pedido para entrar em uma conta: **Responder**, **Abrir** ou **Entrar**, depois **Adiar** e **Feito**.
- Lembrete: **Feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois desses botões. Nas perguntas da Fleet, as opções **Responder** e **Recusar** continuam disponíveis.

Nada é enviado, pago ou enviado para análise a partir de uma notificação. Um rascunho sempre abre primeiro, para você ver antes de ser enviado. **Abrir rascunho** mostra a tarefa na sua lista, com o rascunho completo. **Fazer** apenas inicia o trabalho em uma nova tarefa.

No app para celular, é preciso desbloquear o aparelho antes de usar **Adiar** e **Feito**. No navegador, essas opções abrem o painel, onde a ação é realizada e você pode desfazê-la. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para abrir (e para adiar o que estiver aguardando). Eles só abrem o painel.

Ao tocar em uma notificação, ou em **Abrir** em um e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja naquele momento: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. A notificação nunca abre o chat. Se a página ainda não estiver atualizada, ela acompanha a tarefa assim que for atualizada.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para informar. Se esse horário for anterior a **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário para incluir as tarefas que voltaram naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega por notificação push e e-mail e é curto o bastante para você ler rapidamente:

- uma saudação com o que importa naquele dia, como “Bom dia, Sam. Há 2 respostas prontas para enviar” ou, se houver uma tarefa, “Bom dia, Sam. Pronta para sua aprovação: enviar o formulário do pedido”;
- as tarefas mencionadas na saudação, cada uma com um link para abrir, e o que vence hoje; se não houver, no máximo três tarefas;
- até cinco tarefas que você mesmo adicionou e que estão aguardando sua atenção, independentemente do que a saudação menciona;
- quantas outras tarefas podem esperar e quanto tempo levaria para resolvê-las no seu ritmo, como “Há mais 12 tarefas que podem esperar. Leva cerca de 5 min para resolver.” As tarefas que aguardam uma resposta sua não entram nesse tempo, e uma tarefa adiada que vence hoje só é contada quando voltar;
- uma linha com suas reuniões.

**Abrir** mostra a tarefa destacada na sua lista, mesmo se estiver feita ou adiada. Uma promessa abre a tarefa correspondente ou, se ela ainda não tiver uma, abre a página da promessa.

A notificação push mostra o mesmo conteúdo, sem links. Toque nela ou no link no final do e-mail para ver esse resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez por dia de trabalho, no horário definido em **Horário de trabalho**, que por padrão é 15 minutos antes de **Até**, pelos meios escolhidos na linha acima. Se você não tiver concluído nenhuma tarefa nem participado de reuniões naquele dia, não receberá o resumo. Ele começa com uma contagem do dia, como “Boa noite, Sam. 4 tarefas feitas hoje”, seguida de uma seção de **Trabalho** e outra de **Pessoal**. As seções sem conteúdo não aparecem. Cada uma inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois “+12 outras” e as reuniões do dia, como “+3 reuniões: chamada sobre preços e mais 2”;
- **Em aberto para amanhã** (ou para o próximo dia de trabalho, se for sexta-feira): as próximas reuniões e o que vence.

No final, aparece quantas tarefas ainda precisam da sua atenção. Toque na notificação push ou no link no final do e-mail para ler o resumo de novo, com **Copiar Trabalho** e **Copiar Pessoal**. Para deixar de recebê-lo, desative a opção correspondente.

## Privacidade

A notificação push vai da sua Machine diretamente para o seu dispositivo, criptografada para ele. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando o modo [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para não recebê-la por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma mensagem simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
