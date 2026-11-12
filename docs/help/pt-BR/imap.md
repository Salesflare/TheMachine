---
title: Outro e-mail (IMAP)
area: connections
summary: E-mail de qualquer provedor com IMAP, como iCloud, Yahoo, Fastmail, Telenet ou seu próprio domínio. Por enquanto só lê.
covers: connector:imap
code: imap_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## O que ela lê

Sua caixa de entrada e sua pasta Enviados: os últimos 7 dias ao conectar, depois tudo o que chega de novo. O e-mail que você envia também conta: assim ela aprende como você escreve e o que prometeu. As outras pastas não são lidas.

Nada muda na sua caixa. Os e-mails não são marcados como lidos.

## O que ela pode fazer

Por enquanto ela só lê: ainda não envia a partir desta caixa. Uma resposta preparada para você, você copia para o seu programa de e-mail.

## Conecte

1. No painel, abra **Conexões**, depois **+ Adicionar**, e escolha **Outro e-mail**.
2. Preencha seu endereço de e-mail e sua senha.
3. Toque em **Conectar**.

Muitos provedores pedem uma senha de app para programas de e-mail, não a sua senha normal. Crie uma nas configurações da conta do seu provedor:

- iCloud: uma senha específica de app em account.apple.com.
- Yahoo: Segurança da conta, Gerar senha de app.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: sua senha normal do e-mail da Telenet.
- Proton Mail: rode o Proton Mail Bridge no mesmo computador e use a senha que o Bridge mostra.

As configurações do servidor são preenchidas para a maioria dos provedores. O seu não foi encontrado? Abra **Configurações do servidor** e digite o que seu provedor informa para programas de e-mail: o servidor IMAP, a porta e a segurança (SSL/TLS ou STARTTLS). The Machine nunca se conecta sem TLS.

Gmail ou e-mail da Microsoft, também no seu próprio domínio? Escolha **Gmail** ou **Outlook**. Eles entram sem senha.

## Quando para

- **O servidor de e-mail recusou a senha**: você a mudou, ou a senha de app foi removida. Conecte de novo com a nova.
- **Não foi possível alcançar o servidor de e-mail**: ela tenta de novo sozinha. Se continuar falhando, confira o nome do servidor em Configurações do servidor.

## Remova

**Conexões**, abra a conta, **Detalhes**, depois **Desconectar**. Ela para de ler, e o que já trouxe fica. Remova também a senha de app no seu provedor.
