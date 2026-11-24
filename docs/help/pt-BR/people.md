---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: perfil, resumo e linha do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e671ff84b143e74
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros e-mails automáticos não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: confira [O Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta como parte da organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Perfil de alguém

No início, aparecem a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias". Para contatos mais antigos, aparece uma data. Passe o cursor sobre ela para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, junto com a fonte (Google Contatos, Google Agenda, Facebook, suas notas ou você): confira [O Graph](graph.md#birthday).
- **Com você**: o que essa pessoa é para você, se é um contato de trabalho ou pessoal, e se faz parte da sua Família ou do seu Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre o perfil da pessoa no Slack ou a conversa mais recente de vocês por lá.
- As **Pessoas** e os **Projetos** dos quais ela faz parte, o que está **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feito** e **Descartar**) e a **Linha do tempo**.

Os endereços e chats de alguém são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia. Isso também acontece quando alguém com quem você conversa agenda uma ligação pelo link que você enviou e o sobrenome ou a empresa bate.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, toque em **Algo errado?** na parte de baixo da página.

## Resumo

Algumas linhas curtas no início do perfil de alguém: o que foi decidido, pedido, planejado ou prometido, com o nome de todos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Geralmente, uma vez por dia. Se algo mudar entre vocês, como um novo prazo ou um pedido retirado, o resumo é atualizado em algumas horas.

Uma linha vaga fica de fora. Se não houver nada específico para dizer, não aparece nenhum resumo. Cada linha leva à fonte: mensagens do mesmo dia aparecem juntas, com uma data e a quantidade de mensagens, e abrem ao mesmo tempo.

Use **Editar** para escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o resumo para ela.

As preparações para reuniões usam esse resumo, mas só as linhas relacionadas àquela tarefa, de Trabalho ou Pessoal. Ele fica na sua Machine; sua equipe nunca o vê.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros no início mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no início, em **Em breve**, começando pela mais próxima. **Mostrar todos os próximos** mostra as outras reuniões. Cada reunião mostra quem participou, com cada pessoa listada uma vez. Se houver notas ou uma transcrição, aparece **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que as regras de compartilhamento permitem. Na página de alguém, **Equipe**, acima da linha do tempo, mostra o que colegas compartilharam, com a indicação de quem enviou cada item. **Meus** mostra apenas os seus itens.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas de acordo com o tipo indicado no perfil. A escolha que você fez (**Editar**) tem prioridade. Caso contrário, pessoas da sua Família e amigos, além de familiares ou amigos seus (como esposa ou pai), são classificadas como Pessoal, independentemente do endereço usado para escrever. Sua equipe nunca tem acesso aos contatos pessoais.

## Adicionar alguém

Toque em **Nova pessoa** no início da lista Pessoas ou em **+** na barra superior do celular. Informe o nome e, se souber, o e-mail e a organização. Se alguém parecido já estiver no seu Graph, o formulário mostra essa pessoa primeiro para você abrir o perfil existente. **Adicionar** abre o perfil novo.

A pessoa que você adicionar fica na lista mesmo que ainda não haja mensagens. A primeira mensagem associa as duas coisas.

## Editar alguém

**Editar**, no início do perfil, permite alterar o nome, o cargo, a organização, a cidade, o LinkedIn, os telefones e e-mails, o que a pessoa é para você e se é um contato de Trabalho ou Pessoal. O campo **Notas** serve para você guardar o que quiser lembrar. As notas continuam lá mesmo depois de mesclar perfis. **Salvar** guarda as alterações. **Cancelar** descarta as alterações.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente e também depois de **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor encontrado na consulta. Se apagar o nome, ele volta a ser o nome usado nas mensagens.

Para trocar a foto, clique nela: **Enviar uma imagem**, escolha uma das fotos encontradas para a pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, o perfil pergunta se elas são a mesma pessoa, e a lista Pessoas mostra os perfis em **Mesma pessoa?**. **Mesclar** une os perfis e mantém todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém os perfis separados. Sua resposta aparece no par por um momento, e depois ele sai da lista. A lista desaparece quando não há mais perguntas.

Um endereço que apenas se parece com o de alguém que você conhece, como acme-corp.example e acmecorp.example, nunca é sugerido como sendo da mesma pessoa. Só você pode atribuir uma função a essa pessoa.

Um nome sozinho nunca basta para associar alguém entre dois domínios, já que qualquer pessoa pode digitar o mesmo nome. Dois endereços de domínios diferentes só são sugeridos quando há outra conexão, como as mesmas pessoas ou um projeto. Alguém que usa seu nome em um endereço que não é seu nunca é sugerido. Em vez disso, adicione seus outros endereços em **Configurações**, em [Seus endereços](settings.md#your-addresses).

Quando apenas o primeiro nome coincide em domínios diferentes, como "Sam" e "Sam Lee", os perfis só são sugeridos se tiverem o mesmo telefone ou perfil do LinkedIn.

Se apenas o primeiro nome coincidir com o de alguém de uma reunião marcada por um chat, ou se o endereço pertencer a alguém que você já conhecia e apenas a pessoa no chat disser que é dela, você será perguntado. The Machine nunca abre um link para descobrir.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que só têm um nome em comum também não são associados automaticamente: eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. **Desfazer** logo em seguida separa todos de novo.

Para associar duas pessoas por conta própria, abra um dos perfis, toque em **⋯**, depois em **Mesma pessoa que…** e escolha a outra pessoa. O perfil de uma pessoa associada mostra o motivo em **Associado de**, com a opção **Desfazer** para separar os perfis.

## Excluir alguém permanentemente

No perfil da pessoa, abra o menu ⋯, escolha **Excluir permanentemente…** e depois **Excluir**. Isso remove a pessoa e o que sua Machine sabe sobre ela: o perfil, os endereços, os dados encontrados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa continuam, mas sem o nome dela. Ela não será adicionada de novo, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado a alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço da pessoa aparece primeiro. Novos rascunhos nunca são enviados para esse endereço se outro estiver disponível. Se esse for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail conta como devolvido quando o servidor de e-mail informa que o endereço não existe ou após três falhas temporárias ao longo de uma semana. O aviso é removido quando a pessoa escreve novamente desse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço da empresa têm o cargo, a foto, o LinkedIn e a cidade consultados como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta usa apenas o nome da pessoa e o domínio da empresa. Para buscar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança: **Buscar contatos de trabalho**.

Essa opção também impede a leitura do site antes da primeira reunião e a pesquisa na web, se estiver configurada (consulte [Pronta para suas reuniões](calendar.md#ready-for-your-meetings)).

Quando a consulta encontra os dados da pessoa, o perfil também mostra a descrição, há quanto tempo ela está na função atual e as duas funções anteriores. As preparações também usam essas informações, mas só mostram a descrição quando a pessoa não tem uma biografia própria.

Suas conexões ficam mais completas com as informações que já foram consultadas: cargo, telefone e fuso horário do Slack; biografia e cidade do X; título e foto do LinkedIn; cargos dos contatos do Google e do Salesflare; e foto do contato do Salesflare, se ele tiver uma. Passe o cursor sobre a linha abaixo do nome para ver de onde vieram as informações.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram vêm da sincronização do WhatsApp e da conexão com seus chats do Telegram: até 50 por dia em cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém que ainda não tem foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de um Fleet de Trabalho, uma cópia pequena da foto profissional acompanha o registro compartilhado da pessoa. Fotos dos contatos do Google, WhatsApp, Telegram ou Facebook, além de fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, incluindo seus aliases, sempre são você, nunca alguém no seu Graph. Se você pesquisar por si ou adicionar alguém com um dos seus endereços, **Sobre você** será aberto, e sua própria linha será ignorada na importação.

A página Sobre você lista seus endereços e de onde vieram. Altere-os em **Configurações**, na seção Conta. Para enviar suas informações de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Confira [Compartilhar um contato](share-contact.md).

## O que essa pessoa é para você

As funções que sua Machine identifica nas mensagens aparecem no perfil da pessoa em **Para você**, com apenas as palavras que mostram a função, como um cargo. Alguém dizer que é seu contador ou cliente não basta: também são necessárias informações do seu lado, como mensagens suas ou reuniões com essa pessoa. Não é preciso esperar que você confirme. Algo errado? **Editar** no perfil corrige a informação, ou toque em **⋯** na linha correspondente de **Mudanças recentes**. A Machine aprende com suas alterações.

## O que ela sabe sobre alguém

Os fatos sobre essa pessoa aparecem no perfil, em **Informações conhecidas**. A seção Aprendizado guarda os fatos gerais. **Adicionar** permite incluir mais um com as suas palavras. Cada fato tem um menu:

- **Editar** altera o fato ali mesmo.
- **Não é sobre** essa pessoa transforma o fato em uma informação geral, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou descobriu: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou uma mudança de projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Quando uma informação está errada, **⋯** na linha permite corrigir ali mesmo: **Editar**, **Remover**, **Não é sobre** essa pessoa ou **Desfazer** para devolver um projeto ao lugar anterior. São exibidas três linhas. **Mostrar mais** exibe as outras.

Se sua Machine atualizou alguém hoje, aparece um ponto ao lado do nome na lista Pessoas, e o aviso **4 pessoas atualizadas hoje** no início da lista mostra quem são. Confira [O Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, inicia uma tarefa sobre ela.
