---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 24033419578a8c8f
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas no dia em que voltam,
- acompanhamentos de tarefas que você repassou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegam por e-mail.

Uma reunião em dois calendários aparece uma vez só. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais apagado, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro e de vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Na Agenda, uma viagem aparece primeiro em cada um dos seus dias. Na Semana e no Mês, aparece como uma faixa que cobre todos os dias, como “Viagem a Lisboa”.

Um plano feito em conjunto aparece como uma única promessa, marcada como “Com” e com o nome da outra pessoa. Uma promessa sobre uma reunião daquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque uma execução a identificou como concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo informa a data inicial. Depois que o [histórico](history.md) for carregado, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos, e tocar em um dia lista os itens dele.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem comprometer a leitura. Os demais aparecem como **+N**. Toque neles para abrir o dia na agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar por aqui, como a de outra pessoa ou uma reunião com convidados, mostra os detalhes: quando e onde acontece e quem participa. As pessoas que o Graph conhece, além das organizações e dos projetos relacionados à reunião, levam às respectivas páginas. **Abrir no Google Calendar** ou **Abrir no Outlook**, logo abaixo, abre o item nesse serviço. Só de consultar, nada é alterado.

Uma sala de reunião reservada para uma reunião aparece em “Onde”, nunca como pessoa nem no seu Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para entrar.

## Viagens e eventos

Quando uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento de aeroporto chega por e-mail, sua Machine a adiciona a uma viagem. As reservas de uma mesma jornada ficam em uma só viagem, mesmo que venham de caixas de entrada diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e a volta. As reservas são agrupadas quando os dias se sobrepõem ou quando uma termina no dia em que a outra começa.

A viagem aparece como uma faixa que cobre todos os dias. Abra-a para ver cada reserva em ordem cronológica, com horários, endereço, código da reserva e assento.

Ingressos para shows, jogos, festivais ou conferências criam um evento, um por evento, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao evento existente. Um evento reservado pelo seu e-mail de trabalho é classificado como Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à viagem.

Para uma viagem que ainda vai acontecer, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites** ou que não há reserva para ir do aeroporto ao hotel. Essas linhas aparecem em tom mais apagado e com a marcação **Nenhuma reserva**. Uma viagem sem hospedagem não informa nada sobre as noites.

- Cada linha informa de quem veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se uma tarefa tiver sido criada a partir do e-mail, como pagar os ingressos, **Abrir a tarefa** mostra a tarefa.
- Uma reserva alterada atualiza a linha correspondente, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva feita para outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações inclui os detalhes em um formato que sua Machine consegue ler sem IA. Quando não inclui, como em um e-mail encaminhado ou de um site pequeno de reservas, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda quando você está perto do limite de uso. Os e-mails de reserva do ano incluído no [histórico](history.md) que sua Machine mantém são lidos em segundo plano depois que o histórico é carregado.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** são o resumo: decisões e itens de ação. **Transcrição** mostra, palavra por palavra, o que foi dito. Ela começa recolhida, com a duração. Toque em **Mostrar** para abrir.

Se não carregar, o sistema tenta de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem as opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para arquivos Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte fica nela. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Com [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) conectado, as notas aparecem em Notas e a transcrição em Transcrição, com a marcação **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem vir do evento da reunião no calendário, adicionadas depois que ela começa, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas a partir delas somente quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, é criada uma única tarefa, com a reunião como origem: “Origem: notas da” reunião.

Uma reunião com transcrição e sem notas tem a opção **Gerar notas**. The Machine cria notas a partir da transcrição: um resumo curto, decisões e itens de ação com as pessoas responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e o processo continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos e usa seu próprio modelo. As notas indicam **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça em uma tarefa, por exemplo: “adicione esta transcrição à reunião do conselho de hoje”. Uma transcrição vai para Transcrição; um resumo, para Notas. No Calendário, uma reunião com esse conteúdo mostra **Notas** ou **Transcrição**.

The Machine lê os dois tipos de conteúdo para identificar os follow-ups da reunião. Eles são classificados como Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também vai.

A reunião abre com esses detalhes onde quer que você a encontre: em uma linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e os outros calendários só permitem visualizar. **Novo evento** adiciona um evento. No celular, fica dentro de **+**, na barra superior. Escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** o evento (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha seu próprio texto.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas convidadas aparecem acima do botão, que mostra quantas são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite nem uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma coleta. Ela mostra exatamente o que vai mudar. A alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para remarcar ou sugerir que você recuse o convite. Nada é enviado até você aprovar.

Eventos de dia inteiro, marcados como livre ou provisórios nunca contam, e cada conflito aparece uma única vez. Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê o evento com o qual há conflito.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar para** a reunião. É um resumo breve:

- **Quem:** quem são, de acordo com seu Graph, com informações sobre o histórico delas quando disponíveis.
- **Organização:** o que a empresa delas faz que seja relevante para a reunião.
- **Até agora:** o que vocês discutiram, perguntaram e ofereceram, e em que ponto estão. Depois da reunião, essas mensagens aparecem como fontes da tarefa.
- **Promessas em aberto:** o que você ou essas pessoas ainda têm a cumprir.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que resolver ou levar, e o que provavelmente será importante para elas.

O resumo chega na manhã de um dia útil: no próprio dia da reunião, se ela acontecer à tarde; caso contrário, no dia útil anterior. É só para leitura. Toque em **Feito** quando terminar de ler. Uma promessa ou pergunta que exija uma ação tem sua própria tarefa.

Ele usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também faz uma busca rápida na web pelo nome da pessoa e da empresa e mostra um link ao lado do que encontrou. Só o nome público da pessoa, o nome da empresa e o site são enviados para a busca, nunca suas mensagens. Os resultados da busca são reutilizados por 30 dias. Com **Buscar contatos de trabalho** desativado em Configurações, Segurança, não há busca.

Sem histórico útil, nenhuma tarefa é criada. Reuniões recorrentes, internas, pessoais e recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua sendo a mesma, no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Quando uma atualização muda o conteúdo de um resumo, os resumos das reuniões que ainda vão acontecer são reescritos uma vez, já com as informações atualizadas. O título, as fontes e o lugar na lista continuam iguais. Um resumo que você alterou, adiou ou encerrou continua como está. O mesmo vale para um resumo de uma reunião que começa nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque de distância do chat.
