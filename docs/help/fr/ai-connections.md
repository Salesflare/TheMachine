---
title: Connecter d’autres IA
area: connections
summary: Permettez à Claude, ChatGPT, Cursor, Codex ou GBrain de lire vos tâches et votre Graph. Avec **Lecture et modification**, elles peuvent aussi apporter des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: cf0776c294917228
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, vos synthèses d’équipe, ainsi que les personnes et les entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail, et mettre à jour votre Graph : enregistrer un fait, corriger des informations, des champs et des étiquettes, ou ajouter une ligne au résumé d’une personne.

Chaque changement apparaît dans **Activité**, avec **Annuler**. Elles ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent est marqué **IA :** avec leur nom. Votre Machine le considère comme leur affirmation, jamais comme une instruction de votre part.

Un brouillon attend que vous le lisiez et que vous appuyiez vous-même sur Envoyer. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place.

Un brouillon auquel il manque des éléments à remplir, qui mentionne un fichier qu’elle n’a pas, ou qui ne contient que votre propre adresse est renvoyé à l’IA pour correction. Si une IA demande deux fois de suite la même tâche ou le même brouillon, vous ne le recevez qu’une fois.

## En connecter une

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine**, vous trouverez **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse**, vous trouverez l’adresse unique de l’application officielle pour chaque Machine, `https://mcp.themachine.computer/mcp`, ainsi que **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, chacune avec **Copier**.

Sur une Machine installée sur votre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page de votre compte s’ouvre : vérifiez qu’elle affiche le même code, confirmez et choisissez un nom. Votre Machine s’associe automatiquement, sans redémarrage. Cette étape est nécessaire dans les deux cas.

Votre Machine configure ensuite elle-même son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans l’annuaire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur Connecter. Avec Team et Enterprise, un propriétaire doit l’ajouter dans les paramètres de l’organisation.

Pour utiliser une adresse dans Claude à la place, ouvrez Customize, Connectors, appuyez sur + Add, puis sur Add custom connector. Nommez-la The Machine, collez l’adresse, appuyez sur Continue, puis sur Add.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur Install plugin. Avec Business et Enterprise, un administrateur devra peut-être d’abord l’autoriser.

L’application officielle se connecte à une Machine hébergée et à une Machine installée sur votre ordinateur dès qu’elle dispose de son adresse.

Pour utiliser votre adresse privée, ou une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Add custom MCP server. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement et appuyez sur Create as a plugin. Votre forfait ou votre espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’application officielle, l’IA vous demande de vous connecter à votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis autorisez la connexion sur la page de votre Machine. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. **Dissocier cette Machine**, en bas de **Paramètres**, puis **Compte**, déconnecte de nouveau votre compte une Machine installée sur votre ordinateur.

Votre Machine vous indique quelle IA envoie la demande. Si elle ne peut pas l’identifier, elle indique l’origine de la demande. Ne la connectez que si vous venez de lancer cette opération vous-même.

Choisissez ce qu’elle peut faire : **Lire** ou **Lecture et modification**. Si vous avez des comptes professionnel et personnel, choisissez ce qu’elle peut consulter. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Connecter**, ou sur **Annuler** pour refuser sans rien envoyer.

## Application officielle ou adresse privée

L’application officielle est la solution la plus simple : une seule adresse pour tout le monde, et votre compte trouve votre Machine. Notre cloud relaie les demandes sans jamais enregistrer leur contenu.

Avec votre adresse privée, tout est chiffré de bout en bout jusqu’à votre Machine. Le cloud ne fait que relayer les demandes et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez autorisée sur sa page peut accéder à votre Machine, avec les droits que vous avez choisis. Dans **Paramètres**, puis **Applis**, une IA connectée par l’application officielle porte la mention **App officielle**.

## Ce qu’elle peut voir

Une connexion ne donne accès qu’à son espace. L’espace Travail comprend les tâches et les promesses de vos comptes professionnels, vos contacts professionnels, vos entreprises, vos projets et la synthèse d’équipe de votre Fleet Travail. L’espace Personnel comprend le reste. Le contenu des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cette option, une IA ne voit les sources d’une tâche qu’en fonction de l’expéditeur, de l’objet et de la date.

Les fiches du Graph d’équipe de vos collègues ne sont jamais transmises à une IA externe.

## Messages

**Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack et WhatsApp, ainsi que vos autres chats. Cette option est désactivée tant que vous ne l’activez pas, sur la page où vous connectez l’IA ou plus tard dans **Paramètres**, puis **Applis**. Elle permet uniquement de lire : l’IA n’envoie, ne supprime et ne marque jamais rien.

Elle ne lit que les messages de son espace. Certains messages ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les fils que The Machine a jugés sensibles (transactions, RH, juridique, santé, finances), les fils que vous avez gardés privés et les messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les fils concernés, jamais leur contenu. Votre Machine transmet le texte en le marquant comme une donnée, afin que l’IA ne suive pas les instructions écrites dans un message.

Tant que Messages est activé, les changements apportés à votre Graph par une IA avec **Lecture et modification** attendent votre approbation. Appuyez sur **Appliquer** ou **Écarter** pour le changement dans **Activité**.

## Dans les paramètres

Ouvrez **Paramètres**, puis **Applis**, pour voir une seule entrée par IA connectée, avec ses droits d’accès, son espace, sa date d’expiration et sa dernière utilisation. Vous pouvez activer ou désactiver **Messages** au même endroit. Appuyez sur **Modifier** pour changer ses droits d’accès, son espace ou la durée d’accès. Ces changements s’appliquent à la prochaine demande. **Activité** répertorie chaque demande, y compris celles qui ont été refusées. **Désactiver maintenant** suspend l’accès : toutes les sessions sont fermées, mais l’historique est conservé. **Retirer** supprime l’IA ainsi que son historique.

Si vous vous reconnectez à la même IA, la nouvelle autorisation remplace la précédente.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les droits d’accès et la durée, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affiche qu’une seule fois. L’IA l’envoie sous la forme `Authorization: Bearer <key>`.

## Protéger votre compte

Chaque demande est enregistrée, y compris celles qui ont été refusées. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion : une copie de ces données ne permet d’accéder à rien.
