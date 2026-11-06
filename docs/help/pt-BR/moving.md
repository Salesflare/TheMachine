---
title: Mudar para outro computador
area: getting-started
summary: Exporte tudo o que sua Machine sabe em um único arquivo criptografado e importe em outra Machine, hospedada ou a sua.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Tudo o que sua IA aprende é seu: mensagens, conversas, tarefas com histórico, rascunhos, o Graph, memórias, habilidades e trabalhos de agentes. Você pode levar tudo, mesmo se parar de usar The Machine.

## Exportar

No seu próprio computador:

1. Em **Configurações** › **Geral** › **Exportar**, clique em **Exportar** ao lado de Tudo.
2. Se quiser, escolha uma frase secreta. Sem ela, você recebe um código de exportação: anote, a importação precisa dele.
3. Se quiser, ative **Incluir chaves e tokens** (precisa de uma frase secreta), para não precisar conectar suas fontes de novo.
4. Clique em **Iniciar exportação** e depois em **Baixar**. O arquivo é excluído depois de 24 horas, ou na hora com **Excluir**.

Em uma Machine hospedada, **Exportar** ao lado de Tudo abre a página da sua conta. Clique em **Exportar tudo** e depois em **Baixar**. Sua Machine exclui o arquivo depois de 24 horas, ou na hora com **Excluir agora**.

O arquivo é sempre criptografado. Depois de uma exportação, Configurações mostra o que está nela, com contagens, e o que não está e por quê. Logins no Google e na Microsoft pelo serviço hospedado sempre pedem um novo login do outro lado.

## Importar

1. Em **Configurações** › **Geral** › **Exportar**, clique em **Escolher arquivo** ao lado de Importar e escolha a exportação.
2. Digite a frase secreta ou o código de exportação e clique em **Abrir**. The Machine confere o arquivo inteiro primeiro.
3. Hospedada: clique em **Importar agora**. The Machine reinicia com ela em alguns minutos. No seu próprio computador: clique em **Substituir por esta exportação** e depois em **Substituir**. The Machine reinicia com ela em um ou dois minutos, e as Configurações mostram **Importada**.

A importação substitui o que essa Machine tem agora e guarda uma cópia antes. Nada que estava esperando sai sozinho: envios na fila esperam até você enviar de novo.

Avançado: num computador em que The Machine roda sem gerenciador de serviços, as Configurações mostram os comandos. Você também pode rodá-los: `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

Em um computador novo, [instale The Machine primeiro](self-hosted-setup.md). Depois cancele seu plano hospedado se não precisar mais dele: veja [Cancelar ou excluir](cancel-and-delete.md).
