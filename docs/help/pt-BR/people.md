---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: páginas, resumos e linhas do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 315403ed8889dbac
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada uma tem seus próprios filtros: veja [O Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta como parte da organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem como uma data. Passe o cursor sobre ela para ver a data exata. Abaixo:

- **Contato**: telefones e e-mails. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, junto com a origem da informação (Google Contacts, Google Calendar, Facebook, suas notas ou você): veja [O Graph](graph.md#birthday).
- **Com você**: quem essa pessoa é para você, se é um contato de Trabalho ou Pessoal e se faz parte da sua família ou do seu Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas nos dois sentidos, com **Marcar como feito** e **Descartar**) e sua **Linha do tempo**.

Os endereços e chats de alguém são associados automaticamente quando fica claro que são da mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia. Isso também acontece quando alguém com quem você conversa marca uma chamada pelo link que você enviou e a empresa ou o sobrenome corresponde.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte de baixo da página.

## Resumo

Algumas linhas curtas no topo da página de uma pessoa: o que foi decidido, pedido, planejado ou prometido, com o nome de todos os envolvidos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Geralmente, isso acontece uma vez por dia. Se algo mudar, como um novo prazo ou um pedido retirado, o resumo é atualizado em algumas horas.

Uma linha vaga fica de fora. Se não houver nada específico para dizer, não há resumo. Cada linha leva à origem da informação: mensagens do mesmo dia aparecem agrupadas sob uma data, com a quantidade, e abrem juntas.

**Editar** o resumo para deixá-lo do seu jeito. Quando houver novidades, The Machine mostra uma **Atualização sugerida**, com **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o texto para ela.

A preparação para reuniões usa o resumo, mas só as linhas relacionadas àquela tarefa, de Trabalho ou Pessoal. Ele fica na sua Machine; sua equipe nunca o vê.

## Linha do tempo

Toda página de pessoa ou organização tem uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas no Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros no topo mostram uma fonte de cada vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** mostra as demais. Uma reunião mostra quem participou, cada pessoa uma vez. Reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Em uma página, **Equipe**, acima da linha do tempo, adiciona o que as outras pessoas da equipe compartilharam, com a origem de cada item. **Meus** mostra apenas os seus itens.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas de acordo com o tipo definido na página delas. A sua escolha (**Editar**) prevalece. Caso contrário, as pessoas da sua família e seus amigos, além de familiares e amigos seus (como esposa ou pai), são classificados como Pessoal, independentemente do endereço usado para escrever. Sua equipe nunca vê seus contatos pessoais.

## Adicionar alguém

Use **Nova pessoa** no topo de Pessoas ou **+** na barra superior do celular. Informe um nome e, se tiver, um e-mail e uma organização. Se já houver alguém parecido no seu Graph, o formulário mostra essa pessoa primeiro, para você abrir a página existente. **Adicionar** abre a nova página.

A pessoa que você adiciona permanece na lista, mesmo sem mensagens. A primeira mensagem associa as mensagens a ela.

## Editar alguém

**Editar**, no topo da página da pessoa, permite mudar o nome, o cargo, a organização, a localização, o LinkedIn, os telefones e e-mails, quem ela é para você e se é um contato de Trabalho ou Pessoal. O campo **Notas** serve para registrar o que você quiser lembrar. As notas permanecem após mesclagens. **Salvar** aplica as mudanças; **Cancelar** mantém tudo como estava.

Suas edições são mantidas quando os dados da pessoa são consultados novamente, e também após **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se apagar o nome, o nome das mensagens será restaurado.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, selecione uma das fotos encontradas para a pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página pergunta se são a mesma pessoa, e Pessoas as lista em **Mesma pessoa?**. **Mesclar** une as duas, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém as pessoas separadas permanentemente. Sua resposta aparece por um momento no par, que depois sai da lista. A lista desaparece quando não houver mais nada para confirmar.

Alguém com um endereço que só parece com o de uma pessoa que você conhece, como acme-corp.example e acmecorp.example, nunca será sugerido como a mesma pessoa. Só você pode atribuir uma função a essa pessoa.

Um nome sozinho nunca basta para mesclar pessoas de domínios diferentes, já que qualquer pessoa pode usar o mesmo nome. Endereços de domínios diferentes só são sugeridos para mesclagem quando outro elemento os associa, como as mesmas pessoas ou um projeto pequeno. Um primeiro nome sozinho ("Sam" e "Sam Lee") exige mais informações: a mesma empresa, o mesmo telefone ou o mesmo perfil do LinkedIn.

Alguém que use seu nome em um endereço que não é seu nunca será sugerido para mesclagem. Em vez disso, adicione seus outros endereços em **Configurações**, em [Seus endereços](settings.md#your-addresses).

Quando apenas o primeiro nome coincide em domínios diferentes, como "Sam" e "Sam Lee", a mesclagem só é sugerida se o telefone ou o perfil do LinkedIn também forem os mesmos.

Quando apenas o primeiro nome coincide com o de alguém de uma reunião marcada por um chat, ou quando o endereço pertence a alguém que você já conhecia e só a pessoa no chat diz que é dela, você será perguntado. The Machine nunca abre um link para confirmar.

Um endereço compartilhado, como info@ ou o de uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que só têm um nome em comum não são associados automaticamente: eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. **Desfazer** logo depois separa todos novamente.

Para associar duas pessoas por conta própria, abra uma delas, toque em **⋯**, escolha **Mesma pessoa que…** e selecione a outra. A página da pessoa mesclada mostra o motivo em **Associada a partir de**, com **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Em seguida, toque em **Excluir**. Isso remove a pessoa e o que sua Machine sabe sobre ela: o registro, os endereços, os dados consultados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa permanecem, mas o nome é removido. Ela não será adicionada novamente, nem por uma importação nem por uma tarefa de aniversários do Facebook com o nome ou o endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado para alguém volta, o endereço aparece como **Devolvido**, com a data, e outro endereço da pessoa passa a aparecer primeiro. Se outro endereço for conhecido, novos rascunhos nunca serão enviados para o endereço devolvido. Se esse for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail conta como devolvido quando o servidor informa que o endereço não existe ou após 3 falhas temporárias em uma semana. O aviso é removido quando a pessoa escreve desse endereço novamente ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço de trabalho recebem um cargo, uma foto, o LinkedIn e a cidade, consultados como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para buscar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, em Segurança: **Buscar contatos de trabalho**.

Essa opção também impede a leitura do site antes da primeira reunião e a pesquisa na web, quando configurada (veja [Prepare-se para suas reuniões](calendar.md#ready-for-your-meetings)).

Quando os dados são encontrados, a página da pessoa também mostra o texto de apresentação, desde quando ela está no cargo atual e os dois cargos anteriores. A preparação para reuniões também usa essas informações, mas só mostra o texto de apresentação quando a pessoa não tem uma biografia própria.

Suas conexões ganham mais informações com o que já foi consultado: cargo, telefone e fuso horário do Slack; biografia e localização do X; título profissional e foto do LinkedIn; cargos do Google Contacts e do Salesflare; e a foto de um contato do Salesflare, quando ele mesmo mantém uma. Passe o cursor sobre a linha abaixo do nome para ver a origem das informações.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram vêm da sincronização do WhatsApp e da conexão com seus chats do Telegram: até 50 por dia em cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém que não tem foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de um Fleet de Trabalho, uma cópia pequena da foto de trabalho acompanha o registro compartilhado da pessoa. Fotos do Google Contacts, WhatsApp, Telegram ou Facebook, assim como fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, incluindo aliases, são sempre seus, nunca de alguém no seu Graph. Ao pesquisar por você ou adicionar alguém com um dos seus endereços, a página **Sobre você** é aberta, e uma importação ignora sua própria linha.

A página Sobre você lista seus endereços e a origem de cada um. Altere-os em **Configurações**, em Conta. Para enviar seu contato a alguém da equipe ou a um amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## Quem essa pessoa é para você

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, apenas com as palavras que indicam a função, como um cargo. Alguém dizer que é seu contador ou cliente não basta: também é preciso haver algo que indique isso do seu lado, como suas mensagens ou reuniões com essa pessoa. Não é preciso confirmar. Algo está errado? **Editar** na página da pessoa corrige a informação, assim como **⋯** na linha correspondente em **Mudanças recentes**. A Machine aprende com suas edições.

## O que ela sabe sobre alguém

As informações sobre uma pessoa ficam na página dela, em **Informações conhecidas**. Aprendizado guarda as informações gerais. **Adicionar** salva outra informação com as suas palavras. Cada informação tem um menu:

- **Editar** altera a informação ali mesmo.
- **Não é sobre essa pessoa** transforma a informação em uma informação geral novamente, em **Aprendizado**, **Fatos**.
- **Remover** exclui a informação de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine mudou ou aprendeu sobre ela: uma função, onde alguém trabalha, a relação entre duas pessoas, uma informação ou a mudança de um projeto. Cada linha mostra a data e a origem. Toque na origem para ler a mensagem.

Se uma linha estiver errada, use **⋯** para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre essa pessoa** ou **Desfazer** para devolver um projeto ao lugar onde estava. São exibidas três linhas; **Mostrar mais** mostra as demais.

Uma pessoa atualizada hoje pela sua Machine aparece com um ponto pequeno na lista Pessoas, e **4 pessoas atualizadas hoje** no topo da lista mostra quem são. Veja [O Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, cria uma tarefa sobre essa pessoa, organização ou projeto.
