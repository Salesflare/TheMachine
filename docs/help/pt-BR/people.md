---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: a página, o resumo e a linha do tempo de cada uma, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: a16cc66e51a64fd2
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: veja [Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) é associada à organização, não a uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias", e o contato mais antigo aparece como uma data. Passe o cursor sobre ela para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, junto com a origem da informação (Contatos do Google, Google Calendar, Facebook, suas notas ou você): veja [Graph](graph.md#birthday).
- **Com você**: o que a pessoa representa para você, se é um contato de trabalho ou pessoal, e se faz parte da sua família ou da Fleet, com a opção **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feita** e **Descartar**) e a **Linha do tempo**.

Os endereços e chats de alguém são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia.

Se a página mostrar **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte de baixo da página.

## Resumo

Algumas linhas curtas no topo da página de uma pessoa: o que foi decidido, pedido, planejado ou prometido, com o nome de todos os envolvidos. The Machine reescreve o resumo quando há novidades, somente para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Geralmente, uma vez por dia. Quando algo muda, como um novo prazo ou a retirada de um pedido, a atualização pode aparecer em algumas horas.

Uma informação vaga fica de fora. Se não houver nada específico para dizer, não há resumo. Cada linha tem um link para a origem: mensagens do mesmo dia aparecem juntas, com uma data e a quantidade de mensagens, e podem ser abertas.

Use **Editar** para escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o texto para ela.

Os preparativos para reuniões também usam o resumo, mas só as linhas da categoria daquela tarefa, Trabalho ou Pessoal. O resumo fica na sua Machine; sua equipe nunca o vê.

## Linha do tempo

Toda página de pessoa e organização tem uma linha do tempo, da atividade mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros no topo mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões ficam no topo, em **Em breve**, começando pela mais próxima. **Mostrar todos os próximos** mostra as demais. Uma reunião mostra quem participou, cada pessoa uma vez. Se tiver notas ou uma transcrição, aparece **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Em uma página, **Equipe**, acima da linha do tempo, adiciona o que seus colegas compartilharam. Cada item indica quem compartilhou. **Meus** mostra apenas o que você compartilhou.

## Trabalho e pessoal

As abas **Trabalho** e **Pessoal** organizam as pessoas pelo tipo definido na página delas. A opção escolhida por você (**Editar**) tem prioridade. Caso contrário, sua família e seus amigos, assim como familiares ou amigos seus (uma esposa, um pai), são classificados como contatos pessoais, independentemente do endereço usado para escrever. Sua equipe nunca vê seus contatos pessoais.

## Adicionar alguém

Use **Nova pessoa** no topo de Pessoas ou **+** na barra superior do celular. Informe um nome e, se tiver, um e-mail e uma organização. Se já houver alguém parecido no seu Graph, o formulário mostra essa pessoa primeiro, para você poder abrir a página existente. **Adicionar** abre a nova página.

A pessoa que você adicionar continua na lista, mesmo sem mensagens. A primeira mensagem dela é associada à pessoa.

## Editar alguém

**Editar**, no topo da página da pessoa, permite alterar o nome, o cargo, a organização, a cidade, o LinkedIn, os telefones e e-mails, o que ela representa para você e se é um contato de trabalho ou pessoal. O campo **Notas** serve para guardar qualquer informação que você queira lembrar. As notas são mantidas ao mesclar pessoas. **Salvar** aplica as alterações; **Cancelar** descarta as mudanças.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente e também após **Mesclar** e **Desfazer**. Apague um campo para voltar a usar o valor consultado. Se apagar o nome, ele volta a ser o nome usado nas mensagens da pessoa.

Para alterar a foto, clique nela e escolha **Enviar uma imagem**, selecione uma foto encontrada para a pessoa ou use **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página pergunta se são a mesma pessoa, e Pessoas mostra as duas em **Mesma pessoa?**. **Mesclar** combina os dados, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém as pessoas separadas permanentemente. Sua resposta aparece no par por um instante, e depois ele sai da lista. A lista desaparece quando não há mais nada para confirmar.

Alguém com um endereço que só se parece com outro que você conhece, como acme-corp.example e acmecorp.example, nunca é sugerido como a mesma pessoa. Só você pode atribuir uma função a essa pessoa.

Um nome sozinho nunca basta para associar pessoas de domínios diferentes, porque qualquer um pode digitar o mesmo nome. Dois endereços em domínios diferentes só são sugeridos quando há outra ligação entre eles, como as mesmas pessoas ou um projeto. Alguém que usa seu nome em um endereço que não é seu nunca é sugerido. Em vez disso, adicione seus outros endereços em Configurações, em [Seus endereços](settings.md#your-addresses).

Se apenas o primeiro nome corresponder em domínios diferentes, como "Sam" e "Sam Lee", as pessoas só serão sugeridas se tiverem o mesmo número de telefone ou perfil do LinkedIn.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que têm apenas um nome em comum também não são associados automaticamente: aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. **Desfazer** logo depois separa todos novamente.

Para associar duas pessoas por conta própria, abra uma delas e selecione **⋯**, **Mesma pessoa que…** e a outra pessoa. A página de uma pessoa mesclada mostra o motivo em **Associada a partir de**, com a opção **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Depois, selecione **Excluir**. A pessoa e as informações que sua Machine tem sobre ela serão removidas: o cadastro, os endereços, os dados consultados, as mensagens trocadas somente entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa continuam, mas sem o nome dela. Ela não será adicionada novamente, nem por uma importação nem por uma tarefa de aniversários do Facebook que contenha o nome ou o endereço dela. Não é possível desfazer essa ação.

## E-mails devolvidos

Quando um e-mail enviado para alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço dessa pessoa passa a ser usado primeiro. Novos rascunhos nunca são enviados para esse endereço quando há outro conhecido. Se for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail é considerado devolvido quando o servidor de e-mail informa que o endereço não existe ou após 3 falhas temporárias em uma semana. O aviso é removido quando a pessoa escreve novamente usando esse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço corporativo têm cargo, foto, LinkedIn e cidade consultados, assim como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta usa apenas o nome da pessoa e o domínio da empresa. Para buscar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Para desativar esse recurso, vá até **Configurações** e, na seção Segurança, desative **Buscar contatos de trabalho**.

Quando a consulta encontra os dados da pessoa, a página também mostra a descrição, desde quando ela está no cargo atual e os dois cargos anteriores. Os preparativos também usam essas informações. A descrição só é usada quando a pessoa não tem uma bio própria.

Suas conexões são enriquecidas com informações que já estavam disponíveis: cargo, telefone e fuso horário do Slack; bio e cidade do X; título e foto do LinkedIn; cargos dos Contatos do Google e do Salesflare; e a foto de um contato do Salesflare, se ele tiver uma. Passe o cursor sobre a linha abaixo do nome para ver a origem da informação.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são sincronizadas pela conexão do WhatsApp e dos chats do Telegram: até 50 por dia em cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém que ainda não tem uma quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de uma Fleet de trabalho, uma cópia pequena da foto de trabalho acompanha o cadastro compartilhado da pessoa. Fotos dos Contatos do Google, WhatsApp, Telegram ou Facebook, e fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus endereços e números, incluindo aliases, são sempre seus e nunca são associados a alguém no seu Graph. Se você pesquisar por si mesmo ou adicionar alguém com um dos seus endereços, **Sobre você** será aberto, e uma importação ignorará seu próprio registro.

A página Sobre você lista seus endereços e a origem de cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seus dados de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que a pessoa representa para você

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, junto apenas das palavras que indicam a função, como um cargo. Não basta alguém dizer que é seu contador ou cliente: é preciso haver informações do seu lado também, como suas mensagens ou reuniões com essa pessoa. Você não precisa confirmar nada. Se estiver errado, use **Editar** na página da pessoa ou **⋯** na linha em **Mudanças recentes** para corrigir. A Machine aprende com suas alterações.

## O que sabe sobre alguém

As informações sobre uma pessoa ficam na página dela, em **Informações conhecidas**. O aprendizado guarda as informações gerais. Use **Adicionar** para incluir mais uma informação com suas próprias palavras. Cada informação tem um menu:

- **Editar** permite alterar a informação ali mesmo.
- **Não é sobre** essa pessoa transforma a informação em um dado geral novamente, em **Aprendizado**, **Fatos**.
- **Remover** exclui a informação de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, que fica recolhida logo acima da linha do tempo de uma pessoa, organização ou projeto, mostra o que sua Machine alterou ou aprendeu sobre ela: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou uma mudança em um projeto. Cada linha mostra a data e a origem. Toque na origem para ler a mensagem.

Se uma informação estiver errada, use **⋯** na linha para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** a pessoa ou **Desfazer** para devolver um projeto ao lugar anterior. São exibidas três linhas; **Mostrar mais** mostra as demais.

Uma pessoa cujas informações sua Machine atualizou hoje tem um pequeno ponto na lista Pessoas, e **4 pessoas atualizadas hoje** aparece no topo da lista com os nomes. Veja [Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, cria uma tarefa sobre ela.
