---
title: Mudar para outro computador
area: getting-started
summary: Exporte tudo que sua Machine sabe em um único arquivo criptografado e importe em outra Machine, hospedada ou sua.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
translated: a08d8cd091c7d47b
---
Tudo que sua Machine aprende pertence a você: mensagens, tarefas, rascunhos, o Graph, memórias e habilidades. Leve tudo para outra Machine ou guarde uma cópia.

## Exportar

No seu próprio computador:

1. Em **Configurações** › **Geral** › **Exportar**, pressione **Exportar** ao lado de Tudo.
2. Se quiser, escolha uma senha. Sem ela, você recebe um código de exportação. Anote-o, pois vai precisar dele para importar.
3. Se quiser, ative **Incluir chaves e tokens** (é necessário definir uma senha) para não precisar conectar suas fontes novamente.
4. Pressione **Iniciar exportação** e depois **Baixar**. O arquivo é excluído após 24 horas ou imediatamente com **Excluir**.

Em uma Machine hospedada, **Exportar** ao lado de Tudo abre a página da sua conta. Pressione **Exportar tudo** e depois **Baixar**. Sua Machine exclui o arquivo após 24 horas ou imediatamente com **Excluir agora**.

O arquivo é sempre criptografado. Em seguida, Configurações mostra o que está incluído e o que não está. Você vai precisar fazer login novamente nas contas do Google e da Microsoft conectadas pelo nosso login hospedado.

## Importar

1. Em **Configurações** › **Geral** › **Exportar**, pressione **Escolher arquivo** ao lado de Importar e selecione o arquivo de exportação.
2. Digite a senha ou o código de exportação e pressione **Abrir**. A Machine verifica o arquivo inteiro primeiro.
3. Em uma Machine hospedada, pressione **Importar agora**. No seu próprio computador, pressione **Substituir por esta exportação** e depois **Substituir**. Em alguns minutos, a Machine reinicia com os dados importados e Configurações mostra **Importada**.

A importação substitui o que está na Machine, mas antes guarda uma cópia. Nada é enviado automaticamente: os envios na fila aguardam sua ação.

Se Configurações não conseguir reiniciar The Machine no seu computador, ela mostra os comandos que você precisa executar.

Em um computador novo, [instale The Machine](self-hosted-setup.md) primeiro. Depois, cancele seu plano hospedado se não precisar mais dele: veja [Cancelar ou excluir](cancel-and-delete.md).
