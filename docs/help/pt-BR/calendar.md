---
title: Calendário
area: calendar
summary: A semana à frente em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9f38e3718f3e8639
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas que voltam naquele dia,
- acompanhamentos de trabalhos que você delegou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) dos e-mails de reservas e ingressos.

Uma reunião que aparece em dois calendários é mostrada uma só vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em uma cor mais apagada, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro e com vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Na Agenda, uma viagem aparece primeiro em cada um dos dias. Na Semana e no Mês, aparece como uma faixa ao longo dos dias, por exemplo, "Viagem a Lisboa".

Um plano feito em conjunto é uma única promessa, marcada como "Com" e o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída (você já respondeu ou a execução identificou que ela foi concluída) não aparece como **Prazo**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os dias seguintes ou para cima (ou toque em **Mostrar dias anteriores**) para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo informa a partir de que dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos, e um toque lista os itens daquele dia.

**Hoje**, ‹ e › na parte superior permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem perder a legibilidade. Os demais aparecem como **+N**. Toque para abrir aquele dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como uma reunião de outra pessoa ou com convidados, mostra os detalhes: quando, onde e quem. Uma pessoa que o seu Graph conhece, assim como as organizações e os projetos relacionados à reunião, aparecem como links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre a reunião no respectivo serviço. Só olhar não altera nada.

Uma sala de reunião reservada para uma reunião aparece em onde, nunca como uma pessoa ou no seu Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando chega no seu e-mail uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto, sua Machine adiciona a reserva a uma viagem. As reservas de uma mesma jornada ficam em uma viagem, mesmo que venham de caixas de e-mail diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e o trajeto de volta. As reservas são agrupadas quando os dias se sobrepõem ou quando uma começa no dia em que a outra termina.

A viagem aparece como uma faixa ao longo dos dias. Abra para ver cada reserva em ordem cronológica, com os horários, o endereço, o código da reserva e o assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um por evento, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao evento existente. Um evento reservado pela sua caixa de e-mail de trabalho é Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à viagem.

Para uma viagem futura, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites**, ou que não há reserva do aeroporto até o hotel. Essas linhas aparecem em uma cor mais apagada e com a etiqueta **Nenhuma reserva**. Uma viagem sem nenhuma hospedagem não informa nada sobre as noites.

- Cada linha informa de quem veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se uma tarefa veio do e-mail, como pagar pelos ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva para outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine consegue ler sem IA. Quando isso não acontece, como em um e-mail encaminhado ou de um site pequeno de reservas, seu [modelo](model.md) lê o e-mail em segundo plano, alguns por vez, e espera se você estiver perto do limite de uso. Os e-mails de reserva do ano incluído no [histórico](history.md) mantido pela sua Machine são lidos em segundo plano assim que esse histórico estiver disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo, com decisões e itens de ação. **Transcrição** registra o que foi dito, palavra por palavra. Ela começa recolhida, com a duração; **Mostrar** abre a transcrição.

Se não carregarem, o sistema tenta de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte fica nela. Em uma reunião que você pode alterar, a opção **Notas** abaixo do formulário abre as notas.

Se você conectou [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md), as notas desses serviços aparecem em Notas e a transcrição aparece em Transcrição, identificada como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se houver as duas versões, ambas aparecem.

As notas também podem vir do evento da reunião no calendário, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas a partir dessas notas somente quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, é criada uma única tarefa, com a reunião como origem: "Origem: notas da" reunião.

Uma reunião com transcrição, mas sem notas, mostra a opção **Gerar notas**. The Machine cria as notas a partir da transcrição: um breve resumo, decisões e itens de ação com as pessoas responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e a criação continua mesmo se você fechar a reunião. Uma reunião longa pode levar alguns minutos, usando seu próprio modelo. As notas são identificadas como **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: "adicione esta transcrição à reunião de hoje do quadro". Uma transcrição vai para Transcrição; um resumo vai para Notas. Quando uma reunião tem notas ou transcrição, aparece **Notas** ou **Transcrição** no Calendário.

The Machine lê as duas para encontrar acompanhamentos da reunião. Eles são de Trabalho ou Pessoais, como a reunião, e só vão para sua equipe quando a reunião também é de Trabalho.

Os detalhes da reunião aparecem sempre que você a abre: na linha do tempo, nos resultados de uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e outros calendários são somente para visualização. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, lugares que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção aparece somente no seu próprio calendário. Os convidados aparecem listados acima do botão, que informa quantos são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém é convidado nem recebe uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar um local de embarque. Ela mostra exatamente o que será alterado, e somente **Adicionar**, **Salvar** ou **Excluir** confirma a alteração.

Ainda não há reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode criar um rascunho curto de mensagem para remarcar ou sugerir recusar o convite. Nada é enviado até você aprovar.

Eventos de dia inteiro, marcados como livre ou provisórios nunca contam, e cada conflito aparece uma só vez. Uma tarefa de Trabalho informa apenas que há um conflito, para sua equipe nunca ver o evento pessoal. Só você vê com o que ele coincide.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um breve resumo:

- **Quem:** quem são essas pessoas, de acordo com seu Graph, incluindo informações sobre o histórico delas quando disponíveis.
- **Organização:** o que a empresa delas faz que seja relevante para a reunião.
- **Até agora:** o que vocês conversaram, pediram e ofereceram, e em que ponto estão. Depois da reunião, essas mensagens aparecem como fontes da tarefa.
- **Promessas em aberto:** o que você ou essas pessoas ainda têm a cumprir, de acordo com as promessas na sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado, e o que provavelmente será importante para essas pessoas.

A tarefa chega na manhã de um dia útil: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia útil anterior. É só para leitura: marque **Feito** quando terminar de ler. Uma promessa ou pergunta que exija uma ação tem sua própria tarefa.

Ela usa o que já está na sua Machine. Para a primeira reunião com alguém de uma empresa, também faz uma breve busca na web pelo nome da pessoa e da empresa e mostra um link ao lado do que encontrou. A busca recebe apenas o nome público da pessoa, o nome da empresa e o site, nunca suas mensagens. Os resultados de uma busca são reutilizados por 30 dias. Se **Buscar contatos de trabalho** estiver desativado em Configurações, em Segurança, não haverá busca.

Sem um histórico útil, não há tarefa. Reuniões recorrentes, internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua a mesma, no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Quando uma atualização altera o conteúdo de um resumo, os resumos de reuniões futuras são reescritos uma vez no novo formato. O título, as fontes e o lugar na lista continuam iguais. Um resumo que você alterou, adiou ou encerrou não muda, assim como o de uma reunião que começa nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque do chat.
