---
title: Calendário
area: calendar
summary: A semana à frente em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 7187a83e373922b3
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você delegou,
- promessas com data.

Uma reunião que aparece em dois calendários é exibida uma só vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca geram tarefas. Eventos de dia inteiro e com vários dias são exibidos como eventos de dia inteiro em cada dia que abrangem.

Um plano feito em conjunto é uma só promessa, marcada como "Com" e o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída (você já respondeu ou a execução dela concluiu que foi feita) não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias, ou para cima (ou toque em **Mostrar dias anteriores**) para ver os anteriores. Ela volta até uma semana antes de você conectar seu calendário e mostra no topo uma linha indicando a partir de qual dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, são exibidos três dias.
- **Mês** mostra o mês inteiro. No computador, são exibidos até três itens por dia; no celular, aparecem pontos. Toque em um dia para ver a lista de eventos.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem prejudicar a leitura. Os demais aparecem como **+N**. Toque para abrir esse dia na agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma com convidados, mostra os detalhes: quando, onde e quem. As pessoas que o Graph reconhece, além das organizações e dos projetos relacionados à reunião, levam às respectivas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre a reunião no serviço correspondente. Apenas visualizar não altera nada.

Uma sala de reunião reservada para uma reunião aparece em onde, nunca como pessoa ou no seu Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para entrar.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** traz o resumo: decisões e itens de ação. **Transcrição** mostra palavra por palavra o que foi dito. Ela começa recolhida e indica a duração. Toque em **Mostrar** para abrir.

Se não carregar, ela tenta novamente por conta própria por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O que você adiciona em uma parte fica nela. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Com [Zoom](zoom.md) ou [Google Meet](google-meet.md) conectado, as notas do serviço aparecem em Notas e a transcrição aparece em Transcrição, marcadas como **Do Zoom** ou **Do Google Meet**. Elas nunca substituem o que você adicionou. Se as duas versões estiverem disponíveis, ambas serão exibidas.

As notas também podem vir do próprio evento da reunião no calendário, adicionadas depois que ela começou, ou por e-mail do Zoom ou do Gemini. Depois que a reunião termina, The Machine cria tarefas a partir delas somente quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, elas geram uma só tarefa, cuja origem é a reunião: **Notas de** reunião.

Uma reunião com transcrição, mas sem notas, tem a opção **Gerar notas**. The Machine cria as notas a partir da transcrição: um resumo curto, decisões e itens de ação com as pessoas responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e o processo continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos. Para isso, é usado o modelo que você escolheu. As notas indicam **Escrito por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: "adicione esta transcrição à reunião de hoje do conselho". A transcrição vai para Transcrição; o resumo, para Notas. No Calendário, uma reunião com esses itens mostra **Notas** ou **Transcrição**.

The Machine lê ambos para acompanhar os próximos passos da reunião. Eles são classificados como Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também vai.

Uma reunião abre com esses detalhes onde quer que você a encontre: na linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte de baixo, mostra o convite como foi recebido.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e os outros calendários são apenas para visualização. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Somente as palavras que você digitar serão enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas que receberão um convite aparecem acima do botão, que indica quantas são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe convite nem atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar um compromisso para buscar alguém. Ela mostra exatamente o que vai mudar. A alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não há reuniões? Se você não tiver um calendário, **Conecte seu calendário** abre Conexões. Conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar um recado curto para remarcar ou sugerir recusar o convite. Nada é enviado até você aprovar.

Eventos de dia inteiro, com status livre ou provisório nunca são considerados, e cada conflito aparece uma só vez. Uma tarefa de Trabalho só informa que há um conflito, para sua equipe nunca ver o evento pessoal. Só você vê com o que ele coincide.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Prepare-se para** a reunião. É um breve resumo:

- **Quem:** quem são, de acordo com seu Graph.
- **Último contato:** sua última conversa com essas pessoas. Essa mensagem será a origem da tarefa depois da reunião.
- **Promessas em aberto:** o que você ou elas ainda precisam fazer.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser resolvido ou levado.

A tarefa aparece na manhã de um dia útil: no próprio dia da reunião, se ela for à tarde; caso contrário, no dia útil anterior. Ela usa somente o que já está na sua Machine. É só para leitura. Toque em **Feito** depois de ler. Uma promessa ou pergunta que exija uma ação terá sua própria tarefa.

Se não houver histórico útil, nenhuma tarefa é criada. Reuniões recorrentes, internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, a tarefa continua sendo a mesma e passa para o novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Os detalhes da reunião mostram a tarefa em **Tarefa**. Toque nela para abrir o chat.
