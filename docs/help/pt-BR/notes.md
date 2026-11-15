---
title: Notas
area: graph
summary: Uma página fácil de ler para cada assunto, como uma viagem ou sua casa, vinculada às pessoas e aos projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a71c5e46042cddd0
---
Uma nota é um resumo de um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto com Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

**Nova nota** no topo de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** inclui o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista para inserir o nome como link. A página do item vinculado mostra **Vinculado de** com sua nota.

## Notas dentro de outras notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra essa estrutura em árvore: toque na seta ao lado de uma nota para abrir as notas dentro dela. Para mover uma nota, toque em **Editar** e escolha onde colocá-la em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota ali mesmo.

No topo da página de uma nota, você vê onde ela fica, como **Notas › Filhos**. Toque em qualquer parte para ir até lá. No celular, as notas intermediárias ficam recolhidas no menu ⋯.

## Notas que sua Machine mantém

Sua Machine também cria notas com base nas suas mensagens e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail. Toque nela para abrir a mensagem. Uma linha de **O que aprendi** mostra **Com base no que aprendi**.

Uma reunião ou consulta no seu calendário nunca aparece como uma linha separada: ela fica em [Calendário](calendar.md). O mesmo vale para os e-mails relacionados: o convite, as respostas, as atualizações e os cancelamentos.

**Casa**, **Saúde** e **Filhos** só aparecem quando sua Machine tem pelo menos duas informações concretas para incluir, como uma conta ou algo que aprendeu. Até lá, elas nem aparecem na lista. Se ficarem sem informações de novo, desaparecem.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine mantém essas mudanças quando atualiza a nota. Se você excluir uma linha ou uma nota, ela não volta. Notas posteriores sobre o mesmo assunto ficam onde você colocou a primeira.

**Voltar ao original** mostra novamente as palavras da sua Machine. Se você editar uma linha que veio do que sua Machine aprendeu, ela também muda em **O que aprendi**, para que haja uma só versão.

## Páginas escritas

Quando uma nota tem pelo menos duas linhas das suas mensagens ou do que sua Machine aprendeu, sua Machine escreve o conteúdo da página no topo. Ela lê as conversas, não apenas os assuntos:

- Um resumo curto sobre o assunto e a situação atual.
- **Fatos importantes**, **Decisões**, **Itens em aberto** e uma **Linha do tempo**, cada um incluído somente quando há algo concreto a dizer.
- As linhas da nota aparecem abaixo, numeradas, em **Fontes**. Cada frase termina com os números das linhas usadas como fonte. Toque em um número para ir até a linha correspondente.

A página só é reescrita quando as linhas da nota mudam, no máximo cerca de uma vez por dia. Se as fontes não trouxerem nada concreto, não há página, apenas as linhas. Se você remover uma linha, o que veio somente dela também sai da página. Na lista de Notas, aparece o início do resumo da página abaixo do nome da nota.

Um projeto ou uma organização já tem sua própria página no Graph, com a descrição no topo. As conversas sobre eles vão para essa página, não para uma nota.

## Anotações das suas conversas

Sua Machine lê conversas inteiras e organiza cada uma na nota correspondente: uma conversa por e-mail de qualquer uma das suas caixas de entrada, um chat no WhatsApp, Slack, Telegram, LinkedIn ou outro app conectado, ou suas anotações de reunião. As mensagens de chat contam como uma conversa até o chat ficar sem atividade por dois dias.

- Uma conversa sobre um projeto ou uma organização no Graph vai para a página correspondente, não para uma nota nova.
- Uma conversa pode ficar em uma parte de **Casa**, **Saúde** ou **Filhos**, em uma nota sua ou em uma nota que sua Machine cria dentro de **Trabalho**, **Carro**, **Impostos** ou outra pasta.
- Sua Machine só cria uma nota nova para um assunto com pelo menos duas conversas ou para um assunto sobre o qual você escreveu e que claramente ainda está em andamento.
- Cada linha corresponde a uma conversa, da mais recente para a mais antiga. Toque nela para abrir a conversa.

Ela envia à IA um trecho curto de cada conversa, sem respostas citadas nem assinaturas. Cada conversa é analisada uma vez, e as novas mensagens são incluídas nela.

E-mails em massa e chats nunca vão para uma nota nem são enviados à IA: spam, promoções, newsletters e outras mensagens de listas, notificações automáticas, bots e canais de transmissão. Uma conversa em que você escreveu ainda conta, assim como e-mails de reservas para **Viagens** e **Eventos**.

Na primeira vez, sua Machine analisa os últimos três meses em algumas horas, fora do período noturno e somente enquanto houver espaço no seu plano de IA. Depois, ela organiza novas conversas quando houver dez aguardando ou quando uma estiver aguardando há meio dia.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega ao seu e-mail, sua Machine a adiciona a uma viagem em **Viagens**. As reservas da mesma jornada ficam em uma só viagem: a ida, o hotel e a volta. A viagem inclui o código da reserva, o assento e o bilhete de cada linha, em ordem cronológica, e mostra as datas. Em [Calendário](calendar.md), ela aparece como uma faixa ao longo desses dias. Toque nela para abrir a viagem.

Sua Machine lê os detalhes da reserva que companhias aéreas, hotéis e sites de reserva incluem nos e-mails de confirmação. Um e-mail sem esses detalhes não cria uma viagem. E-mails de reserva anteriores, dentro do ano de [histórico](history.md) que sua Machine mantém, são analisados em segundo plano assim que o histórico é carregado, começando pelas suas caixas de entrada Pessoais. Se uma confirmação antiga for lida depois, ela será adicionada à viagem que já existe.

Uma reserva alterada atualiza a linha correspondente, e uma reserva cancelada é removida. Quando todas as reservas de uma viagem são canceladas, a viagem também é removida.

## Eventos

Quando ingressos para um show, uma partida, um festival ou uma conferência chegam ao seu e-mail, sua Machine adiciona o evento em **Eventos**, com uma nota para cada evento. Uma linha informa o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento aparece na mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa em [Calendário](calendar.md). Toque nela para abrir a nota.

- Cada linha indica quem enviou os ingressos, como **De Example Tickets**, e abre o e-mail correspondente.
- Se o e-mail dos ingressos gerar uma tarefa, como pagar pelos ingressos, **Abrir a tarefa** mostra essa tarefa.
- Um evento reservado pelo seu e-mail de trabalho é de Trabalho. Caso contrário, é Pessoal.

Sua Machine lê os detalhes dos ingressos que os vendedores incluem nos e-mails de confirmação, sem usar IA. Um e-mail sem esses detalhes não cria um evento. Uma reserva cancelada é removida. Quando todos os ingressos de um evento são cancelados, o evento também é removido.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma parte aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha com a frequência e a data da última conta. **Abrir a tarefa** mostra a conta. O valor e os detalhes do pagamento ficam nela.
- Uma assinatura que você mantém ganha uma linha que abre a tarefa de **Assinaturas**. Uma assinatura cancelada não aparece na lista.
- Quem costuma escrever sobre sua casa, como a empresa de energia, a provedora de internet ou a prefeitura, ganha uma linha com a frequência das mensagens. Toque nela para abrir o e-mail mais recente.
- O que sua Machine aprendeu sobre sua casa, como a marca da sua lava-louças, também vira uma linha. Se você editar essa informação, ela também muda em **O que aprendi**.
- Se você mantiver sua própria nota em uma parte, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela vão para essa nota. Sua Machine não cria notas desse tipo por conta própria.

Só são usadas contas, assinaturas e mensagens Pessoais. As notas de Casa são sempre Pessoais. Sua Machine pergunta uma vez à IA sobre cada conta, assinatura ou informação nova que aprendeu, para identificar se é sobre sua casa. No caso de uma conta, ela informa quem a enviou, nunca o valor.

Suas conversas também vão para essas notas, como explicado acima em **Anotações das suas conversas**.

## Saúde

Em **Saúde**, sua Machine mantém o que sabe sobre sua saúde: **Consultas**, **Resultados dos testes**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma parte aparece quando tem pelo menos duas linhas.

- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa. O valor fica nela.
- Cada e-mail do seu consultório, de um hospital, laboratório ou plano de saúde vira uma linha com a data e o assunto, para que seu histórico se forme com o tempo. Toque na linha para abrir o e-mail.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também vira uma linha. Se você editar essa informação, ela também muda em **O que aprendi**.
- Se você tiver uma nota própria em uma parte, como uma nota sobre seu fisioterapeuta em **Consultas**, as informações sobre ele vão para essa nota.

As notas de Saúde são sempre Pessoais, mesmo quando uma conta chega ao seu endereço de trabalho. Sua Machine pergunta uma vez à IA sobre cada conta ou informação nova que aprendeu, para identificar se é sobre sua saúde.

## Filhos

Em **Filhos**, sua Machine mantém o que sabe sobre seus filhos: **Escola**, **Atividades**, **Cuidados infantis**, **Médicos e cuidados** e **Contas e taxas**. Babás e creches ficam em Cuidados infantis, nunca em Médicos e cuidados. Uma parte aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor ou o dia da aula de natação, vira uma linha vinculada à página dele. Ela considera alguém seu filho quando em **Para você** essa pessoa aparece como filha ou filho.
- Uma conta da escola, de um clube ou de uma creche ganha uma linha que abre a tarefa. O valor fica nela.
- Cada e-mail da escola, de um clube ou de uma creche, como um aviso sobre um passeio ou uma mudança de planos, vira uma linha com a data e o assunto. Assim, todas as mensagens ficam em um só lugar. Toque na linha para abrir o e-mail.
- Se você tiver uma nota própria para um filho em uma parte, como uma nota sobre Isla em **Escola**, as informações sobre essa criança vão para a nota.

As notas de Filhos são sempre Pessoais, mesmo quando a escola escreve para seu endereço de trabalho. Sua Machine pergunta uma vez à IA sobre cada informação nova para identificar se é sobre seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. Daí em diante, sua Machine adiciona novas informações a essa nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por alguns instantes. O mesmo acontece quando você remove uma linha.

## Diferente das anotações de reunião

As anotações de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas daqui são páginas próprias.
