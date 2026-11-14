---
title: Pessoas
area: graph
summary: Todas as pessoas com quem você mantém contato: perfil, resumo e linha do tempo, além de como adicionar, editar, mesclar ou excluir alguém.
code: graph.py, crm.py, bounces.py, enrichment.py, record_log.py, dashboard.html
order: 2
translated: 97ffaf9944299a8b
---
Todas as pessoas com quem você mantém contato, começando pelas mais próximas, com base nas suas mensagens e reuniões. Newsletters, recibos e outros e-mails enviados em massa não adicionam ninguém até você responder. Eles ficam em Remetentes ocultos, abaixo da lista. **Mostrar como pessoa** adiciona alguém à lista. Os campos, as tags e a importação funcionam da mesma forma nas três listas, e cada lista tem seus próprios filtros: veja [Graph](graph.md).

Uma caixa de entrada compartilhada (info@, atendimento ao cliente, o nome de uma loja) é vinculada à organização, não a uma pessoa, mesmo depois que você escreve para ela.

## Perfil de alguém

No início, aparecem a foto, o nome, o cargo, a organização e o local da pessoa, além de uma linha sobre como vocês mantêm contato ("Conversa diária · último contato ontem · próxima reunião ter., 27 de out."). O contato recente aparece como "agora", "há 3 horas", "ontem" ou "há 3 dias"; contatos mais antigos aparecem com a data. Passe o cursor sobre a data para ver o dia exato. Abaixo, você encontra:

- **Contato**: telefones e e-mails da pessoa. Toque em um deles para ligar ou escrever, ou em **Copiar**. O **Aniversário** também aparece aqui, com a indicação da origem (Google Contacts, Google Calendar, Facebook ou você): veja [Graph](graph.md#birthday).
- **Com você**: o que a pessoa representa para você, se é um contato de Trabalho ou Pessoal, e sua Família ou Fleet, com **Ver no Fleet**.
- **Também em**: os outros lugares onde você conversa com essa pessoa. **Slack** abre o perfil dela no Slack ou a conversa mais recente de vocês no Slack.
- **Pessoas** e **Projetos** dos quais ela faz parte, o que está **Em aberto entre vocês** (promessas nos dois sentidos, com **Marcar como feita** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de alguém são associados automaticamente quando fica claro que pertencem à mesma pessoa, como um e-mail de trabalho com o próprio endereço da pessoa em cópia.

Se aparecer **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se a mensagem continuar aparecendo, toque em **Algo errado?** na parte inferior da página.

## Resumo

Algumas linhas curtas no início do perfil de alguém: o que foi decidido, pedido, planejado ou prometido, com o nome de todas as pessoas envolvidas. The Machine reescreve o resumo quando há novidades, apenas para pessoas com quem você realmente mantém contato, e verifica cada linha antes. Em geral, isso acontece uma vez por dia, ou em poucas horas quando algo muda, como um novo prazo ou um pedido retirado.

Uma informação vaga fica de fora. Se não houver nada específico para dizer, não há resumo. Cada linha leva à origem: mensagens do mesmo dia aparecem juntas, com uma única data e a quantidade de mensagens, e podem ser abertas juntas.

Toque em **Editar** para escrever do seu jeito. Quando há novidades, The Machine mostra uma **Atualização sugerida**, com as opções **Usar** e **Manter a minha**. **Deixar The Machine escrever** devolve o resumo para ela.

As preparações para reuniões usam o resumo, mas só as linhas relacionadas ao tipo daquela tarefa, Trabalho ou Pessoal. Ele fica na sua Machine. Sua equipe nunca vê o resumo.

## Linha do tempo

Toda página de pessoa ou organização tem uma linha do tempo, da mais recente para a mais antiga: e-mails, reuniões e os respectivos resumos do Zoom, conversas do Intercom (com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os filtros na parte de cima mostram uma fonte por vez. **Mostrar mais** carrega itens mais antigos.

As próximas reuniões aparecem no início, em **Em breve**, começando pela mais próxima. **Mostrar todos os próximos** mostra as demais. Cada reunião mostra quem participou, com cada pessoa listada uma única vez. Reuniões com notas ou transcrição mostram **Notas** ou **Transcrição**. Clique para ler.

Suas linhas do tempo são só suas: o Graph da equipe mostra apenas o que as suas regras de compartilhamento permitem. Em uma página, **Equipe**, acima da linha do tempo, mostra o que seus colegas compartilharam, com a indicação de quem compartilhou cada item. **Meus** mostra apenas o que é seu.

## Trabalho e Pessoal

As abas **Trabalho** e **Pessoal** listam as pessoas de acordo com o Tipo indicado no perfil. A opção que você escolhe (**Editar**) tem prioridade. Caso contrário, sua Família e seus Amigos, além de familiares ou amigos que você tem (como uma esposa ou um pai), são classificados como Pessoal, independentemente do endereço usado para escrever. Sua equipe nunca tem acesso aos contatos pessoais.

## Adicionar alguém

Toque em **Nova pessoa**, na parte de cima de Pessoas, ou em **+**, na barra superior do celular. Informe um nome e, se tiver, um e-mail e uma organização. Se alguém parecido já estiver no seu Graph, o formulário mostra essa pessoa primeiro para você abrir o perfil existente. Toque em **Adicionar** para abrir o novo perfil.

A pessoa que você adicionar fica salva, mesmo que ainda não haja mensagens. A primeira mensagem recebida será associada a ela.

## Editar alguém

A opção **Editar**, na parte de cima do perfil, permite mudar o nome, o cargo, a organização, o local, o LinkedIn, os telefones e os e-mails da pessoa, além de como ela se relaciona com você e se é de Trabalho ou Pessoal. O campo **Notas** serve para registrar o que você quiser lembrar. As notas são mantidas após mesclar perfis. Toque em **Salvar** para guardar as alterações ou em **Cancelar** para descartá-las.

Suas alterações são mantidas, inclusive quando os dados da pessoa são consultados novamente, e também após **Mesclar** e **Desfazer**. Apague o conteúdo de um campo para voltar a usar o valor consultado. Se apagar o nome, o nome usado nas mensagens da pessoa será restaurado.

Para mudar a foto, clique nela e escolha **Enviar uma imagem**, selecione uma foto encontrada para a pessoa ou toque em **Remover foto**. A foto fica na sua Machine.

## Mesclar duas pessoas

Quando duas pessoas podem ser a mesma, o perfil pergunta se são a mesma pessoa, e Pessoas as lista em **Mesma pessoa?**. **Mesclar** une os perfis, incluindo todas as mensagens, notas, funções e projetos. **Não é a mesma** mantém os perfis separados. Sua resposta aparece por um momento no par, que depois sai da lista. A lista desaparece quando não houver mais nada para perguntar.

Alguém com um endereço que apenas se parece com o de uma pessoa conhecida, como acme-corp.example e acmecorp.example, nunca será sugerido como a mesma pessoa. Só você pode atribuir uma função a essa pessoa.

Um endereço compartilhado, como info@ ou uma lista de e-mails, nunca é associado às pessoas que escrevem por ele. Um contato de trabalho de fora da sua empresa e um chat pessoal que só têm um nome em comum também não são associados automaticamente. Eles aparecem como uma pergunta.

**Mesclar todos** mescla todos os pares da lista de uma só vez, exceto os que você marcou como **Não é a mesma**. Toque em **Desfazer** logo depois para separar todos de novo.

Para associar duas pessoas por conta própria, abra um dos perfis e toque em **⋯**, **Mesma pessoa que…** e escolha a outra pessoa. O perfil de uma pessoa mesclada mostra o motivo em **Mesclado de**, com a opção **Desfazer** para separar os perfis novamente.

## Excluir alguém permanentemente

No perfil da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**. Depois, toque em **Excluir**. Isso remove a pessoa e tudo o que sua Machine sabe sobre ela: o perfil, os endereços, os dados consultados, as mensagens trocadas apenas entre vocês e as notas sobre ela.

As tarefas relacionadas à pessoa continuam, mas o nome dela é removido. Ela não será adicionada de novo, nem por uma importação ou por uma tarefa de aniversários do Facebook com o nome ou endereço dela. Não é possível desfazer essa ação.

## E-mail devolvido

Quando um e-mail enviado para alguém é devolvido, o endereço aparece como **Não entregue**, com a data, e outro endereço da pessoa aparece primeiro. Rascunhos novos nunca são enviados para esse endereço se outro estiver disponível. Se for o único endereço, a tela de envio avisa, mas você ainda pode enviar.

Um e-mail é considerado devolvido quando o servidor de e-mail informa que o endereço não existe, ou após 3 falhas temporárias ao longo de uma semana. O aviso desaparece quando a pessoa escreve novamente usando esse endereço ou quando um e-mail enviado para ele é entregue.

## Cargo e foto

Pessoas com um endereço de e-mail da empresa têm cargo, foto, LinkedIn e cidade consultados da mesma forma que os [dados da organização](organization-data.md). Em uma Machine hospedada, a consulta recebe apenas o nome da pessoa e o domínio da empresa. Para buscar uma foto, o Gravatar recebe um hash do endereço de trabalho, nunca o próprio endereço. Para desativar essa opção, abra **Configurações** e, em Segurança, desative **Buscar contatos de trabalho**.

Quando a consulta encontra informações sobre a pessoa, o perfil também mostra o texto de apresentação, desde quando ela ocupa o cargo atual e os dois cargos anteriores. As preparações também usam essas informações. O texto de apresentação só é usado quando a pessoa não tem uma biografia própria.

Suas conexões ficam mais completas com informações que já foram lidas: cargo, telefone e fuso horário do Slack; biografia e local do X; título e foto do LinkedIn; cargos do Google Contacts e do Salesflare; e foto de um contato do Salesflare, quando o próprio serviço mantém uma. Passe o cursor sobre a linha abaixo do nome para ver de onde veio cada informação.

O Outlook adiciona fotos de colegas da sua organização e dos seus contatos do Outlook, além dos cargos e das empresas dos seus contatos ([Microsoft](microsoft.md#photos-of-colleagues-and-contacts)).

As fotos do WhatsApp e do Telegram são obtidas pela sincronização do WhatsApp e pela conexão de chats do Telegram: até 50 por dia de cada serviço, apenas para pessoas que já estão no seu Graph. Nada é enviado a elas. Uma importação de aniversários do Facebook adiciona a foto do perfil de alguém que ainda não tem foto quando você salva a importação ([Rotinas](routines.md)). Tudo fica na sua Machine.

No [Graph da equipe](team-graph.md) de um Fleet de Trabalho, uma cópia pequena da foto de trabalho acompanha o registro compartilhado da pessoa. Fotos dos contatos do Google, WhatsApp, Telegram ou Facebook, além das fotos que você alterou ou removeu, nunca são compartilhadas.

## Sobre você

Seus próprios endereços e números, inclusive aliases, são sempre seus, nunca de alguém no seu Graph. Se você pesquisar por si mesmo ou adicionar uma pessoa com um dos seus endereços, **Sobre você** será aberto. Uma importação também ignora a sua própria linha.

A página Sobre você lista seus endereços e a origem de cada um. Para alterá-los, abra **Configurações** e acesse Conta. Para enviar seus dados de contato a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## O que a pessoa representa para você

As relações identificadas pela sua Machine nas mensagens aparecem no perfil, em **Para você**, junto com a linha que ela identificou. Não é preciso esperar sua confirmação. Se algo estiver errado, corrija em **Editar**, no perfil, ou em **⋯**, na linha correspondente em **Mudanças recentes**. A Machine aprende com as suas alterações.

## O que ela sabe sobre alguém

Os fatos sobre uma pessoa aparecem no perfil, em **Informações conhecidas**. O Aprendizado guarda os fatos gerais. Toque em **Adicionar** para incluir outro fato com as suas próprias palavras. Cada fato tem um menu:

- **Editar** altera o fato ali mesmo.
- **Não é sobre** essa pessoa transforma o fato em uma informação geral de novo, em **Aprendizado**, **Fatos**.
- **Remover** exclui o fato de todos os lugares.

## Mudanças recentes

**Mudanças recentes**, recolhido logo acima da linha do tempo de uma pessoa, organização ou projeto, lista o que sua Machine alterou ou aprendeu sobre ela: uma relação, onde alguém trabalha, como duas pessoas se relacionam, um fato ou uma mudança de projeto. Cada linha mostra a data e a origem. Toque na origem para ler a mensagem.

Se uma informação estiver errada, toque em **⋯** na linha para corrigi-la ali mesmo: **Editar**, **Remover**, **Não é sobre** essa pessoa ou **Desfazer**, para devolver um projeto ao estado anterior. Três linhas são exibidas. Toque em **Mostrar mais** para ver o restante.

Uma pessoa atualizada pela sua Machine hoje aparece com um pequeno ponto na lista Pessoas, e **4 pessoas atualizadas hoje**, na parte de cima da lista, mostra quem são. Veja [Graph](graph.md).

## Uma tarefa sobre alguém

**Nova tarefa**, no menu **⋯** de uma pessoa, organização ou projeto, inicia uma tarefa sobre ela.
