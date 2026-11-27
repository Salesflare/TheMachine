---
title: Connecter d’autres IA
area: connections
summary: Autorisez Claude, ChatGPT, Cursor, Codex ou GBrain à lire vos tâches et votre Graph. Avec Lecture et modification, elles peuvent aussi apporter des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: acdce4a5793f7c67
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, les briefs de votre équipe, ainsi que les personnes et les entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail, et mettre à jour votre Graph : enregistrer une information, corriger des détails, des champs et des tags, ou ajouter une ligne au résumé d’une personne.

Chaque modification apparaît dans **Activité**, avec **Annuler**. Les IA ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent porte la mention **AI:** suivie de leur nom. Votre Machine le considère comme une affirmation de leur part, jamais comme une instruction de votre part.

Un brouillon reste en attente jusqu’à ce que vous le lisiez et appuyiez vous-même sur Envoyer. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place.

Un brouillon auquel il manque des éléments à compléter, qui mentionne un fichier qu’elle n’a pas, ou qui ne contient que votre propre adresse, est renvoyé à l’IA pour qu’elle le corrige. Si une IA demande deux fois de suite la même tâche ou le même brouillon, vous n’en recevez qu’un.

## Connecter une IA

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine**, vous trouverez **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse**, vous trouverez l’adresse unique de l’app officielle pour toutes les Machines, `https://mcp.themachine.computer/mcp`, et **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, chacune avec **Copier**.

Sur une Machine installée sur votre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page de votre compte s’ouvre : vérifiez que le code affiché est le même, confirmez, puis choisissez un nom. Votre Machine s’associe automatiquement, sans redémarrage. Cette étape est nécessaire dans les deux cas.

Votre Machine configure ensuite automatiquement son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans le répertoire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur Connecter. Avec les offres Team et Enterprise, un propriétaire doit l’ajouter dans les paramètres de l’organisation.

Pour utiliser une adresse dans Claude à la place, ouvrez Customize, Connectors, appuyez sur + Add, puis sur Add custom connector. Nommez-le The Machine, collez l’adresse, appuyez sur Continue, puis sur Add.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur Install plugin. Avec les offres Business et Enterprise, un administrateur devra peut-être d’abord l’autoriser.

L’app officielle se connecte à une Machine hébergée, ainsi qu’à une Machine installée sur votre ordinateur une fois celle-ci dotée de son adresse.

Pour votre adresse privée, ou pour une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Add custom MCP server. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement, puis appuyez sur Create as a plugin. Votre forfait ou votre espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’app officielle, l’IA vous demande de vous connecter à votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis approuvez la connexion sur la page de votre Machine. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA utilisées sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. **Dissocier cette Machine**, en bas de **Paramètres**, puis **Compte**, retire de nouveau de votre compte une Machine installée sur votre ordinateur.

Votre Machine indique quelle IA fait la demande. Si elle ne peut pas l’identifier, elle indique l’origine de la demande. Connectez-la uniquement si vous venez de lancer vous-même cette action.

Choisissez ce qu’elle peut faire : **Lire** ou **Lecture et modification**. Si vous avez des comptes Work et Personal, choisissez ce à quoi elle peut accéder. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Connecter**, ou sur **Annuler** pour refuser la connexion.

## App officielle ou adresse privée

L’app officielle est la solution la plus simple : tout le monde utilise la même adresse, et votre compte trouve votre Machine. Notre cloud transmet les requêtes sans jamais stocker leur contenu.

Avec votre adresse privée, tout est chiffré jusqu’à votre Machine. Le cloud ne fait que transmettre les requêtes et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez autorisée sur sa page peut accéder à votre Machine, avec les droits que vous avez choisis. Dans **Paramètres**, puis **Applis**, une IA connectée par l’app officielle porte la mention **App officielle**.

## Ce qu’elle peut voir

Une connexion n’accède qu’à son périmètre. Work comprend les tâches et les promesses de vos comptes professionnels, les personnes, les entreprises et les projets professionnels, ainsi que le brief d’équipe de votre Fleet Travail. Personal couvre le reste. Le contenu des messages reste sur votre Machine, sauf si vous activez **Messages**. Sans cette option, une IA ne voit les sources d’une tâche qu’avec l’expéditeur, l’objet et la date.

Les fiches du Team Graph de vos collègues ne sont jamais transmises à une IA externe.

## Messages

**Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack, WhatsApp et vos autres chats. Cette option est désactivée jusqu’à ce que vous l’activiez, sur la page où vous connectez l’IA ou plus tard dans **Paramètres**, puis **Applis**. L’IA peut uniquement lire les messages. Elle ne les envoie pas, ne les supprime pas et ne les marque pas.

Elle ne lit que les messages de son périmètre. Certains ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les fils que The Machine a jugés sensibles (transactions, RH, questions juridiques, santé, argent), les fils que vous avez gardés privés et les messages supprimés.

Chaque lecture apparaît dans l’**Activité** de l’IA, avec le nombre de messages et les fils concernés, jamais leur contenu. Votre Machine transmet le contenu en le marquant comme une donnée, pour que l’IA ne suive pas les instructions présentes dans un message.

Lorsque **Messages** est activé, les modifications du Graph proposées par une IA ayant accès à **Lecture et modification** attendent votre accord. Appuyez sur **Appliquer** ou **Écarter** sur la modification dans **Activité**.

## Dans les paramètres

Ouvrez **Paramètres**, puis **Applis** pour voir chaque IA connectée, avec ses droits, son périmètre, sa date d’expiration et sa dernière utilisation. Vous pouvez activer et désactiver **Messages** au même endroit. Appuyez sur **Modifier** pour changer ses droits, son périmètre ou la durée de l’autorisation. Le prochain appel utilisera les nouveaux paramètres. **Activité** répertorie tous les appels, y compris ceux qui ont été refusés. **Désactiver maintenant** suspend l’accès : toutes les connexions prennent fin, mais l’historique est conservé. **Retirer** supprime l’IA et son historique.

Si vous vous connectez de nouveau à la même IA, la nouvelle autorisation remplace la précédente. Si cette IA était déjà connectée, elle le reste avec les nouveaux droits. Une IA que vous utilisez reste connectée jusqu’à la date d’expiration. Si vous ne l’utilisez pas pendant 90 jours, vous devrez vous connecter de nouveau.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les droits et la durée, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affiche qu’une seule fois. L’IA la transmet sous la forme `Authorization: Bearer <key>`.

## Protéger vos données

Tous les appels sont consignés, y compris ceux qui sont refusés. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion. Une copie de ses données ne permet donc pas d’accéder à quoi que ce soit.
