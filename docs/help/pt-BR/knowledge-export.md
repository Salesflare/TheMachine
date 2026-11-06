---
title: Conhecimento para outra IA
area: settings
summary: Leve o que sua Machine aprendeu para qualquer outra IA, em arquivos simples Markdown, JSONL e CSV.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Tudo o que sua Machine aprende é seu. Leve para outra IA, ou guarde, mesmo que pare de usar The Machine.

## Exportar

1. Em **Configurações** › **Geral**, toque em **Exportar** ao lado de **Conhecimento para outra IA**.
2. Deixe **Texto das mensagens** desligado para exportar só de onde veio cada coisa, e quando. Ligue para incluir o texto.
3. **Privado e Cuidadoso** fica desligado, a não ser que você queira também os projetos só seus, as conversas privadas e os Fleets no modo Cuidadoso.
4. Se quiser, defina uma **Frase secreta** de pelo menos 10 caracteres para criptografar o arquivo.
5. Toque em **Baixar**. O arquivo é feito na sua Machine e pode ser baixado uma vez.

Em uma Machine hospedada funciona igual, nas Configurações da sua própria Machine. No seu próprio computador, `assistant export-knowledge` cria o mesmo arquivo.

## O que tem nele

- Pessoas, organizações e projetos: uma página Markdown para cada, com como se relacionam.
- Fatos e preferências: o que sua Machine sabe, sobre você e sobre eles.
- Regras, como você escreve e assinaturas: o que seus rascunhos seguem.
- Habilidades: seus guias, ligados e desligados.
- Contexto: briefings da equipe, linhas de resumo, promessas e tarefas abertas.
- Fontes: de onde veio cada coisa, com id e data.

Os registros são JSONL, contatos e tarefas também CSV. Um README.md no topo explica a estrutura e diz a uma IA como usar. Entregue a pasta, ou o zip, à IA como arquivo de conhecimento ou projeto.

## O que fica de fora

Senhas, chaves e logins nunca entram. O que parece uma chave é substituído. Dados de colegas e de outras Machines, configurações e fotos também ficam de fora. Para uma cópia completa para mudar sua Machine, veja [Mudar para o seu próprio computador](moving.md).

O formato é aberto e versionado: veja [o esquema](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
