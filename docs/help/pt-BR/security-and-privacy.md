---
title: Segurança e privacidade
area: security
summary: Sua Machine privada, e-mails armazenados com criptografia e nada é enviado sem sua aprovação. O resumo, com links.
covers:
code: message_seal.py, next_actions.py, SECURITY.md
order: 1
keywords: private, privacy, data, gdpr, encrypted, who can see, safe, stored, keep
translated: 27c910c92b215ad3
---
## Em resumo

- Sua própria Machine: uma Machine hospedada funciona na nuvem da UE, só para você, nunca é compartilhada. Ou use a Machine no seu próprio computador.
- Não lemos seus e-mails: as mensagens são armazenadas com criptografia, e nossas ferramentas de suporte não conseguem abri-las.
- Nada é enviado sem sua aprovação: ela lê e prepara rascunhos, mas você decide o que é enviado. Veja [Fazer](do-it.md).
- Seus dados não são usados para treinar IA: não temos uma IA própria. Seu provedor funciona na sua conta e segue os termos dele.
- Aprendizados para a equipe, a menos que você desative o compartilhamento: de vez em quando, algumas dicas gerais, nada pessoal, revisadas antes de serem enviadas. Veja [Compartilhar aprendizados](share-learnings.md).
- Relatórios de erro, a menos que você desative o envio: quando algo dá errado, enviamos o tipo de erro e o local no código. Nunca suas mensagens, nomes ou endereços. Veja [Relatórios de erro](error-reports.md).
- Contagens de uso em uma Machine hospedada: contagens diárias do que você fez, como tarefas abertas ou e-mails enviados, nunca o conteúdo, e o tempo que o painel leva para abrir, medido apenas por celular ou computador, app ou navegador.
- Leve seus dados com você ou exclua-os: exporte tudo em **Configurações** › **Geral**, ou exclua sua Machine e os backups dela com um botão. Veja [Cancelar ou excluir](cancel-and-delete.md).
- Nosso acesso é registrado: sempre que alguém da nossa equipe consulta o relatório ou os registros da sua Machine hospedada. Os donos e admins de Fleets podem ver isso em **Atividade**. Veja [Fleets](fleet.md).

## Backups

Uma Machine hospedada faz backup dos seus dados todas as noites. O backup é criptografado na sua Machine antes de sair dela e armazenado no Microsoft Azure, na Holanda (UE). Mantemos os últimos 7 backups diários, 4 semanais e 3 mensais, ou seja, cerca de 3 meses. Eles são excluídos quando sua Machine é excluída.

Podemos acessá-los? Sim, para restaurar uma Machine que parou de funcionar: mantemos a chave separada dos backups. As mensagens no backup são criptografadas mais uma vez, com uma segunda chave que também mantemos, guardada em segurança e nunca incluída no backup.

Eles são uma rede de segurança. Por isso, mantenha sua própria cópia do que não pode perder: **Tudo**, em **Configurações** › **Geral** › **Exportar**. Veja [Mudar para outro computador](moving.md).

No seu próprio computador, nada é copiado automaticamente e não temos uma cópia. Basta fazer um backup criptografado todas as noites da sua pasta pessoal: veja [Primeiros passos](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md#later).

## Níveis de segurança

**Padrão** mantém as configurações padrão de hoje. **Cuidadoso** não mostra texto nas notificações, não salva dados de acesso e guarda menos informações. O admin de um Fleet de Trabalho pode definir o Fleet como Cuidadoso. Veja [Níveis de segurança](security-levels.md).

## Acesso

Para acessar um painel hospedado, você precisa de uma chave de acesso ou de entrar com Google ou Microsoft e usar um código do app autenticador.

## Conexões

O artigo de cada conexão explica o que ela lê e o que pode enviar. Você pode desconectar qualquer uma a qualquer momento: veja [Conexões](connections.md).

## Ajuda

A ajuda funciona na sua própria Machine e não consegue ver seus dados. Só o assunto de cada pergunta é enviado à equipe da The Machine, nunca o que você escreveu. Veja [Pergunte à Ajuda](help-chat.md#what-the-team-sees).

## Mais informações

- [Segurança](/security): como o sistema foi desenvolvido, o que nossa equipe pode ou não ver e como procuramos problemas.
- [Aviso de privacidade](/privacy) e [termos de processamento de dados](/dpa).
- Encontrou um problema de segurança? Veja a [política de segurança](https://github.com/Salesflare/TheMachine/blob/main/SECURITY.md).
