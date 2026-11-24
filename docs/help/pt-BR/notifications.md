---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar faz barulho. O resto fica em um único resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 3c469ec1032f6bea
---
Menos notificações ou de outro tipo? Em **Configurações**, **Notificações**, escolha onde cada tipo chega até você:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, um login necessário para uma tarefa ou uma pergunta do Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está esperando, quando voltam.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no seu celular ou computador), **Telegram** depois de configurar e **E-mail** em uma Machine hospedada ou em uma na The Machine Network. Todas ficam ativadas, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma aba: dias de trabalho, quando as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, um aviso no Telegram ou um e-mail só chega para:

- uma tarefa que vence hoje ou está marcada como urgente;
- uma resposta que alguém está esperando, em rascunho e pronta para enviar;
- uma tarefa que precisa que você faça login;
- um item adiado que voltou no horário escolhido.

Todo o resto aparece discretamente no painel (e sem aviso no Telegram) e espera pelo resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje faz barulho. No máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, você recebe apenas o resumo da manhã até voltar.

## Quando as notificações chegam

O sistema verifica se você está usando o painel, não apenas se ele está aberto:

- Em uso (na sua frente, e você clicou, digitou ou rolou a página nos últimos 10 minutos): nada faz barulho. O Telegram chega sem aviso. Só abrir ou recarregar o painel não conta.
- Ausente (em segundo plano, fechado ou sem atividade por 10 minutos): a notificação push chega um minuto depois que você sai, a menos que você volte e veja o item.
- Se nada chegar até você nos 15 minutos seguintes e não puder esperar: você recebe um e-mail sobre isso, no máximo um por hora. O que você já viu ou resolveu fica de fora, e cada tarefa aparece uma única vez, no estado atual. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Considera-se que algo chegou quando uma notificação aparece no celular ou navegador, ou quando o Telegram recebe a mensagem. Um celular desligado, sem conexão ou com as notificações desativadas não conta. O mesmo vale para o Telegram enquanto o painel está em uso. Se aparecer apenas no computador, o que for urgente ou vencer hoje ainda será enviado por e-mail: talvez você esteja longe do computador.
- Sem app no celular, notificações do navegador ou Telegram? O e-mail chega para tudo o que foi listado acima.
- Se não for possível acessar o Telegram: a notificação push é enviada mesmo assim, uma vez, e o sistema tenta enviar pelo Telegram novamente por conta própria.
- Se alguém da equipe passar uma tarefa para você e sua Machine não tiver celular ou Telegram para entrar em contato: você recebe um e-mail com o título e um link, 15 minutos depois, se ainda não tiver visto. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Fora do seu horário de trabalho: nada chega. O resumo da manhã inclui o item.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo do próximo dia de trabalho. A tarefa mostra quando vai chegar, como em “Notificação seg, 2 nov · 08:30”.

O progresso e as edições nunca geram notificações. Se houver um novo resultado em uma tarefa que você ainda não viu, ele é atualizado sem uma nova notificação. Vários avisos seguidos geram uma única notificação. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões das notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feito**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feito**.
- Resultado pronto: **Abrir**, **Marcar como feito**, **Adiar**.
- Precisa da sua resposta, está bloqueada ou exige login: **Responder**, **Abrir** ou **Fazer login**, depois **Adiar** e **Marcar como feito**.
- Lembrete: **Marcar como feito**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

O navegador e o Telegram mostram dois desses botões. Nas perguntas do Fleet, as opções **Responder** e **Recusar** ficam disponíveis.

Nada é enviado, pago ou submetido a partir de uma notificação. Um rascunho sempre é aberto primeiro para você conferir antes do envio. **Abrir rascunho** mostra a tarefa na sua lista com o rascunho completo. **Fazer** apenas inicia o trabalho em uma tarefa nova.

No app para celular, **Adiar** e **Marcar como feito** pedem que você desbloqueie o aparelho primeiro. No navegador, eles abrem o painel, que executa a ação e mostra a opção de desfazer. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para abrir (e para adiar o que está esperando). Eles apenas abrem o painel.

Ao tocar em uma notificação ou em **Abrir** no e-mail ou no Telegram, a tarefa aparece destacada na sua lista, onde quer que esteja agora: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. O chat nunca é aberto. Se a página ainda não estiver atualizada, ela acompanha a tarefa assim que estiver.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para mostrar. Se esse horário for anterior a **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega por push e e-mail, em um formato curto para ler rapidamente:

- uma saudação com o que importa hoje, como “Bom dia, Sam, há 2 respostas prontas para enviar” ou, para uma única tarefa, “Bom dia, Sam, aguardando sua aprovação: enviar o formulário do pedido”. Só contam como prontas as tarefas com um rascunho ou resultado para aprovar. Uma tarefa que primeiro precisa da sua resposta não conta;
- as tarefas contadas na saudação, cada uma com um link para abrir, e o que vence hoje. Caso contrário, no máximo três tarefas;
- até cinco tarefas que você mesmo adicionou e que estão esperando por você, independentemente do que a saudação conta;
- quantas outras tarefas podem esperar e quanto tempo levariam no seu ritmo, como “Mais 12 podem esperar, cerca de 5 min para resolver”. Tarefas que esperam sua resposta não entram nesse tempo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou em que The Machine ainda está trabalhando, só entra na contagem quando estiver esperando por você. A contagem corresponde às tarefas que estão esperando na sua lista.
- suas reuniões em uma linha.

**Abrir** mostra a tarefa destacada na sua lista, mesmo que esteja feita ou adiada. Uma promessa abre a tarefa correspondente ou, se ainda não houver uma, a página da própria promessa.

A notificação push mostra o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**, por padrão 15 minutos antes de **Até**, pelos canais escolhidos na opção acima. Só chega em um dia em que você esteve presente: usou o painel ou escolheu o que fazer com uma tarefa no painel, no Telegram, no chat ou por voz. Você não recebe o resumo em um dia sem tarefas concluídas ou reuniões realizadas.

Ele começa com um resumo do dia em números, como “Boa noite, Sam, 4 tarefas feitas hoje”, seguido de uma seção **Trabalho** e outra **Pessoal**. Se uma seção estiver vazia, ela não aparece. Um alerta sobre a própria sua Machine não aparece em nenhuma das duas. Cada seção tem:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois “+12 mais” e as reuniões do dia, como “+3 reuniões: reunião sobre preços e mais 2”;
- **Em aberto para amanhã** (na sexta-feira, para o próximo dia de trabalho): as primeiras reuniões e o que vence.

O resumo termina com o número de tarefas que ainda precisam da sua atenção. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com **Copiar Trabalho** e **Copiar Pessoal**. Para parar de receber, desative a opção correspondente.

## Privacidade

As notificações push são enviadas diretamente da sua Machine para o seu dispositivo, com criptografia. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando o modo [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para que ele não apareça nos e-mails.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) envia uma linha simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
