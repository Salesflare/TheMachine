---
title: Configurações
area: settings
summary: Onde encontrar cada configuração, do modo claro à segurança e à sua conta.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Abra **Configurações** pela engrenagem no topo. As abas:

- **Conta**: **Seus endereços** (os que contam como seus) e **Sair**, no topo. Em uma Machine hospedada, também ficam aqui seu plano, as faturas, o Fleet, os amigos, o acesso e os dados, com **Cancelar plano** e **Excluir conta** lá embaixo. Em uma Machine no seu computador, conectada à Network: seu Fleet, nome de usuário, amigos e acesso, cada um com um link que abre essa parte da sua conta (faça login por lá), e **Excluir conta** no final. Se ainda não estiver conectada: **Entrar na Network**, no topo. Veja [Planos e cobrança](plans-and-billing.md).
- **Geral**: idioma e região, este dispositivo, entrada por voz, o navegador da sua Machine, seu Fleet, exportação e importação, e a versão em execução. Se não houver a aba Conta, **Entrar na Network** aparece no final.
- **Segurança**: Padrão ou Cuidadoso. Veja [Níveis de segurança](security-levels.md). **Acesso de suporte** também aparece enquanto estiver ativado: veja [Receber suporte](get-support.md#support-access).
- **Atividade**: tudo o que The Machine fez por você, começando pelo mais recente. Veja [Atividade](activity.md).
- **Notificações**: o que chega até você e onde, além do seu horário de trabalho. Veja [Notificações](notifications.md) e [Horário de trabalho](work-hours.md).
- **Escrita**: assinaturas e seu jeito de escrever. Veja [Escrita](writing.md).
- **Habilidades**: instruções que sua Machine segue. Veja [Habilidades](skills.md).
- **Apps**: os apps da The Machine para seu celular e computador, depois Claude, ChatGPT e outras IAs que você conectou, e o que cada uma pode fazer. Veja [O app para celular](mobile-app.md) e [Conectar outras IAs](ai-connections.md).
- **Modelo**: a IA que lê e cria rascunhos para você, e os limites dela. Veja [Modelo](model.md). Também **Codex e Claude Code**: veja [Passar para o Claude Code ou Codex](hand-to-agent.md). E **Busca por significado**, mais abaixo.

Uma aba sem nada para mostrar fica oculta.

## Geral

- **Idioma e região**: sua **Região** define como as datas, horas e números são exibidos (24 out. ou 24 out.). **Formato de hora** escolhe entre 12 horas (2:05 PM) e 24 horas (14:05). As tarefas, o Telegram, o resumo e as mensagens do Fleet seguem essas duas configurações. Uma Machine hospedada começa com o fuso horário escolhido na inscrição.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. A configuração inicial usa o idioma do seu navegador. O painel, a Ajuda, as notificações, o Telegram, o resumo semanal e as tarefas que sua Machine escreve mudam assim que você escolhe o idioma. Os textos mais antigos continuam como estavam. Seus colegas de equipe recebem perguntas do Fleet e da família no idioma deles, e os rascunhos para outras pessoas continuam no idioma da conversa.
- **Este dispositivo**: **Instalar app**, **Notificações** com **Enviar um teste** e **Modo claro**, apenas neste navegador ou celular. Veja [Instalar o app e ativar as notificações](phone-app.md). No [Omarchy](omarchy.md), também aparece **Tema do Omarchy**.
- **Entrada por voz**: como o que você diz vira texto e qual voz é usada no Talk ao vivo. Veja [Entrada por voz](voice-input.md) e [Conversa ao vivo](talk-live.md).
- **Abrir o navegador da Machine ↗**: o navegador que sua Machine usa para sites como o LinkedIn.
- **Regras do Fleet**: veja [Regras de compartilhamento](sharing-rules.md).
- **Exportar**:
  - **Tudo**: tudo o que sua Machine sabe em um arquivo criptografado, para transferir ou guardar. Use **Importar** para importar um arquivo. Veja [Mudar para outro computador](moving.md).
  - **Conhecimento para outra IA**: o que sua Machine aprendeu, em arquivos que qualquer IA pode ler. Veja [Conhecimento para outra IA](knowledge-export.md).

## Versão

A versão em execução na sua Machine. As atualizações são instaladas automaticamente. Quando uma versão mais recente estiver disponível em uma Machine hospedada, **Atualizar agora** instala a atualização imediatamente. Isso leva alguns minutos, e seus dados são mantidos.

No seu computador, um temporizador diário instala cada nova versão assinada no Linux. Veja [Executar no seu próprio computador](self-hosted-setup.md).

## Busca por significado

Em **Configurações**, **Modelo**. A busca encontra e-mails, mensagens e notas pelo assunto, não apenas pelas palavras usadas. Em uma Machine hospedada, uma IA pequena faz isso na própria Machine, sem enviar nada para lugar nenhum. Ela fica ativada a partir de 8 GB de memória. Com 4 GB, ative-a pelo botão. Ela usa cerca de meio gigabyte, então uma Machine ocupada pode ficar mais lenta.

No seu computador, essa configuração fica no bloco `embeddings` de `config.json`. Reinicie a Machine depois de alterar.

## Nesta Machine

Quando sua Machine está no seu computador, algumas coisas são feitas lá, em um terminal:

- O arquivo de configurações, `config.json`: todas as configurações em um só lugar. Reinicie a Machine depois de alterar.
- `assistant connect`: adicione uma fonte, como `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off`: mensagens no Telegram. Veja [Telegram](telegram.md).
- `assistant doctor`: verifica tudo e mostra uma correção para cada problema.

## Seus endereços

Todos os seus endereços encontrados pela Machine: suas contas, aliases do Gmail ou Outlook, seu calendário e seus perfis no Slack e Intercom. E-mails e reuniões de qualquer um deles contam como seus. Use **Remover** nos que não forem seus.

Um endereço compartilhado, como info@ ou um Grupo do Google, nunca conta por conta própria. Um endereço sobre o qual a Machine não tem certeza fica em **Talvez seus**. Escolha uma opção:

- **Meu: só eu respondo**: o endereço conta como seu. E-mails enviados para ele podem virar tarefas.
- **Da equipe: outros também respondem**: o endereço não é seu. E-mails enviados somente para ele não geram tarefas nem rascunhos para você. Ainda assim, ele contribui para o Graph.
- **Não é meu**: o endereço não vai contar como seu.

Escolha de acordo com quem responde por ele hoje. Uma caixa de entrada da equipe, como support@, pertence à equipe. Um endereço como partnerships@, ao qual só você responde, é seu. Mude a opção quando outras pessoas também começarem a responder.

**Mudar** na linha do endereço permite alterar a opção mais tarde. Seu próprio endereço de acesso sempre é seu.

### Domínios da sua empresa

Os domínios dos seus próprios endereços contam como domínios da sua empresa. Você também usa outro, como acme.co além de acme.com? Digite-o em **Domínios da sua empresa** e pressione **Adicionar**.

As pessoas desses domínios passam a ser colegas, nunca clientes: as conversas delas não aparecem no Team Graph, e nenhuma organização é criada para elas. Use **Remover** para retirar um domínio. Não é possível adicionar domínios de e-mail gratuitos, como gmail.com.

Um alias seu do Gmail também pode aparecer como **De** em um rascunho, se o Gmail confirmar que você pode enviar mensagens por ele. Veja [Gmail](gmail.md#what-it-can-send).
