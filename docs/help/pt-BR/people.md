---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: páginas, resumos e linhas do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 2fe1c104a74711c4
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros e-mails não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista. **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros. Veja [The Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta como parte da organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de uma pessoa

No início da página, aparecem a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam diariamente · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem com a data. Passe o cursor sobre ela para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou em **Copiar** para copiar. O **Aniversário** também aparece aqui, junto com a fonte da informação (Google Contacts, Google Calendar, Facebook ou você). Veja [The Graph](graph.md#birthday).
- **Com você**: o que a pessoa representa para você, se é um contato de Trabalho ou Pessoal e se faz parte da sua família ou Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares em que vocês conversam. **Slack** abre a pessoa no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feita** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de alguém são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal da pessoa em cópia.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, toque em **Algo errado?** na parte inferior da página.

## Resumo

Algumas frases curtas no início da página da pessoa: o que foi decidido, pedido, planejado ou prometido, com os nomes de todos os envolvidos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada frase antes. Em geral, isso acontece uma vez por dia. Se algo relacionado à pessoa mudar, como um novo prazo ou um pedido retirado, o resumo é atualizado em algumas horas.

Informações vagas ficam de fora. Se não houver nada específico a dizer, o resumo não aparece. Cada frase leva à fonte: mensagens do mesmo dia compartilham uma data com a quantidade de mensagens e podem ser abertas juntas.

Use **Editar** para escrever do seu jeito. Quando houver novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o resumo para ela.

As preparações de reuniões usam esse resumo, mas só as frases do lado daquela tarefa, Trabalho ou Pessoal. O resumo fica na sua Machine; sua equipe nunca pode vê-lo.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e movimentações de projetos. Os filtros no topo mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** mostra as demais. Cada reunião mostra quem participou, com cada pessoa aparecendo uma única vez. Reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são pessoais: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Em uma página, **Equipe**, acima da linha do tempo, adiciona o que seus colegas compartilharam, com a indicação de quem compartilhou cada item. **Meus** mostra apenas o que é seu.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** mostram as pessoas de acordo com o Tipo indicado na página delas. Sua escolha (**Editar**) tem prioridade. Caso contrário, sua família e seus amigos, assim como familiares ou amigos da pessoa (esposa, pai), são classificados como Pessoal, independentemente do endereço usado para escrever. Sua equipe nunca vê os contatos pessoais.

## Adicionar alguém

Toque em **Nova pessoa**, no topo de Pessoas, ou em **+**, na barra superior do celular. Informe um nome e, se souber, um e-mail e uma organização. Se já houver alguém parecido no seu Graph, o formulário mostra essa pessoa primeiro para você abrir o perfil existente. **Adicionar** abre a nova página.

A pessoa que você adiciona continua na lista, mesmo sem nenhuma mensagem. A primeira mensagem associa a pessoa ao perfil.

## Editar alguém

**Editar**, no topo da página da pessoa, permite alterar o nome, o cargo, a organização, a localização, o LinkedIn, os telefones e os e-mails, o que ela representa para você e se é um contato de Trabalho ou Pessoal. O campo **Notas** serve para registrar o que você quiser lembrar. As notas são mantidas quando você mescla perfis. **Salvar** guarda as alterações; **Cancelar** mantém tudo como estava.

Suas alterações são mantidas quando os dados da pessoa são consultados novamente e também depois de usar **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para usar novamente o valor consultado. Se apagar o nome, o nome usado nas mensagens da pessoa volta a aparecer.

Para alterar a foto, clique nela e escolha **Enviar uma imagem**, selecione uma imagem encontrada para a pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página delas pergunta se são a mesma pessoa, e a lista Pessoas mostra os perfis em **Mesma pessoa?**. **Mesclar** junta os perfis e reúne todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém os perfis separados permanentemente. Sua resposta aparece por um momento no par, que depois sai da lista. A lista desaparece quando não houver mais nada para confirmar.

Um endereço compartilhado, como info@ ou o endereço de uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e uma conversa pessoal que só têm um nome em comum também não são associados automaticamente. Em vez disso, aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma vez, exceto os que você marcou como **Não é a mesma**. Use **Desfazer** logo em seguida para separar todos novamente.

Para associar duas pessoas manualmente, abra uma delas e toque em **⋯**, **Mesma pessoa que…** e escolha a outra. A página da pessoa associada mostra o motivo em **Associada de**, com a opção **Desfazer** para separar os perfis novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Depois, toque em **Excluir**. Isso remove a pessoa e tudo o que sua Machine sabe sobre ela: o perfil, os endereços, os dados consultados, as mensagens que só vocês trocaram e as notas sobre ela.

As tarefas que envolvem a pessoa continuam, mas o nome dela é removido. Ela não será adicionada novamente, nem por uma importação nem por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail para alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço da pessoa aparece primeiro. Novos rascunhos nunca são enviados para esse endereço se outro endereço for conhecido. Se esse for o único endereço, a tela de envio mostra um aviso, mas você ainda pode enviar o e-mail.

Um e-mail conta como devolvido quando o servidor de e-mail informa que o endereço não existe ou depois de 3 falhas temporárias ao longo de uma semana. O aviso desaparece quando a pessoa escreve novamente usando esse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço corporativo têm cargo, foto, LinkedIn e cidade consultados como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para buscar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Para desativar esse recurso, acesse **Configurações** e, em Segurança, desative **Buscar contatos de trabalho**.

Quando a consulta encontra informações sobre a pessoa, a página também mostra o texto de apresentação, desde quando ela está no cargo atual e os dois cargos anteriores. As preparações também usam essas informações, mas só incluem o texto de apresentação quando a pessoa não tem uma biografia própria.

Suas conexões ganham mais informações com o que já foi lido: cargo, telefone e fuso horário do Slack; biografia e localização do X; título e foto do LinkedIn; cargos do Google Contacts e Salesflare; e foto do contato do Salesflare, quando o próprio Salesflare mantém uma foto. Passe o cursor sobre a linha abaixo do nome para ver de onde cada informação veio.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são obtidas pela sincronização do WhatsApp e pela conexão com seus chats do Telegram: até 50 por dia em cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto de perfil de alguém que ainda não tenha uma foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Team Graph](team-graph.md) de um Fleet de Trabalho, uma pequena cópia da foto profissional acompanha o registro compartilhado da pessoa. Fotos do Google Contacts, WhatsApp, Telegram ou Facebook, além de fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, inclusive aliases, são sempre seus, nunca de alguém no seu Graph. Ao pesquisar por você ou adicionar alguém usando um dos seus endereços, a página **Sobre você** é aberta. Uma importação também ignora sua própria linha.

A página Sobre você lista seus endereços e mostra de onde veio cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seus dados de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que você representa para essa pessoa

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, junto com o trecho em que foram identificadas. Não é preciso esperar que você confirme. Algo está errado? **Editar** na página corrige a informação, ou toque em **⋯** na linha correspondente em **Mudanças recentes**. A Machine aprende com suas alterações.

## O que ela sabe sobre alguém

Os fatos sobre uma pessoa ficam na página dela, em **Informações conhecidas**. Os fatos gerais ficam em Aprendizado. Toque em **Adicionar** para incluir outro fato com as suas próprias palavras. Cada fato tem um menu:

- **Editar** altera o fato ali mesmo.
- **Não é sobre** transforma o fato em uma informação geral novamente, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre ela: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou uma mudança de projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Se uma informação estiver errada, use **⋯** na linha para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** ou **Desfazer** para devolver um projeto ao lugar onde estava. São exibidas três linhas. **Mostrar mais** exibe as demais.

Uma pessoa que sua Machine atualizou hoje aparece com um ponto pequeno na lista Pessoas, e **4 pessoas atualizadas hoje** no topo da lista mostra quem são. Veja [The Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, inicia uma tarefa sobre ela.
