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

## Dans l’app Codex

- **Ouvrir dans Codex** ouvre le fil de la tâche dans l’app Codex. Tant que Codex y travaille ici, l’app ne peut pas encore l’ouvrir. Il s’ouvre une fois terminé.
- **Modifier** sur un fil ouvert dans l’app Codex continue dans cette même conversation là-bas, et la tâche la suit.
- Un travail ne s’arrête que si Codex ne fait rien pendant 30 minutes, ou après 6 heures au total. Un redémarrage de The Machine ne l’arrête pas.

## La configurer

Dans **Paramètres**, **Modèle**, sous **Codex et Claude Code** :

- **Codex** : où il tourne. Sur votre ordinateur, il n’a besoin de rien de plus ici ; **Modifier** ouvre votre page de configuration.
- **Codex cloud** : son identifiant d’environnement, depuis Codex, et éventuellement une **Branche** de départ.
- **Claude Code** : le lien d’une session Claude Code.

Claude renvoie son résultat via le connecteur The Machine. Ajoutez-le une fois dans claude.ai, Settings, Connectors, Add custom connector, avec l’adresse affichée sous la session.

## Où Codex tourne

Sur une Machine hébergée, choisissez-le sur votre page de configuration, sous **Ajoutez-en d’autres à tout moment**, **Codex** :

- **Sur mon ordinateur** (par défaut) : la mission tourne sur votre propre ordinateur, avec le Codex connecté là-bas. Rien de Codex n’est sur votre serveur, et la mission est chiffrée pour cet ordinateur uniquement : le Network la transmet mais ne peut pas la lire. Installez The Machine sur cet ordinateur, associez-le sur la page de votre compte et lancez `codex login` dessus. Laissez The Machine tourner dessus. La mission apparaît comme un fil dans l’app Codex sur cet ordinateur, et le résultat revient sur la tâche. Quand l’ordinateur est éteint, les missions attendent son retour.
- **Cloud Codex** : la mission tourne dans le cloud d’OpenAI. Appuyez sur **Connecter Codex**. Il utilise le même abonnement ChatGPT que votre modèle, et OpenAI demande un code de plus, pour Codex. Saisissez ensuite l’environnement cloud Codex dans les Paramètres.

Sur une Machine hébergée, Codex et Claude Code apparaît dès que GitHub ou Codex est connecté. La section apparaît aussi sur les configurations qui exécutent les missions ailleurs. Plus d’infos dans le [guide des agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
