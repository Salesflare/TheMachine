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
3. Deixe **Incluir o relatório de suporte** ativado, a menos que prefira não incluir: versões, verificações e erros recentes, sem mensagens, chaves ou endereços.
   Se pudermos precisar olhar mais de perto, marque também **Deixe o suporte olhar por 24 horas**. Veja [Acesso de suporte](get-support.md#support-access).
4. Toque em **Revisar**. Aparece tudo o que vai ser enviado, exatamente como vai.
5. Toque em **Enviar**. Nada é enviado antes disso.

Respondemos por e-mail. Uma Machine auto-hospedada pode enviar um relatório quando está na Network. Se não estiver, escreva para nós.

Se um relatório não puder sair na hora (você está offline ou enviou muitos em pouco tempo), ele não se perde. A sua Machine guarda o relatório, avisa quando ele vai sair e envia sozinha. Relatórios que ainda estão esperando aparecem em **Aguardando envio**.

## Acesso de suporte

Nossa equipe pode olhar a sua Machine por você, mas só depois que você permitir. Quando você relatar um bug, marque **Deixe o suporte olhar por 24 horas**. Ele é ativado quando você toca em **Enviar**. No seu próprio computador, a sua Machine precisa estar [pareada com a sua conta](friends.md).

- Só leitura: logs, configurações, versões, como cada conexão sincroniza e erros recentes, limpos como no relatório de suporte. Nunca suas mensagens, chaves, senhas ou quem são seus contatos.
- Termina sozinho depois de 24 horas. Enquanto está ativo, **Configurações**, **Segurança** mostra o acesso: **Desativar** termina agora.
- Cada acesso aparece listado ali, com a hora.

## No seu próprio computador

Execute `assistant support-bundle`. Ele salva um arquivo com versões, as verificações do `assistant doctor`, logs recentes e suas configurações, sem chaves, tokens, senhas ou endereços. Dê uma olhada e depois envie para quem estiver ajudando você.

Para um bug no app de código aberto, abra uma issue no [GitHub](https://github.com/Salesflare/TheMachine/issues), só com dados inventados.
