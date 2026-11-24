---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: f3f41306aad03084
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos do trabalho que você passou para outra pessoa,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegam por e-mail.

Uma reunião que aparece em dois calendários é exibida uma vez só. Os eventos de um calendário compartilhado com você aparecem esmaecidos, com o primeiro nome de quem compartilhou. Eles nunca geram uma tarefa. Eventos de dia inteiro ou de vários dias aparecem como de dia inteiro em cada dia que abrangem. Na Agenda, uma viagem aparece primeiro em cada um dos dias. Nas visualizações Semana e Mês, aparece como uma faixa ao longo dos dias, como "Viagem a Lisboa".

Um plano feito em conjunto é uma promessa só, marcada como "Com" e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque uma execução verificou que ela foi concluída, não aparece como **Prazo**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima (ou toque em **Mostrar dias anteriores**) para ver os dias anteriores. Ela volta até uma semana antes de você conectar o calendário e mostra uma linha no topo com a data inicial. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, aparecem até três itens por dia. No celular, aparecem pontos. Toque em um dia para ver a lista.

**Hoje**, ‹ e ›, no topo, permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva naquele dispositivo.

Na grade semanal, eventos no mesmo horário ficam lado a lado, sem perder a legibilidade. Os demais aparecem como **+N**. Toque para abrir aquele dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Se não for possível alterar uma reunião aqui, como uma reunião de outra pessoa ou com convidados, você verá os detalhes: quando e onde será e quem vai participar. Quem você conhece pela Graph, além das organizações e dos projetos relacionados à reunião, aparece como link para a respectiva página. **Abrir no Google Calendar** (ou **Abrir no Outlook**) aparece abaixo e abre a reunião no calendário correspondente. Visualizar não altera nada.

Uma sala reservada para uma reunião aparece em "Onde", nunca como pessoa nem na sua Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento de aeroporto chega por e-mail, sua Machine a adiciona a uma viagem. As reservas da mesma viagem ficam juntas em uma só viagem, de qualquer uma das suas caixas de e-mail: o trem até o aeroporto, os voos, o carro, a hospedagem e o caminho de volta. As reservas ficam juntas quando os dias se sobrepõem ou quando uma começa no dia em que a outra termina.

A viagem aparece como uma faixa ao longo dos dias. Abra-a para ver cada reserva em ordem cronológica, com horários, endereço, código da reserva e assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um para cada ocasião, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento fica junto do primeiro. Um ingresso reservado pela sua caixa de e-mail de trabalho é classificado como Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem ficam na própria viagem.

Se ainda falta tempo para a viagem, sua Machine avisa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites** ou que não há nada reservado para ir do aeroporto ao hotel. Essas linhas aparecem esmaecidas e marcadas como **Nenhuma reserva**. Se não houver hospedagens, a viagem não mostra informações sobre noites.

- Cada linha indica de onde veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se o e-mail gerou uma tarefa, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva de outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine consegue ler sem IA. Se uma confirmação não estiver nesse formato, como um e-mail encaminhado ou de um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda quando você está perto do limite de uso. Os e-mails de reserva do ano incluído no [histórico](history.md) mantido pela sua Machine são lidos em segundo plano quando o histórico estiver disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** registra palavra por palavra o que foi dito. Ela começa recolhida e mostra sua duração. Toque em **Mostrar** para abrir.

Se não carregarem, o sistema tenta de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem as opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O que você adiciona em uma parte fica nela. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Quando [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) está conectado, as notas aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem vir do evento da reunião no próprio calendário, se forem adicionadas depois que ela começou, ou de um e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine só cria tarefas a partir delas quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma tarefa só, com a reunião como origem: "Origem: notas da" reunião.

Uma reunião com transcrição, mas sem notas, mostra a opção **Gerar notas**. The Machine cria as notas com base na transcrição: um resumo curto, decisões e itens de ação com a pessoa responsável, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e o processo continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos. O processo usa seu próprio modelo. As notas são marcadas como **Escrito por The Machine** e nunca substituem as notas que você adicionou.

Você também pode pedir para The Machine adicionar notas. Por exemplo, em uma tarefa, peça: "adicione esta transcrição à reunião de hoje do quadro". A transcrição fica em Transcrição e o resumo, em Notas. No Calendário, uma reunião com notas ou transcrição mostra **Notas** ou **Transcrição**.

The Machine lê as duas partes para encontrar os acompanhamentos da reunião. Eles são classificados como Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também for de trabalho.

A reunião abre com esses detalhes de onde quer que você a encontre: na linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, no final, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e os outros calendários são somente para consulta. **Novo evento** adiciona um evento. No celular, essa opção fica em **+**, na barra superior. Escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** para removê-lo (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, lugares que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas que receberão um convite aparecem acima do botão, que indica quantas são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe convites nem atualizações.

Uma tarefa também pode sugerir uma alteração, como adicionar um traslado. Ela mostra exatamente o que vai mudar. A alteração só é feita quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo do seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente dos dois. Ela pode preparar uma mensagem curta para remarcar ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Eventos de dia inteiro, com disponibilidade livre ou provisórios nunca são considerados, e cada conflito aparece uma vez só. Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê com o que ele coincide.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar para** a reunião. É um resumo breve:

- **Quem:** quem são as pessoas, de acordo com sua Graph, e informações sobre o histórico delas, quando disponíveis.
- **Organização:** o que a empresa delas faz, para quem e a que preço, quando isso for relevante para a reunião.
- **Até agora:** o que vocês discutiram, perguntaram e ofereceram, e em que ponto estão. Depois da reunião, essas mensagens aparecem como fontes da tarefa.
- **Combinado anteriormente:**, **Mudou desde então:** e **Ainda em aberto:** o que surgiu em reuniões anteriores com as mesmas pessoas. Cada linha indica a reunião ou mensagem de origem.
- **Promessas em aberto:** o que você ou as outras pessoas ainda precisam cumprir, de acordo com as promessas na sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado, e o que provavelmente será importante para as outras pessoas.

Ela chega na manhã de um dia útil: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia útil anterior. Serve apenas para consulta. Toque em **Feito** depois de ler. Uma promessa ou pergunta que exija uma ação gera sua própria tarefa.

Reuniões anteriores são consideradas quando há alguém de fora em ambas, seja qual for o nome da reunião e o endereço usado pela pessoa. The Machine lê as notas que estão na sua Machine: as suas, as do app de reuniões ou as que foram enviadas por e-mail. Se não houver notas, lê a transcrição ou as notas do evento no calendário. As reuniões mais recentes têm mais peso, e um assunto resolvido depois não aparece como em aberto.

Notas e mensagens do [Histórico](history.md) também são consideradas. Assim, o resumo pode incluir reuniões de antes de você começar a usar o produto.

Um resumo de trabalho não lê notas pessoais nem informações de outra Machine. O texto fica com você: um repasse nunca o inclui, e ele não pode ser enviado para revisão. Se não houver notas, essas linhas não aparecem.

O resumo usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também lê a página inicial do site da empresa.

Se a busca na web estiver configurada na sua Machine, ela também faz uma busca rápida na web pelo nome da pessoa e pela empresa. Uma Machine hospedada não vem com esse recurso. No seu próprio computador, você pode configurá-lo no OpenClaw. Os resultados vêm acompanhados de um link. A busca recebe apenas o nome público da pessoa, o nome da empresa e o site, nunca suas mensagens. Os resultados são reutilizados por 30 dias.

Assim, uma primeira reunião que você aceitou pode ter um resumo antes mesmo de vocês conversarem: o que a empresa faz, o que isso significa para você e, quando houver informações, quem é a pessoa. Se você só tiver o primeiro nome, o resultado da busca só será usado quando apontar para uma pessoa específica. Se **Buscar contatos de trabalho** estiver desativado em Configurações, em Segurança, nada será pesquisado.

Uma reunião recorrente só gera um resumo quando há algo novo desde a última vez: uma mensagem, notas ou uma promessa. O resumo mostra o que mudou, não repete o conteúdo do anterior. Ele chega depois que a reunião anterior termina, no máximo para duas reuniões recorrentes por dia.

Se não houver nada útil para dizer, nenhuma tarefa será criada. Reuniões internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua a mesma, com o novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é fechada automaticamente.

Se uma atualização mudar o conteúdo de um resumo, os resumos abertos de reuniões futuras serão reescritos uma vez, no novo formato. O título, as fontes e o lugar na lista não mudam. Um resumo que você alterou, adiou ou fechou continua como está. O mesmo vale para um resumo de uma reunião que começa nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque do chat.
