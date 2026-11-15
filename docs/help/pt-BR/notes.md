---
title: Notas
area: graph
summary: Uma página fácil de consultar para cada assunto, como uma viagem ou sua casa, vinculada às pessoas e aos projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 88cfd4099bf27f38
---
Uma nota reúne o que você precisa saber sobre um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto de Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

Toque em **Nova nota**, na parte de cima de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** inclui o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista. O nome aparece como link. Na página do item vinculado, aparece **Vinculado de** com sua nota.

## Notas dentro de outras notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Em Notas, elas aparecem em uma árvore: toque na seta ao lado de uma nota para abrir as notas dentro dela. Para mover uma nota, toque em **Editar** e escolha onde ela fica em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota dentro dela.

Na parte de cima da página de uma nota, aparece onde ela fica, como **Notas › Filhos**. Toque em qualquer parte para ir até lá. No celular, as notas entre uma parte e outra ficam escondidas no menu ⋯.

## Notas que sua Machine mantém

Sua Machine também cria notas com base nas suas mensagens e mantém essas notas atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail. Toque nela para abrir a mensagem. Uma linha baseada em **O que aprendi** traz a indicação **Com base no que aprendi**. Uma reunião ou consulta no seu calendário nunca aparece como uma linha por conta própria: ela fica em [Calendário](calendar.md).

**Casa**, **Saúde** e **Filhos** só aparecem quando sua Machine tem pelo menos duas informações concretas para incluir, como uma conta ou algo que aprendeu. Até lá, essas notas não aparecem na lista. Se ficarem sem informações, elas desaparecem.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine mantém as mudanças quando atualiza a nota. Se você excluir uma linha ou uma nota, ela não volta. Notas criadas depois sobre o mesmo assunto ficam onde você colocou a primeira.

**Voltar ao original** mostra novamente as palavras da sua Machine. Se você editar uma linha baseada no que sua Machine aprendeu, a alteração também aparece em **O que aprendi**, para que exista uma só versão.

## Páginas criadas automaticamente

Quando uma nota tem pelo menos duas linhas de mensagens suas ou de informações que sua Machine aprendeu, sua Machine cria uma página no topo. Ela analisa o conteúdo das conversas, não só os assuntos:

- Um resumo curto: do que se trata e em que ponto está.
- **Fatos importantes**, **Decisões**, **Itens em aberto** e uma **Linha do tempo**, cada seção só aparece quando há algo concreto para incluir.
- Depois vêm as linhas da nota, numeradas, em **Fontes**. No fim de cada frase aparecem os números das linhas usadas. Toque em um deles para ir até a linha.

A página só é reescrita quando as linhas da nota mudam, no máximo uma vez por dia, aproximadamente. Se as fontes não tiverem nada concreto, a página não aparece e só ficam as linhas. Se você remover uma linha, o que veio só dela também desaparece da página. Na lista de Notas, aparece o início do resumo de cada página, abaixo do nome da nota.

Um projeto ou uma organização já tem sua própria página no Graph, com uma descrição no topo. As conversas sobre eles ficam nessa página, não em uma nota.

## Anotações das suas conversas

Sua Machine lê conversas inteiras e organiza cada uma na nota relacionada ao assunto: uma conversa por e-mail de qualquer uma das suas caixas de entrada, um chat no WhatsApp, Slack, Telegram, LinkedIn ou outro app conectado, ou suas anotações de reunião. Mensagens de chat contam como uma conversa até o chat ficar sem atividade por dois dias.

- Uma conversa sobre um projeto ou uma organização no Graph fica na página correspondente, não em uma nota nova.
- Uma conversa pode ficar em uma seção de **Casa**, **Saúde** ou **Filhos**, em uma nota sua ou em uma nota que sua Machine cria dentro de **Trabalho**, **Carro**, **Impostos** ou outra pasta.
- Sua Machine só cria uma nota para um assunto quando há pelo menos duas conversas sobre ele ou quando você escreveu nela e está claro que o assunto ainda está em andamento.
- Cada linha corresponde a uma conversa, da mais recente para a mais antiga. Toque nela para abrir a conversa.

Sua Machine envia à IA um trecho curto de cada conversa, sem respostas citadas nem assinaturas. Cada conversa é analisada uma vez. As novas mensagens ficam junto dela.

E-mails em massa e chats nunca vão para uma nota nem são enviados à IA: spam, promoções, newsletters e outros e-mails de listas, notificações de endereços que não aceitam respostas, bots e canais de transmissão. Uma conversa em que você escreveu ainda conta, assim como os e-mails de reservas de **Viagens** e **Eventos**.

Na primeira vez, sua Machine analisa as conversas dos últimos três meses ao longo de algumas horas, fora do período noturno e somente quando houver espaço no seu plano de IA. Depois, organiza novas conversas quando houver dez aguardando ou quando uma delas estiver aguardando há meio dia.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega à sua caixa de entrada, sua Machine adiciona a reserva a uma viagem em **Viagens**. As reservas da mesma viagem ficam juntas: ida, hotel e volta. A viagem mostra o código da reserva, o assento e o bilhete de cada linha, em ordem cronológica, além das datas. Em [Calendário](calendar.md), ela aparece como uma faixa que cobre esses dias e abre a viagem.

Sua Machine lê os detalhes da reserva que companhias aéreas, hotéis e sites de reservas incluem no e-mail de confirmação. Um e-mail sem esses detalhes não cria uma viagem. Os e-mails de reserva anteriores, dentro do ano de [histórico](history.md) mantido pela sua Machine, são lidos em segundo plano quando esse histórico termina de ser carregado, começando pelas suas caixas de entrada pessoais. Se um e-mail de confirmação mais antigo for lido depois, ele é adicionado à viagem que já existe.

Se uma reserva mudar, a linha correspondente é atualizada. Se for cancelada, a linha desaparece. Quando todas as reservas de uma viagem são canceladas, a viagem também desaparece.

## Eventos

Quando ingressos para um show, jogo, festival ou conferência chegam à sua caixa de entrada, sua Machine adiciona o evento em **Eventos**, com uma nota para cada evento. Uma linha mostra o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento aparece na mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa em [Calendário](calendar.md) que abre a nota.

- Cada linha indica de quem vieram os ingressos, como **De Example Tickets**, e abre o e-mail.
- Se o e-mail dos ingressos tiver gerado uma tarefa, como pagar pelos ingressos, **Abrir a tarefa** mostra essa tarefa.
- Um evento reservado na sua caixa de entrada do trabalho é Trabalho. Caso contrário, é Pessoal.

Sua Machine lê os detalhes dos ingressos incluídos pelos vendedores no e-mail de confirmação, sem usar IA. Um e-mail sem esses detalhes não cria um evento. Se uma reserva for cancelada, ela desaparece. Quando todos os ingressos de um evento são cancelados, o evento também desaparece.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como de energia ou água, ganha uma linha com a frequência e a data da última cobrança. **Abrir a tarefa** mostra a conta. O valor e os dados de pagamento ficam nela.
- Uma assinatura que você mantém ganha uma linha que abre a tarefa de **Assinaturas**. As assinaturas canceladas não aparecem.
- Quem costuma entrar em contato sobre sua casa, como a empresa de energia, o provedor de internet ou a prefeitura, ganha uma linha com a frequência dos contatos. Toque nela para abrir o e-mail mais recente.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também aparece em uma linha. Se você editar essa informação, ela também muda em **O que aprendi**.
- Se você criar uma nota própria dentro de uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela ficam nessa nota. Sua Machine não cria notas desse tipo por conta própria.

Só são usadas contas, assinaturas e mensagens pessoais. As notas de Casa são sempre pessoais. Sua Machine pergunta uma vez à IA se cada nova conta, assinatura ou informação aprendida é sobre sua casa. No caso de uma conta, ela envia quem a emitiu, nunca o valor.

As conversas também ficam nessas notas, como explicado acima em **Anotações das suas conversas**.

## Saúde

Em **Saúde**, sua Machine mantém o que sabe sobre a sua saúde: **Consultas**, **Resultados dos testes**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa correspondente. O valor fica nela.
- Cada e-mail do consultório, hospital, laboratório ou plano de saúde vira uma linha com a data e o assunto, para que seu histórico se acumule com o tempo. Toque na linha para abrir o e-mail.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também aparece em uma linha. Se você editar essa informação, ela também muda em **O que aprendi**.
- Se você criar uma nota própria dentro de uma seção, como uma nota sobre seu fisioterapeuta em **Consultas**, as informações sobre ele ficam nessa nota.

As notas de Saúde são sempre pessoais, mesmo quando uma conta chega ao seu endereço de trabalho. Sua Machine pergunta uma vez à IA se cada nova conta ou informação aprendida é sobre a sua saúde.

## Filhos

Em **Filhos**, sua Machine mantém o que sabe sobre seus filhos: **Escola**, **Atividades**, **Cuidados infantis**, **Médicos e cuidados** e **Contas e taxas**. Babás e creches ficam em Cuidados infantis, nunca em Médicos e cuidados. Uma seção aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor da turma ou o dia da natação, aparece em uma linha vinculada à página dele. Sua Machine considera alguém seu filho quando em **Para você** aparece essa relação, como filha ou filho.
- Uma conta da escola, de um clube ou de cuidados infantis ganha uma linha que abre a tarefa correspondente. O valor fica nela.
- Cada e-mail da escola, de um clube ou de um serviço de cuidados infantis, como um aviso sobre um passeio ou uma mudança de planos, vira uma linha com a data e o assunto, para que todas as mensagens fiquem em um só lugar. Toque na linha para abrir o e-mail.
- Se você criar uma nota própria sobre uma criança dentro de uma seção, como uma nota sobre Isla em **Escola**, as informações sobre ela ficam nessa nota.

As notas de Filhos são sempre pessoais, mesmo quando a escola escreve para o seu endereço de trabalho. Sua Machine pergunta uma vez à IA se cada informação nova é sobre seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. A partir daí, sua Machine adiciona as novas informações a essa nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por alguns instantes. Isso também acontece quando você remove uma linha.

## Diferente das anotações de reunião

As anotações de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas desta seção são páginas próprias.
