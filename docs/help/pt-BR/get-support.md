---
title: Obter suporte
area: troubleshooting
summary: Relate um bug pelo seu painel, escreva para nós ou deixe nossa equipe olhar sua Machine por um dia.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
---
## Escreva para nós

Mande um e-mail para support@themachine.computer. Uma pessoa responde.

Em uma Machine hospedada, o rodapé do painel tem "Algo errado?", que abre o formulário **Relatar um problema** da sua conta.

## Relatar um bug

Abra **Ajuda** e depois **Relatar um bug**. Uma mensagem de erro também tem um botão **Relatar um bug**.

1. Diga o que deu errado.
2. Adicione uma captura de tela, se ajudar: **Tirar uma captura de tela** do painel, ou **Anexar uma imagem**.
3. Deixe **Incluir um relatório de suporte** ativado, a menos que prefira não incluir. Ele adiciona versões, verificações e erros recentes, sem mensagens, chaves ou endereços, e deixa nossa equipe ler os logs e as configurações da sua Machine por 24 horas. Veja [Acesso de suporte](get-support.md#support-access). Desmarcado, só vão o que você escreveu e o seu screenshot.
4. Toque em **Enviar**. O formulário fecha na hora. A sua Machine adiciona o relatório de suporte sozinha; uma verificação lenta nunca segura o seu relato.

A partir daí é com a gente. Uma Machine auto-hospedada pode enviar um relatório quando está na Network. Se não estiver, escreva para nós.

Quando corrigimos um bug que você relatou e sua Machine já tem a correção, avisamos uma vez: uma linha curta no seu painel (**Entendi** fecha) e um e-mail curto. Uma Machine auto-hospedada fica sabendo quando está na Network.

Se um relatório não puder sair na hora (você está offline ou enviou muitos em pouco tempo), ele não se perde. A sua Machine guarda o relatório, avisa quando ele vai sair e envia sozinha. Relatórios que ainda estão esperando aparecem em **Aguardando envio**.

## Acesso de suporte

Nossa equipe pode olhar a sua Machine por você, mas só depois que você permitir. Quando você relata um bug com **Incluir um relatório de suporte** ativado, ele é ativado quando você toca em **Enviar**. No seu próprio computador, a sua Machine precisa estar [pareada com a sua conta](friends.md).

- Só leitura: logs, configurações, versões, como cada conexão sincroniza e erros recentes, limpos como no relatório de suporte. Nunca suas mensagens, chaves, senhas ou quem são seus contatos.
- Termina sozinho depois de 24 horas. Enquanto está ativo, **Configurações**, **Segurança** mostra o acesso: **Desativar** termina agora.
- Cada acesso aparece em Configurações, **Atividade**, com a hora. Veja [Atividade](activity.md).

## No seu próprio computador

Execute `assistant support-bundle`. Ele salva um arquivo com versões, as verificações do `assistant doctor`, logs recentes e suas configurações, sem chaves, tokens, senhas ou endereços. Dê uma olhada e depois envie para quem estiver ajudando você.

Para um bug no app de código aberto, abra uma issue no [GitHub](https://github.com/Salesflare/TheMachine/issues), só com dados inventados.
