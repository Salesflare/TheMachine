---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: páginas, resumos e linhas do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 5e808343918f7f47
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, a partir das suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: veja [O Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) é associada à organização, não a uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

No início da página, aparecem a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre o contato entre vocês ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem com a data. Passe o cursor sobre ela para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, com a fonte da informação (Google Contacts, Google Calendar, Facebook, suas notas ou você): veja [O Graph](graph.md#birthday).
- **Com você**: o que essa pessoa representa para você, se é um contato de Trabalho ou Pessoal e se faz parte da sua Família ou do seu Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, o que está **Em aberto entre vocês** (promessas nos dois sentidos, com **Marcar como feita** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de uma pessoa são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, toque em **Algo errado?** na parte inferior da página.

## Resumo

Algumas frases curtas no início da página de uma pessoa: o que foi decidido, pedido, planejado ou prometido, com o nome de todos os envolvidos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada frase antes. Em geral, uma vez por dia. Se algo envolvendo a pessoa mudar, como um novo prazo ou um pedido retirado, o resumo pode ser atualizado em poucas horas.

Frases vagas ficam de fora. Se não houver nada específico para dizer, não há resumo. Cada frase tem um link para a fonte: mensagens do mesmo dia compartilham uma data com o número de mensagens e podem ser abertas juntas.

Use **Editar** para deixar o resumo do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o resumo para ela.

Os preparativos para reuniões usam o resumo, mas somente as frases relacionadas ao tipo daquela tarefa (Trabalho ou Pessoal). O resumo fica na sua Machine. Sua equipe nunca vê.

## Linha do tempo

Toda página de pessoa e organização tem uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), conversas do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros no topo mostram uma fonte de cada vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no início, em **Em breve**, começando pela mais próxima. **Mostrar todos os próximos** exibe as demais. Uma reunião mostra quem participou, cada pessoa uma única vez. Reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são privadas: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Na página, **Equipe** acima da linha do tempo mostra o que os colegas compartilharam, com a indicação de quem compartilhou cada item. **Meus** mostra apenas os seus itens.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas conforme o Tipo indicado na página delas. A opção que você escolher (**Editar**) tem prioridade. Caso contrário, sua Família e seus Amigos, além de familiares ou amigos seus (como uma esposa ou um pai), são classificados como Pessoais, independentemente do endereço de onde escrevem. Sua equipe nunca vê os contatos Pessoais.

## Adicionar alguém

Toque em **Nova pessoa** no início da lista de Pessoas ou em **+** na barra superior do celular. Informe um nome e, se tiver, um e-mail e uma organização. Se alguém parecido já estiver no seu Graph, o formulário mostra essa pessoa primeiro, para que você possa abrir a página existente. Toque em **Adicionar** para abrir a nova página.

A pessoa que você adicionar continuará na lista, mesmo sem mensagens. A primeira mensagem será associada a ela.

## Editar alguém

**Editar**, no início da página, permite alterar o nome, o cargo, a organização, a cidade, o LinkedIn, os telefones e os e-mails da pessoa, o que ela representa para você e se é um contato de Trabalho ou Pessoal. O campo **Notas** serve para você anotar o que quiser lembrar. As notas são mantidas mesmo depois de mesclar pessoas. **Salvar** aplica as alterações. **Cancelar** descarta as alterações.

Suas edições são mantidas mesmo quando os dados da pessoa são consultados novamente, e também depois de **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se apagar o nome, o nome das mensagens da pessoa será restaurado.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, uma imagem encontrada para a pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas talvez sejam a mesma, a página pergunta se são a mesma pessoa, e a lista de Pessoas as mostra em **Mesma pessoa?**. **Mesclar** combina as duas pessoas e mantém todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém as pessoas separadas permanentemente. Sua resposta aparece por um momento no par, que depois sai da lista. A lista desaparece quando não há mais nada a confirmar.

Alguém com um endereço que apenas se parece com outro que você conhece, como acme-corp.example e acmecorp.example, nunca é sugerido como a mesma pessoa. Além disso, só você pode atribuir uma função a essa pessoa.

Um nome, por si só, nunca é suficiente para associar pessoas de domínios diferentes, porque qualquer um pode usar o mesmo nome. Dois endereços de domínios diferentes só são sugeridos quando há outro vínculo, como pessoas em comum ou um projeto. Alguém que usa seu nome em um endereço que não é seu nunca é sugerido. Em vez disso, adicione seus outros endereços em **Configurações**, em [Seus endereços](settings.md#your-addresses).

Quando apenas o primeiro nome corresponde em domínios diferentes, como "Sam" e "Sam Lee", as pessoas só são sugeridas se tiverem o mesmo número de telefone ou perfil do LinkedIn.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e uma conversa pessoal que tenham apenas um nome em comum não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** combina de uma só vez todos os pares da lista, exceto aqueles que você marcou como **Não é a mesma**. **Desfazer** logo depois separa todos novamente.

Para associar duas pessoas manualmente, abra uma delas e toque em **⋯**, **Mesma pessoa que…** e escolha a outra. A página de uma pessoa associada mostra o motivo em **Associada a partir de**, com **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Depois, toque em **Excluir**. Isso remove a pessoa e tudo o que sua Machine sabe sobre ela: o cadastro, os endereços, os dados consultados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa continuam, mas sem o nome dela. Ela não será adicionada novamente, nem por uma importação nem por uma tarefa de aniversários do Facebook que inclua o nome ou o endereço dela. Não é possível desfazer essa ação.

## E-mails devolvidos

Quando um e-mail enviado para alguém é devolvido, o endereço mostra **Devolvido** e a data. Outro endereço da pessoa aparece primeiro. Novos rascunhos nunca usam esse endereço se outro for conhecido. Se for o único endereço, a tela de envio avisa, mas você ainda pode enviar.

Um e-mail é considerado devolvido quando o servidor informa que o endereço não existe ou após três falhas temporárias ao longo de uma semana. O aviso é removido quando a pessoa escreve novamente desse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço de e-mail corporativo têm cargo, foto, LinkedIn e cidade consultados como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta usa apenas o nome da pessoa e o domínio da empresa. Para encontrar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança: **Buscar contatos de trabalho**.

Essa opção também desativa a breve pesquisa na web antes da primeira reunião (veja [Preparativos para suas reuniões](calendar.md#ready-for-your-meetings)).

Quando a consulta encontra esses dados, a página da pessoa também mostra a descrição, desde quando ela ocupa o cargo atual e os dois cargos anteriores. Os preparativos também usam essas informações. A descrição só é usada quando a pessoa não tem uma biografia própria.

Suas conexões completam esses dados com o que já leem: cargo, telefone e fuso horário do Slack; biografia e cidade do X; título e foto do LinkedIn; cargos do Google Contacts e do Salesflare; e a foto de um contato do Salesflare, se o próprio Salesflare tiver uma. Passe o cursor sobre a linha abaixo do nome para ver de onde veio a informação.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são obtidas pela sincronização do WhatsApp e pela conexão com seus chats do Telegram: até 50 por dia de cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém sem foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de um Fleet de Trabalho, uma cópia pequena da foto profissional acompanha o cadastro compartilhado da pessoa. Fotos do Google Contacts, WhatsApp, Telegram ou Facebook, e fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus endereços e números, inclusive seus pseudônimos, são sempre seus, nunca de alguém no seu Graph. Ao pesquisar por você ou adicionar alguém com um dos seus endereços, **Sobre você** é aberto, e sua própria linha é ignorada na importação.

A página Sobre você lista seus endereços e a origem de cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seu contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que essa pessoa representa para você

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, com apenas as palavras que indicam a função, como um cargo. Alguém dizer que é seu contador ou cliente não basta: também é preciso haver sinais do seu lado, como suas mensagens ou reuniões com essa pessoa. Você não precisa confirmar nada. Se algo estiver errado, **Editar** na página da pessoa corrige a informação, assim como **⋯** na linha correspondente em **Mudanças recentes**. Sua Machine aprende com suas edições.

## O que sua Machine sabe sobre alguém

Os fatos sobre a pessoa aparecem na página dela, em **Informações conhecidas**. O Aprendizado mantém as informações gerais. **Adicionar** inclui mais uma informação com suas próprias palavras. Cada fato tem um menu:

- **Editar** altera o fato diretamente.
- **Não é sobre essa pessoa** transforma o fato em uma informação geral novamente, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre eles: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou a mudança de um projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Se uma informação estiver errada, use **⋯** na linha para corrigi-la diretamente: **Editar**, **Remover**, **Não é sobre essa pessoa** ou **Desfazer** para devolver um projeto ao lugar onde estava. Três linhas são exibidas. **Mostrar mais** exibe as demais.

Uma pessoa atualizada hoje pela sua Machine recebe um pequeno ponto na lista de Pessoas, e a mensagem **4 pessoas atualizadas hoje** aparece no início da lista. Veja [O Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, inicia uma tarefa sobre ela.
