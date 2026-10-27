---
title: Configurações
area: settings
summary: Onde encontrar cada configuração, do modo claro à segurança e à sua conta.
covers: settings:general
code: dashboard.html
order: 1
---
Abra **Configurações** pela engrenagem no topo. As abas:

- **Conta**: **Seus endereços**, os que contam como você, com a origem de cada um. Seu plano em resumo, botões para as páginas da sua conta e **Sair**. Veja [Planos e cobrança](plans-and-billing.md).
- **Geral**: idioma e região, este dispositivo, o navegador da sua Machine, seu Fleet e sua conta.
- **Segurança**: Padrão ou Cuidadoso, e as configurações que cada um define. Veja [Níveis de segurança](security-levels.md). Também **Acesso de suporte**, enquanto está ativo: veja [Obter suporte](get-support.md#support-access).
- **Notificações**: o que chega até você e onde, e o seu horário de trabalho. Veja [Notificações](notifications.md) e [Horário de trabalho](work-hours.md).
- **Escrita**: assinaturas e como você escreve. Veja [Escrita](writing.md).
- **Habilidades**: instruções que a sua Machine segue. Veja [Habilidades](skills.md).
- **Modelo**: o que responde por você, e os limites dele. Veja [Modelo](model.md). Também **Codex e Claude Code**: veja [Passar para o Claude Code ou o Codex](hand-to-agent.md).

Uma aba sem nada para mostrar fica escondida.

## Geral

- **Idioma e região**: a sua **Região** define como as datas aparecem (Oct 24 ou 24 Oct) e o relógio de costume. **Formato de hora** escolhe 12 horas (2:05 PM) ou 24 horas (14:05). Tarefas, Telegram, o resumo e as mensagens do Fleet seguem essa escolha. Uma Machine hospedada começa com o país do fuso horário que você escolheu ao criar a conta. Horários como "há 3 horas" e números também seguem essa escolha.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano ou Português (Brasil). Na primeira vez que você abre o painel, ele usa o idioma do seu navegador, se for um desses (português de Portugal recebe português do Brasil por enquanto). O painel, as datas, as mensagens do Telegram, as notificações, o resumo semanal e as notas e títulos de tarefas que a sua Machine escreve para você seguem o idioma a partir do momento em que você escolhe. O que já foi escrito fica como estava. As perguntas do Fleet e da família aparecem no idioma de cada pessoa. Rascunhos para outras pessoas ficam no idioma da conversa. A Ajuda e as páginas dela também seguem essa escolha.
- **Este dispositivo**: o app (**Instalar app**), **Notificações** com **Enviar um teste**, e **Modo claro**, só para este navegador ou celular. Veja [Instalar o app e ativar notificações](phone-app.md).
- **Abrir o navegador da Machine ↗**: o navegador que a sua Machine usa para sites como o LinkedIn.
- **Regras do Fleet**: veja [Regras de compartilhamento](sharing-rules.md).
- **Conta**: **Abrir conta** e **Sair**, em uma Machine hospedada.

## Nesta Machine

Algumas configurações ficam no computador onde a sua Machine roda, não no app:

- `config.json`: todas as configurações, em um arquivo. Reinicie a Machine depois de uma mudança.
- `assistant connect`: adiciona uma fonte, como `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off`: mensagens no Telegram. Veja [Telegram](telegram.md).
- `assistant doctor`: verifica tudo e mostra uma solução para cada problema.

## Seus endereços

Cada endereço seu que a Machine encontrou: suas contas, aliases do Gmail ou do Outlook, seu calendário, seu perfil no Slack e no Intercom. E-mails e reuniões de qualquer um deles aparecem como você. Use **Remover** para tirar um que não é seu.

Um endereço compartilhado, como info@ ou um Google Group, nunca conta sozinho. Um endereço do qual a Machine não tem certeza fica em **Talvez seus**, e nada é escolhido por você. Escolha um:

- **Meu: só eu respondo**: conta como seu. E-mails para ele podem virar suas tarefas.
- **Da equipe: outros também respondem**: não é você. E-mails que só foram para ele não criam tarefas nem rascunhos para você. Ele continua alimentando o Graph, compartilhado com sua equipe como antes.
- **Não é meu**: não conta como seu.

Escolha por quem responde hoje. Uma caixa da equipe como support@ é da equipe. Um endereço como partnerships@ que agora só você responde é seu; mude para a equipe quando outros também responderem.

**Mudar** na linha dele troca isso depois. Seu próprio endereço de login é sempre seu.

### Domínios da sua empresa

Os domínios dos seus próprios endereços contam como os da sua empresa. Se ela usa outro, como acme.co ao lado de acme.com, digite em **Domínios da sua empresa** e toque em **Adicionar**.

Quem está lá passa a ser seu colega, nunca cliente: as conversas ficam fora do Team Graph como qualquer conversa só entre colegas, e nenhuma organização é criada. **Remover** tira de novo. Um domínio de e-mail gratuito como gmail.com não pode ser adicionado.
