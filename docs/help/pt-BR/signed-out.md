---
title: Sua Machine saiu de um site
area: troubleshooting
summary: O LinkedIn ou X desconectou sua Machine. Entre de novo, uma vez ou para sempre.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
Sites como LinkedIn e X são acessados pelo navegador da sua Machine. Às vezes, um site desconecta sua Machine.

## Entre de novo

**Conexões** e o topo das suas tarefas mostram que ela foi desconectada. Pressione **Entre aqui** e faça login em uma janela pequena no painel.

Marque **Salvar para a próxima vez** para entrar com um toque se isso acontecer de novo. A senha fica criptografada na sua Machine, e a IA nunca a vê. Se você tiver várias contas no mesmo site, **Salvar como** dá um nome a esta conta (Trabalho, Pessoal), e a janela pergunta qual usar quando a tarefa não especificar.

## Senhas e códigos

Digite as senhas manualmente. Você também precisa inserir os códigos da verificação em duas etapas.

Os logins salvos ficam em **Conexões**, **Logins**. **Esquecer** remove um login. **Importar** traz logins de um gerenciador de senhas.

## Se o site recusar o login ou pedir uma verificação de robô

O LinkedIn, o X e sites com verificação do Cloudflare muitas vezes recusam logins feitos por um navegador na nuvem. Em uma Machine hospedada, o login mostra **Entrar pela sua conexão de casa**. Essa opção abre a página de configuração, onde o navegador da sua Machine pode acessar a internet pela sua conexão de casa usando Tailscale ou pelo seu próprio proxy. Depois, entre de novo.

No seu próprio computador, você não precisa fazer isso: o navegador já está conectado à sua rede de casa.
