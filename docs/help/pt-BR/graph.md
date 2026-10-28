---
title: O Graph
area: graph
summary: As pessoas, organizações e projetos das suas mensagens, sempre atualizados sozinhos.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, enrichment.py, dashboard.html
order: 1
---
Sua Machine monta um mapa de com quem você lida e do que está acontecendo, a partir das suas mensagens, reuniões e decisões. Não há nada para configurar, e tudo fica na sua Machine.

## Pessoas

Todo mundo com quem você tem contato, os mais próximos primeiro. A página de uma pessoa começa com a foto, o nome, o cargo, a organização e o local, e uma linha sobre como vocês se falam ("Falam todo dia · última sex, 23 out · próxima reunião ter, 27 out"). Abaixo disso:

- **Contato**: os telefones e e-mails da pessoa. Toque em um para ligar ou escrever, ou em **Copiar**.
- **Com você**: o que ela é para você, contato de Trabalho ou Pessoal, e sua Família ou seu Fleet, com **Ver no Fleet**.
- **Também em**: os outros lugares onde vocês conversam. **Slack** abre a pessoa no Slack, ou sua conversa mais recente com ela no Slack.
- **Pessoas** e **Projetos** de que ela faz parte, **Em aberto entre vocês** (promessas nos dois sentidos, com **Feito** e **Descartar**) e a **Linha do tempo** dela.

Os endereços e chats de alguém são unidos sozinhos quando fica claro que são da mesma pessoa, como um e-mail de trabalho com o endereço pessoal dela em CC.

As abas **Trabalho** e **Pessoal** listam só esses contatos. **Baixar CSV**, no menu de ordem, salva a aba em que você está como planilha, também para Organizações e Projetos.

### Linha do tempo

Toda página de pessoa e de organização tem uma, as mais recentes primeiro: e-mails, reuniões e os resumos do Zoom delas, conversas do Intercom (abertas ou fechadas, com **Abrir no Intercom**), chats do WhatsApp, Telegram, Slack, LinkedIn e X, tarefas, promessas e mudanças em projetos. Os chips no topo mostram uma fonte por vez. **Mostrar mais** carrega as mais antigas.

As reuniões que ainda vão acontecer ficam separadas no topo, em **Em breve**, as mais próximas primeiro. **Mostrar todos os próximos** mostra o resto. Uma reunião que está em mais de uma das suas agendas aparece uma vez só.

A linha do tempo de uma organização tem as mensagens das pessoas dela e as conversas do Intercom do domínio dela. Suas linhas do tempo são suas: o Graph da equipe mostra só o que suas regras de compartilhamento permitem.

Se uma página mostrar **Não foi possível carregar esta página.**, toque em **Tentar de novo**. Se continuar assim, use **Algo errado?** no fim da página.

## Filtrar e ordenar

**Filtrar**, ao lado das abas em Pessoas, Organizações e Projetos, restringe a lista por dono, tag, quadro, etapa, organização, valor, data prevista de fechamento e **Sem resposta há mais de 10 dias**. Pessoas e organizações entram pelos projetos abertos delas. Em Projetos, a lista e o quadro usam um só filtro.

Os filtros escolhidos aparecem acima da lista, com **Limpar**. O menu de ordem também ordena por **Valor** e **Data de fechamento**. Sua Machine faz a filtragem, então listas longas continuam rápidas. No celular, os filtros abrem em uma folha.

## Equipe

**Equipe**, ao lado de Meus, mostra o que seus colegas compartilham. Tem as mesmas abas, o mesmo menu de ordem e **Nova pessoa** ou **Nova organização** como em Meus. O que você adiciona é seu. **Filtrar** restringe por quem compartilhou, por organização (Pessoas) ou por estado (Projetos). Em Projetos, **Meus**, **Comigo** e **Todos** escolhem os mesmos projetos que em um quadro compartilhado.

## Dono

Em um Fleet de Trabalho, cada pessoa, organização e projeto tem um dono: **Proprietário**, em Com você, na página. É você, a menos que escolha alguém do seu Fleet de Trabalho. **Proprietário** em Filtrar mostra só os seus, na lista e no quadro. Um card no quadro mostra o nome do dono. Cada mudança aparece na linha do tempo. Um registro compartilhado com a sua equipe leva o dono junto, com as mesmas regras do resto.

## Campos e tags

Em Campos, em uma pessoa, organização ou projeto, clique em um valor para mudá-lo: **Salvar** ou Enter mantém, **Cancelar** ou Esc deixa como estava, **Remover** esvazia. **Gerenciar campos** adiciona ou remove campos: **Novo campo** adiciona um para todos daquele tipo: texto, número, data ou uma escolha de uma lista. **Remover** tira um campo de todos eles.

**+ Tag** adiciona uma tag, como VIP ou parceiro. **×** tira a tag. As tags aparecem nas listas, e **Filtrar** as encontra. Um registro compartilhado com a sua equipe leva os campos e as tags junto.

## Importar uma planilha

**Importar CSV…**, no menu de ordem de Pessoas, Organizações ou Projetos, adiciona uma planilha salva como CSV. Sua Machine adivinha qual coluna é qual pelos cabeçalhos e pelo conteúdo. Mude qualquer uma delas.

Quando seu modelo pode rodar, ele também confere as colunas, em qualquer idioma e com qualquer grafia dos cabeçalhos, com um motivo curto quando não tem certeza. Ele vê só os cabeçalhos, alguns valores por coluna e as células que as regras não conseguiram ler, na sua Machine, como em uma revisão. Sem ele, vale o palpite pelos cabeçalhos.

**Revisar**, ao lado das correções sugeridas, lista as correções fáceis como antes e depois: espaços a mais, nomes em maiúsculas, telefones no formato internacional, erros de digitação em e-mails (gmial.com), sites como domínio, datas e valores em qualquer formato ("€12k" é 12000), várias tags em uma célula, uma etapa escrita diferente da do quadro e a mesma linha duas vezes.

Desmarque um tipo ou uma linha para deixar como está. Nada é corrigido se não estiver marcado.

A prévia mostra cada linha como nova, como correspondente a uma que já está no seu Graph ou como ignorada, com o motivo. Uma correspondência é o mesmo e-mail para uma pessoa (senão, o mesmo nome na mesma organização), o mesmo site ou nome para uma organização e o mesmo nome para um projeto.

**Importar** adiciona as novas e completa as correspondentes. Uma célula vazia não muda nada. **Desfazer** logo depois, ou **Desfazer última importação** no menu de ordem, desfaz a última importação enquanto esses registros não tiverem mudado desde então. Correções feitas depois são mantidas: se Desfazer fosse sobrescrever uma, ele explica o motivo em vez disso. O arquivo fica na sua Machine.

## Uma organização, vários sites

**⋯**, **Mesma organização que…** na página de uma organização a torna parte de outra, com as pessoas, projetos e notas dela. **Adicionar um site…** adiciona mais um site dela, como o .io ao lado do .com: pessoas com um endereço lá entram nela, e os detalhes são buscados para cada site.

Eles aparecem em **Sites**, cada um com **Separar** para desfazer. Edições posteriores na organização combinada são mantidas. Organizações que parecem duplicadas aparecem em **Mesma organização?**: **Mesclar** ou **Não é a mesma**.

## Adicionar uma pessoa ou organização

**Nova pessoa** no topo de Pessoas, **Nova organização** no topo de Organizações ou, no celular, **+** na barra superior. Informe um nome e, para uma pessoa, um e-mail e uma organização, se tiver. Para uma organização, o site. Quando já existe alguém parecido no seu Graph, o formulário mostra essa pessoa primeiro, para você abrir essa em vez de criar outra. **Adicionar** abre a nova página.

Quem você adiciona fica, mesmo sem mensagens ainda. A primeira mensagem se junta a essa pessoa. Uma organização que você adicionou pode ser excluída pelo menu **⋯** enquanto não tiver ninguém nela.

## Sobre você

Seus próprios endereços e números, apelidos também, são sempre você, nunca alguém no seu Graph. Pesquisar por você mesmo, ou adicionar uma pessoa com um dos seus endereços, abre **Sobre você**, e uma importação ignora sua própria linha.

Sobre você lista seus endereços com a origem de cada um. Mude-os em **Configurações**, em Conta. Uma pessoa criada antes a partir do seu próprio endereço vai sozinha para Sobre você, com um backup guardado na sua Machine.

Para enviar seu próprio cartão a um colega ou amigo, escolha **Compartilhar meu contato**. Veja [Compartilhar um contato](share-contact.md).

## Foto

Clique na foto da página de uma pessoa ou organização para mudá-la: **Enviar uma imagem**, escolher uma encontrada para ela ou **Remover foto**. Ela fica na sua Machine.

## Notas

**Editar** na página de uma pessoa ou organização tem um campo **Notas**, para qualquer coisa que você queira lembrar. As notas aparecem na página e se mantêm quando há mesclagem.

## Editar alguém

**Editar**, no topo da página, muda o nome, o cargo, a organização, o local, o LinkedIn, os telefones e e-mails, o que a pessoa é para você e Trabalho ou Pessoal. **Salvar** mantém, **Cancelar** deixa como estava.

Suas edições ficam, mesmo quando os detalhes são buscados de novo ou uma revisão lê outra coisa, e também com **Mesclar** e **Desfazer**. Esvazie um campo para usar de novo o valor buscado. Um nome vazio traz de volta o das mensagens.

## Mesma pessoa?

Quando duas pessoas podem ser uma só, a página pergunta se são a mesma pessoa, e Pessoas lista as duas em **Mesma pessoa?**. **Mesclar** junta as duas, com todas as mensagens, notas, cargos e projetos. **Não é a mesma** mantém as duas separadas de vez.

**Mesclar todos** mescla todos os pares da lista de uma vez, menos os que você marcou como **Não é a mesma**. **Desfazer** logo depois separa todos de novo.

A página de uma pessoa unida mostra o motivo em **Unida a partir de**. **Desfazer** separa de novo.

Para unir duas pessoas você mesmo, abra uma delas, depois **⋯**, **Mesma pessoa que…** e escolha a outra.

## Cargo e foto

Pessoas com um endereço de empresa recebem cargo, foto, LinkedIn e cidade, buscados como os [detalhes de organização](organization-data.md). Em uma Machine hospedada, só o nome e o domínio da empresa são enviados. Desative em **Configurações**, em Segurança: **Buscar contatos de trabalho**.

Suas conexões completam mais coisas enquanto rodam, com o que já leem e sem pedir nada a mais: cargo, telefone e fuso horário do Slack, bio, local e site do X, título e foto do LinkedIn, e cargos dos contatos do Google e do Salesflare. O que a pessoa diz sobre si mesma vem primeiro. Passe o mouse sobre a linha abaixo do nome para ver de onde veio. Tudo fica na sua Machine.

As fotos do WhatsApp vêm pela sua sincronização do WhatsApp sempre ativa, quando ela permite: até 50 por dia, só para pessoas que já estão no seu Graph. Nada é enviado a elas.

## Excluir alguém permanentemente

Na página da pessoa, abra o menu ⋯ e escolha **Excluir permanentemente…**, depois **Excluir**. Isso remove a pessoa e o que sua Machine sabe sobre ela: o registro, os endereços, os detalhes buscados, as mensagens só entre vocês dois e as notas sobre ela. As tarefas que a envolvem ficam, com o nome dela retirado. Ela não será adicionada de novo. Não dá para desfazer.

## Quem é quem

Cargos que sua Machine leu nas suas mensagens, esperando a sua palavra. **✓ Correto** confirma um. **Editar** abre a página da pessoa em Editar. Ela aprende com as suas edições. Isso só aparece quando há cargos esperando.

## Em um Fleet de Trabalho

O trabalho com clientes é compartilhado com as Machines dos seus colegas, e o deles aparece na sua. Cada conversa mostra **Equipe** ou **Só você**. Veja [Graph da equipe](team-graph.md).

## Organizações

Empresas, a partir dos endereços e nomes nas suas mensagens. Veja [Detalhes de organização](organization-data.md).

A página de uma organização é montada como a de uma pessoa: o logo, o nome e o que ela faz, uma linha sobre como vocês se falam, depois **Contato** (o site e o LinkedIn), **Com você** (o que ela é para você), as pessoas de lá e a **Linha do tempo**.

Os **Projetos** dela listam os abertos primeiro, cada um com a etapa. As mudanças deles aparecem na linha do tempo. **Editar** no topo muda os detalhes e o que ela é para você. **Perguntar ao Fleet quem conhece** encontra um caminho até ela pelo seu Fleet.

E-mails de ferramentas de aquecimento de e-mail ficam de fora, em "Oculto como aquecimento", com **Desfazer** por domínio.

## Projetos

Nomeados pela sua Machine a partir do assunto das suas mensagens. Sinais que parecem fazer parte aparecem como "provavelmente faz parte". Renomear um projeto com o nome de outro projeto junta os dois.

Ou gerencie os projetos à mão, como negócios em um CRM:

- **Novo projeto**: no topo de um quadro, **+ Adicionar** em uma etapa, **Novo projeto** no topo da lista, **+** na barra superior no celular, ou na página de uma pessoa ou organização. Dê um nome, um quadro e uma etapa, uma organização (pesquise no seu Graph ou **Adicionar** uma nova), um valor, uma data prevista de fechamento, pessoas e notas. Projetos que já estão no seu Graph com um nome parecido aparecem primeiro.
- **Editar** na página de um projeto, ou **Editar** no **⋯** de um card no quadro (ou aperte E em um card). Muda tudo o que está acima.
- **Ganho** ou **Perdido**, com o motivo. Ganho move o projeto para a última etapa do quadro, Perdido para Parado ou recusado. **Reabrir** desfaz.
- **Arquivar** tira o projeto do quadro e das listas. Uma nova mensagem sobre ele o traz de volta. **Excluir** remove de vez. As mensagens e as pessoas ficam.
- Mova um card arrastando, ou com **⋯**, **Mover para** no celular. Sua mudança vale até uma mensagem mais nova mover o card.
- **Etapas**, no topo de um quadro, mostra só as etapas que você escolher, por quadro. **Limpar** mostra todas de novo.
- "4 sem resposta há mais de 10 dias" em uma etapa: toque para ver só esses, no quadro e na lista. Toque de novo para ver todos.

### As tarefas de um projeto

Uma tarefa pode pertencer a um projeto. Sua Machine escolhe o projeto quando a conversa da tarefa ou as pessoas de quem ela trata estão em um único projeto aberto, e a tarefa mostra o nome dele abaixo do título. **Mudar projeto** em **Mais** da tarefa, ou **Colocar em um projeto** no menu de comandos (Ctrl K), muda ou tira o projeto. Sua escolha fica.

A página de um projeto lista as tarefas em **Tarefas**, as abertas primeiro, e o card dele no quadro diz quantas estão abertas. Ligar uma tarefa a um projeto compartilhado não compartilha nada a mais: sua equipe continua vendo só o que veio de mensagens compartilhadas.

### A organização de um projeto

Cada projeto pode ser ligado a uma organização. A página, a linha e o card dele no quadro a mostram, com um link para ela.

Quando ninguém escolheu uma, sua Machine define a organização a partir das pessoas do projeto e das mensagens dele, deixando seus colegas de fora. Ela só faz isso quando uma organização é claramente o outro lado: e-mail pessoal como o Gmail nunca conta, e um projeto com várias empresas fica sem nenhuma. O formulário do projeto então diz "Pelas pessoas".

Sua escolha em **Editar** sempre fica, mesmo quando você a tira. **Mesma organização que…** leva junto os projetos de uma organização, e **Separar** os traz de volta.

### Quadros

Projetos de um tipo em etapas, como um pipeline de avaliação. **⋯** em um quadro: **Editar quadro** (nome, etapas, quais projetos fazem parte), **Abrir neste quadro** e **Novo quadro**. As revisões continuam adicionando projetos que se encaixam e os colocam em uma etapa. Quando não têm certeza, o quadro mostra "2 projetos podem fazer parte daqui": **Adicionar** ou **Deixar de fora**.

Marque alguns, ou **Selecionar tudo**, para fazer de uma vez, e **Desfazer** logo depois se mudar de ideia. Um projeto que junta várias contrapartes vira um projeto por contraparte quando você o adiciona.

**Pipeline**, no topo de um quadro, soma o valor dos projetos abertos por etapa e o que deve fechar por mês, pelas datas de fechamento. Projetos ganhos, perdidos e parados não estão abertos. O que você ganhou neste mês aparece à parte. Os valores são em euros, a menos que sua Machine esteja configurada para outra moeda. Com **Proprietário** em Filtrar, conta só os seus.

Um quadro novo, ou um quadro sugerido que você salva, passa uma vez por todo o seu histórico. Ele encontra projetos e organizações que se encaixam, cria um projeto por organização e coloca cada um em uma etapa. O cabeçalho diz "Olhando seu histórico…" enquanto trabalha, e depois quantos adicionou e quantos esperam sua revisão. Um quadro Só você guarda o que encontra só para você.

### O quadro de um colega

Em **Equipe**, os quadros que seus colegas compartilham aparecem ao lado dos seus, primeiro os que têm mais projetos seus. Cada card diz o que aconteceu por último, com a data, como no quadro do dono: a linha mais nova compartilhada com a equipe, ou então a última mudança de etapa. O nome do dono só aparece quando uma etapa tem cards de mais de um colega; se uma pessoa é dona do quadro todo, o cabeçalho diz.

**Meus**, **Comigo** e **Todos** escolhem o que um quadro compartilhado mostra, e também a lista de projetos da equipe. Meus é aquilo em que você está: uma conversa dele, um projeto que você é dono ou tem, ou uma tarefa sua sobre ele. Comigo é o que espera por você: uma tarefa aberta sobre ele, ou uma conversa em que a mensagem mais nova foi escrita para você.

O resto de uma etapa fica em **Mostrar mais N**. Projetos parecidos, como uma série de testes "… avaliação de CRM", ficam juntos em uma linha com uma contagem; toque nela para abri-los. Nada disso muda o que é compartilhado.

## Uma tarefa sobre alguém

**Nova tarefa** no menu **⋯** de uma pessoa, organização ou projeto começa uma tarefa sobre eles.

## O que ela sabe sobre alguém

Em Sabe sobre, cada fato tem um menu:

- **Esquecer** apaga o fato em todo lugar.
- Não é sobre a pessoa só tira o fato daquela página.
