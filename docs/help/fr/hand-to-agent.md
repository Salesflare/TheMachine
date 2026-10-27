---
title: Transférer à Claude Code ou Codex
area: cards
summary: Envoyez une tâche de code à Claude Code ou Codex. Le résultat revient sur la tâche.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Transférer une tâche

1. Sur la tâche, ouvrez **Plus** et choisissez **Transférer à Codex** ou **Transférer à Claude Code**. L’option apparaît quand l’outil est configuré.
2. Vérifiez le résumé et ce qui lui est transmis, ajoutez une note si vous voulez, et appuyez sur **Transférer**. **Voir la mission complète** affiche tout le brief.

La tâche indique ensuite qu’elle est en cours, puis le résultat une fois terminé, avec **Afficher les modifications**. **Modifier** lui demande des changements. **Transférer à nouveau** recommence de zéro.

Une mission n’envoie jamais rien à votre place.

## La configurer

Dans **Paramètres**, **Général**, sous **Agents de code** :

- **Session Claude Code** : l’adresse d’une session Claude Code.
- **Environnement cloud Codex** : son identifiant d’environnement.
- **Tourne sur**, et éventuellement une **Branche**.

Claude renvoie son résultat via le connecteur The Machine. Ajoutez-le une fois dans claude.ai, Settings, Connectors, Add custom connector, avec l’adresse affichée à cet endroit. Pour Codex sur une Machine hébergée, appuyez d’abord sur **Connecter Codex** sur votre page de configuration, sous **Ajoutez-en d’autres à tout moment**. Il utilise le même abonnement ChatGPT que votre modèle, et OpenAI demande un code de plus, pour Codex.

Sur une Machine hébergée, Agents de code apparaît dès que GitHub ou Codex est connecté. La section apparaît aussi sur les configurations qui exécutent les missions ailleurs. Plus d’infos dans le [guide des agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
