---
title: Notificações
area: settings
summary: O que chega até você, onde e quando: só o que não pode esperar faz barulho. O resto vai para um único resumo da manhã.
covers: settings:notify
code: notify.py, dashboard.html, assistant.py, sw.js
order: 2
keywords: alerts, notify, ping, buzz, quiet, too many, push, sound, interrupt
translated: 4a782ad03270e7b0
---
Quer receber menos notificações ou receber outras? Em **Configurações**, **Notificações**, escolha onde receber cada tipo:

- **Novas tarefas**: só o que não pode esperar, como algo que vence hoje ou é urgente.
- **Resultados e perguntas**: uma resposta pronta para enviar, um login que uma tarefa exige ou uma pergunta do Fleet.
- **Lembretes**: tarefas adiadas e respostas que você está aguardando, quando voltarem.
- **Resumo da manhã**: um resumo curto do seu dia. Veja abaixo.
- **Resumo do fim do dia**: o que foi feito hoje e o que ficou em aberto para amanhã. Veja abaixo.

Cada tipo tem uma opção para **Push** (o app no celular ou computador), **Telegram** quando estiver configurado e **E-mail** em uma Machine hospedada ou em uma na The Machine Network. Tudo fica ativado, exceto os resumos no Telegram.

Seu **Horário de trabalho** fica na mesma aba: dias de trabalho, quando as notificações podem chegar, quando os itens adiados voltam, os horários dos resumos e seu fuso horário. Veja [Horário de trabalho](work-hours.md).

## Só o que não pode esperar

Uma notificação push, um aviso no Telegram ou um e-mail só chega quando há:

- uma tarefa que vence hoje ou foi marcada como urgente;
- uma resposta que alguém está aguardando, preparada e pronta para enviar;
- uma tarefa que exige que você faça login;
- um item adiado que voltou no horário escolhido.

Todo o resto aparece silenciosamente no painel (e sem aviso no Telegram) e espera pelo resumo da manhã. Em um dia de folga, só o que é urgente ou vence hoje faz barulho. Você recebe no máximo 8 notificações push por dia. Depois de 3 dias sem abrir o painel, só chega o resumo da manhã, até você voltar.

## Quando as notificações chegam

O sistema verifica se você está usando o painel de verdade, não apenas se ele está aberto:

- Em uso (na tela e com algum clique, texto digitado ou rolagem nos últimos 10 minutos): nada faz barulho. O Telegram chega sem aviso. Só abrir ou recarregar o painel não conta.
- Ausente (em segundo plano, fechado ou sem atividade por 10 minutos): a notificação push chega um minuto depois que você sai, a menos que você volte e veja antes.
- Se ainda não tiver sido vista 15 minutos depois e não puder esperar: chega um e-mail sobre ela, no máximo um por hora. O que você já resolveu fica de fora. Na maioria dos dias, o resumo da manhã é o único e-mail.
- Se alguém da equipe passar uma tarefa para você e sua Machine não tiver um celular ou Telegram para entrar em contato: chega um e-mail com o título e um link, 15 minutos depois, se ainda não tiver sido vista. Desative **E-mail** em **Resultados e perguntas** para não receber esse e-mail.
- Fora do seu horário de trabalho: nada chega. O resumo da manhã inclui o que ficou pendente.
- Uma nova tarefa de trabalho em um dia de folga espera até o horário do resumo no seu próximo dia de trabalho. A tarefa mostra quando chegará até você, como Notificação seg., 2 de nov. · 08:30.

Atualizações de progresso e edições nunca geram notificações. Um novo resultado em uma tarefa que você ainda não viu atualiza a tarefa sem gerar outra notificação. Várias notificações de uma só vez geram um único aviso. O ícone do app mostra quantas tarefas precisam da sua atenção.

## Botões nas notificações

Cada notificação tem botões para a próxima etapa. No app para celular:

- Nova tarefa: **Fazer**, **Adiar**, **Marcar como feita**.
- Rascunho pronto: **Abrir rascunho**, **Adiar**, **Marcar como feita**.
- Resultado pronto: **Abrir**, **Marcar como feita**, **Adiar**.
- Pergunta, problema ou pedido de login: **Responder**, **Abrir** ou **Entrar**, depois **Adiar** e **Marcar como feita**.
- Lembrete: **Marcar como feita**, **Adiar**, **Abrir**.
- Resumo da manhã: toque para abrir.

No navegador e no Telegram, aparecem dois desses botões. As perguntas do Fleet mantêm **Responder uma vez** e **Recusar**.

Nada é enviado, pago ou submetido a partir de uma notificação. Um rascunho sempre abre primeiro para você conferir antes do envio. **Abrir rascunho** mostra a tarefa na sua lista com o rascunho completo. **Fazer** só inicia o trabalho em uma tarefa nova.

No app para celular, **Adiar** e **Marcar como feita** pedem que você desbloqueie o celular primeiro. No navegador, abrem o painel, onde a ação é realizada e aparece **Desfazer**. **Adiar** faz a tarefa voltar em duas horas ou, no caso de um lembrete, na manhã seguinte.

Os e-mails têm links para **Abrir** (e para **Adiar** no caso do que está pendente). Eles só abrem o painel.

Ao tocar em uma notificação, ou em **Abrir** no e-mail ou no Telegram, a tarefa aparece na sua lista, destacada, onde quer que esteja naquele momento: **Feito agora**, **Feito**, **Volta mais tarde** ou outra visualização. O chat nunca é aberto. Se a página ainda não tiver atualizado, ela acompanha a tarefa assim que isso acontecer.

## O resumo da manhã

Ele chega nos dias de trabalho, no horário de **Resumo da manhã**, a menos que não haja nada para informar. Se esse horário for antes de **Itens adiados voltam às**, o resumo espera até 5 minutos depois desse horário para incluir as tarefas que voltam naquela manhã. **Prévia** mostra o resumo sem enviá-lo. Por padrão, ele chega por push e e-mail e é curto o bastante para uma leitura rápida:

- uma saudação com o que importa naquele dia, como “Bom dia, Sam, 2 respostas estão prontas para enviar” ou, para uma tarefa, “Bom dia, Sam, esperando sua aprovação: enviar o formulário do pedido”. Só contam como prontas as tarefas com um rascunho ou resultado para aprovar; uma que precisa primeiro da sua resposta não conta;
- as tarefas mencionadas na saudação, cada uma com um link para abrir, e o que vence hoje; caso contrário, no máximo três tarefas;
- até cinco tarefas que você mesmo adicionou e que dependem de você, independentemente do que a saudação menciona;
- quantas outras tarefas podem esperar e quanto tempo levam no seu ritmo, como “Mais 12 podem esperar, cerca de 5 min para resolver”. As tarefas que esperam sua resposta não entram nesse tempo. Uma tarefa que vence hoje, mas foi adiada para mais tarde, ou na qual The Machine ainda está trabalhando, só entra na contagem quando depender de você. A contagem corresponde às tarefas que estão aguardando na sua lista.
- suas reuniões, em uma linha.

**Abrir** mostra a tarefa na sua lista, destacada, mesmo que esteja feita ou adiada. Uma promessa abre a tarefa correspondente ou, se ainda não houver uma, a página da própria promessa.

A notificação push tem o mesmo conteúdo, sem links. Toque nela ou no link no fim do e-mail para ler o resumo novamente em **Tarefas**.

## O resumo do fim do dia

Ele chega uma vez nos dias de trabalho, no horário definido em **Horário de trabalho**. Por padrão, chega 15 minutos antes de **Até**, pelos meios escolhidos na opção acima. Só chega em um dia em que você esteve presente: usou o painel ou tomou uma decisão sobre uma tarefa lá, no Telegram, no chat ou por voz. Se nenhuma tarefa foi concluída nem houve reunião, você não recebe o resumo.

Ele começa com um resumo do dia em números, como “Boa noite, Sam, 4 tarefas feitas hoje”, depois traz uma seção de **Trabalho** e outra de **Pessoal**. Se uma seção estiver vazia, ela não aparece. Cada seção inclui:

- **Feito hoje**: até três tarefas concluídas por você ou pela sua Machine, depois “+12 outras” e as reuniões do dia, como “+3 reuniões: conversa sobre preços e mais 2”;
- **Em aberto para amanhã** (ou para o próximo dia de trabalho, se for sexta-feira): as primeiras reuniões e o que vence.

No fim, ele informa quantas tarefas ainda precisam de você. Toque na notificação push ou no link no fim do e-mail para ler o resumo novamente, com as opções **Copiar Trabalho** e **Copiar Pessoal**. Para parar de recebê-lo, desative a opção correspondente.

## Privacidade

A notificação push vai diretamente da sua Machine para o dispositivo, criptografada para ele. O e-mail passa pelo servidor de e-mail da The Machine e pelo seu provedor de e-mail. Quando o nível [Cuidadoso](security-levels.md) oculta o texto das tarefas nas notificações, os e-mails mostram apenas as contagens. Desative **E-mail** para um tipo de notificação para não recebê-lo por e-mail.

Ative as notificações push para um dispositivo em **Este dispositivo** ou veja [Instalar o app](phone-app.md). O [app para celular](mobile-app.md) recebe uma linha de texto simples pela Apple ou pelo Google e, em seguida, pede à sua Machine o título e a próxima etapa.
