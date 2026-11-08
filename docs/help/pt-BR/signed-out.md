---
title: Desconectado de um site
area: troubleshooting
summary: O LinkedIn ou o X desconectou sua Machine. Entre de novo, uma vez ou de vez.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
---
Sites como LinkedIn e X são lidos no navegador da própria Machine. Às vezes um site a desconecta.

## Entrar de novo

A fonte em **Conexões** e o topo das suas Tarefas mostram que ela está desconectada. Clique em **Entrar de novo** e faça login em uma pequena janela no painel.

Marque **Salvar para a próxima vez** quando entrar. Na próxima vez que o site desconectar sua Machine, ela entra de novo com um toque. A senha fica criptografada na sua Machine. A IA nunca a vê.

## Senhas e códigos

Digite as senhas você mesmo. Os códigos de verificação em duas etapas também ficam por sua conta.

Os logins salvos ficam em **Conexões**, **Logins**. **Esquecer** remove um deles.

## Se o site recusar ou pedir uma verificação de robô

LinkedIn, X e sites atrás de uma verificação da Cloudflare costumam recusar logins de um navegador na nuvem. Em uma Machine hospedada, o login mostra então **Entrar pela sua conexão de casa**. Isso abre sua página de configuração, onde o navegador da sua Machine pode sair pela internet da sua casa com o Tailscale, ou pelo seu próprio proxy. Depois, entre de novo.

No seu próprio computador isso não é necessário: o navegador dele já está em casa.
