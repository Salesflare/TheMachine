---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 7f9f9d9e9a502b7d
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você repassou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegam por e-mail.

Uma reunião que está em dois calendários aparece uma só vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro e com vários dias aparecem como eventos de dia inteiro em cada dia que abrangem. Na Agenda, uma viagem aparece primeiro em cada um dos dias. Nas visualizações Semana e Mês, aparece como uma faixa que se estende por esses dias, como “Viagem a Lisboa”.

Um plano feito em conjunto é uma única promessa, marcada como “Com” e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução constatou que foi feita, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima (ou toque em **Mostrar dias anteriores**) para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo indica a partir de qual dia. Quando seu [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos. Toque em um dia para ver a lista de itens.

**Hoje**, ‹ e ›, no topo, permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, os eventos no mesmo horário aparecem lado a lado, mas continuam legíveis. Os demais aparecem como **+N**. Toque para abrir aquele dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como uma reunião de outra pessoa ou com convidados, mostra os detalhes: quando, onde e quem. As pessoas que sua Graph conhece, as organizações e os projetos relacionados à reunião têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) aparece abaixo e abre a reunião no calendário correspondente. Só olhar não altera nada.

Uma sala de reunião reservada para uma reunião aparece em “Onde”, nunca como pessoa nem na sua Graph.

O link de uma reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando chega ao seu e-mail uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto, sua Machine adiciona a reserva a uma viagem. As reservas da mesma jornada ficam em uma única viagem, mesmo que cheguem a caixas de entrada diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e a volta. As reservas são agrupadas quando os dias se sobrepõem ou quando uma começa no mesmo dia em que a outra termina.

A viagem aparece como uma faixa que se estende pelos dias correspondentes. Abra-a para ver cada reserva em ordem cronológica, com horários, endereço, código da reserva e assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um por evento, com o local, o código da reserva, o assento e a quantidade de ingressos. Um segundo pedido para o mesmo evento é incluído nele. Um ingresso reservado pelo seu e-mail de trabalho é Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à própria viagem.

Se uma viagem ainda não começou, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites** ou que não há reserva para ir do aeroporto ao hotel. Essas linhas aparecem em tom mais claro e com a indicação **Nenhuma reserva**. Se a viagem não tiver nenhuma hospedagem, ela não informa nada sobre as noites.

- Cada linha informa de onde veio a reserva, como **Do Example Tickets**, e abre esse e-mail.
- Se uma tarefa veio do e-mail, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha correspondente, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva feita para outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine consegue ler sem IA. Quando não consegue, como no caso de um e-mail encaminhado ou de um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda quando você está perto do limite de uso. Os e-mails de reserva do ano incluído no [histórico](history.md) que sua Machine guarda são lidos em segundo plano assim que esse histórico estiver disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** registra o que foi dito, palavra por palavra. Ela começa recolhida e mostra sua duração. Toque em **Mostrar** para abrir.

Se não carregar, o sistema tenta novamente por conta própria durante cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte fica nela. Em uma reunião que você pode alterar, a opção **Notas**, abaixo do formulário, abre as notas.

Se [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) estiver conectado, as notas aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem vir do evento da reunião no calendário, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas com base nelas, mas somente para próximos passos claros. Se as mesmas notas chegarem por dois meios, elas geram uma única tarefa, cuja origem é a reunião: “Origem: notas de” seguida do nome da reunião.

Uma reunião com transcrição, mas sem notas, tem a opção **Gerar notas**. The Machine cria as notas com base na transcrição: um resumo curto, decisões e itens de ação com as pessoas responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e o processo continua mesmo quando você fecha a reunião. Uma reunião longa pode levar alguns minutos e usa seu próprio modelo. As notas indicam **Escrito por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso no chat de uma tarefa, por exemplo: “adicione esta transcrição à reunião da equipe de hoje”. Uma transcrição vai para Transcrição; um resumo, para Notas. No Calendário, uma reunião que tenha esse conteúdo mostra **Notas** ou **Transcrição**.

The Machine lê as duas partes para identificar os acompanhamentos da reunião. Eles são de Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também for de Trabalho.

A reunião abre com esses detalhes onde quer que você a encontre: na linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google aqui. O Outlook e outros calendários são apenas para consulta. **Novo evento** adiciona um evento (no celular, fica em **+**, na barra superior): escolha o calendário, o título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas que receberão um convite aparecem acima do botão, que informa a quantidade: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe convite nem atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que vai mudar. A alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões, onde você pode conectar o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho se sobrepõe a algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para remarcar ou sugerir que você recuse o convite. Nada é enviado sem sua aprovação.

Um evento que se sobrepõe a vários outros gera uma única tarefa, sobre esse evento. Se houver uma nova sobreposição enquanto a tarefa estiver em aberto, ela é adicionada à mesma tarefa. Depois que a tarefa é concluída ou descartada, só uma reunião criada ou alterada mais tarde faz com que ela volte.

Eventos de dia inteiro, livres e provisórios nunca contam, e cada conflito é identificado uma única vez. O local de trabalho, o horário de concentração e a ausência temporária do Google também não contam. O mesmo vale para um bloqueio criado por você que contenha outras reuniões, como um dia no escritório: só as reuniões dentro dele podem gerar conflitos. Um bloqueio sem outras pessoas nem reuniões, como um voo, ainda pode gerar conflito com um evento que tenha outras pessoas.

Uma tarefa de Trabalho apenas informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê com o que ele entra em conflito: os dois primeiros eventos e quantos outros há. Uma tarefa que você não fez nada para resolver fecha sozinha quando o conflito está em outra tarefa ou quando não era um conflito, afinal.

## Preparação para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve:

- **Quem:** quem são, de acordo com sua Graph, e informações sobre o histórico delas, quando disponíveis.
- **Organização:** o que a empresa delas faz, para quem e a que preço, quando isso for relevante para a reunião.
- **Até agora:** o que vocês conversaram, pediram e ofereceram, e em que ponto estão. Essas mensagens passam a ser as fontes da tarefa depois da reunião.
- **Combinado antes:**, **Mudou desde então:** e **Ainda em aberto:** o que surgiu em reuniões anteriores com as mesmas pessoas. Cada linha indica a reunião ou mensagem de origem.
- **Promessas em aberto:** o que você ou elas ainda precisam cumprir, com base nas promessas da sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que vocês precisam decidir ou levar e o que provavelmente será importante para as outras pessoas.

A tarefa aparece na manhã de um dia de trabalho: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia de trabalho anterior. Ela é para consulta: fica **Feito** quando você a lê. Uma promessa ou pergunta que exija uma ação tem sua própria tarefa.

Pergunte sobre a reunião no chat dela ou adicione o que você sabe. The Machine responde ou inclui sua anotação no resumo, por exemplo em **Decidir ou levar**, e aprende com ela. Nada é enviado a partir de um resumo.

Reuniões anteriores são consideradas quando há alguém de fora em ambas, independentemente do nome da reunião ou do endereço usado. The Machine lê as notas que sua Machine tem: as suas, as do app da reunião ou as que ela enviou por e-mail. Se não houver, lê a transcrição ou as notas do evento no calendário. As mais recentes têm mais peso, e um ponto resolvido depois não aparece como em aberto.

Notas e mensagens do [Histórico](history.md) também são consideradas, para que o resumo leve em conta reuniões anteriores ao início do uso.

Um resumo de Trabalho não lê notas pessoais nem conteúdo da Machine de outra pessoa. O texto fica só com você: não é levado junto em um repasse e não pode ser enviado para revisão. Se não houver notas, essas linhas não aparecem.

O resumo usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também lê a página inicial do site da empresa.

Também faz uma breve busca na web pelo nome da pessoa e da empresa. Em uma Machine hospedada, a busca usa seu login do ChatGPT ou do Claude e consome um pouco do seu plano. No seu próprio computador, usa o provedor de busca configurado no OpenClaw ou seu login, depois que você ativar essa opção (`meeting_prep_signin_search` em `config.json`). Um provedor que você configurou sempre tem prioridade.

Somente o nome público da pessoa, o nome da empresa e o site são enviados à busca, nunca suas mensagens. Os resultados vêm acompanhados de um link e são reutilizados por 30 dias. No ChatGPT, o modelo fornece o link, mas ele não é verificado. Abra-o antes de confiar no que diz. O chat da tarefa mostra **Pesquisou na web**.

Assim, uma primeira reunião que você aceitou pode ter um resumo antes mesmo de vocês trocarem uma palavra: o que a empresa faz, o que isso significa para você e, quando possível, quem é a pessoa. Se você tiver apenas o primeiro nome, os resultados da busca só serão usados quando apontarem para uma única pessoa. Com **Buscar contatos de trabalho** desativado em Configurações, Segurança, nada é consultado nem pesquisado.

Uma reunião recorrente só recebe um resumo quando há algo novo desde a última: uma mensagem, notas ou uma promessa. O resumo informa o que mudou, não repete o resumo anterior. Ele chega depois que o horário da reunião anterior termina, para no máximo duas reuniões recorrentes por dia.

Uma reunião apenas com sua equipe só recebe um resumo quando notas anteriores da mesma série (ou do mesmo título, se uma das reuniões da série estiver nas notas) deixam algo pendente para você: uma etapa que cabe a você, uma pergunta para você, uma decisão a tomar ou uma promessa sua. Etapas que só cabem a colegas não geram um resumo. The Machine não consulta informações sobre seus colegas, e o resumo chega na manhã da própria reunião, quando possível.

Se não houver nada útil para dizer, nenhuma tarefa é criada. Reuniões pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua a mesma, no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada fecha sozinha.

Quando uma atualização muda o conteúdo do resumo, os resumos em aberto de reuniões futuras são atualizados uma vez. O título, as fontes e o lugar na lista continuam iguais. Um resumo que você alterou, adiou ou fechou permanece como está. O mesmo vale para o de uma reunião que começa nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque de distância do chat.
