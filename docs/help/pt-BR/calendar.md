---
title: Calendário
area: calendar
summary: A semana à frente em um só lugar: reuniões, tarefas com prazo para hoje, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: ae462ef9e7316cb6
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas com prazo para aquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de tarefas que você delegou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegaram por e-mail.

Uma reunião que aparece em dois calendários é exibida uma só vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom esmaecido, com o primeiro nome dela; esses eventos nunca geram uma tarefa. Eventos de dia inteiro e com vários dias aparecem como eventos de dia inteiro em cada dia que abrangem. Na Agenda, uma viagem aparece primeiro em cada um dos dias. Na Semana e no Mês, aparece como uma faixa que abrange esses dias, por exemplo, "Viagem a Lisboa".

Um plano feito em conjunto conta como uma promessa, marcada como "Com" e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída (você já respondeu ou a execução identificou que ela foi concluída) não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os dias anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo informa a partir de qual dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, aparecem até três itens por dia. No celular, aparecem pontos, e ao tocar neles você vê a lista daquele dia.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, mas continuam legíveis. Os demais aparecem como **+N**. Toque neles para abrir aquele dia na agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar por aqui, como uma reunião de outra pessoa ou com convidados, mostra os detalhes: quando, onde e quem. Uma pessoa que sua Graph conhece, além das organizações e dos projetos relacionados à reunião, têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre a reunião no respectivo calendário. Só olhar não altera nada.

Uma sala de reunião reservada para uma reunião aparece em onde, nunca como pessoa ou na sua Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto chega por e-mail, sua Machine a adiciona a uma viagem. As reservas da mesma jornada ficam em uma só viagem, mesmo que venham de caixas de e-mail diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e a volta. As reservas são agrupadas quando os dias se sobrepõem ou quando uma termina no mesmo dia em que a outra começa.

A viagem aparece como uma faixa que abrange os dias. Abra-a para ver cada reserva em ordem cronológica, com os horários, o endereço, o código da reserva e o assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um por evento, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao mesmo evento. Um ingresso reservado na sua caixa de e-mail do trabalho é marcado como Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à viagem.

Para uma viagem que ainda vai acontecer, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites**, ou que não há reserva para ir do aeroporto ao hotel. Essas linhas aparecem em tom esmaecido e com a marcação **Nenhuma reserva**. Uma viagem sem hospedagem não mostra informações sobre as noites.

- Cada linha informa de quem veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se uma tarefa foi criada a partir do e-mail, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva para outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine consegue ler sem IA. Quando não traz, como em um e-mail encaminhado ou de um site pequeno de reservas, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda quando você está perto do limite de uso. Os e-mails de reservas do ano incluído no [histórico](history.md) que sua Machine mantém são lidos em segundo plano quando esse histórico fica disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** registra palavra por palavra o que foi dito. Ela começa recolhida e mostra a duração. **Mostrar** abre a transcrição.

Se as informações não carregarem, o sistema tenta de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte não é movido para a outra. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Com [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) conectado, as notas aparecem em Notas e a transcrição em Transcrição, com a marcação **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem aparecer no evento da reunião no próprio calendário, adicionadas depois que ela começou, ou chegar por e-mail do Zoom ou do Gemini. Quando a reunião termina, The Machine cria tarefas a partir delas somente para os próximos passos claros. Se as mesmas notas chegarem por dois meios, uma só tarefa é criada, com a reunião como origem: "Origem: notas de" seguida da reunião.

Uma reunião com transcrição e sem notas tem a opção **Gerar notas**. The Machine cria notas com base na transcrição: um resumo curto, decisões e itens de ação com as pessoas responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e o processo continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos, usando seu próprio modelo. As notas são identificadas como **Escrito por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo, "adicione esta transcrição à reunião do conselho de hoje". Uma transcrição vai para Transcrição e um resumo vai para Notas. No Calendário, uma reunião com notas ou transcrição mostra **Notas** ou **Transcrição**.

The Machine lê as duas para acompanhar o que ficou pendente na reunião. As tarefas são marcadas como Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também for de Trabalho.

Os detalhes da reunião aparecem sempre que você a abrir: na linha do tempo, nos resultados de uma busca em mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e os outros calendários são apenas para consulta. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os lugares que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha o texto que você escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas que receberão um convite aparecem acima do botão, que informa quantas são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite ou uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar um local para buscar alguém. Ela mostra exatamente o que será alterado, e só o seu toque em **Adicionar**, **Salvar** ou **Excluir** faz a alteração.

Ainda não tem reuniões? Se você ainda não conectou um calendário, **Conecte seu calendário** abre Conexões, onde você pode conectar o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho se sobrepõe a algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode criar um rascunho de mensagem curta para remarcar ou sugerir recusar o convite. Nada é enviado até você aprovar.

Eventos de dia inteiro, eventos marcados como livre e eventos provisórios nunca contam, e cada conflito aparece uma só vez. Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê com o que ele se sobrepõe.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve:

- **Quem:** quem são essas pessoas, de acordo com sua Graph, com informações sobre o histórico delas quando disponíveis.
- **Organização:** o que a empresa delas faz que seja relevante para a reunião.
- **Até agora:** o que foi discutido, perguntado e oferecido, e em que pé está. Depois da reunião, essas mensagens são as fontes da tarefa.
- **Promessas em aberto:** o que você ou elas ainda precisam fazer.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que resolver ou levar, e o que provavelmente será importante para elas.

O resumo chega na manhã de um dia útil: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia útil anterior. É só para consulta. Toque em **Feito** quando terminar de ler. Uma promessa ou pergunta que exija alguma ação tem sua própria tarefa.

O resumo usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também faz uma busca rápida na web pelo nome da pessoa e da empresa, e mostra um link ao lado do que encontrou. Só o nome público da pessoa, o nome da empresa e o site são enviados para a busca, nunca suas mensagens. Os resultados da busca são reutilizados por 30 dias. Com **Buscar contatos de trabalho** desativado em Configurações, Segurança, não há busca.

Sem um histórico útil, não há tarefa. Reuniões recorrentes, internas, pessoais e recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua a mesma, no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque do chat dela.
