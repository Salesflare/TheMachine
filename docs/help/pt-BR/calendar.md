---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: c1941aa6ca09b134
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você delegou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegam por e-mail.

Uma reunião que aparece em dois calendários é exibida uma vez só. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais apagado, com o primeiro nome dela. Esses eventos nunca geram tarefas. Eventos que duram o dia todo ou vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Na Agenda, uma viagem aparece primeiro em cada um dos dias. Na Semana e no Mês, aparece como uma faixa que atravessa os dias, por exemplo, "Viagem a Lisboa".

Um plano feito em conjunto é uma única promessa, marcada como "Com" e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução identificou que ela foi concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo informa a partir de que dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos. Toque em um dia para ver a lista de itens.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade da semana, eventos no mesmo horário aparecem lado a lado, sem perder a legibilidade. Os demais aparecem como **+N**. Toque para abrir aquele dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como a reunião de outra pessoa ou uma com convidados, mostra os detalhes: quando, onde e quem. As pessoas que o Graph conhece, além das organizações e dos projetos associados à reunião, têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo deles abre o evento no respectivo calendário. Só visualizar não altera nada.

Uma sala reservada para uma reunião aparece em Onde, nunca como pessoa nem no seu Graph.

O link de uma reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento de aeroporto chega ao seu e-mail, sua Machine a adiciona a uma viagem. As reservas de uma mesma viagem ficam em um único item, mesmo que venham de caixas de entrada diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e a volta. As reservas são agrupadas quando os dias se sobrepõem ou quando uma termina no mesmo dia em que a outra começa.

A viagem aparece como uma faixa que atravessa seus dias. Abra-a para ver cada reserva em ordem cronológica, com horários, endereço, código da reserva e assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um por evento, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao mesmo item. Um evento reservado pelo seu e-mail de trabalho é marcado como Trabalho. Caso contrário, é marcado como Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à viagem.

Se ainda falta tempo para a viagem, sua Machine informa o que está faltando, por exemplo, **Nenhuma hospedagem reservada por 2 noites** ou nenhuma reserva para ir do aeroporto ao hotel. Essas linhas aparecem em tom mais apagado e com a etiqueta **Nenhuma reserva**. Se a viagem não tiver nenhuma hospedagem, não aparece nenhuma informação sobre noites.

- Cada linha informa de onde veio a reserva, por exemplo, **Do Example Tickets**, e abre o e-mail correspondente.
- Se o e-mail gerou uma tarefa, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Se uma reserva for alterada, a linha correspondente é atualizada. Se for cancelada, ela é removida. Quando todas as reservas forem canceladas, a viagem ou o evento também é removido.
- Uma reserva feita para outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações inclui os detalhes em um formato que sua Machine consegue ler sem IA. Quando isso não acontece, como em um e-mail encaminhado ou de um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda se você estiver perto do limite de uso. Os e-mails de reservas do ano coberto pelo [histórico](history.md) que sua Machine mantém são lidos em segundo plano depois que o histórico fica disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** são o resumo: decisões e itens de ação. **Transcrição** registra palavra por palavra o que foi dito. Ela começa recolhida, com a duração indicada. Toque em **Mostrar** para abrir.

Se não carregar, o sistema tenta de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover**. Para remover, toque duas vezes. O conteúdo de uma parte não altera a outra. Em uma reunião que você pode alterar, a opção **Notas**, abaixo do formulário, abre as notas.

Se você conectou [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md), as notas aparecem em Notas e a transcrição em Transcrição, com a indicação **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem vir do próprio evento de calendário da reunião, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas a partir delas somente quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma única tarefa, com a reunião como origem: "Origem: notas da" reunião.

Uma reunião com transcrição, mas sem notas, tem a opção **Gerar notas**. The Machine cria as notas a partir da transcrição: um resumo curto, decisões e itens de ação indicando quem deve realizá-los, no idioma da reunião.

A opção **Escrevendo as notas…** aparece enquanto o processo continua, mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos, usando seu próprio modelo. As notas indicam **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: "adicione esta transcrição à reunião de hoje do quadro". A transcrição vai para Transcrição e o resumo, para Notas. No Calendário, uma reunião com esses conteúdos mostra **Notas** ou **Transcrição**.

The Machine lê as notas e a transcrição para encontrar os acompanhamentos da reunião. Eles são marcados como Trabalho ou Pessoal, conforme a reunião, e só vão para sua equipe se a reunião também for compartilhada com ela.

A reunião abre com esses detalhes onde quer que você a encontre: em uma linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, no fim da página, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e outros calendários são somente para visualização. **Novo evento** cria um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou em **Excluir** para apagá-lo. Para excluir, toque duas vezes.

**Onde** sugere lugares enquanto você digita: primeiro, os que você usou antes e os das suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas convidadas aparecem acima do botão, que informa a quantidade: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite nem uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar um local de retirada. Ela mostra exatamente o que será alterado. A alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tem um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode sugerir uma mensagem curta para mudar o horário ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Eventos de dia inteiro, marcados como livre ou provisórios nunca contam, e cada conflito aparece uma só vez. Uma tarefa de Trabalho só informa que há um conflito, para sua equipe nunca ver o evento pessoal. Só você vê com qual evento há conflito.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve:

- **Quem:** quem são, de acordo com o seu Graph.
- **Último contato:** sua última conversa com essas pessoas. Depois da reunião, essa mensagem aparece como origem da tarefa.
- **Promessas em aberto:** o que você ou elas ainda têm a cumprir.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado.

A tarefa aparece na manhã de um dia útil: no próprio dia da reunião se ela for à tarde; caso contrário, no dia útil anterior. Ela usa somente o que já está na sua Machine. É só para ler. Quando terminar, toque em **Feito**. Uma promessa ou pergunta que precise de alguma ação gera sua própria tarefa.

Se não houver histórico útil, nenhuma tarefa é criada. Reuniões recorrentes, internas, pessoais e recusadas não geram tarefas. Se uma reunião mudar de horário, sua tarefa continua sendo a mesma, agora no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque de distância do chat.
