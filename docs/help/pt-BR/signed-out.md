---
title: Um site desconectou sua Machine
area: troubleshooting
summary: O LinkedIn ou o X encerrou a sessão da sua Machine. Faça login de novo, só desta vez ou de forma permanente.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
Sites como LinkedIn e X são acessados no navegador próprio da sua Machine. Às vezes, um site encerra a sessão dela.

## Faça login novamente

**Conexões** e o início de **Tarefas** avisam quando ela está desconectada. Clique em **Entre aqui** e faça login em uma janela pequena no painel.

Marque **Salvar para a próxima vez** para fazer login de novo com um toque quando isso acontecer. A senha fica criptografada na sua Machine, e a IA nunca a vê. Se você tiver várias contas no mesmo site, **Salvar como** dá um nome a esta conta (Trabalho, Pessoal), e a janela pergunta qual usar quando a tarefa não especificar.

## Senhas e códigos

Digite as senhas você mesmo. Os códigos da verificação em duas etapas também ficam por sua conta.

Os logins salvos ficam em **Conexões** > **Logins**. **Esquecer** remove um login. **Importar** traz logins de um gerenciador de senhas, pela própria página de exportação dele no navegador da sua Machine ou por um arquivo de exportação.

## Se o site recusar o login ou pedir uma verificação de robô

O LinkedIn, o X e sites com verificação da Cloudflare costumam recusar logins em navegadores na nuvem. Em uma Machine hospedada, a tela de login mostra **Entrar pela sua conexão de casa**. Essa opção abre a página de configuração, onde o navegador da sua Machine pode acessar a internet pela sua conexão de casa usando Tailscale ou pelo seu próprio proxy. Depois, faça login de novo.

No seu próprio computador, você não precisa fazer isso: o navegador já está conectado pela sua rede de casa.
