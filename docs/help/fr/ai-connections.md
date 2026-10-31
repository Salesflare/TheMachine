---
title: Connecter d’autres IA
area: connections
summary: Laissez Claude, ChatGPT, Cursor, Codex ou GBrain lire vos tâches et votre Graph via MCP, chacun avec son accès et sa durée.
covers: ai-connections
code: ai_access.py, ai_app.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Ce qu’une autre IA peut faire

D’autres IA peuvent se connecter à votre Machine via MCP : Claude, ChatGPT, Cursor, Codex, GBrain et d’autres. Elles peuvent lire vos tâches, vos promesses, les briefings d’équipe et les personnes et entreprises de votre Graph.

Au plus, elles ajoutent une tâche, ou une tâche avec un brouillon d’e-mail. Un brouillon attend dans votre Machine jusqu’à ce que vous le lisiez et appuyiez vous-même sur **Envoyer**. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place. Do it et les agents de votre Machine n’en font pas partie.

## En connecter une

Dans l’autre IA, ajoutez un connecteur personnalisé ou un serveur MCP avec l’adresse de votre Machine suivie de `/mcp`. Sur une Machine hébergée, c’est `https://<votre nom>.app.themachine.computer/mcp`. Sur une Machine sur votre propre ordinateur, c’est l’adresse de votre tableau de bord, que seuls les appareils de votre tailnet atteignent.

L’IA vous envoie vers votre Machine pour vous connecter. Votre Machine montre de quelle IA il s’agit. Une IA qu’elle ne reconnaît pas montre l’adresse d’où elle vient : connectez seulement si vous venez de lancer cela vous-même.

Choisissez ce qu’elle peut faire, **Lire** ou **Lecture et brouillons**. Avec des comptes Travail et personnels, choisissez aussi ce qu’elle peut voir. Puis choisissez la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Se connecter**, ou sur **Annuler** pour la renvoyer sans rien.

## Ce qu’elle voit

Une connexion ne voit que son domaine. Travail couvre les tâches et promesses de vos comptes de travail, les contacts de travail, les entreprises, les projets et le briefing d’équipe de votre Work Fleet. Personnel couvre le reste. Le texte des messages reste sur votre Machine : une IA voit les sources d’une tâche seulement par expéditeur, objet et date.

Les données Team Graph de vos coéquipiers ne vont jamais à une IA extérieure.

## Sécurité

Chaque appel est noté, les refusés aussi. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. La connexion utilise OAuth avec PKCE. Votre Machine ne garde qu’une empreinte de chaque jeton, donc une copie de ses données n’ouvre rien.
