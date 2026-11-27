---
title: Calendário
area: calendar
summary: A semana à frente em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 4b5bc600fefb624c
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você repassou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e passagens que chegam por e-mail.

Uma reunião que aparece em dois calendários só é mostrada uma vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca geram tarefas. Eventos de dia inteiro e que duram vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Na Agenda, uma viagem aparece primeiro em cada um dos seus dias. Na Semana e no Mês, aparece como uma faixa que cobre todos os dias, como "Viagem para Lisboa".

Um plano feito em conjunto é uma única promessa, marcada com "Com" e o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução encontrou tudo pronto, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os anteriores. Ela volta até uma semana antes de você conectar o calendário, e uma linha no topo informa a partir de que dia. Depois que o [histórico](history.md) for carregado, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, aparecem até três itens por dia. No celular, aparecem pontos; toque em um dia para ver a lista.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem perder a legibilidade. Os demais aparecem como **+N**. Toque para abrir o dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma com convidados, mostra os detalhes: quando e onde será, e quem vai participar. Pessoas que a sua Graph conhece, além das organizações e dos projetos associados à reunião, têm links para suas páginas. **Abrir no Google Calendar** ou **Abrir no Outlook**, abaixo desses links, abre o evento no calendário correspondente. Só de visualizar, nada é alterado.

A sala de reunião reservada para um evento aparece abaixo do local, nunca como uma pessoa nem na sua Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando chega ao seu e-mail uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto, sua Machine a adiciona a uma viagem. As reservas de uma mesma jornada ficam em uma única viagem, mesmo que venham de caixas de e-mail diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e o caminho de volta. As reservas são agrupadas quando as datas se sobrepõem ou quando uma começa no fim da outra.

A viagem aparece como uma faixa que cobre todos os seus dias. Abra-a para ver cada reserva em ordem cronológica, com horários, endereço, código da reserva e assento.

Ingressos para um show, uma partida, um festival ou uma conferência geram um evento, um por evento, com local, código da reserva, assento e número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao evento existente. Um ingresso reservado pelo seu e-mail de trabalho é de Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à viagem.

Se uma viagem ainda vai acontecer, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites** ou a falta de uma reserva para ir do aeroporto ao hotel. Essas linhas aparecem em tom mais claro e com a marcação **Nenhuma reserva**. Se uma viagem não tiver nenhuma hospedagem, não aparece nenhuma informação sobre noites.

- Cada linha informa de onde veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se o e-mail gerou uma tarefa, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Se uma reserva for alterada, a linha correspondente será atualizada. Se for cancelada, será removida. Quando todas as reservas forem canceladas, a viagem ou o evento também será removido.
- Reservas feitas para outra pessoa, como o voo de um colega encaminhado para você, não aparecem nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine lê sem IA. Quando isso não acontece, como em um e-mail encaminhado ou em um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda quando você está perto do limite de uso. Os e-mails de reserva do ano incluído no [histórico](history.md) que sua Machine mantém são lidos em segundo plano assim que esse histórico é carregado.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** são o resumo: decisões e itens de ação. **Transcrição** registra o que foi dito, palavra por palavra. Ela começa recolhida, com a duração; **Mostrar** abre a transcrição.

Se não carregarem, o sistema tenta de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para enviar um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O que você adiciona a uma parte fica nela. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Com [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) conectado, as notas do serviço aparecem em Notas e a transcrição, em Transcrição, com a marcação **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem vir do evento da reunião no calendário, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas a partir delas somente quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma única tarefa, com a reunião como origem: "Origem: notas de" a reunião.

Uma reunião com transcrição, mas sem notas, mostra a opção **Gerar notas**. The Machine cria as notas com base na transcrição: um resumo breve, decisões e itens de ação com os responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece enquanto o processo continua, mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos e usa seu próprio modelo. As notas indicam **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: "adicione esta transcrição à reunião de equipe de hoje". A transcrição vai para Transcrição e o resumo, para Notas. No Calendário, uma reunião com esses itens mostra **Notas** ou **Transcrição**.

The Machine lê as notas e a transcrição para acompanhar os próximos passos da reunião. Eles são de Trabalho ou Pessoal, como a reunião, e só vão para sua equipe quando a reunião também for compartilhada com ela.

A reunião abre com esses detalhes onde quer que você a encontre: na linha do tempo, na busca de mensagens ou como origem de uma tarefa. **Convite original**, no fim da página, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google aqui. O Outlook e outros calendários são apenas para consulta. **Novo evento** adiciona um evento. No celular, fica em **+** na barra superior. Escolha o calendário, o título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou em **Excluir** para removê-lo (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, lugares usados antes e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. Quem vai receber um convite aparece acima do botão, que informa quantas pessoas serão convidadas: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe convite nem atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que será alterado. A alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho se sobrepõe a algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para sugerir outro horário ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Se um evento se sobrepuser a vários outros, será criada uma tarefa sobre ele. Novas sobreposições são adicionadas enquanto a tarefa estiver em aberto. Depois que ela for concluída ou descartada, só uma reunião criada ou alterada mais tarde fará o conflito aparecer de novo.

Eventos de dia inteiro, com status livre ou provisório nunca contam, e cada conflito é identificado uma única vez. O local de trabalho, o horário de foco e o status de ausência do Google também não contam. O mesmo vale para um bloqueio criado por você que contém outras reuniões, como um dia no escritório: só as reuniões dentro dele podem entrar em conflito. Um bloqueio sem outras pessoas nem reuniões, como um voo, ainda pode entrar em conflito com um evento que tenha outras pessoas.

Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê com o que ele entra em conflito: os dois primeiros eventos e quantos outros há. Uma tarefa em que você não fez nada é fechada automaticamente se o conflito estiver em outra tarefa ou se, no fim das contas, não houver conflito.

## Prepare-se para as reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve com informações para você:

- **Quem:** quem são as pessoas, de acordo com sua Graph, incluindo informações sobre a trajetória delas quando disponíveis.
- **Organização:** o que a empresa delas faz, para quem e por qual preço, quando isso for relevante para a reunião.
- **Até agora:** o que vocês conversaram, perguntaram e ofereceram, e em que ponto estão. Essas mensagens aparecem como fontes da tarefa depois da reunião.
- **Combinado antes:**, **O que mudou:** e **Ainda em aberto:** o que resultou de reuniões anteriores com as mesmas pessoas, com cada linha indicando a reunião ou a mensagem de origem.
- **Promessas em aberto:** o que você ou essas pessoas ainda precisam fazer, com base nas promessas registradas na sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado, e o que provavelmente será importante para as outras pessoas.

A tarefa aparece na manhã de um dia útil: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia útil anterior. Ela serve para leitura: toque em **Feito** depois de ler. Uma promessa ou pergunta que exija alguma ação tem sua própria tarefa.

Pergunte sobre a reunião no chat dela ou adicione o que você sabe. The Machine responde ou incorpora sua observação ao resumo, por exemplo em **Decidir ou levar**, e aprende com ela. Nada é enviado a partir de um resumo.

Reuniões anteriores contam quando incluem alguém de fora, mesmo que tivessem outro nome ou a pessoa usasse outro endereço. The Machine lê as notas disponíveis na sua Machine: as suas, as do app de reuniões ou as enviadas por e-mail. Se não houver notas, lê a transcrição ou as notas do evento no calendário. As mais recentes têm mais peso, e um assunto resolvido depois não aparece como pendente.

Notas e mensagens do [Histórico](history.md) também contam, para que o resumo inclua reuniões de antes de você começar a usar The Machine.

Um resumo de Trabalho não lê notas pessoais nem informações da Machine de outra pessoa. O texto fica só com você: ele não é incluído em um repasse e não pode ser enviado para revisão. Se não houver notas, essas linhas não aparecem.

O resumo usa o que já está na sua Machine. Para a primeira reunião com alguém de uma empresa, também lê a página inicial do site da empresa.

Se a busca na web estiver configurada na sua Machine, ela também faz uma busca breve na web pelo nome da pessoa e da empresa. Uma Machine hospedada não vem com esse recurso. No seu próprio computador, você pode configurá-lo no OpenClaw. Os resultados vêm acompanhados de um link. Só o nome público da pessoa, o nome da empresa e o site são enviados para a busca, nunca suas mensagens. Os resultados são reutilizados por 30 dias.

Assim, uma primeira reunião que você aceitou pode ter um resumo antes mesmo de vocês trocarem uma palavra: o que a empresa faz, o que isso significa para você e, quando possível, quem é a pessoa. Se você só tiver o primeiro nome, os resultados da busca só serão mantidos quando apontarem para uma única pessoa. Se **Buscar contatos de trabalho** estiver desativado em Configurações, em Segurança, nada será pesquisado.

Uma reunião recorrente só recebe um resumo quando há algo novo desde a última vez: uma mensagem, notas ou uma promessa. O resumo informa o que mudou, não o que o resumo anterior já dizia. Ele aparece depois que a reunião anterior termina, para no máximo duas reuniões recorrentes por dia.

Uma reunião só com sua equipe recebe um resumo apenas quando as notas de reuniões anteriores mostram uma decisão pendente, uma etapa que alguém precisa cumprir ou novidades. Essas informações vêm da mesma série de reuniões ou de reuniões com o mesmo título que incluam alguém em comum, nunca de outra reunião com os mesmos colegas. O resumo não apresenta seus colegas nem pesquisa informações sobre eles. Reuniões diárias comuns não recebem um resumo.

Se não houver nada útil a dizer, nenhuma tarefa é criada. Reuniões pessoais ou recusadas também não geram tarefas. Se uma reunião mudar de horário, a tarefa será mantida no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é fechada automaticamente.

Se uma atualização mudar as informações do resumo, os resumos de reuniões futuras ainda em aberto são reescritos uma vez, com as novas informações. O título, as fontes e a posição na lista permanecem. Resumos que você alterou, adiou ou fechou não mudam. O mesmo vale para reuniões que começam nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque de distância do chat.
