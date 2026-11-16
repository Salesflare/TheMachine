---
title: Outro e-mail (IMAP)
area: connections
summary: E-mails de qualquer provedor com IMAP, como iCloud, Yahoo, Fastmail, Telenet ou seu próprio domínio.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## O que ela lê

Sua caixa de entrada e a pasta Enviados: as mensagens dos últimos 7 dias quando você conecta e, depois, todas as novas. As mensagens que você envia também contam, para que ela aprenda como você escreve e o que prometeu. Ela não lê outras pastas.

Nada é alterado na sua caixa de entrada, exceto uma cópia do que a The Machine envia, salva na pasta Enviados. As mensagens não são marcadas como lidas.

## O que ela pode fazer

Ela só envia e-mails depois que você pressiona **Enviar**, pelo servidor de e-mail do seu provedor (SMTP), usando a mesma senha. Uma cópia fica na pasta Enviados. As respostas mantêm a conversa, e sua assinatura é a que está em Configurações ou, se não houver uma, a que aparece no fim dos e-mails que você envia.

## Conectar

1. No painel, abra **Conexões**, depois **E-mail** e escolha **Outro e-mail**.
2. Digite seu endereço de e-mail e sua senha.
3. Pressione **Conectar**.

Muitos provedores exigem uma senha de app para aplicativos de e-mail, em vez da sua senha normal. Crie uma nas configurações da conta do provedor:

- iCloud: uma senha específica para apps em account.apple.com.
- Yahoo: Segurança da conta, Gerar senha de app.
- Fastmail: Configurações, Privacidade e segurança, Senhas de app.
- Telenet: sua senha normal de e-mail da Telenet.
- Zoho Mail com autenticação de dois fatores: uma senha específica para aplicativos na seção Segurança da sua conta Zoho.
- Proton Mail: execute o Proton Mail Bridge no mesmo computador e use a senha exibida pelo Bridge. Isso só funciona com a The Machine nesse mesmo computador. A The Machine mostra a impressão digital do certificado do Bridge e confia apenas nele.

As configurações do servidor são preenchidas automaticamente para a maioria dos provedores. Não encontrou as suas? Abra **Configurações do servidor** e digite os dados que seu provedor fornece para aplicativos de e-mail: os servidores IMAP e SMTP, as portas e o tipo de segurança (SSL/TLS ou STARTTLS). A The Machine nunca se conecta sem TLS.

Usa Gmail ou e-mail da Microsoft, inclusive em um domínio próprio? Escolha **Gmail** ou **Outlook**. O login é feito sem senha. Se você digitar os servidores deles em Configurações do servidor, eles também serão usados: a Microsoft não aceita mais senhas de aplicativos de e-mail.

Digitou um endereço do Microsoft 365? O formulário identifica o endereço e mostra **Entrar com a Microsoft** no lugar do campo de senha. Isso abre a página de login do Outlook. Se o endereço não for identificado em alguns segundos, o formulário de senha continua disponível.

## Quando a conexão para de funcionar

- **O servidor de e-mail recusou a senha**: você mudou a senha ou a senha de app foi removida. Conecte a conta novamente com a nova senha.
- **O servidor de e-mail recusou a senha para envio**: nada foi enviado. Conecte a conta novamente. Se o servidor continuar recusando, confira o servidor SMTP em Configurações do servidor. Até lá, ela só lê os e-mails.
- **Não foi possível alcançar o servidor de e-mail**: a The Machine tenta novamente automaticamente. Se continuar sem funcionar, confira o nome do servidor em Configurações do servidor.
- **O certificado do servidor de e-mail é de** outro nome: em hospedagens compartilhadas, o servidor costuma responder com o próprio nome. Digite o nome mostrado em Configurações do servidor. A The Machine nunca ignora a verificação do certificado.

## Remover a conta

**Conexões**, abra a conta, **Detalhes** e depois **Desconectar**. Ela para de ler os e-mails, mas o que já importou continua disponível. Remova também a senha de app no site do provedor.
