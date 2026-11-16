---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: a página, o resumo e a linha do tempo delas, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 0eb2dcc70fba84c2
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Essas pessoas ficam em Remetentes ocultos, abaixo da lista. **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: veja [The Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta como parte da organização, não como uma pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e a cidade da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversam todos os dias · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias". Contatos mais antigos aparecem com a data. Passe o cursor sobre a data para ver o dia exato. Abaixo, você encontra:

- **Contato**: telefones e e-mails. Toque em um deles para ligar ou escrever, ou em **Copiar**. O **Aniversário** também aparece aqui, junto com a fonte (Contatos do Google, Google Calendar, Facebook, suas notas ou você): veja [The Graph](graph.md#birthday).
- **Com você**: o que essa pessoa representa para você, como contato de trabalho ou pessoal, e se faz parte da sua família ou da sua Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre o perfil da pessoa no Slack ou a conversa mais recente de vocês por lá.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feita** e **Descartar**) e a **Linha do tempo**.

Os endereços e chats de alguém são associados automaticamente quando fica claro que são da mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, use **Algo errado?** na parte inferior da página.

## Resumo

Algumas linhas curtas no início da página de uma pessoa, sobre o que foi decidido, perguntado, planejado ou prometido, com o nome de todos os envolvidos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Normalmente, isso acontece uma vez por dia. Quando algo muda, como um novo prazo ou a retirada de um pedido, o resumo é atualizado em algumas horas.

Linhas vagas não aparecem. Se não houver nada específico para dizer, não há resumo. Cada linha leva à fonte. Mensagens do mesmo dia ficam agrupadas em uma única data, com a quantidade de mensagens, e podem ser abertas juntas.

Use **Editar** para escrever do seu jeito. Quando houver novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o texto para ela.

Os preparativos para reuniões usam o resumo, mas apenas as linhas do tipo daquela tarefa (Trabalho ou Pessoal). O resumo fica na sua Machine. Sua equipe nunca o vê.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros na parte de cima mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no início, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** mostra as demais. A reunião mostra quem participou, com cada pessoa listada uma única vez. Reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas. O Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Na página, **Equipe**, acima da Linha do tempo, adiciona o que foi compartilhado por colegas. Cada item informa quem compartilhou. **Meus** mostra apenas o que é seu.

## Trabalho e pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas de acordo com o Tipo definido na página delas. Sua escolha (**Editar**) prevalece. Caso contrário, sua família e seus amigos, além das pessoas que são da sua família ou suas amigas (como uma esposa ou um pai), ficam como contatos pessoais, não importa de qual endereço escrevam. Sua equipe nunca tem acesso aos contatos pessoais.

## Adicionar alguém

Use **Nova pessoa** na parte de cima de Pessoas ou **+** na barra superior do celular. Informe o nome e, se souber, o e-mail e a organização. Se já houver alguém parecido no seu Graph, essa pessoa aparece primeiro no formulário para você abrir a página existente. **Adicionar** abre a nova página.

A pessoa que você adicionar continuará na lista, mesmo sem mensagens. A primeira mensagem será associada a ela.

## Editar alguém

Use **Editar** no início da página para mudar o nome, o cargo, a organização, a cidade, o LinkedIn, os telefones e e-mails, o que essa pessoa representa para você e se é um contato de Trabalho ou Pessoal. O campo **Notas** serve para você registrar o que quiser lembrar. As notas são mantidas ao mesclar pessoas. **Salvar** mantém as alterações. **Cancelar** descarta as alterações.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente, e também ao usar **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se você apagar o nome, o nome das mensagens será restaurado.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, uma das fotos encontradas para essa pessoa ou **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, a página delas pergunta se são a mesma pessoa, e a lista de Pessoas mostra as duas em **Mesma pessoa?**. **Mesclar** junta as duas, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém as pessoas separadas. Sua resposta aparece no par por um instante e, depois, ele sai da lista. A lista desaparece quando não houver mais nada para perguntar.

Alguém com um endereço que apenas se parece com um que você conhece, como acme-corp.example e acmecorp.example, nunca será sugerido como a mesma pessoa. Só você pode atribuir uma função a essa pessoa.

Um nome sozinho nunca basta para associar pessoas de dois domínios diferentes, porque qualquer pessoa pode digitar o mesmo nome. Dois endereços em domínios diferentes só são sugeridos quando há outra ligação entre eles, como as mesmas pessoas ou um projeto. Alguém que use seu nome em um endereço que não é seu nunca será sugerido. Em vez disso, adicione seus outros endereços em **Configurações**, em [Seus endereços](settings.md#your-addresses).

Quando apenas o primeiro nome é igual em domínios diferentes, como "Sam" e "Sam Lee", as pessoas só são sugeridas se tiverem o mesmo número de telefone ou perfil do LinkedIn.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que tenham apenas um nome em comum não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma só vez, exceto os que você marcou como **Não é a mesma**. Use **Desfazer** logo depois para separá-los novamente.

Para associar duas pessoas manualmente, abra uma delas e escolha **⋯**, **Mesma pessoa que…** e a outra pessoa. A página da pessoa associada explica o motivo em **Associada a partir de**, com **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…** e, depois, **Excluir**. Isso remove a pessoa e tudo o que sua Machine sabe sobre ela: o registro, os endereços, os dados consultados, as mensagens que só foram trocadas entre vocês e as notas sobre ela.

As tarefas que envolvem essa pessoa continuam, mas o nome dela é removido. Ela não será adicionada novamente, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado a alguém é devolvido, o endereço aparece como **Devolvido**, com a data, e outro endereço dessa pessoa aparece primeiro. Rascunhos novos nunca são enviados para esse endereço quando há outro conhecido. Se for o único endereço, a tela de envio mostra um aviso, mas você ainda pode enviar.

Um e-mail é considerado devolvido quando o servidor de e-mail informa que o endereço não existe ou após 3 falhas temporárias durante uma semana. O aviso é removido quando a pessoa escreve novamente usando esse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço corporativo podem ter cargo, foto, LinkedIn e cidade consultados, como explicado em [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta usa apenas o nome da pessoa e o domínio da empresa. Para encontrar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Para desativar, acesse **Configurações** e, em Segurança, desative **Buscar contatos de trabalho**.

Quando a consulta encontra essas informações, a página da pessoa também mostra a descrição, desde quando ela está no cargo atual e os dois cargos anteriores. Os preparativos também usam essas informações. A descrição só é usada quando a pessoa não tem uma biografia própria.

Suas Conexões são complementadas com as informações que já foram consultadas: cargo, telefone e fuso horário do Slack; biografia e cidade do X; título e foto do LinkedIn; cargos dos Contatos do Google e do Salesflare; e a foto de um contato do Salesflare, se o próprio Salesflare tiver uma. Passe o cursor sobre a linha abaixo do nome para ver de onde veio a informação.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são adicionadas pela sincronização do WhatsApp e pela conexão com seus chats do Telegram: até 50 por dia em cada serviço, apenas de pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto de perfil de alguém que não tenha foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Team Graph](team-graph.md) de uma Fleet de Trabalho, uma pequena cópia da foto de trabalho acompanha o registro compartilhado da pessoa. Fotos dos Contatos do Google, WhatsApp, Telegram ou Facebook, além das fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, incluindo aliases, são sempre seus, nunca de alguém no seu Graph. Ao pesquisar por você ou adicionar uma pessoa com um dos seus endereços, **Sobre você** é aberto, e sua própria linha é ignorada na importação.

Sobre você lista seus endereços e informa de onde veio cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seus dados de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que você representa para alguém

As funções que sua Machine identifica nas mensagens aparecem na página da pessoa, em **Para você**, junto com a linha em que foram identificadas. Você não precisa esperar para confirmar nada. Encontrou um erro? Corrija com **Editar** na página da pessoa ou com **⋯** na linha em **Mudanças recentes**. Sua Machine aprende com as suas alterações.

## O que ela sabe sobre alguém

Os fatos sobre essa pessoa ficam na página dela, em **Informações conhecidas**. Aprendizado guarda os fatos gerais. Use **Adicionar** para incluir outro fato com suas próprias palavras. Cada fato tem um menu:

- **Editar** altera o fato ali mesmo.
- **Não é sobre essa pessoa** transforma o fato novamente em uma informação geral, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre eles: uma função, onde alguém trabalha, a relação entre duas pessoas, um fato ou a mudança de um projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Se uma linha estiver errada, use **⋯** para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre essa pessoa** ou **Desfazer** para devolver um projeto ao lugar onde estava. São exibidas três linhas. **Mostrar mais** mostra as demais.

Uma pessoa atualizada hoje pela sua Machine aparece com um ponto pequeno na lista de Pessoas, e **4 pessoas atualizadas hoje** aparece na parte de cima da lista. Veja [The Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, inicia uma tarefa sobre essa pessoa.
