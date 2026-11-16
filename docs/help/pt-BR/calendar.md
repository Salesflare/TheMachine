---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 93fe9794660b0ab2
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você delegou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) dos e-mails de reservas e ingressos.

Uma reunião que aparece em dois calendários é exibida uma vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais discreto, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro ou que duram vários dias aparecem como eventos de dia inteiro em cada dia que abrangem. Na Agenda, uma viagem aparece primeiro em cada um dos seus dias. Na Semana e no Mês, ela aparece como uma faixa que abrange todos os dias, por exemplo, "Viagem a Lisboa".

Um plano feito em conjunto é uma só promessa, marcada como "Com" e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução confirmou que ela foi concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** mostra cada dia. Role para baixo para ver os dias seguintes ou para cima, ou toque em **Mostrar dias anteriores**, para ver os dias anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo informa a data inicial. Depois que o [histórico](history.md) for carregado, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos. Toque em um dia para ver a lista de itens.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem prejudicar a leitura. Os demais aparecem como **+N**. Toque neles para abrir o dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma reunião com convidados, mostra os detalhes: quando, onde e quem participa. As pessoas que sua Graph conhece e as organizações e os projetos associados à reunião têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre a reunião no serviço correspondente. A visualização não altera nada.

Uma sala de reunião reservada para uma reunião aparece em Onde, nunca como uma pessoa nem na sua Graph.

O link de uma reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando um voo, hotel, trem, ônibus, balsa ou carro alugado aparece no seu e-mail, sua Machine adiciona a reserva a uma viagem. As reservas de uma mesma jornada ficam em uma só viagem: a ida, o hotel e a volta. A viagem aparece como uma faixa que abrange todos os dias. Abra-a para ver o código da reserva, o assento e o ingresso de cada reserva, em ordem cronológica.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um para cada ocasião, com o local, o código da reserva, o assento e a quantidade de ingressos. Um segundo pedido para o mesmo evento é adicionado ao evento existente. Um evento reservado pelo seu e-mail de trabalho é de Trabalho. Caso contrário, é Pessoal.

- Cada linha informa de quem veio a reserva, por exemplo, **Do Example Tickets**, e abre o e-mail correspondente.
- Se um e-mail gerou uma tarefa, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha correspondente, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.

A Machine lê os detalhes que companhias aéreas, hotéis, sites de reservas e vendedores de ingressos incluem nos e-mails de confirmação, sem usar IA. Um e-mail sem esses detalhes não gera nada. Os e-mails de reserva do ano coberto pelo [histórico](history.md) que sua Machine mantém são lidos em segundo plano depois que esse histórico é carregado.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e ações a fazer. **Transcrição** registra, palavra por palavra, o que foi dito. Ela começa recolhida e mostra a duração. Toque em **Mostrar** para abri-la.

Se não carregarem, elas tentam carregar de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções: **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O que você adiciona a uma parte permanece nela. Em uma reunião que você pode alterar, **Notas** abaixo do formulário abre as notas.

Com [Zoom](zoom.md) ou [Google Meet](google-meet.md) conectado, as notas do serviço aparecem em Notas e a transcrição, em Transcrição, com a indicação **Do Zoom** ou **Do Google Meet**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem chegar no evento da reunião no calendário, depois que ela começar, ou por e-mail do Zoom ou Gemini. Quando a reunião termina, The Machine cria tarefas com base nelas apenas para próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma só tarefa, com a reunião como origem: "Origem: notas da" reunião.

Uma reunião com transcrição, mas sem notas, mostra **Gerar notas**. The Machine cria as notas com base na transcrição: um resumo curto, decisões e ações a fazer, com os responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e The Machine continua trabalhando mesmo quando você fecha a reunião. Uma reunião longa leva alguns minutos e usa seu próprio modelo. As notas mostram **Escrito por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: "adicione esta transcrição à reunião de hoje do quadro". Uma transcrição vai para Transcrição, e um resumo, para Notas. No Calendário, uma reunião com notas ou transcrição mostra **Notas** ou **Transcrição**.

The Machine lê as duas para identificar os acompanhamentos da reunião. Eles são de Trabalho ou Pessoal, como a reunião, e só vão para sua equipe quando a reunião também for compartilhada com ela.

A reunião abre com esses detalhes onde quer que você a encontre: em uma linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google aqui. O Outlook e outros calendários são somente para visualização. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro os que você já usou e os das suas organizações, depois endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digita são enviadas para a busca. Escolha uma sugestão ou mantenha seu próprio texto.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. Quem receberá um convite aparece acima do botão, que informa quantas pessoas serão convidadas: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite ou uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma coleta. Ela mostra exatamente o que será alterado. A alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda sem reuniões? Se não tiver um calendário, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho se sobrepõe a algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode criar um rascunho curto de mensagem para reagendar ou sugerir que você recuse o convite. Nada é enviado até você aprovar.

Eventos de dia inteiro, com status livre ou provisório nunca contam, e cada conflito aparece uma única vez. Uma tarefa de Trabalho só informa que há um conflito, então sua equipe nunca vê o evento pessoal. Só você vê com qual evento ele conflita.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve com informações úteis:

- **Quem:** quem são, com base na sua Graph.
- **Último contato:** sua última conversa com elas. Depois da reunião, essa mensagem aparece como origem da tarefa.
- **Promessas em aberto:** o que você ou elas ainda precisam fazer.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado.

A tarefa chega na manhã de um dia útil: no próprio dia da reunião, se ela for à tarde, ou no dia útil anterior. Ela usa apenas o que já está na sua Machine. Serve apenas para consulta. Toque em **Feito** depois de ler. Uma promessa ou pergunta que exija uma ação tem sua própria tarefa.

Sem um histórico útil, nenhuma tarefa é criada. Reuniões recorrentes, internas, pessoais ou recusadas não geram tarefas. Se a reunião mudar de horário, a tarefa continua sendo a mesma, no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Os detalhes da reunião mostram a tarefa em **Tarefa**. Toque uma vez para abrir o chat dela.
