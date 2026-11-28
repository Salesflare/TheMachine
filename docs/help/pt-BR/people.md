---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: páginas, resumos e linhas do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 84312952f04b8597
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, a partir das suas mensagens e reuniões. Newsletters, recibos e outros envios não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista: **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: consulte [O Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) conta para a organização, não como pessoa, mesmo depois que você escreve para ela.

## Página de alguém

A página começa com a foto, o nome, o cargo, a organização e a localização da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversa diária · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora mesmo", "há 3 horas", "ontem" ou "há 3 dias"; contatos mais antigos aparecem como uma data. Passe o cursor sobre a data para ver a data exata. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou **Copiar**. O **Aniversário** também aparece aqui, com a fonte da informação (Contatos do Google, Google Agenda, Facebook, suas notas ou você): consulte [O Graph](graph.md#birthday).
- **Com você**: o que essa pessoa representa para você, se é um contato de Trabalho ou Pessoal e se faz parte da sua Família ou do seu Fleet, com **Ver no Fleet**.
- **Também em**: outros lugares onde vocês conversam. **Slack** abre o perfil da pessoa no Slack ou a conversa mais recente de vocês por lá.
- **Pessoas** e **Projetos** dos quais ela faz parte, **Em aberto entre vocês** (promessas dos dois lados, com **Marcar como feito** e **Descartar**) e a **Linha do tempo**.

Os endereços e chats de alguém são vinculados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em cópia. Isso também acontece quando alguém com quem você conversa marca uma ligação pelo link que você enviou e o nome da empresa ou o sobrenome corresponde.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, toque em **Algo errado?** no fim da página.

## Resumo

Algumas linhas curtas no topo da página de uma pessoa mostram o que foi decidido, pedido, planejado ou prometido, com os nomes de todos os envolvidos. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes de mostrá-la. Normalmente, isso acontece uma vez por dia; se algo relacionado à pessoa mudar, como um novo prazo ou um pedido retirado, o resumo é atualizado em algumas horas.

Uma informação vaga fica de fora. Se não houver nada específico a dizer, não há resumo. Cada linha leva à fonte: mensagens do mesmo dia aparecem juntas, com uma única data e a quantidade de mensagens, e podem ser abertas de uma só vez.

**Editar** permite escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o texto para ela.

Os preparativos para reuniões usam esse resumo, mas apenas as linhas do lado daquela tarefa (Trabalho ou Pessoal). Ele fica na sua Machine; sua equipe nunca o vê.

## Linha do tempo

Todas as páginas de pessoas e organizações têm uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e movimentações de projetos. Os filtros no topo mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no topo, em **Em breve**, da mais próxima para a mais distante. **Mostrar todos os próximos** exibe o restante. A reunião mostra quem participou, cada pessoa uma vez. As reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que suas regras de compartilhamento permitem. Em uma página, **Equipe**, acima da Linha do tempo, adiciona o que as outras pessoas da equipe compartilharam, com o nome de quem compartilhou cada item. **Meus** mostra apenas o que você compartilhou.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas pelo tipo definido na página delas. A opção que você escolhe (**Editar**) tem prioridade. Caso contrário, sua Família e seus Amigos, além de familiares ou amigos seus (como uma esposa ou um pai), são classificados como Pessoais, independentemente do endereço de onde escrevem. Sua equipe nunca vê seus contatos pessoais.

## Adicionar alguém

Toque em **Nova pessoa**, no topo de Pessoas, ou em **+**, na barra superior do celular. Informe o nome e, se souber, o e-mail e a organização. Se já houver alguém parecido no seu Graph, o formulário mostra essa pessoa primeiro para você abrir a página existente. **Adicionar** abre a nova página.

A pessoa que você adicionar continuará na lista mesmo sem mensagens. A primeira mensagem vai vinculá-la.

## Editar alguém

**Editar**, no topo da página, permite alterar o nome, cargo, organização, localização, LinkedIn, telefones e e-mails da pessoa, o que ela representa para você e se é um contato de Trabalho ou Pessoal. O campo **Notas** serve para guardar o que você quiser lembrar. As notas são mantidas mesmo quando você mescla pessoas. **Salvar** guarda as alterações; **Cancelar** descarta as alterações.

Suas alterações são mantidas mesmo quando os dados da pessoa são consultados novamente, e também ao usar **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor encontrado. Se apagar o nome, o nome das mensagens da pessoa volta a aparecer.

Para alterar a foto, clique nela e escolha **Enviar uma imagem**, selecione uma imagem encontrada para essa pessoa ou toque em **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas talvez sejam a mesma, a página delas pergunta se são a mesma pessoa, e Pessoas as mostra em **Mesma pessoa?**. **Mesclar** junta as duas, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém as páginas separadas permanentemente. Sua resposta aparece por um momento no par; depois, ele sai da lista. A lista desaparece quando não houver mais perguntas.

Uma pessoa com um endereço que apenas se parece com um endereço conhecido, como acme-corp.example e acmecorp.example, nunca é sugerida como a mesma pessoa. Só você pode atribuir uma função a ela.

Um nome sozinho nunca basta para associar duas pessoas de domínios diferentes, porque qualquer pessoa pode digitar esse nome. Dois endereços de domínios diferentes só são sugeridos quando há outro vínculo, como as mesmas pessoas ou um projeto pequeno. Um primeiro nome sozinho ("Sam" e "Sam Lee") exige mais: a mesma empresa, o mesmo número de telefone ou o mesmo perfil do LinkedIn.

Alguém que usa seu nome em um endereço que não é seu nunca é sugerido. Em vez disso, adicione seus outros endereços em **Configurações**, em [Seus endereços](settings.md#your-addresses).

Quando só o primeiro nome coincide em domínios diferentes, como "Sam" e "Sam Lee", as pessoas só são sugeridas se tiverem o mesmo número de telefone ou perfil do LinkedIn.

Se apenas o primeiro nome coincidir com o de alguém de uma reunião marcada a partir de um chat, ou se o endereço for de alguém que você já conhecia e só a pessoa no chat disser que é dela, você será perguntado. The Machine nunca abre um link para descobrir.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e uma conversa pessoal com apenas um nome em comum não são associados automaticamente: eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma só vez, exceto aqueles que você marcou como **Não é a mesma**. **Desfazer** separa todos eles novamente se você fizer isso logo depois.

Para juntar duas pessoas por conta própria, abra uma delas, toque em **⋯**, escolha **Mesma pessoa que…** e selecione a outra. A página da pessoa mesclada mostra o motivo em **Mesclada a partir de**, com a opção **Desfazer** para separá-las novamente.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Depois, toque em **Excluir**. Isso remove a pessoa e o que sua Machine sabe sobre ela: o perfil, os endereços, os dados encontrados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas relacionadas à pessoa continuam, mas o nome é removido. Ela não será adicionada novamente, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado a alguém é devolvido, o endereço aparece como **Não entregue**, com a data, e outro endereço da pessoa passa a ser o principal. Rascunhos novos nunca são enviados para esse endereço quando outro é conhecido. Se for o único endereço, a tela de envio avisa você, mas ainda é possível enviar.

Um e-mail é considerado devolvido quando o servidor de e-mail informa que o endereço não existe ou depois de 3 falhas temporárias ao longo de uma semana. O aviso desaparece quando a pessoa escreve novamente desse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço corporativo recebem um cargo, uma foto, informações do LinkedIn e a cidade, consultados como os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para obter uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o endereço em si. Desative essa opção em **Configurações**, na seção Segurança: **Buscar contatos de trabalho**.

Essa opção também impede a leitura do site antes da primeira reunião e a busca na web (consulte [Pronta para suas reuniões](calendar.md#ready-for-your-meetings)).

Quando a consulta encontra informações sobre a pessoa, a página também mostra o texto "Sobre", desde quando ela está no cargo atual e os dois cargos anteriores. Os preparativos também usam essas informações. O texto "Sobre" só é usado quando a pessoa não tem uma biografia própria.

Suas Conexões ficam mais completas com informações que já foram consultadas: cargo, telefone e fuso horário do Slack; biografia e localização do X; título e foto do LinkedIn; cargos dos Contatos do Google e do Salesflare; e a foto de um contato do Salesflare, se o próprio Salesflare tiver uma. Passe o cursor sobre a linha abaixo do nome para ver de onde veio a informação.

O Outlook adiciona as fotos dos colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram vêm da sincronização do WhatsApp e da conexão com seus chats do Telegram: até 50 por dia em cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém que ainda não tem foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de um Fleet de Trabalho, uma cópia pequena da foto de trabalho acompanha o registro compartilhado da pessoa. Fotos dos Contatos do Google, WhatsApp, Telegram ou Facebook, além de fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus endereços e números, incluindo aliases, são sempre seus e nunca correspondem a alguém no seu Graph. Ao buscar por você ou adicionar uma pessoa com um dos seus endereços, **Sobre você** é aberta, e uma importação ignora seu próprio registro.

Sobre você lista seus endereços e a origem de cada um. Altere-os em **Configurações**, na seção Conta. Para enviar seu contato a um colega de equipe ou amigo, escolha **Compartilhar meu contato**. Consulte [Compartilhar um contato](share-contact.md).

## O que essa pessoa representa para você

As funções que sua Machine identifica nas suas mensagens aparecem na página da pessoa, em **Para você**, com apenas as palavras que indicam a função, como um cargo. Alguém dizer que é seu contador ou cliente não basta: isso também precisa aparecer do seu lado, por exemplo, em mensagens suas ou em reuniões com essa pessoa. Não é preciso esperar você confirmar. Se algo estiver errado, use **Editar** na página da pessoa ou **⋯** na linha correspondente em **Mudanças recentes**. A Machine aprende com suas alterações.

## O que a Machine sabe sobre alguém

As informações sobre a pessoa ficam na página dela, em **Informações conhecidas**. O **Aprendizado** guarda as informações gerais. **Adicionar** inclui outra informação com suas próprias palavras. Cada item tem um menu:

- **Editar** altera a informação ali mesmo.
- **Não é sobre** essa pessoa transforma a informação novamente em geral, em **Aprendizado**, **Fatos**.
- **Remover** exclui a informação de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhidas logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre ela: uma função, onde alguém trabalha, a relação entre duas pessoas, uma informação ou uma mudança de projeto. Cada linha mostra a data e a fonte. Toque na fonte para ler a mensagem.

Quando uma linha está errada, **⋯** permite corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** essa pessoa ou **Desfazer** para colocar um projeto de volta onde estava. São mostradas três linhas; **Mostrar mais** exibe o restante.

Uma pessoa cujas informações foram atualizadas pela sua Machine hoje tem um ponto ao lado do nome na lista Pessoas, e **4 pessoas atualizadas hoje** aparece no topo da lista com os nomes. Consulte [O Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, cria uma tarefa sobre ela.
