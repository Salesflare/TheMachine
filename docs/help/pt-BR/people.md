---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: páginas, resumos e linhas do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: b23d3ebdc4f162f2
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista. **Mostrar como pessoa** adiciona alguém. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada uma tem seus próprios filtros: veja [O Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta para a organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e a localização da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem como uma data. Passe o cursor sobre ela para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, com a origem da informação (Contatos do Google, Google Agenda, Facebook, suas notas ou você): veja [O Graph](graph.md#birthday).
- **Com você**: o que a pessoa é para você, se é um contato de Trabalho ou Pessoal e se faz parte da sua Família ou do seu Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês por lá.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas nos dois sentidos, com **Marcar como feita** e **Descartar**) e a **Linha do tempo**.

Os endereços e chats de uma pessoa são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia. Isso também acontece quando alguém com quem você conversa marca uma ligação pelo link que você enviou no chat e o sobrenome ou a empresa corresponde.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte de baixo da página.

## Resumo

Algumas linhas curtas no topo da página de uma pessoa: o que foi decidido, pedido, planejado ou prometido, com o nome de todos os envolvidos. The Machine reescreve o resumo quando há novidades, somente para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Isso costuma acontecer uma vez por dia, ou em poucas horas quando algo muda, como um novo prazo ou um pedido retirado.

Uma linha vaga fica de fora. Se não houver nada específico para dizer, não há resumo. Cada linha leva à origem: mensagens do mesmo dia compartilham uma data e mostram a quantidade de mensagens. Toque na data para abri-las.

**Editar** o resumo para deixá-lo do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o resumo para The Machine.

As preparações para reuniões usam o resumo, mas somente as linhas relacionadas ao tipo daquela tarefa, Trabalho ou Pessoal. Ele fica na sua Machine. Sua equipe nunca o vê.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma linha do tempo, da atividade mais recente para a mais antiga: e-mails, reuniões e seus resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e movimentações de projetos. Os chips no topo mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** mostra as demais. A reunião mostra quem participou, cada pessoa uma única vez. Quando há notas ou uma transcrição, aparece **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Na página, **Equipe**, acima da linha do tempo, adiciona o que as pessoas da equipe compartilharam, com a indicação de quem enviou cada item. **Meus** mostra somente os seus itens.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** organizam as pessoas pelo tipo definido na página de cada uma. A opção que você escolher (**Editar**) tem prioridade. Caso contrário, sua família e seus amigos, além de familiares e amigos da pessoa (uma esposa, um pai), são classificados como Pessoal, não importa de qual endereço escrevam. Sua equipe nunca recebe contatos Pessoais.

## Adicionar alguém

Use **Nova pessoa**, no topo da seção Pessoas, ou **+** na barra superior do celular. Informe o nome e, se tiver, o e-mail e a organização. Se alguém parecido já estiver no seu Graph, o formulário mostra essa pessoa primeiro para que você possa abrir a página dela. **Adicionar** abre a página da nova pessoa.

A pessoa que você adiciona continua na lista, mesmo sem mensagens. A primeira mensagem associa as informações a ela.

## Editar alguém

**Editar**, no topo da página, permite alterar nome, cargo, organização, localização, LinkedIn, telefones e e-mails, o que a pessoa é para você e se ela é de Trabalho ou Pessoal. O campo **Notas** serve para você anotar o que quiser lembrar. As notas são mantidas ao mesclar pessoas. **Salvar** guarda as alterações; **Cancelar** descarta as alterações.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente, e também ao usar **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para usar novamente o valor consultado. Se apagar o nome, o nome das mensagens da pessoa será restaurado.

Para alterar a foto, clique nela e escolha **Enviar uma imagem**, uma foto encontrada para a pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página pergunta se são a mesma pessoa, e a seção Pessoas as mostra em **Mesma pessoa?**. **Mesclar** junta as duas pessoas e todas as mensagens, notas, funções e projetos delas. **Não é a mesma** mantém as pessoas separadas permanentemente. Sua resposta aparece no par por um instante, e depois ele sai da lista. A lista desaparece quando não há mais nada para revisar.

Alguém com um endereço que apenas parece com o de uma pessoa conhecida, como acme-corp.example e acmecorp.example, nunca é sugerido como a mesma pessoa. Além disso, só você pode atribuir uma função a essa pessoa.

Um nome sozinho nunca basta para associar pessoas de domínios diferentes, já que qualquer pessoa pode usá-lo. Dois endereços de domínios diferentes só são sugeridos quando algo mais os relaciona, como as mesmas pessoas ou um projeto. Alguém que use seu nome em um endereço que não é seu nunca é sugerido. Em vez disso, adicione seus outros endereços em Configurações, em [Seus endereços](settings.md#your-addresses).

Quando apenas o primeiro nome corresponde em domínios diferentes, como "Sam" e "Sam Lee", as pessoas só são sugeridas se tiverem o mesmo número de telefone ou perfil do LinkedIn.

Quando apenas o primeiro nome corresponde a uma reunião criada a partir de um chat, ou quando o endereço pertence a alguém que você já conhecia e só a pessoa no chat diz que é dela, o sistema pergunta. The Machine nunca abre um link para descobrir.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que só têm um nome em comum não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. Selecione **Desfazer** logo depois para separar todos novamente.

Para associar duas pessoas manualmente, abra uma delas, toque em **⋯**, escolha **Mesma pessoa que…** e selecione a outra. A página da pessoa mesclada mostra o motivo em **Associada a partir de**, com a opção **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Depois, selecione **Excluir**. Isso remove a pessoa e o que sua Machine sabe sobre ela: o registro, os endereços, os dados consultados, as mensagens trocadas somente entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa continuam, mas o nome dela é removido. Ela não será adicionada novamente, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado para alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço da pessoa é exibido primeiro. Rascunhos novos nunca são enviados para esse endereço quando há outro conhecido. Se esse for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail é considerado devolvido quando o servidor de e-mail informa que o endereço não existe ou após três falhas temporárias ao longo de uma semana. O aviso é removido quando a pessoa escreve novamente desse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço corporativo recebem um cargo, uma foto, informações do LinkedIn e a cidade, consultados como em [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta usa somente o nome da pessoa e o domínio da empresa. Para encontrar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança: **Buscar contatos de trabalho**.

Essa opção também interrompe a consulta ao site antes da primeira reunião e a busca na Web quando há um provedor de busca configurado (veja [Preparação para suas reuniões](calendar.md#ready-for-your-meetings)).

Quando a consulta encontra informações sobre a pessoa, a página também mostra o texto de apresentação, desde quando ela ocupa o cargo atual e os dois cargos anteriores. As preparações também consultam essas informações. O texto de apresentação só é usado quando a pessoa não tem uma biografia própria.

Suas conexões incluem mais informações que elas já consultaram: cargo, telefone e fuso horário do Slack; biografia e localização do X; título e foto do LinkedIn; cargos dos Contatos do Google e do Salesflare; e a foto de um contato do Salesflare, quando o próprio Salesflare a mantém. Passe o cursor sobre a linha abaixo do nome para ver de onde veio a informação.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são obtidas pela sincronização do WhatsApp e pela conexão com os chats do Telegram: até 50 por dia em cada serviço, somente para pessoas que já estão no seu Graph. Nada é enviado a essas pessoas. Uma importação de aniversários do Facebook adiciona a foto de perfil de alguém sem foto quando você a salva ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de um Fleet de Trabalho, uma cópia pequena de uma foto profissional acompanha o registro compartilhado da pessoa. Fotos dos Contatos do Google, WhatsApp, Telegram ou Facebook, assim como fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, inclusive aliases, são sempre você, nunca alguém no seu Graph. Se você procurar por si ou adicionar alguém com um dos seus endereços, **Sobre você** será aberto. Uma importação também ignora sua própria linha.

A seção Sobre você lista seus endereços e a origem de cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seu contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que essa pessoa é para você

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, somente com as palavras que indicam a função, como um cargo. Não basta alguém dizer que é seu contador ou cliente. Isso também precisa aparecer do seu lado, por exemplo, nas suas mensagens ou reuniões com a pessoa. Não é preciso esperar você dizer. Se algo estiver errado, **Editar** na página da pessoa corrige, ou use **⋯** na linha correspondente em **Mudanças recentes**. A Machine aprende com suas alterações.

## O que a Machine sabe sobre alguém

As informações sobre a pessoa ficam na página dela, em **Informações conhecidas**. O **Aprendizado** mantém as informações gerais. **Adicionar** inclui mais uma informação, escrita com suas próprias palavras. Cada informação tem um menu:

- **Editar** altera a informação ali mesmo.
- **Não é sobre** essa pessoa transforma a informação em uma informação geral novamente, em **Aprendizado**, **Fatos**.
- **Remover** exclui a informação de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre ela: uma função, onde a pessoa trabalha, a relação entre duas pessoas, uma informação ou uma mudança de projeto. Cada linha mostra a data e a origem. Toque na origem para ler a mensagem.

Quando uma linha está errada, use **⋯** para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** essa pessoa ou **Desfazer** para colocar um projeto de volta onde estava. São exibidas três linhas. **Mostrar mais** exibe as demais.

Uma pessoa cujas informações sua Machine atualizou hoje aparece com um ponto na lista de Pessoas, e **4 pessoas atualizadas hoje** no topo da lista mostra quem são. Veja [O Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, cria uma tarefa sobre ela.
