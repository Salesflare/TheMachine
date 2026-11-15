---
title: Você saiu de um site
area: troubleshooting
summary: LinkedIn ou X desconectou sua Machine. Entre de novo, uma vez ou para sempre.
covers:
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: 96c09e57cd3dca62
---
Sites como LinkedIn e X são acessados pelo navegador da sua própria Machine. Às vezes, um site desconecta sua Machine.

## Entre de novo

**Conexões** e o topo das suas tarefas indicam que você saiu da conta. Clique em **Entre aqui** e faça login em uma janela pequena no painel.

Marque **Salvar para a próxima vez** para entrar com um toque se isso acontecer de novo. A senha fica criptografada na sua Machine, e a IA nunca a vê.

## Senhas e códigos

Digite as senhas você mesma. Você também precisa inserir os códigos de verificação em duas etapas.

Os logins salvos ficam em **Conexões**, **Logins**. **Esquecer** remove um login.

## Se o site recusar o login ou pedir uma verificação de robô

LinkedIn, X e sites com uma verificação da Cloudflare muitas vezes recusam logins feitos por um navegador na nuvem. Em uma Machine hospedada, aparece a opção **Entrar pela sua conexão de casa**. Ela abre a página de configuração, onde o navegador da sua Machine pode acessar a internet pela sua conexão de casa com o Tailscale ou por meio do seu próprio proxy. Depois, entre de novo.

No seu próprio computador, você não precisa fazer isso: o navegador já está na sua conexão de casa.
