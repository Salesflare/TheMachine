---
title: Notas
area: graph
summary: Uma página fácil de consultar para cada assunto, como uma viagem ou sua casa, vinculada às pessoas e aos projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, folder_overview.py, memory_seed.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 1087ac0970878932
---
Uma nota é um resumo de um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, ao lado de Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

Toque em **Nova nota** no topo de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** inclui o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista para inserir o nome como link. Na página do item vinculado, aparece **Vinculado de** com sua nota.

## Notas dentro de outras notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra essa estrutura em árvore: toque na seta ao lado de uma nota para abrir as notas dentro dela. Para mover uma nota, toque em **Editar** e escolha onde ela ficará em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota ali mesmo.

No topo da página de uma nota, você vê onde ela fica, como **Notas › Filhos**. Toque em qualquer parte para abrir esse local. No celular, as notas intermediárias ficam recolhidas no menu ⋯.

## Notas que sua Machine mantém

Sua Machine também cria notas automaticamente a partir das suas mensagens e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o email. Toque nela para abrir a mensagem. Uma linha de **O que aprendi** mostra **Com base no que aprendi**.

Uma reunião ou consulta na sua agenda nunca aparece como uma linha separada: ela continua em [Calendário](calendar.md). O mesmo vale para os emails relacionados: o convite, as respostas, as atualizações e os cancelamentos.

**Casa**, **Saúde** e **Filhos** só aparecem quando sua Machine tem pelo menos duas informações concretas para incluir, como uma conta ou algo que aprendeu. Até lá, elas não aparecem na lista. Se ficarem sem conteúdo de novo, desaparecem.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine manterá essas mudanças quando atualizar a nota. Se você excluir uma linha ou uma nota, ela não voltará. Notas futuras sobre o mesmo assunto serão adicionadas onde você colocou a primeira.

**Voltar ao original** mostra novamente o texto que sua Machine escreveu. Se você editar uma linha que veio do que sua Machine aprendeu, ela também será alterada em **O que aprendi**, para que haja uma única versão.

## Páginas escritas

Quando uma nota tem pelo menos duas linhas das suas mensagens ou do que sua Machine aprendeu, sua Machine escreve um resumo no topo da página. Ela lê as conversas, não apenas os assuntos:

- Um resumo curto: do que se trata e qual é a situação.
- **Fatos importantes**, **Decisões**, **Itens em aberto** e uma **Linha do tempo**, cada um incluído apenas quando há algo concreto a dizer.
- As linhas da nota aparecem abaixo, numeradas, em **Fontes**. Cada frase termina com os números das linhas usadas como fonte. Toque em um número para ir até a linha.

A página só é reescrita quando as linhas da nota mudam, no máximo mais ou menos uma vez por dia. Se as fontes não trouxerem nada concreto, não há página, apenas as linhas. Se você remover uma linha, tudo o que veio somente dela também será removido da página. Na lista de Notas, o começo do resumo aparece abaixo do nome da nota.

Um projeto ou uma organização já tem sua própria página no Graph, com uma descrição no topo. As conversas sobre eles ficam nessa página, não em uma nota.

## Visões gerais

Uma nota com outras notas dentro dela, como **Trabalho** ou **Casa**, ganha uma visão geral curta no topo quando pelo menos duas dessas notas têm novidades: uma ou duas frases sobre o que está acontecendo e alguns acontecimentos recentes ou próximos. No fim de cada item, aparecem os nomes das notas de onde ele veio. Toque em um nome para abrir a nota.

A visão geral é criada a partir das páginas e das linhas mais recentes das notas dentro dela, no máximo uma vez por dia e somente quando houver mudanças. Quando não há novidades, não há visão geral. Na lista de Notas, o começo dela aparece abaixo do nome da pasta.

## Anotações das suas conversas

Sua Machine lê conversas completas e organiza cada uma na nota relacionada: uma conversa por email de qualquer uma das suas caixas de entrada, um chat no WhatsApp, Slack, Telegram, LinkedIn ou outro app conectado, e suas anotações de reuniões. As mensagens de chat contam como uma conversa até o chat ficar sem atividade por dois dias.

- Uma conversa sobre um projeto ou uma organização no seu Graph vai para a página desse item, não para uma nota nova.
- Uma conversa pode ficar em uma seção de **Casa**, **Saúde** ou **Filhos**, em uma nota sua ou em uma nota que sua Machine cria dentro de **Trabalho**, **Carro**, **Impostos** ou outra pasta.
- Sua Machine só cria uma nota nova para um assunto com pelo menos duas conversas ou para um assunto sobre o qual você escreveu e que claramente continua em andamento.
- Cada linha representa uma conversa, da mais recente para a mais antiga. Toque nela para abrir a conversa.

Ela envia à IA um trecho curto de cada conversa, sem respostas citadas nem assinaturas. Cada conversa é analisada uma vez, e as novas mensagens são incluídas nela.

Emails em massa e chats nunca vão para uma nota nem são enviados à IA: spam, promoções, newsletters e outros emails de listas, notificações de endereços que não aceitam respostas, bots e canais de transmissão. Uma conversa em que você escreveu ainda conta. Emails de reservas para **Viagens** e **Eventos** também contam.

Na primeira vez, sua Machine analisa as conversas dos últimos três meses ao longo de algumas horas, fora do período da noite e somente enquanto houver espaço no seu plano de IA. Depois, ela organiza as conversas novas quando houver dez esperando ou quando uma delas estiver esperando há meio dia.

## Notas da memória do OpenClaw

Se você já usou o OpenClaw, sua Machine lê uma vez as páginas sobre assuntos específicos na pasta de memória, como uma página sobre uma viagem ou sua saúde. O que for relevante vai para a nota sobre o assunto ou para uma nota nova. Cada linha indica de que página veio, como **Das páginas da sua memória · Lisboa**, e inclui a data. Passe o cursor sobre ela para ver onde fica essa página.

Ela nunca altera essas páginas e ignora registros diários, páginas sobre a própria assistente e pastas marcadas como sensíveis ou privadas. Ela lê no máximo 80 páginas, algumas de cada vez, e não volta a lê-las.

## Viagens

Quando sua caixa de entrada recebe uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado, sua Machine adiciona a reserva a uma viagem em **Viagens**. As reservas da mesma viagem ficam juntas: a ida, o hotel e a volta. A viagem inclui o código da reserva, o assento e o bilhete de cada linha, em ordem cronológica, e mostra as datas. Em [Calendário](calendar.md), ela aparece como uma faixa que cobre esses dias e abre a viagem.

Sua Machine lê os detalhes da reserva que companhias aéreas, hotéis e sites de reserva incluem nos emails de confirmação. Um email sem esses detalhes não cria uma viagem. Emails de reserva anteriores ao período do ano coberto pelo [histórico](history.md) que sua Machine mantém são lidos em segundo plano quando o histórico estiver pronto, começando pelas suas caixas de entrada pessoais. Se uma confirmação mais antiga for lida depois, ela será adicionada à viagem que já existe.

Se uma reserva mudar, a linha correspondente será atualizada. Se for cancelada, a linha será removida. Quando todas as reservas de uma viagem forem canceladas, a viagem também será removida.

## Eventos

Quando sua caixa de entrada recebe ingressos para um show, uma partida, um festival ou uma conferência, sua Machine adiciona o evento em **Eventos**, em uma nota por evento. Uma linha informa o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento vai para a mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa em [Calendário](calendar.md), que abre a nota.

- Cada linha informa de quem vieram os ingressos, como **De Example Tickets**, e abre o email correspondente.
- Se um email dos ingressos gerar uma tarefa, como pagar pelos ingressos, **Abrir a tarefa** mostra essa tarefa.
- Um evento reservado pela sua caixa de entrada do trabalho é de Trabalho. Caso contrário, é Pessoal.

Sua Machine lê os detalhes dos ingressos que os vendedores incluem nos emails de confirmação, sem usar IA. Um email sem esses detalhes não cria um evento. Se uma reserva for cancelada, ela será removida. Quando todos os ingressos de um evento forem cancelados, o evento também será removido.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha com a frequência de cobrança e a data da última conta. **Abrir a tarefa** mostra a própria conta. O valor e os detalhes de pagamento ficam nela.
- Uma assinatura que você mantém ganha uma linha que abre a tarefa em **Assinaturas**. Assinaturas canceladas não aparecem.
- Quem escreve para você regularmente sobre sua casa, como a empresa de energia, a provedora de internet ou a prefeitura, ganha uma linha que informa a frequência das mensagens. Toque nela para abrir o email mais recente.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também aparece em uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- Se você tiver uma nota própria em uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre esse item vão para sua nota. Sua Machine não cria esse tipo de nota por conta própria.

São usadas apenas contas, assinaturas e emails pessoais, e as notas de Casa são sempre pessoais. Sua Machine pergunta à IA uma vez sobre cada conta, assinatura ou informação nova que aprendeu para saber se o assunto é sua casa. No caso de uma conta, ela informa quem a enviou, nunca o valor.

Suas conversas também vão para essas notas, como explicado acima em **Anotações das suas conversas**.

## Saúde

Em **Saúde**, sua Machine mantém o que sabe sobre sua saúde: **Consultas**, **Resultados dos testes**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta de um médico, dentista ou farmácia ganha uma linha que abre a tarefa correspondente. O valor fica na tarefa.
- Cada email do seu consultório, de um hospital, laboratório ou plano de saúde aparece como uma linha com data e assunto, para que seu histórico se acumule com o tempo. Toque na linha para abrir o email.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também aparece em uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- Se você tiver uma nota própria em uma seção, como uma nota sobre seu fisioterapeuta em **Consultas**, as informações sobre esse assunto vão para ela.

As notas de Saúde são sempre pessoais, mesmo quando uma conta chega no seu endereço de trabalho. Sua Machine pergunta à IA uma vez sobre cada conta ou informação nova que aprendeu para saber se o assunto é sobre sua saúde.

## Filhos

Em **Filhos**, sua Machine mantém o que sabe sobre seus filhos: **Escola**, **Atividades**, **Cuidados infantis**, **Médicos e cuidados** e **Contas e taxas**. Babás e creches ficam em Cuidados infantis, nunca em Médicos e cuidados. Uma seção aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor da turma ou o dia da aula de natação, aparece em uma linha vinculada à página dele. Ela identifica alguém como seu filho quando o campo **Para você** indica isso, como filha ou filho.
- Uma conta da escola, de um clube ou de um serviço de cuidados infantis ganha uma linha que abre a tarefa correspondente. O valor fica na tarefa.
- Cada email da escola, de um clube ou de um serviço de cuidados infantis, como um aviso sobre um passeio ou uma mudança de planos, aparece em uma linha com data e assunto. Assim, tudo o que enviam fica em um só lugar. Toque na linha para abrir o email.
- Se você tiver uma nota própria para um dos seus filhos em uma seção, como uma nota sobre Isla em **Escola**, as informações sobre essa criança vão para ela.

As notas de Filhos são sempre pessoais, mesmo quando a escola escreve para o seu endereço de trabalho. Sua Machine pergunta à IA uma vez sobre cada informação nova para saber se o assunto é sobre seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. A partir daí, sua Machine adiciona as informações novas a essa nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por alguns instantes. Isso também acontece quando você remove uma linha.

## Diferente das anotações de reuniões

As anotações de reuniões e as notas sobre uma pessoa ou organização continuam onde estavam. As notas desta seção são páginas próprias.
