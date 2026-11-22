---
title: Connecter d’autres IA
area: connections
summary: Laissez Claude, ChatGPT, Cursor, Codex ou GBrain lire vos tâches et votre Graph, puis apporter, avec **Lecture et modification**, des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, les briefs de votre équipe, ainsi que les personnes et les entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail, et mettre à jour votre Graph : enregistrer un fait, corriger des détails, des champs et des tags, ou ajouter une ligne au résumé d’une personne.

Chaque changement apparaît dans **Activité**, avec l’option **Annuler**. Les IA ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent porte la mention **AI:** suivie de leur nom. Votre Machine le considère comme une affirmation de leur part, jamais comme une instruction de votre part.

Un brouillon attend que vous le lisiez et que vous appuyiez vous-même sur Envoyer. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place.

## Connecter une IA

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine**, vous trouverez **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse**, vous trouverez l’adresse unique de l’application officielle pour chaque Machine, `https://mcp.themachine.computer/mcp`, et **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, avec **Copier** à côté de chacune.

Pour une Machine installée sur votre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page s’ouvre dans votre compte : vérifiez que le même code y apparaît, confirmez, puis choisissez un nom. Votre Machine s’associe automatiquement, sans redémarrage. Cette étape est nécessaire dans les deux cas.

Votre Machine configure ensuite elle-même son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans l’annuaire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur Connect. Avec Team et Enterprise, un propriétaire doit l’ajouter dans les paramètres de l’organisation.

Pour utiliser une adresse dans Claude à la place, ouvrez Customize, puis Connectors, appuyez sur + Add, puis sur Add custom connector. Nommez-la The Machine, collez l’adresse, appuyez sur Continue, puis sur Add.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur Install plugin. Avec Business et Enterprise, un administrateur devra peut-être d’abord l’autoriser.

L’application officielle se connecte à une Machine hébergée, ainsi qu’à une Machine installée sur votre ordinateur une fois son adresse configurée.

Pour utiliser votre adresse privée, ou une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Add custom MCP server. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement, puis appuyez sur Create as a plugin. Votre forfait ou votre espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’application officielle, l’IA vous demande de vous connecter à votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis approuvez la connexion sur sa propre page. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA installées sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. L’option **Dissocier cette Machine**, en bas de **Paramètres**, puis **Compte**, déconnecte de nouveau de votre compte une Machine installée sur votre ordinateur.

Votre Machine indique quelle IA cherche à se connecter. Si elle ne peut pas l’identifier, elle indique l’origine de la demande : ne vous connectez que si vous venez de lancer cette opération.

Choisissez ce qu’elle peut faire : **Lire** ou **Lecture et modification**. Si vous avez des comptes Travail et Perso, choisissez ce qu’elle peut voir. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Connecter**, ou sur **Annuler** pour refuser sans rien envoyer.

## Application officielle ou adresse privée

L’application officielle est la solution la plus simple : une seule adresse pour tout le monde, et votre compte trouve votre Machine. Notre cloud transmet les demandes sans rien stocker.

Avec votre adresse privée, tout est chiffré de bout en bout jusqu’à votre Machine. Le cloud ne fait que transmettre les demandes et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez approuvée sur sa page peut y accéder, avec les droits que vous avez choisis. Dans **Paramètres**, puis **Applis**, une IA connectée par l’application officielle porte la mention **App officielle**.

## Ce qu’elle peut voir

Une connexion ne voit que son espace. L’espace Travail comprend les tâches et les promesses de vos comptes professionnels, les personnes, les entreprises et les projets professionnels, ainsi que le brief d’équipe de votre Fleet Travail. L’espace Perso comprend le reste. Le texte des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cette option, une IA ne voit les sources d’une tâche que par l’expéditeur, l’objet et la date.

Les fiches du Graph d’équipe de vos collègues ne sont jamais transmises à une IA externe.

## Messages

**Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack, WhatsApp et vos autres chats. Cette option est désactivée jusqu’à ce que vous l’activiez, sur la page de connexion ou plus tard dans **Paramètres**, puis **Applis**. L’IA ne fait que lire : elle n’envoie rien, ne supprime rien et ne marque aucun message.

Elle ne lit que les messages de son espace. Certains ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les conversations que The Machine a jugées sensibles (transactions, RH, questions juridiques, santé, argent), les conversations que vous avez gardées privées et les messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les conversations consultées, jamais leur contenu. Votre Machine transmet le texte en le signalant comme une donnée, afin que l’IA ne suive pas les instructions contenues dans un message.

Tant que Messages est activé, les changements apportés au Graph par une IA avec **Lecture et modification** attendent votre accord. Appuyez sur **Appliquer** ou **Écarter** pour le changement dans **Activité**.

## Dans les paramètres

Ouvrez **Paramètres**, puis **Applis** pour voir une seule entrée par IA connectée, avec ses droits, son espace, sa date d’expiration et sa dernière utilisation. Vous pouvez activer ou désactiver **Messages** au même endroit. Appuyez sur **Modifier** pour changer ses droits, son espace ou sa durée d’accès. La prochaine demande utilisera les nouveaux réglages. **Activité** répertorie chaque demande, y compris celles qui ont été refusées. **Désactiver maintenant** suspend l’accès : toutes les sessions sont fermées, mais l’historique est conservé. **Retirer** supprime l’IA et son historique.

Si vous vous reconnectez à la même IA, la nouvelle autorisation remplace la précédente.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les droits et la durée, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affiche qu’une fois. L’IA l’envoie avec `Authorization: Bearer <key>`.

## Protéger votre compte

Chaque demande est enregistrée, y compris celles qui sont refusées. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion, afin qu’une copie de ses données ne donne accès à rien.
