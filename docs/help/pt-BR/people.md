---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: a página, o resumo e a linha do tempo delas, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 907cec019dc70184
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as etiquetas e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: confira [The Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome da própria loja) conta para a organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e o local da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversa diária · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora", "há 3 horas", "ontem" ou "há 3 dias", e os contatos mais antigos aparecem com a data. Passe o cursor sobre ela para ver a data exata. Abaixo:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, com a fonte (Google Contacts, Google Calendar, Facebook, suas notas ou você): confira [The Graph](graph.md#birthday).
- **Com você**: o que a pessoa é para você, contato de Trabalho ou Pessoal, e se faz parte da sua Família ou Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas nos dois sentidos, com **Marcar como feita** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de alguém são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal em cópia.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte de baixo da página.

## Resumo

Algumas linhas curtas no topo da página de uma pessoa: o que foi decidido, pedido, planejado ou prometido, com o nome de todos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Normalmente, isso acontece uma vez por dia; quando algo muda com essa pessoa, como um novo prazo ou um pedido retirado, o resumo é atualizado em algumas horas.

Uma linha vaga fica de fora. Se não houver nada específico para dizer, não há resumo. Cada linha leva à fonte: mensagens do mesmo dia ficam agrupadas em uma data com a contagem e são abertas juntas.

**Editar** para escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** permite que ela atualize o resumo.

As preparações para reuniões usam o resumo, mas apenas as linhas do lado daquela tarefa (Trabalho ou Pessoal). O resumo fica na sua Machine. Sua equipe nunca o vê.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma, com os itens mais recentes primeiro: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros no topo mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, começando pelas mais próximas. **Mostrar todos os próximos** exibe as outras. A reunião mostra quem participou, com cada pessoa listada uma vez. As reuniões com notas ou uma transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Em uma página, **Equipe**, acima da Linha do tempo, adiciona o que seus colegas compartilharam. Cada item indica quem o compartilhou. **Meus** mostra apenas os seus.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas de acordo com o Tipo definido na página delas. A opção que você escolheu (**Editar**) tem prioridade. Caso contrário, sua Família e seus Amigos, e quem é da sua família ou amigo (como uma esposa ou um pai), são classificados como Pessoal, seja qual for o endereço usado para escrever. Sua equipe nunca vê contatos Pessoais.

## Adicionar alguém

Use **Nova pessoa** no topo de Pessoas ou **+** na barra superior do celular. Informe um nome e, se tiver, um e-mail e uma organização. Se alguém parecido já estiver no seu Graph, o formulário mostra essa pessoa primeiro, para você abrir o perfil existente. **Adicionar** abre a nova página.

A pessoa que você adiciona fica salva, mesmo sem mensagens. A primeira mensagem associa a pessoa automaticamente.

## Editar alguém

**Editar**, no topo da página da pessoa, permite alterar o nome, o cargo, a organização, o local, o LinkedIn, os telefones e os e-mails, o que ela é para você e se é de Trabalho ou Pessoal. O campo **Notas** serve para anotar o que você quiser lembrar. As notas são mantidas ao mesclar pessoas. **Salvar** guarda as alterações. **Cancelar** mantém tudo como estava.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente e depois de usar **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se apagar o nome, o nome usado nas mensagens da pessoa será restaurado.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, selecione uma foto encontrada para a pessoa ou use **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas talvez sejam a mesma, a página delas pergunta se são a mesma pessoa, e Pessoas as lista em **Mesma pessoa?**. **Mesclar** combina as duas, incluindo mensagens, notas, funções e projetos. **Não é a mesma** mantém as pessoas separadas permanentemente. Sua resposta aparece por um momento no par, que depois sai da lista. A lista desaparece quando não há mais nada para perguntar.

Alguém com um endereço que apenas se parece com outro que você conhece, como acme-corp.example e acmecorp.example, nunca é sugerido como a mesma pessoa. Só você pode atribuir uma função a essa pessoa.

Um nome sozinho nunca basta para associar pessoas de domínios diferentes, já que qualquer um pode digitar o mesmo nome. Dois endereços em domínios diferentes só são sugeridos quando há outro vínculo, como pessoas em comum ou um projeto. Alguém que usa seu nome em um endereço que não é seu nunca é sugerido. Em vez disso, adicione seus outros endereços em **Configurações**, em [Seus endereços](settings.md#your-addresses).

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que só têm um nome em comum não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** combina todos os pares da lista de uma vez, exceto aqueles que você marcou como **Não é a mesma**. Use **Desfazer** logo depois para separar todos novamente.

Para associar duas pessoas por conta própria, abra uma delas e use **⋯**, **Mesma pessoa que…** e selecione a outra. A página da pessoa mesclada mostra o motivo em **Associada a partir de**, com **Desfazer** para separar as pessoas novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu **⋯**, selecione **Excluir permanentemente…** e depois **Excluir**. Isso remove a pessoa e o que sua Machine sabe sobre ela: o perfil, os endereços, os dados consultados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa são mantidas, mas o nome dela é removido. Ela não será adicionada novamente, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou o endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado para alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço da pessoa aparece primeiro. Novos rascunhos nunca são enviados para esse endereço quando outro endereço é conhecido. Se esse for o único endereço, a tela de envio mostra um aviso, mas você ainda pode enviar.

Um e-mail conta como devolvido quando o servidor de e-mail diz que o endereço não existe ou depois de 3 falhas temporárias ao longo de uma semana. O aviso é removido quando a pessoa escreve novamente usando esse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço de trabalho recebem um cargo, uma foto, um perfil do LinkedIn e uma cidade, consultados da mesma forma que os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para encontrar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança, usando **Buscar contatos de trabalho**.

Quando a consulta encontra esses dados, a página da pessoa também mostra o texto sobre ela, desde quando ocupa a função atual e as duas funções anteriores. As preparações também usam essas informações, mas só incluem o texto sobre a pessoa quando ela não tem uma biografia própria.

Suas conexões incluem mais informações do que já está disponível: cargo, telefone e fuso horário do Slack; biografia e local do X; título e foto do LinkedIn; cargos do Google Contacts e do Salesflare; e a foto do contato do Salesflare, se o serviço tiver uma. Passe o cursor sobre a linha abaixo do nome para ver a fonte.

O Outlook adiciona as fotos dos colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são adicionadas pela sincronização do WhatsApp e pela conexão de chats do Telegram: até 50 por dia de cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém sem foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de uma Fleet de Trabalho, uma cópia pequena da foto de trabalho é incluída no perfil compartilhado da pessoa. Fotos do Google Contacts, WhatsApp, Telegram ou Facebook, além das fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, incluindo os aliases, sempre são seus e nunca são de alguém no seu Graph. Se você pesquisar por si ou adicionar uma pessoa com um dos seus endereços, a opção **Sobre você** será aberta, e a importação ignorará sua própria linha.

A página Sobre você lista seus endereços e de onde vieram. Altere-os em **Configurações**, na seção Conta. Para enviar seus dados de contato a um colega ou amigo, selecione **Compartilhar meu contato**. Confira [Compartilhar um contato](share-contact.md).

## O que a pessoa é para você

As funções que sua Machine identifica nas suas mensagens aparecem na página da pessoa, em **Para você**, junto com o trecho que ela identificou. Você não precisa confirmar nada. Algo está errado? Use **Editar** na página da pessoa ou **⋯** na linha em **Mudanças recentes**. A Machine aprende com suas alterações.

## O que sabe sobre alguém

Os fatos sobre alguém ficam na página da pessoa, em **Informações conhecidas**. A seção Aprendizado guarda os fatos gerais. Use **Adicionar** para incluir outro fato com suas próprias palavras. Cada fato tem um menu:

- **Editar** altera o fato ali mesmo.
- **Não é sobre** a pessoa transforma o fato em uma informação geral novamente, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre eles: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou uma mudança em um projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Se uma linha estiver errada, use **⋯** para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** a pessoa ou **Desfazer** para devolver um projeto ao lugar em que estava. Três linhas são exibidas. **Mostrar mais** exibe as outras.

Alguém que sua Machine atualizou hoje aparece com um pequeno ponto na lista de Pessoas, e **4 pessoas atualizadas hoje** no topo da lista mostra quem são. Confira [The Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa** no menu **⋯** de uma pessoa, organização ou projeto cria uma tarefa sobre ela.
