---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 970b39054ae39543
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você delegou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das confirmações de reserva e ingressos que chegam por e-mail.

Uma reunião que aparece em dois calendários é exibida uma só vez. Os eventos de um calendário compartilhado com você aparecem esmaecidos, com o primeiro nome de quem compartilhou. Eles nunca geram uma tarefa. Eventos de dia inteiro e de vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Na Agenda, uma viagem aparece primeiro em cada um dos seus dias. Na Semana e no Mês, aparece como uma faixa que atravessa esses dias, como “Viagem a Lisboa”.

Um plano feito em conjunto é uma só promessa, marcada como “Com” e o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução confirmou que ela foi concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os anteriores. Ela volta até uma semana antes de você conectar o calendário e mostra uma linha no topo com a data inicial. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, aparecem até três itens por dia. No celular, aparecem pontos; toque em um dia para ver a lista.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, os eventos que acontecem no mesmo horário ficam lado a lado, sem prejudicar a leitura. Os demais aparecem como **+N**. Toque para abrir esse dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Se não for possível alterar uma reunião por aqui, como uma reunião de outra pessoa ou com convidados, os detalhes serão exibidos: quando e onde acontece e quem participa. As pessoas que o Graph conhece, além das organizações e dos projetos associados à reunião, têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abre a reunião no calendário correspondente. A visualização não altera nada.

A sala reservada para uma reunião aparece em Onde, nunca como pessoa nem no seu Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega por e-mail, sua Machine a adiciona a uma viagem. As reservas de uma mesma jornada ficam juntas em uma viagem: ida, hotel e volta. A viagem aparece como uma faixa que atravessa seus dias. Abra para ver, em ordem cronológica, o código da reserva, o assento e o ingresso de cada reserva.

Ingressos para shows, partidas, festivais ou conferências criam um evento por ocasião, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao evento já existente. Um evento reservado pelo seu e-mail de trabalho é marcado como Trabalho. Caso contrário, é marcado como Pessoal.

- Cada linha informa de quem veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se um e-mail gerou uma tarefa, como pagar pelos ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha correspondente; uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.

A Machine lê os detalhes que companhias aéreas, hotéis, sites de reservas e vendedores de ingressos incluem nos e-mails de confirmação, sem usar IA. Um e-mail sem esses detalhes não gera nada. Os e-mails de reserva do ano coberto pelo [histórico](history.md) que sua Machine mantém são lidos em segundo plano quando esse histórico fica disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** registra exatamente o que foi dito. Ela aparece recolhida, com a duração; **Mostrar** abre a transcrição.

Se não carregar, a reunião tenta carregar de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções: **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte não é colocado na outra. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Se [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) estiver conectado, as notas aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem chegar pelo evento da reunião no calendário, depois que ela começar, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas com base nelas apenas para próximos passos claros. Se as mesmas notas chegarem por dois caminhos, elas geram uma só tarefa, com a reunião como origem: “Origem: notas da reunião”.

Uma reunião com transcrição e sem notas tem a opção **Gerar notas**. The Machine escreve as notas com base na transcrição: um resumo curto, decisões e itens de ação com quem vai realizá-los, no idioma da reunião.

A reunião mostra **Escrevendo as notas…** e continua o processo mesmo que você a feche. Uma reunião longa pode levar alguns minutos, usando seu próprio modelo. As notas indicam **Escritas por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: “adicione esta transcrição à reunião de hoje do conselho”. Uma transcrição vai para Transcrição; um resumo, para Notas. No Calendário, uma reunião com notas ou transcrição mostra **Notas** ou **Transcrição**.

The Machine lê as duas partes para encontrar os acompanhamentos da reunião. Eles são marcados como Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também for compartilhada com ela.

Os detalhes da reunião são os mesmos em qualquer lugar onde ela apareça: na linha do tempo, nos resultados da busca de mensagens ou como origem de uma tarefa. **Convite original**, no fim, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu calendário do Google por aqui. O Outlook e os outros calendários são somente para visualização. **Novo evento** adiciona um evento. No celular, essa opção fica em **+** na barra superior. Escolha o calendário, o título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os que você já usou e os das suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas que receberão um convite aparecem acima do botão, que informa quantas são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite ou uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma parada para buscar algo. Ela mostra exatamente o que vai mudar. A alteração só é feita quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para remarcar ou sugerir que você recuse o convite. Nada é enviado sem sua aprovação.

Eventos de dia inteiro, com disponibilidade livre ou provisórios nunca contam como conflitos, e cada conflito aparece uma só vez. Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê o que está em conflito com ele.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve com:

- **Quem:** quem são essas pessoas, de acordo com seu Graph.
- **Último contato:** sua última conversa com elas. Depois da reunião, essa mensagem aparece como origem da tarefa.
- **Promessas em aberto:** o que você ou essas pessoas ainda precisam fazer.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado.

A tarefa chega na manhã de um dia útil: no próprio dia da reunião, se ela acontecer à tarde; caso contrário, no dia útil anterior. Ela usa apenas o que já está na sua Machine. É só para leitura: toque em **Feito** quando terminar de ler. Qualquer promessa ou pergunta que exigir uma ação terá sua própria tarefa.

Se não houver histórico relevante, não será criada uma tarefa. Reuniões recorrentes, internas, pessoais ou recusadas não geram tarefas. Se uma reunião for remarcada, a mesma tarefa muda para o novo horário. Uma tarefa descartada não volta a aparecer. A tarefa de uma reunião cancelada é fechada automaticamente.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque do chat.
