---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: página, resumo e linha do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 26845dd199228f90
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista. **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: veja [The Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta para a organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre o contato entre vocês ("Conversa diária · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem com a data. Passe o cursor sobre ela para ver a data exata. Abaixo:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. A **Aniversário** também aparece aqui, junto da origem da informação (Google Contacts, Google Calendar, Facebook, suas notas ou você): veja [The Graph](graph.md#birthday).
- **Com você**: o que a pessoa é para você, se é um contato de Trabalho ou Pessoal, e se faz parte da sua família ou do seu Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, itens **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feita** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de uma pessoa são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte inferior da página.

## Resumo

Algumas linhas curtas no início da página de uma pessoa: o que foi decidido, pedido, planejado ou prometido, com todas as pessoas mencionadas. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Geralmente, isso acontece uma vez por dia. Se algo mudar em uma questão envolvendo essa pessoa, como um novo prazo ou um pedido retirado, o resumo é atualizado em poucas horas.

Uma linha vaga fica de fora. Se não houver nada específico para dizer, não há resumo. Cada linha leva à fonte da informação: mensagens do mesmo dia aparecem juntas sob uma única data, com a quantidade de mensagens, e podem ser abertas juntas.

Use **Editar** para escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o resumo para ela.

A preparação para reuniões usa esse resumo, mas só as linhas relacionadas à tarefa daquele lado (Trabalho ou Pessoal). O resumo fica na sua Machine. Sua equipe nunca tem acesso a ele.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma, em ordem da mais recente para a mais antiga: e-mails, reuniões e seus resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros na parte de cima mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** exibe as demais. A reunião mostra quem participou, com cada pessoa listada uma única vez. As reuniões com notas ou transcrição exibem **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são pessoais: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Na página, **Equipe**, acima da Linha do tempo, adiciona o que colegas compartilharam, com o nome de quem compartilhou em cada item. **Meus** mostra apenas os seus itens.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas pelo Tipo definido na página de cada uma. A escolha que você faz (**Editar**) prevalece. Caso contrário, sua família e seus amigos, assim como familiares ou amigos seus (uma esposa, um pai), são classificados como Pessoal, independentemente do endereço usado para escrever. Sua equipe nunca tem acesso aos contatos Pessoais.

## Adicionar alguém

Use **Nova pessoa** na parte superior de Pessoas ou **+** na barra superior do celular. Informe um nome e, se souber, um e-mail e uma organização. Se já houver alguém parecido no seu Graph, o formulário mostra essa pessoa primeiro, para você abrir o cadastro existente. **Adicionar** abre a nova página.

A pessoa que você adiciona permanece na lista, mesmo sem mensagens. A primeira mensagem que você receber dela será associada ao cadastro.

## Editar alguém

**Editar**, na parte superior da página, permite alterar o nome, cargo, organização, localização, LinkedIn, telefones e e-mails da pessoa, o que ela é para você e se é de Trabalho ou Pessoal. O campo **Notas** serve para você guardar o que quiser lembrar. As notas permanecem após mesclagens. **Salvar** mantém as alterações; **Cancelar** descarta tudo.

Suas edições são mantidas mesmo quando os dados da pessoa são consultados novamente, e também após **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se apagar o nome, o nome usado nas mensagens da pessoa volta a aparecer.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, uma foto encontrada para a pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página delas pergunta se são a mesma pessoa, e Pessoas as lista em **Mesma pessoa?**. **Mesclar** une as duas, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém os cadastros separados. Sua resposta aparece no par por um momento, e depois ele sai da lista. A lista desaparece quando não houver mais nada para confirmar.

Um endereço que apenas parece com um endereço conhecido, como acme-corp.example em vez de acmecorp.example, nunca é apresentado como sendo da mesma pessoa. Só você pode atribuir uma função a esse contato.

Um endereço compartilhado, como info@ ou uma lista de distribuição, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e uma conversa pessoal em que só o nome coincide também não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. Use **Desfazer** logo em seguida para separar todos de novo.

Para associar duas pessoas manualmente, abra uma delas e escolha **⋯**, **Mesma pessoa que…** e a outra pessoa. A página de uma pessoa associada mostra o motivo em **Associada a partir de**, com a opção **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Em seguida, toque em **Excluir**. A pessoa e tudo o que sua Machine sabe sobre ela serão removidos: o cadastro, os endereços, os dados consultados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa permanecem, mas sem o nome dela. Ela não será adicionada novamente, nem por uma importação nem por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Essa ação não pode ser desfeita.

## E-mail devolvido

Quando um e-mail enviado para alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço da pessoa aparece primeiro. Novos rascunhos nunca são enviados para esse endereço quando há outro conhecido. Se esse for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail conta como devolvido quando o servidor de e-mail informa que o endereço não existe ou após 3 falhas temporárias ao longo de uma semana. O aviso desaparece quando a pessoa escreve novamente usando esse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço corporativo têm cargo, foto, LinkedIn e cidade consultados da mesma forma que os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para buscar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança: **Buscar contatos de trabalho**.

Quando os dados são encontrados, a página da pessoa também mostra o texto de apresentação, há quanto tempo ela está no cargo atual e os dois cargos anteriores. As preparações também usam esses dados. O texto de apresentação só é usado quando a pessoa não tem uma biografia própria.

Suas conexões ficam mais completas com informações que já leem: cargo, telefone e fuso horário do Slack; biografia e cidade do X; título e foto do LinkedIn; cargos dos contatos do Google Contacts e do Salesflare; e foto de um contato do Salesflare, quando o próprio Salesflare a mantém. Passe o cursor sobre a linha abaixo do nome para ver a origem dos dados.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são obtidas pela sincronização do WhatsApp e pela conexão dos seus chats do Telegram: até 50 por dia em cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto de perfil de quem não tem foto quando você a salva ([Rotinas](routines.md)). Tudo fica na sua Machine.

Em um Fleet de Trabalho, uma pequena cópia da foto de trabalho acompanha o registro compartilhado da pessoa no [Graph da equipe](team-graph.md). Fotos dos contatos do Google, WhatsApp, Telegram ou Facebook, além das fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, inclusive aliases, são sempre seus e nunca são de alguém no seu Graph. Se você buscar por si mesmo ou adicionar uma pessoa com um dos seus endereços, **Sobre você** será aberto. Uma importação também ignora a sua própria linha.

Sobre você lista seus endereços e a origem de cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seus dados de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que a pessoa é para você

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, junto da frase em que foram identificadas. Não é preciso esperar sua confirmação. Está errado? Corrija em **Editar**, na página da pessoa, ou em **⋯**, na linha correspondente em **Mudanças recentes**. A Machine aprende com suas edições.

## O que ela sabe sobre alguém

Os fatos sobre uma pessoa ficam na página dela, em **Conhecido sobre**. O Aprendizado guarda os fatos gerais. Use **Adicionar** para incluir outro fato com suas próprias palavras. Cada fato tem um menu:

- **Editar** altera o fato na própria página.
- **Não é sobre** a pessoa transforma o fato em uma informação geral de novo, em **Aprendizado**, **Fatos**.
- **Remover** apaga o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre eles: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou uma mudança em um projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Quando uma linha está errada, use **⋯** para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** a pessoa ou **Desfazer** para devolver um projeto ao lugar anterior. São exibidas três linhas. **Mostrar mais** exibe as demais.

Uma pessoa atualizada pela sua Machine hoje aparece com um ponto ao lado do nome na lista Pessoas. No topo da lista, **4 pessoas atualizadas hoje** mostra quem são. Veja [The Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, cria uma tarefa sobre ela.
