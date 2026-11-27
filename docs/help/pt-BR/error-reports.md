---
title: Relatórios de erro
area: security
summary: Quando algo dá errado, sua Machine conta à equipe da The Machine o que falhou e onde no código. Nunca envia suas mensagens, nomes ou endereços.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: d474cfa6bcefd25a
---
## O que é

Quando algo dá errado na The Machine, sua Machine envia à nossa equipe uma nota breve e anônima sobre o erro, para que possamos corrigi-lo antes que alguém o relate. O envio fica ativado por padrão e requer a [The Machine Network](/network).

## O que é enviado

Somente estas informações, para cada tipo de erro:

- o tipo de erro, como `KeyError`;
- a mensagem, sem informações específicas: números, IDs, trechos entre aspas, endereços de e-mail, links, caminhos de arquivos, chaves e qualquer palavra que possa ser um nome;
- onde o erro aconteceu no próprio código da The Machine, nunca em uma pasta do seu computador;
- a versão do app, quantas vezes aconteceu e quando aconteceu pela primeira e pela última vez.

Por exemplo: `IndexError`, `list index out of range`, em `machine/faults.py:fault_event:246`, versão `05b17ee6ac79`, 1 vez.

## O que nunca é enviado

O conteúdo das suas mensagens, tarefas, rascunhos ou chats. Nomes, endereços de e-mail, números de telefone, links ou senhas. Nem a conta ou a pessoa envolvida.

## De onde vêm os erros

- tarefas em segundo plano: verificações de novas mensagens, preparação de tarefas, chats, conexões e sincronizações;
- o painel, no navegador ou no app, incluindo erros exibidos para você;
- solicitações do painel que falham ou atingem o tempo limite: qual solicitação, nunca o que ela enviou;
- tarefas de agentes de programação que falham: somente a ferramenta e o tipo de falha;
- o teste rápido da sua IA quando falha: o erro da IA, sem informações específicas.

Uma verificação interrompida porque você atingiu o limite de uso do plano da sua IA não é um erro e não é enviada: ela aguarda a redefinição do limite. O mesmo vale para uma verificação que falhou porque você saiu da sua IA: **Precisa de você** pede que você entre novamente.

Um conector que você adicionou por conta própria (seu próprio arquivo em `connectors/`) envia somente o nome do serviço e o rótulo do erro, como `notes` e `notes_http: HTTP unauthorized`, para que possamos ajudar a corrigi-lo. Nada mais do código é enviado. O cartão da conexão mostra o erro completo.

Erros repetidos são contabilizados, mas não são enviados novamente. No máximo, um lote é enviado a cada 10 minutos. Mantemos os dados por 30 dias.

## Controle de ritmo

As tarefas em segundo plano aguardam quando os limites do plano da sua IA estão quase no fim, para deixar espaço para seus próprios chats (veja [Seu modelo de IA](model.md)).

Com os relatórios de erro ativados, sua Machine também nos informa uma vez por dia com que frequência isso aconteceu: para cada pausa, a hora, qual limite foi atingido, quanto tempo durou e quantas tarefas aguardaram. Nenhuma informação sobre o conteúdo das tarefas é enviada.

## Desativar

Em **Configurações**, **Segurança**, desative **Enviar relatórios de erro**. Nada mais será registrado ou enviado, e o que estiver aguardando será excluído. Os erros ainda aparecem na sua própria Machine, que pode oferecer uma solução.

Veja [Segurança e privacidade](security-and-privacy.md).
