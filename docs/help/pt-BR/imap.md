---
title: Outro e-mail (IMAP)
area: connections
summary: E-mail de qualquer provedor com IMAP, como iCloud, Yahoo, Fastmail, Telenet ou seu próprio domínio.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## O que ela lê

Sua caixa de entrada e sua pasta Enviados: os últimos 7 dias ao conectar, depois tudo o que chega de novo. O e-mail que você envia também conta: assim ela aprende como você escreve e o que prometeu. As outras pastas não são lidas.

Nada muda na sua caixa, a não ser uma cópia do que The Machine envia, na sua pasta Enviados. Os e-mails não são marcados como lidos.

## O que ela pode fazer

Ela envia e-mail só quando você toca em Enviar, pelo servidor de e-mail do seu provedor (SMTP) com a mesma senha. Uma cópia vai para a sua pasta Enviados. As respostas ficam na conversa delas, e sua assinatura é a das Configurações ou, se não houver, a que fecha seus e-mails enviados.

## Conecte

1. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha **Outro e-mail**.
2. Preencha seu endereço de e-mail e sua senha.
3. Toque em **Conectar**.

Muitos provedores pedem uma senha de app para programas de e-mail, não a sua senha normal. Crie uma nas configurações da conta do seu provedor:

- iCloud: uma senha específica de app em account.apple.com.
- Yahoo: Segurança da conta, Gerar senha de app.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: sua senha normal do e-mail da Telenet.
- Zoho Mail com verificação em duas etapas: uma senha específica de aplicativo na sua conta Zoho, em Segurança.
- Proton Mail: rode o Proton Mail Bridge no mesmo computador e use a senha que o Bridge mostra. Só funciona com The Machine nesse mesmo computador. The Machine mostra a impressão digital do certificado do Bridge e confia só nele.

As configurações do servidor são preenchidas para a maioria dos provedores. O seu não foi encontrado? Abra **Configurações do servidor** e digite o que seu provedor informa para programas de e-mail: os servidores IMAP e SMTP, suas portas e a segurança (SSL/TLS ou STARTTLS). The Machine nunca se conecta sem TLS.

Gmail ou e-mail da Microsoft, também no seu próprio domínio? Escolha **Gmail** ou **Outlook**. Eles entram sem senha. Os servidores deles digitados em Configurações do servidor levam para lá também: a Microsoft não aceita mais senhas de apps de e-mail.

## Quando para

- **O servidor de e-mail recusou a senha**: você a mudou, ou a senha de app foi removida. Conecte de novo com a nova.
- **O servidor de e-mail recusou a senha para enviar**: nada foi enviado. Conecte de novo; se ele continuar recusando, confira o servidor SMTP em Configurações do servidor. Até lá, ela só lê.
- **Não foi possível alcançar o servidor de e-mail**: ela tenta de novo sozinha. Se continuar falhando, confira o nome do servidor em Configurações do servidor.
- **O certificado do servidor de e-mail é para outro nome**: em hospedagem compartilhada, quem responde costuma ser o servidor da própria hospedagem. Digite o nome mostrado em Configurações do servidor. The Machine nunca pula a verificação do certificado.

## Remova

**Conexões**, abra a conta, **Detalhes**, depois **Desconectar**. Ela para de ler, e o que já trouxe fica. Remova também a senha de app no seu provedor.
