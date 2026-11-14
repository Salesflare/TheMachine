---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: páginas, resumos e linhas do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, a partir das suas mensagens e reuniões. Newsletters, recibos e outros envios em massa não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: veja [The Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta para a organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

Ela começa com a foto, o nome, o cargo, a organização e o local da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem com a data. Passe o cursor sobre ela para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, com a origem da informação (contatos do Google, Google Calendar, Facebook ou você): veja [The Graph](graph.md#birthday).
- **Com você**: o que essa pessoa é para você, contato de Trabalho ou Pessoal, e sua Família ou Fleet, com **Ver no Fleet**.
- **Também em**: os outros lugares onde vocês conversam. **Slack** abre o perfil da pessoa no Slack ou a conversa mais recente de vocês por lá.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feita** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de alguém são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal da pessoa em cópia.

Se uma página mostrar **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte inferior da página.

## Resumo

Algumas linhas curtas no início da página de uma pessoa: o que foi decidido, perguntado, planejado ou prometido, com os nomes de todos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Em geral, uma vez por dia. Se algo mudar em um assunto com essa pessoa, como um novo prazo ou um pedido retirado, o resumo é atualizado em algumas horas.

Linhas vagas ficam de fora. Se não houver nada específico para dizer, não haverá resumo. Cada linha leva à fonte: mensagens do mesmo dia compartilham uma data com a quantidade de mensagens e podem ser abertas juntas.

**Editar** para escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o texto para ela.

A preparação para reuniões usa esse resumo, mas apenas as linhas relacionadas à tarefa em questão, de Trabalho ou Pessoal. Ele fica na sua Machine; sua equipe nunca o vê.

## Linha do tempo

Toda página de pessoa ou organização tem uma, começando pelos itens mais recentes: e-mails, reuniões e seus resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros no topo mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** mostra as demais. Uma reunião mostra quem participou, cada pessoa uma única vez. Reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são particulares: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Em uma página, **Equipe** acima da linha do tempo adiciona o que seus colegas compartilharam. Cada item indica quem compartilhou. **Meus** mostra apenas os seus.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas de acordo com o Tipo indicado na página delas. A opção que você escolheu (**Editar**) tem prioridade. Caso contrário, sua Família e seus Amigos, além das pessoas que são sua família ou amigas (como esposa ou pai), são classificadas como Pessoal, independentemente do endereço de onde escrevem. Sua equipe nunca tem acesso aos contatos Pessoais.

## Adicionar alguém

Use **Nova pessoa** no topo de Pessoas ou **+** na barra superior do celular. Informe o nome e, se tiver, o e-mail e a organização. Se já houver alguém parecido no seu Graph, essa pessoa aparecerá primeiro no formulário, para você abrir o perfil existente. **Adicionar** abre a nova página.

A pessoa que você adicionar continuará na lista, mesmo que ainda não haja mensagens. A primeira mensagem associada a ela fará a associação.

## Editar alguém

**Editar**, no topo da página, permite mudar o nome, o cargo, a organização, o local, o LinkedIn, os telefones e e-mails, o que a pessoa é para você e se é de Trabalho ou Pessoal. O campo **Notas** serve para guardar o que você quiser lembrar. As notas permanecem após mesclagens. **Salvar** guarda as alterações. **Cancelar** mantém tudo como estava.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente, e também após **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se apagar o nome, o nome das mensagens da pessoa será restaurado.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, uma imagem encontrada para essa pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página delas pergunta se são a mesma pessoa, e Pessoas as lista em **Mesma pessoa?**. **Mesclar** combina as duas, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém as pessoas separadas permanentemente. Sua resposta aparece no par por um momento, e depois ele sai da lista. A lista desaparece quando não há mais nada para perguntar.

Uma pessoa com um endereço que apenas parece com um endereço que você conhece, como acme-corp.example e acmecorp.example, nunca será sugerida como a mesma pessoa. Só você pode atribuir uma função a ela.

Um endereço compartilhado, como info@ ou uma lista de distribuição, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que só têm um nome em comum não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** combina todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. **Desfazer** logo depois separa todos novamente.

Para associar duas pessoas manualmente, abra uma delas e selecione **⋯**, **Mesma pessoa que…** e escolha a outra. A página da pessoa mesclada mostra o motivo em **Associada a partir de**, com **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…** e depois **Excluir**. Isso remove a pessoa e tudo que sua Machine sabe sobre ela: o registro, os endereços, os dados consultados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas relacionadas a essa pessoa permanecem, mas sem o nome dela. Ela não será adicionada novamente, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado para alguém é devolvido, o endereço da pessoa aparece como **Devolvido**, com a data, e outro endereço dela aparece primeiro. Novos rascunhos nunca são enviados para esse endereço se outro for conhecido. Se for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail conta como devolvido quando o servidor informa que o endereço não existe ou após 3 falhas temporárias ao longo de uma semana. A indicação desaparece quando a pessoa escreve novamente desse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço de e-mail corporativo recebem um cargo, uma foto, informações do LinkedIn e a cidade, consultados como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para obter a foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança: **Buscar contatos de trabalho**.

Quando os dados são encontrados, a página da pessoa também mostra o texto de apresentação, desde quando ela está na função atual e as duas funções anteriores. As preparações também usam essas informações. O texto de apresentação só é usado quando a pessoa não tem uma biografia própria.

Suas conexões são complementadas com informações que já estão disponíveis: cargo, telefone e fuso horário do Slack; biografia e local do X; título e foto do LinkedIn; cargos dos contatos do Google e do Salesflare; e a foto de um contato do Salesflare, se ele tiver uma. Passe o cursor sobre a linha abaixo do nome para ver de onde veio a informação.

O Outlook adiciona as fotos dos colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são obtidas pela sincronização do WhatsApp e pela conexão com os chats do Telegram: até 50 por dia de cada serviço, apenas de pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém que ainda não tem foto quando você a salva ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de uma Fleet de Trabalho, uma pequena cópia da foto de trabalho acompanha o registro compartilhado da pessoa. Fotos dos contatos do Google, WhatsApp, Telegram ou Facebook, além de fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, inclusive aliases, são sempre seus, nunca de alguém no seu Graph. Ao pesquisar por você ou adicionar uma pessoa com um dos seus endereços, **Sobre você** é aberto. Uma importação também ignora a sua própria linha.

**Sobre você** lista seus endereços e a origem de cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seus dados de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que essa pessoa é para você

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, junto com a linha que ela identificou. Você não precisa confirmar. Algo está errado? **Editar** na página da pessoa corrige a informação, ou use **⋯** na linha correspondente em **Mudanças recentes**. Ela aprende com as suas alterações.

## O que ela sabe sobre alguém

Os fatos sobre essa pessoa ficam na página dela, em **Informações conhecidas**. Aprendizado guarda os fatos gerais. **Adicionar** salva mais um fato com as suas palavras. Cada fato tem um menu:

- **Editar** altera o fato ali mesmo.
- **Não é sobre** essa pessoa transforma o fato novamente em um fato geral, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre ele: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou uma mudança em um projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Quando uma linha está errada, use **⋯** para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** essa pessoa ou **Desfazer** para devolver um projeto ao lugar em que estava. São mostradas três linhas. **Mostrar mais** exibe as demais.

Uma pessoa atualizada hoje pela sua Machine tem um ponto pequeno na lista Pessoas, e **4 pessoas atualizadas hoje** no topo da lista mostra quem são. Veja [The Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa** no menu **⋯** de uma pessoa, organização ou projeto cria uma tarefa sobre ela.
