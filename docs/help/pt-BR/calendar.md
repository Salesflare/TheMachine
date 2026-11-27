---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 479aa9c3fadda8bd
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas com prazo naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos do trabalho que você passou para outras pessoas,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) das reservas e dos ingressos que chegam por e-mail.

Uma reunião que aparece em dois calendários é exibida uma só vez. Um calendário que alguém compartilhou com você mostra os eventos dessa pessoa em tom suave, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro e de vários dias aparecem como eventos de dia inteiro em cada dia que abrangem. Na Agenda, uma viagem aparece primeiro em cada um dos seus dias. Na Semana e no Mês, aparece como uma faixa que atravessa esses dias, como "Viagem a Lisboa".

Um plano feito em conjunto é uma só promessa, marcada como "Com" e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução identificou que ela foi concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima, ou toque em **Mostrar dias anteriores**, para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo informa a partir de qual dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, aparecem até três itens por dia. No celular, aparecem pontos. Toque em um dia para ver a lista de itens.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem prejudicar a leitura. Os demais aparecem como **+N**. Toque para abrir esse dia na agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma com convidados, mostra os detalhes: quando, onde e quem. Alguém que sua Graph conhece, assim como as organizações e os projetos relacionados à reunião, tem um link para sua página. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre a reunião nesse serviço. Apenas visualizar não altera nada.

Uma sala de reunião reservada para uma reunião aparece em onde, nunca como pessoa nem na sua Graph.

Um link de reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto chega ao seu e-mail, sua Machine a adiciona a uma viagem. Reservas da mesma jornada ficam em uma só viagem, de qualquer uma das suas caixas de e-mail: o trem até o aeroporto, os voos, o carro, a hospedagem e a volta. As reservas são agrupadas quando as datas se sobrepõem ou quando uma começa no dia em que a outra termina.

A viagem aparece como uma faixa que atravessa seus dias. Abra-a para ver cada reserva em ordem cronológica, com horários, endereço, código da reserva e assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um por evento, com o local, o código da reserva, o assento e a quantidade de ingressos. Um segundo pedido para o mesmo evento é incluído nele. Um evento reservado na sua caixa de e-mail de trabalho é de Trabalho. Caso contrário, é Pessoal. Ingressos para algo que acontece durante uma viagem são incluídos na viagem.

Se uma viagem ainda não aconteceu, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites**, ou que não há transporte reservado do aeroporto ao hotel. Essas linhas aparecem em tom suave e com a etiqueta **Nenhuma reserva**. Uma viagem sem hospedagem não informa nada sobre as noites.

- Cada linha informa de quem veio a reserva, como **Do Example Tickets**, e abre esse e-mail.
- Se uma tarefa veio do e-mail, como pagar os ingressos, **Abrir a tarefa** mostra a tarefa.
- Uma reserva alterada atualiza a linha, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva para outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações inclui os detalhes em um formato que sua Machine lê sem IA. Quando isso não acontece, como em um e-mail encaminhado ou em um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda quando você está perto do limite de uso. E-mails de reserva do ano incluído no [histórico](history.md) mantido pela sua Machine são lidos em segundo plano quando esse histórico fica disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** são o resumo: decisões e itens de ação. **Transcrição** é o que foi dito, palavra por palavra. Ela começa recolhida, com a duração. Toque em **Mostrar** para abrir.

Se não carregarem, elas tentam carregar de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada uma tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma não aparece na outra. Em uma reunião que você pode alterar, **Notas** abaixo do formulário abre as notas.

Com [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) conectados, as notas aparecem em Notas e a transcrição em Transcrição, identificadas como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Quando há conteúdo nos dois lugares, tudo é exibido.

As notas também podem vir do evento da reunião no próprio calendário, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, a The Machine cria tarefas a partir delas somente para próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma só tarefa, com a reunião como origem: "Origem: notas de" a reunião.

Uma reunião com transcrição e sem notas mostra **Gerar notas**. A The Machine escreve as notas com base na transcrição: um resumo curto, decisões e itens de ação com quem vai realizá-los, no idioma da reunião.

A tela mostra **Escrevendo as notas…** e o processo continua quando você fecha a reunião. Uma reunião longa pode levar alguns minutos, usando seu próprio modelo. As notas indicam **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

A The Machine também pode adicioná-las. Peça no chat de uma tarefa, por exemplo: "adicione esta transcrição à reunião de hoje do quadro". Uma transcrição vai para Transcrição, e um resumo vai para Notas. Uma reunião com notas ou transcrição mostra **Notas** ou **Transcrição** no Calendário.

A The Machine lê as duas para encontrar os follow-ups da reunião. Eles são de Trabalho ou Pessoais, assim como a reunião, e só vão para sua equipe quando a reunião também for para ela.

A reunião abre com esses detalhes onde quer que você a encontre: em uma linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google aqui. O Outlook e outros calendários são apenas para visualização. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, o título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares conforme você digita: primeiro, lugares que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. Os convidados aparecem acima do botão, que informa quantos são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe convite nem atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que vai mudar, e só **Adicionar**, **Salvar** ou **Excluir** faz a alteração.

Ainda não tem reuniões? Se não houver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho se sobrepõe a algo no seu calendário pessoal, ou vice-versa, a The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para propor outro horário ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Um evento que se sobrepõe a vários outros gera uma só tarefa sobre esse evento. Uma nova sobreposição é adicionada à tarefa enquanto ela estiver em aberto. Depois que ela for concluída ou descartada, só uma reunião criada ou alterada mais tarde fará com que volte.

Eventos de dia inteiro, com disponibilidade livre ou provisórios nunca contam, e cada conflito é identificado uma só vez. O local de trabalho, o período de concentração e o status "Fora do escritório" do Google também não contam. Um bloqueio criado por você que contenha outras reuniões, como um dia no escritório, também não conta. Só as reuniões dentro dele podem entrar em conflito. Um bloqueio sem outras pessoas nem reuniões, como um voo, ainda entra em conflito com um evento que tenha outras pessoas.

Uma tarefa de Trabalho só informa que há um conflito, para que sua equipe nunca veja o evento pessoal. Só você vê com o que ele está em conflito: os dois primeiros eventos e, em seguida, a quantidade dos demais. Uma tarefa que você não fez nada para resolver se fecha automaticamente quando o conflito está em outra tarefa ou quando, na verdade, não havia conflito.

## Preparação para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, a The Machine cria uma tarefa: **Preparar para** a reunião. É um resumo breve:

- **Quem:** quem são essas pessoas, de acordo com sua Graph, com informações sobre o histórico delas quando disponível.
- **Organização:** o que a empresa delas faz, para quem e a que preço, quando isso for relevante para a reunião.
- **Até agora:** o que vocês discutiram, perguntaram e ofereceram, e em que ponto estão. Depois da reunião, essas mensagens são as fontes da tarefa.
- **Combinado antes:**, **Mudou desde então:** e **Ainda em aberto:** o que surgiu em reuniões anteriores com as mesmas pessoas, cada linha com a reunião ou mensagem de origem.
- **Promessas em aberto:** o que você ou essas pessoas ainda precisam fazer, com base nas promessas da sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado e o que provavelmente será importante para as outras pessoas.

A tarefa aparece na manhã de um dia de trabalho: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia de trabalho anterior. Ela serve para consulta: fica como **Feito** depois que você a lê. Uma promessa ou pergunta que exija alguma ação tem sua própria tarefa.

Pergunte sobre a reunião no chat dela ou adicione o que você sabe. A The Machine responde ou incorpora sua anotação ao resumo, por exemplo em **Decidir ou levar**, e aprende com ela. Nada é enviado a partir do resumo.

Reuniões anteriores contam quando alguém de fora participou de ambas, independentemente do nome da reunião e do endereço usado. A The Machine lê as notas que sua Machine tem: as suas, as do aplicativo de reunião ou as que o aplicativo enviou por e-mail. Se não houver, ela lê a transcrição ou as notas no evento do calendário. As mais recentes têm mais peso, e um assunto resolvido depois não aparece como em aberto.

Notas e mensagens do [Histórico](history.md) também contam, para que o resumo inclua reuniões de antes de você começar a usar o produto.

Um resumo de Trabalho não lê notas pessoais nem informações da Machine de outra pessoa. O texto fica com você: um repasse nunca o leva junto, e ele não pode ser enviado para revisão. Se não houver notas, essas linhas não aparecem.

O resumo usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também lê a página inicial do site da empresa.

Quando a busca na web está configurada na sua Machine, ela também faz uma busca rápida na web pelo nome da pessoa e da empresa. Uma Machine hospedada não vem com esse recurso. No seu próprio computador, você pode configurá-lo no OpenClaw. Os resultados incluem um link. Só o nome público da pessoa, o nome da empresa e o site são enviados à busca, nunca suas mensagens. Os resultados são reutilizados por 30 dias.

Assim, uma reunião inicial que você aceitou pode ter um resumo antes mesmo de vocês trocarem uma palavra: o que a empresa faz, o que isso significa para você e, quando disponível, quem é a pessoa. Se você só tiver o primeiro nome, a busca só é usada quando aponta para uma única pessoa. Se **Buscar contatos de trabalho** estiver desativado em Configurações, em Segurança, nada será pesquisado.

Uma reunião recorrente só gera um resumo quando algo mudou desde a última vez: uma mensagem, notas ou uma promessa. O resumo mostra o que há de novo, não o que dizia o resumo anterior. Ele aparece depois que o horário da reunião anterior termina, para no máximo duas reuniões recorrentes por dia.

Se não houver nada útil a dizer, nenhuma tarefa é criada. Reuniões internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, ela mantém a mesma tarefa, agora no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada se fecha automaticamente.

Quando uma atualização altera o conteúdo de um resumo, os resumos em aberto de reuniões futuras são reescritos uma vez, com as novas informações. O título, as fontes e a posição na lista permanecem iguais. Um resumo que você alterou, adiou ou fechou não muda. O mesmo vale para um resumo de uma reunião que vai começar nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque do chat dela.
