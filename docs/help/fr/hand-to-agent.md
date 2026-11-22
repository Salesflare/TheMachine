---
title: Transférer à Claude Code ou Codex
area: cards
summary: Envoyez une tâche de programmation à Claude Code ou Codex. Le résultat s’affiche sur la tâche.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Transférer une tâche

1. Sur la tâche, ouvrez **…**, puis **Transférer…**, et choisissez **Codex** ou **Claude Code**. Seuls les outils que vous avez configurés s’affichent.
2. Vérifiez le résumé et ce à quoi l’outil aura accès, ajoutez une note si vous le souhaitez, puis appuyez sur **Transférer**. **Voir le travail complet** affiche la demande complète.

La tâche indique qu’elle est en cours, puis affiche le résultat avec **Ce qu’il a fait** et **Voir les modifications**. **Demander des modifications** lui indique ce qu’il faut changer. **Transférer…** dans **…** permet de recommencer. **Masquer** masque le résultat. Une tâche bloquée que vous transférez affiche **En cours…** au lieu de **Bloqué** pendant le traitement.

Une tâche n’envoie jamais rien à votre place. Si une étape de publication ou de déploiement vous est laissée, **Faire** sur la tâche lance cette étape. Une réponse rédigée reste un brouillon que vous envoyez vous-même.

## Dans l’app Codex

- **Ouvrir dans Codex** ouvre le fil de la tâche dans l’app Codex, une fois le travail terminé.
- **Demander des modifications** poursuit dans la même conversation Codex, et la tâche la suit.
- Le traitement s’arrête après 30 minutes sans progression, ou après 6 heures au total. Un redémarrage ne l’interrompt pas.

## Configuration

Dans **Paramètres**, **Modèle**, sous **Codex et Claude Code** :

- **Codex** : où il s’exécute. Sur votre Machine ou sur votre ordinateur, aucune autre configuration n’est nécessaire ici. **Modifier** ouvre votre page de configuration.
- **Codex cloud** : son ID d’environnement, fourni par Codex, et éventuellement une **Branche** à utiliser comme point de départ.
- **Claude Code** : le lien d’une session Claude Code.

Claude renvoie son résultat par le connecteur The Machine. Ajoutez-le une seule fois dans claude.ai, dans Settings, Connectors, Add custom connector, avec l’adresse indiquée sous la session.

## Où Codex s’exécute

Sur une Machine hébergée, sélectionnez l’option sur votre page de configuration, sous **Ajouter à tout moment**, **Codex** :

- **Sur votre Machine** (par défaut) : appuyez sur **Connecter Codex** et saisissez le code affiché par OpenAI. Cette option utilise le même forfait ChatGPT que votre modèle, et les tâches s’exécutent sur votre Machine. Aucun terminal n’est nécessaire. Si vous êtes connecté au même compte ChatGPT, votre Machine peut aussi consulter et utiliser les réinitialisations de votre limite d’utilisation.
- **Autres options**, **Sur mon ordinateur** : la tâche s’exécute sur votre ordinateur, avec le compte Codex connecté sur celui-ci. Les échanges sont chiffrés et réservés à cet ordinateur. Installez The Machine sur cet ordinateur, associez-le sur la page de votre compte, exécutez `codex login` et laissez The Machine en marche. Le résultat s’affiche sur la tâche. Quand l’ordinateur est éteint, les tâches attendent.
- **Autres options**, **Codex cloud** : la tâche s’exécute dans le cloud d’OpenAI. Appuyez sur **Connecter Codex**. Cette option utilise le même forfait ChatGPT que votre modèle, et OpenAI vous demande un autre code, pour Codex. Saisissez ensuite l’environnement Codex cloud dans Paramètres.

Vous pouvez aussi vous connecter depuis votre tableau de bord : **Connexions**, **Projets et code**, **Codex**, **Obtenir un code**. Une Machine auto-hébergée effectue elle-même cette connexion.

Sur une Machine hébergée, **Codex et Claude Code** apparaît dans **Paramètres** une fois GitHub ou Codex connecté. Pour les développeurs : le [guide des agents](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
