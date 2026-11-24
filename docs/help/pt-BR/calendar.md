---
title: Calendário
area: calendar
summary: A semana à frente em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: d6f800709c378338
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas no dia em que voltam,
- atualizações sobre trabalhos que você repassou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegam por e-mail.

Uma reunião que aparece em dois calendários é exibida uma só vez. Um calendário que alguém compartilhou com você mostra os eventos dessa pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro ou de vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Na Agenda, uma viagem aparece primeiro em cada um dos seus dias. Na Semana e no Mês, aparece como uma faixa que atravessa esses dias, como "Viagem a Lisboa".

Um plano feito em conjunto é uma só promessa, marcada como "Com" e o nome da outra pessoa. Uma promessa sobre uma reunião com essa pessoa no mesmo dia aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução encontrou a tarefa concluída, não aparece como **Prazo**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os anteriores. Ela volta até uma semana antes de você conectar o calendário e mostra uma linha no topo indicando a partir de qual dia. Quando seu [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, aparecem até três itens por dia. No celular, aparecem pontos; toque em um dia para ver a lista.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem perder a legibilidade. Os outros aparecem como **+N**. Toque para abrir esse dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma com convidados, mostra os detalhes: quando e onde será, e quem vai participar. Uma pessoa que sua Graph conhece, assim como as organizações e os projetos associados à reunião, têm links para suas páginas. **Abrir no Google Calendar** ou **Abrir no Outlook**, logo abaixo, abre a reunião no respectivo calendário. Só de visualizar, nada é alterado.

Uma sala de reunião reservada para um evento aparece em onde, nunca como pessoa ou na sua Graph.

O link de uma reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para entrar.

## Viagens e eventos

Quando chega um e-mail de reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto, sua Machine adiciona a reserva a uma viagem. As reservas de uma mesma jornada ficam em uma só viagem, de qualquer uma das suas caixas de entrada: o trem até o aeroporto, os voos, o carro, a hospedagem e o caminho de volta. As reservas são agrupadas quando as datas se sobrepõem ou quando uma começa no fim da outra.

A viagem aparece como uma faixa que atravessa seus dias. Abra-a para ver cada reserva em ordem de horário, com os horários, o endereço, o código da reserva e o assento.

Ingressos para um show, jogo, festival ou conferência criam um evento, um por evento, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento aparece no evento existente. Um evento reservado pela sua caixa de e-mail de trabalho é Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem aparecem na viagem.

Para uma viagem que ainda vai acontecer, sua Machine avisa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites**, ou que não há transporte reservado do aeroporto até o hotel. Essas linhas aparecem em tom mais claro e com a etiqueta **Nenhuma reserva**. Se a viagem não tiver nenhuma hospedagem, ela não mostra informações sobre as noites.

- Cada linha informa de onde veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se o e-mail gerou uma tarefa, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza sua linha. Uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva de outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine lê sem IA. Quando isso não acontece, como em um e-mail encaminhado ou de um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns por vez, e aguarda quando você está perto do limite de uso. Os e-mails de reserva do ano coberto pelo [histórico](history.md) da sua Machine são lidos em segundo plano quando esse histórico estiver disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** registra palavra por palavra o que foi dito. Ela começa recolhida e mostra sua duração. Toque em **Mostrar** para abrir.

Se o conteúdo não carregar, o sistema tenta novamente automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte fica nela. Em uma reunião que você pode alterar, **Notas**, logo abaixo do formulário, abre as notas.

Com [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) conectado, as notas aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o conteúdo que você adicionou. Se ambos estiverem disponíveis, os dois aparecem.

Também é possível adicionar notas ao evento da reunião no calendário, depois que ela começar, ou recebê-las por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas com base nelas, mas só para próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma só tarefa, com a reunião como origem: "Origem: notas de" a reunião.

Uma reunião com transcrição e sem notas mostra **Gerar notas**. The Machine cria notas com base na transcrição: um resumo curto, decisões e itens de ação com quem vai realizá-los, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e o processo continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos e usa seu próprio modelo. As notas indicam **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: "adicione esta transcrição à reunião de planejamento de hoje". A transcrição vai para Transcrição e o resumo, para Notas. No Calendário, uma reunião com esses conteúdos mostra **Notas** ou **Transcrição**.

The Machine lê ambos para encontrar os follow-ups da reunião. Eles são de Trabalho ou Pessoal, como a reunião, e só vão para sua equipe quando a reunião também for de Trabalho.

A reunião abre com esses detalhes onde quer que você a encontre: em uma linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google aqui. O Outlook e os outros calendários são apenas para visualização. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** para removê-lo (toque duas vezes).

**Onde** sugere locais enquanto você digita: primeiro, os que você já usou e as suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção aparece somente no seu próprio calendário. A lista de convidados aparece acima do botão, que informa quantas pessoas serão convidadas: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém é convidado nem recebe uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que será alterado, e só a sua ação em **Adicionar**, **Salvar** ou **Excluir** aplica a mudança.

Ainda não há reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para sugerir outro horário ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Eventos de dia inteiro, com status livre ou provisório nunca contam, e cada conflito aparece uma só vez. Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê com o que ele coincide.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve:

- **Quem:** quem são essas pessoas, de acordo com sua Graph, incluindo informações sobre o histórico delas quando disponíveis.
- **Organização:** o que a empresa delas faz, para quem e a que preço, quando isso for relevante para a reunião.
- **Até agora:** o que vocês discutiram, perguntaram e ofereceram, e em que ponto está. Depois da reunião, essas mensagens aparecem como fontes da tarefa.
- **Combinado anteriormente:**, **Alterado desde então:** e **Ainda em aberto:** o que resultou de reuniões anteriores com as mesmas pessoas. Cada linha indica a reunião ou mensagem de origem.
- **Promessas em aberto:** o que você ou essas pessoas ainda precisam cumprir, com base nas promessas da sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser definido ou levado, e o que provavelmente será importante para as outras pessoas.

O resumo chega na manhã de um dia útil: no próprio dia da reunião quando ela acontece à tarde, ou no dia útil anterior. É apenas para leitura. Toque em **Feito** depois de ler. Uma promessa ou pergunta que exige alguma ação gera sua própria tarefa.

Reuniões anteriores são consideradas quando há alguém de fora da empresa em ambas, independentemente do nome da reunião ou do endereço usado. The Machine lê as notas disponíveis na sua Machine: as suas, as do app de reuniões ou as que chegaram por e-mail. Se não houver, lê a transcrição ou as notas do evento no calendário. As mais recentes têm mais peso, e um assunto resolvido depois não aparece como pendente.

Notas e mensagens do [Histórico](history.md) também são consideradas, para que o resumo inclua reuniões de antes de você começar a usar o serviço.

Um resumo de Trabalho não lê notas pessoais nem nada da Machine de outra pessoa. O texto fica só com você: ele não acompanha um repasse e não pode ser enviado para revisão. Se não houver notas, essas linhas não aparecem.

O resumo usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também consulta a página inicial do site da empresa.

Se houver um provedor de busca na web configurado no OpenClaw, o que não vem instalado em uma Machine hospedada, o sistema também faz uma busca rápida na web pelo nome da pessoa e da empresa. Os resultados incluem um link. Só o nome público da pessoa, o nome da empresa e o site são enviados para a busca, nunca suas mensagens. Os resultados são reutilizados por 30 dias.

Assim, uma primeira reunião que você aceitou pode ter um resumo antes de vocês trocarem qualquer mensagem: o que a empresa faz, o que isso significa para você e, quando possível, quem é a pessoa. Se você tiver apenas o primeiro nome, os resultados da busca só são usados quando apontam para uma única pessoa. Com **Buscar contatos de trabalho** desativado em Configurações, Segurança, nada é pesquisado.

Uma reunião recorrente só gera um resumo quando há novidades desde a última vez, como uma mensagem, notas ou uma promessa. O resumo mostra o que mudou, não o que já estava no resumo anterior. Ele chega depois que termina a reunião anterior, no máximo para duas reuniões recorrentes por dia.

Se não houver nada útil a dizer, não será criada uma tarefa. Reuniões internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua a mesma e passa para o novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é fechada automaticamente.

Quando uma atualização altera o conteúdo do resumo, os resumos abertos de reuniões futuras são reescritos uma vez, já com as informações novas. O título, as fontes e o lugar na lista continuam iguais. Um resumo que você alterou, adiou ou fechou não muda. O mesmo vale para o resumo de uma reunião que começa nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**. Toque uma vez para abrir o chat dela.
