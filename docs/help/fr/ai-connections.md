---
title: Connecter d’autres IA
area: connections
summary: Laissez Claude, ChatGPT, Cursor, Codex ou GBrain lire vos tâches et votre Graph via MCP, chacun avec son accès et sa durée.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## Ce qu’une autre IA peut faire

D’autres IA peuvent se connecter à votre Machine via MCP : Claude, ChatGPT, Cursor, Codex, GBrain et d’autres. Elles peuvent lire vos tâches, vos promesses, les briefings d’équipe et les personnes et entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche, ou une tâche avec un brouillon d’e-mail, et modifier votre Graph : enregistrer un fait sur une personne ou une entreprise, corriger ses détails, champs et tags, ou ajouter une ligne au résumé d’une personne.

Chaque modification apparaît dans **Activité** avec **Annuler**. Elles ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent affiche **IA :** et leur nom, dans leur périmètre. Vous pouvez le modifier ou le retirer, et The Machine peut réécrire une ligne de résumé plus tard. Votre Machine le traite comme leur affirmation, jamais comme votre instruction.

Un brouillon attend dans votre Machine jusqu’à ce que vous le lisiez et appuyiez vous-même sur **Envoyer**. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place. Do it et les agents de votre Machine n’en font pas partie.

## En connecter une

Ouvrez **Paramètres**, **IA**. En haut se trouve l’adresse de votre Machine pour les IA, `https://<votre nom>.mcp.themachine.computer/mcp`, avec **Copier**. Sur une Machine installée sur votre ordinateur, appuyez d’abord sur **Obtenir votre adresse**. Une page de votre compte s’ouvre : vérifiez qu’elle affiche le même code, confirmez et choisissez un nom. Votre Machine s’associe d’elle-même, sans redémarrage.

Elle obtient ensuite son propre certificat pour l’adresse. Cela prend quelques minutes et demande le paquet `cryptography` pour Python.

Dans ChatGPT, ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Add custom MCP server. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement et appuyez sur Create as a plugin. Votre forfait ou votre espace de travail doit autoriser les serveurs MCP personnalisés.

Dans Claude, ouvrez Customize, Connectors, appuyez sur + Add, puis sur Add custom connector. Nommez-le The Machine, collez l’adresse, appuyez sur Continue, puis sur Add. Sur Team et Enterprise, un propriétaire l’ajoute dans Organization settings.

Les IA d’un appareil de votre tailnet, comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. **Dissocier** retire de votre compte une Machine installée sur votre ordinateur.

L’IA vous envoie vers votre Machine pour vous connecter. Votre Machine montre de quelle IA il s’agit. Une IA qu’elle ne reconnaît pas montre l’adresse d’où elle vient : connectez seulement si vous venez de lancer cela vous-même.

Choisissez ce qu’elle peut faire, **Lire** ou **Lecture et modification**. Avec des comptes Travail et personnels, choisissez aussi ce qu’elle peut voir. Puis choisissez la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Se connecter**, ou sur **Annuler** pour la renvoyer sans rien.

## Ce qu’elle voit

Une connexion ne voit que son domaine. Travail couvre les tâches et promesses de vos comptes de travail, les contacts de travail, les entreprises, les projets et le briefing d’équipe de votre Work Fleet. Personnel couvre le reste. Le texte des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cela, une IA voit les sources d’une tâche seulement par expéditeur, objet et date.

Les données Team Graph de vos coéquipiers ne vont jamais à une IA extérieure.

## Messages

**Messages** permet à une IA de chercher et lire vos e-mails, Slack, WhatsApp et autres chats. C’est désactivé tant que vous ne l’activez pas, sur la page où vous la connectez ou plus tard dans **Paramètres**, **IA**. Elle lit seulement : elle n’envoie, ne supprime et ne marque jamais rien.

Elle ne lit que les messages de son domaine. Certains ne sortent jamais : codes à usage unique et liens de connexion, messages d’un tableau ou projet **Vous seul**, conversations que The Machine a jugées sensibles (affaires, RH, juridique, santé, argent), conversations que vous avez gardées privées, et messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les conversations, jamais le texte. Votre Machine transmet le texte marqué comme des données, pour que l’IA ne suive pas d’instructions écrites dans un message.

Tant que Messages est activé, les modifications du Graph d’une IA en **Lecture et modification** attendent votre accord. Appuyez sur **Appliquer** ou **Ignorer** sur la modification dans **Activité**.

## Dans Paramètres

Ouvrez **Paramètres**, **IA** pour voir chaque IA connectée, avec sa dernière utilisation et son nombre d’appels. Modifiez-y son accès, son domaine ou sa durée. L’appel suivant en tient compte. **Désactiver maintenant** ferme toutes ses connexions d’un coup. **Activité** liste chaque appel, les refusés aussi. **Retirer** la supprime.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, nommez-la, choisissez l’accès et la durée, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affiche qu’une fois. L’IA l’envoie comme `Authorization: Bearer <key>`.

## Sécurité

Chaque appel est noté, les refusés aussi. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. La connexion utilise OAuth avec PKCE. Votre Machine ne garde qu’une empreinte de chaque jeton, donc une copie de ses données n’ouvre rien.
