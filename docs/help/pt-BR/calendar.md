---
title: Calendário
area: calendar
summary: A semana à frente em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9b7475608bb04e5c
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você repassou,
- promessas com data,
- [viagens e eventos](calendar.md#trips-and-events) encontrados nos e-mails de reservas e ingressos.

Uma reunião que aparece em dois calendários é exibida uma só vez. Os eventos de um calendário que alguém compartilhou com você aparecem esmaecidos, com o primeiro nome da pessoa. Eles nunca geram uma tarefa. Eventos que duram o dia todo ou vários dias aparecem como eventos de dia inteiro em cada dia que abrangem. Na Agenda, uma viagem aparece primeiro em cada um dos dias. Nas visualizações Semana e Mês, aparece como uma faixa que cobre todos os dias, como “Viagem a Lisboa”.

Um plano combinado é uma só promessa, marcada com “Com” e o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque uma execução detectou que ela foi concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** mostra os dias um por um. Role para baixo para ver os próximos dias ou para cima (ou toque em **Mostrar dias anteriores**) para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário, e uma linha no topo indica a partir de que dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos. Toque em um dia para ver a lista de itens.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva naquele dispositivo.

Na grade semanal, eventos que acontecem no mesmo horário ficam lado a lado, mas continuam fáceis de ler. Os demais aparecem como **+N**. Toque para abrir aquele dia na agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a viagem ou o evento, ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma com convidados, mostra os detalhes: quando e onde acontece, e quem participa. As pessoas que seu Graph conhece, as organizações e os projetos associados à reunião têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre o item no calendário correspondente. Só de olhar, nada é alterado.

Uma sala de reunião reservada para uma reunião aparece abaixo do local, nunca como pessoa nem no seu Graph.

Um link de reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Viagens e eventos

Quando um e-mail com uma reserva de voo, hotel, casa de temporada, trem, ônibus, balsa, carro alugado, táxi ou estacionamento no aeroporto chega, sua Machine adiciona a reserva a uma viagem. As reservas de uma mesma jornada ficam em uma viagem, mesmo que venham de caixas de entrada diferentes: o trem até o aeroporto, os voos, o carro, a hospedagem e a volta. As reservas são agrupadas quando os dias se sobrepõem ou uma começa quando a outra termina.

A viagem aparece como uma faixa que cobre todos os dias. Abra-a para ver cada reserva em ordem cronológica, com os horários, o endereço, o código da reserva e o assento.

Ingressos para um show, uma partida, um festival ou uma conferência criam um evento, um para cada ocasião, com o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado ao evento existente. Um ingresso reservado na sua caixa de entrada de trabalho é marcado como Trabalho. Caso contrário, é marcado como Pessoal. Ingressos para algo que acontece durante uma viagem são adicionados à viagem.

Para uma viagem futura, sua Machine informa o que está faltando, como **Nenhuma hospedagem reservada para 2 noites** ou nenhuma reserva para ir do aeroporto ao hotel. Essas linhas aparecem esmaecidas e marcadas como **Nenhuma reserva**. Se não houver nenhuma hospedagem na viagem, não aparecem avisos sobre as noites.

- Cada linha informa de quem veio a reserva, como **Do Example Tickets**, e abre o e-mail correspondente.
- Se o e-mail também gerou uma tarefa, como pagar os ingressos, **Abrir a tarefa** mostra essa tarefa.
- Uma reserva alterada atualiza a linha correspondente, e uma reserva cancelada é removida. Quando todas as reservas são canceladas, a viagem ou o evento também é removido.
- Uma reserva de outra pessoa, como o voo de um colega encaminhado para você, não aparece nas suas viagens.

A maioria das confirmações traz os detalhes em um formato que sua Machine consegue ler sem IA. Quando isso não acontece, como em um e-mail encaminhado ou de um site de reservas pequeno, seu [modelo](model.md) lê o e-mail em segundo plano, alguns de cada vez, e aguarda se você estiver perto do limite de uso. Os e-mails de reserva do ano incluído no [histórico](history.md) que sua Machine mantém são lidos em segundo plano assim que esse histórico estiver disponível.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** mostra palavra por palavra o que foi dito. Ela começa recolhida, com a duração indicada. Toque em **Mostrar** para abri-la.

Se não carregarem, as notas ou a transcrição tentam carregar novamente por conta própria durante cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem as próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte permanece nela. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Se você conectar [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md), as notas do serviço aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom**, **Do Google Meet** ou **Do Granola**. Elas nunca substituem o que você adicionou. Se houver conteúdo dos dois tipos, os dois aparecem.

As notas também podem vir do próprio evento da reunião no calendário, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas com base nelas somente quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, será criada uma só tarefa, com a reunião como origem: “Origem: notas de” seguida do nome da reunião.

Uma reunião com transcrição, mas sem notas, mostra a opção **Gerar notas**. The Machine cria as notas com base na transcrição: um resumo curto, decisões e itens de ação com o nome de quem vai realizá-los, no idioma da reunião.

Aparece **Escrevendo as notas…**, e o processo continua mesmo que você feche a reunião. Uma transcrição longa pode levar alguns minutos para ser processada, usando seu próprio modelo. As notas são marcadas como **Escrito pela The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça em uma tarefa, por exemplo: “adicione esta transcrição às notas da reunião de hoje do quadro”. Uma transcrição vai para Transcrição e um resumo, para Notas. Na agenda, as reuniões com notas ou transcrições mostram **Notas** ou **Transcrição**.

The Machine lê as duas para identificar os follow-ups da reunião. Eles são marcados como Trabalho ou Pessoal, assim como a reunião, e só são enviados para sua equipe quando a reunião também é.

A reunião abre com esses detalhes em qualquer lugar em que você a encontre: na linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, no final, mostra o convite como chegou.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e outros calendários são somente para consulta. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, o título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os lugares que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. Quem receberá um convite aparece acima do botão, que também informa a quantidade: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite ou uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que será alterado, e a alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não há reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para remarcar ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Se um evento coincidir com vários outros, será criada uma só tarefa sobre esse evento. Um novo conflito é adicionado à tarefa enquanto ela estiver em aberto. Depois que ela for concluída ou descartada, só uma reunião criada ou alterada posteriormente fará com que o conflito apareça de novo.

Eventos de dia inteiro, com disponibilidade livre ou provisórios nunca contam, e cada conflito é exibido uma só vez. O local de trabalho, o horário de concentração e o status de ausência do Google também não contam. Um bloqueio de horário criado por você que inclui outras reuniões, como um dia no escritório, também não conta. Só as reuniões dentro dele podem gerar conflitos. Já um bloqueio sem outras pessoas nem reuniões, como um voo, ainda pode coincidir com um evento que tenha outras pessoas.

Uma tarefa de Trabalho informa apenas que há um conflito, então sua equipe nunca vê o evento pessoal. Só você vê com o que ele coincide: os dois primeiros eventos e a quantidade dos demais. Uma tarefa que você não fez nada para resolver é encerrada automaticamente quando o conflito envolve outra tarefa ou quando não era um conflito de verdade.

## Prepare-se para as reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo curto com as seguintes informações:

- **Quem:** quem são essas pessoas, com base no seu Graph, e alguns dados sobre a trajetória delas, quando disponíveis.
- **Organização:** o que a empresa delas faz, para quem e a que preço, quando isso for relevante para a reunião.
- **Até agora:** o que vocês conversaram, perguntaram e ofereceram, e em que pé está. Depois da reunião, essas mensagens aparecem como origens da tarefa.
- **Combinado antes:**, **Alterado desde então:** e **Ainda em aberto:** o que surgiu em reuniões anteriores com as mesmas pessoas. Cada linha indica a reunião ou a mensagem de onde veio.
- **Promessas em aberto:** o que você ou essas pessoas ainda precisam cumprir, com base nas promessas da sua Machine.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser resolvido ou levado, e o que provavelmente será importante para essas pessoas.

A tarefa chega pela manhã, em um dia útil: no próprio dia da reunião, quando ela acontece à tarde; caso contrário, no dia útil anterior. É só para consulta: toque em **Feito** depois de ler. Uma promessa ou pergunta que exija uma ação gera uma tarefa própria.

Reuniões anteriores contam quando há alguém de fora nas duas, independentemente do nome da reunião ou do endereço de e-mail usado. A tarefa usa as notas que sua Machine tiver: as suas, as do aplicativo de reuniões ou as que foram enviadas por e-mail; se não houver, usa a transcrição ou as notas do evento no calendário. As notas mais recentes têm mais peso, e um assunto resolvido depois não aparece como em aberto.

As notas e mensagens do [Histórico](history.md) também contam. Assim, o resumo pode incluir reuniões de antes de você começar a usar a Machine.

Um resumo de Trabalho não lê notas pessoais nem conteúdo da Machine de outra pessoa. O texto fica só com você: ele não é incluído em um repasse nem pode ser enviado para revisão. Se não houver notas, essas linhas não aparecem.

O resumo usa o que já está na sua Machine. Para uma primeira reunião com alguém de uma empresa, também consulta a página inicial do site da empresa.

Quando a busca na web está configurada na sua Machine, ela também faz uma busca rápida na web pelo nome da pessoa e da empresa. Uma Machine hospedada não inclui essa opção. No seu próprio computador, você pode configurá-la no OpenClaw. Os resultados aparecem com um link. Só o nome público da pessoa, o nome da empresa e o site são enviados para a busca, nunca suas mensagens. Os resultados são reutilizados por 30 dias.

Assim, uma reunião inicial que você aceitou pode ter um resumo antes de vocês trocarem uma palavra: o que a empresa faz, o que isso significa para você e, quando disponível, quem é a pessoa. Se você tiver apenas o primeiro nome, os resultados da busca só serão usados quando apontarem para uma única pessoa. Se **Buscar contatos de trabalho** estiver desativado em Configurações, Segurança, nada será pesquisado.

Uma reunião recorrente só recebe um resumo quando há algo novo desde a última vez: uma mensagem, notas ou uma promessa. O resumo mostra o que há de novo, não o que dizia o resumo anterior. Ele chega depois que termina o horário da reunião anterior, no máximo para duas reuniões recorrentes por dia.

Se não houver nada útil para dizer, nenhuma tarefa é criada. Reuniões internas, pessoais e recusadas não geram tarefas. Se uma reunião mudar de horário, a mesma tarefa permanece, com o novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Quando uma atualização altera o conteúdo do resumo, os resumos de reuniões futuras ainda em aberto são refeitos uma vez, já com as informações novas. O título, as origens e a posição na lista continuam iguais. Um resumo que você alterou, adiou ou encerrou não muda. O mesmo vale para o resumo de uma reunião que começa nos próximos minutos.

Os detalhes da reunião mostram a tarefa em **Tarefa**, a um toque do chat.
