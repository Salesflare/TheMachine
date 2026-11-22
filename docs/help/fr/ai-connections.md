---
title: Connecter d’autres IA
area: connections
summary: Permettez à Claude, ChatGPT, Cursor, Codex ou GBrain de lire vos tâches et votre Graph et, avec **Lecture et modification**, d’effectuer des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, les briefs de votre équipe, ainsi que les personnes et les entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail et mettre à jour votre Graph : enregistrer un fait, corriger des détails, des champs et des tags, ou ajouter une ligne au résumé d’une personne.

Chaque modification apparaît dans **Activité**, avec **Annuler**. Elles ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent porte la mention **IA :** suivie de leur nom, et votre Machine le considère comme une affirmation de leur part, jamais comme une instruction de votre part.

Un brouillon attend que vous le lisiez et que vous appuyiez vous-même sur Envoyer. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place.

## En connecter une

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine**, vous trouverez **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse**, vous trouverez l’adresse officielle de l’application, la même pour chaque Machine, `https://mcp.themachine.computer/mcp`, ainsi que **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, avec **Copier** pour chacune.

Sur une Machine installée sur votre propre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page de votre compte s’ouvre : vérifiez que le code affiché est le même, confirmez, puis choisissez un nom. Votre Machine s’associe automatiquement, sans redémarrage. Cette étape est nécessaire dans les deux cas.

Votre Machine configure ensuite elle-même son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans l’annuaire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur Connecter. Avec Team et Enterprise, un propriétaire doit l’ajouter dans les paramètres de l’organisation.

Pour utiliser une adresse dans Claude à la place, ouvrez Personnaliser, Connecteurs, appuyez sur + Ajouter, puis sur Ajouter un connecteur personnalisé. Nommez-le The Machine, collez l’adresse, appuyez sur Continuer, puis sur Ajouter.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur Installer le plugin. Avec Business et Enterprise, un administrateur devra peut-être d’abord l’autoriser.

L’application officielle permet de se connecter à une Machine hébergée, ainsi qu’à une Machine installée sur votre propre ordinateur une fois qu’elle dispose de son adresse.

Pour utiliser votre adresse privée ou une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Ajouter un serveur MCP personnalisé. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement, puis appuyez sur Créer en tant que plugin. Votre forfait ou votre espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’application officielle, l’IA vous demande de vous connecter à votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis autorisez la connexion sur la page de votre Machine. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA installées sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. **Dissocier cette Machine**, en bas de **Paramètres**, puis **Compte**, retire de nouveau de votre compte une Machine installée sur votre propre ordinateur.

Votre Machine indique quelle IA essaie de se connecter. Si elle ne peut pas l’identifier, elle indique d’où vient la demande : ne connectez l’IA que si vous venez de lancer cette opération.

Choisissez ce qu’elle peut faire, **Lire** ou **Lecture et modification**. Si vous avez des comptes Travail et Personnel, choisissez ce qu’elle peut consulter. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Connecter**, ou sur **Annuler** pour refuser la demande sans rien envoyer.

## Application officielle ou adresse privée

L’application officielle est la solution la plus simple : une seule adresse pour tout le monde, et votre compte trouve votre Machine. Notre cloud transmet les demandes et n’enregistre jamais leur contenu.

Avec votre adresse privée, tout est chiffré jusqu’à votre Machine. Le cloud ne fait que transmettre les données et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez autorisée sur sa page peut se connecter, avec les accès que vous avez choisis. Dans **Paramètres**, puis **Applis**, une IA connectée par l’application officielle porte la mention **App officielle**.

## Ce qu’elle peut voir

Une connexion ne voit que les données de son espace. Travail comprend les tâches et les promesses de vos comptes professionnels, vos contacts professionnels, vos entreprises, vos projets et le brief d’équipe de votre Fleet Travail. Personnel comprend le reste. Le texte des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cette option, une IA ne voit les sources d’une tâche qu’avec l’expéditeur, l’objet et la date.

Les fiches du Team Graph de vos collègues ne sont jamais transmises à une IA externe.

## Messages

**Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack, WhatsApp et vos autres chats. L’option est désactivée jusqu’à ce que vous l’activiez, sur la page où vous connectez l’IA ou plus tard dans **Paramètres**, puis **Applis**. L’IA ne fait que lire : elle n’envoie, ne supprime et ne marque rien.

Elle ne lit que les messages de son espace. Certains ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les conversations que The Machine a jugées sensibles (transactions, RH, questions juridiques, santé, finances), les conversations que vous avez gardées privées et les messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les conversations concernées, mais jamais leur texte. Votre Machine transmet le texte en le signalant comme une donnée, afin que l’IA ne suive pas les instructions écrites dans un message.

Tant que Messages est activé, les modifications du Graph proposées par une IA avec **Lecture et modification** attendent votre accord. Appuyez sur **Appliquer** ou **Écarter** sur la modification dans **Activité**.

## Dans les paramètres

Ouvrez **Paramètres**, puis **Applis**, pour voir chaque IA connectée, avec ses accès, son espace, sa date d’expiration et sa dernière utilisation. **Messages** s’active et se désactive au même endroit. Appuyez sur **Modifier** pour changer ses accès, son espace ou la durée de validité. La prochaine demande utilisera les nouveaux paramètres. **Activité** répertorie chaque demande, y compris celles qui ont été refusées. **Désactiver maintenant** met l’accès en pause : toutes les sessions sont interrompues, mais l’historique est conservé. **Retirer** supprime l’IA et son historique.

Si vous vous reconnectez à la même IA, la nouvelle autorisation remplace l’ancienne.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les accès et la durée de validité, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affiche qu’une fois. L’IA l’envoie sous la forme `Authorization: Bearer <key>`.

## Protéger votre compte

Chaque demande est consignée, y compris celles qui sont refusées. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion, donc une copie de ses données ne permet pas d’accéder à quoi que ce soit.
