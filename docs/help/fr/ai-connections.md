---
title: Connecter d’autres IA
area: connections
summary: Permettez à Claude, ChatGPT, Cursor, Codex ou GBrain de lire vos tâches et votre Graph. Avec Lecture et modification, elles peuvent aussi apporter des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, les briefs d’équipe, ainsi que les personnes et les entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail, et mettre à jour votre Graph : enregistrer un fait, corriger des détails, des champs et des tags, ou ajouter une ligne au résumé d’une personne.

Chaque changement apparaît dans **Activité**, avec l’option **Annuler**. Elles ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent est marqué **AI:** et indique leur nom. Votre Machine le considère comme une affirmation de leur part, jamais comme une instruction de votre part.

Un brouillon attend que vous le lisiez et appuyiez vous-même sur Envoyer. Une IA connectée n’envoie jamais rien et n’agit jamais à votre place.

## En connecter une

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine**, vous trouverez **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse**, vous trouverez l’adresse de l’app officielle, la même pour chaque Machine, `https://mcp.themachine.computer/mcp`, ainsi que **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, chacune avec l’option **Copier**.

Si votre Machine est sur votre propre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page s’ouvre dans votre compte : vérifiez que le même code s’affiche, confirmez et choisissez un nom. Votre Machine s’associe automatiquement, sans redémarrer. Cette étape est nécessaire dans les deux cas.

Votre Machine configure ensuite automatiquement son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans le répertoire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur Connect. Avec Team et Enterprise, un propriétaire doit l’ajouter dans les paramètres de l’organisation.

Pour utiliser une adresse dans Claude à la place, ouvrez Customize, puis Connectors, appuyez sur + Add, puis sur Add custom connector. Nommez-la The Machine, collez l’adresse, appuyez sur Continue, puis sur Add.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur Install plugin. Avec Business et Enterprise, un administrateur devra peut-être d’abord l’autoriser.

L’app officielle se connecte à une Machine hébergée, et à une Machine sur votre propre ordinateur une fois qu’elle a son adresse.

Pour utiliser votre adresse privée, ou une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Add custom MCP server. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement, puis appuyez sur Create as a plugin. Votre forfait ou espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’app officielle, l’IA vous demande de vous connecter avec votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis autorisez la connexion sur sa propre page. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA installées sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord, suivie de `/mcp`. L’option **Dissocier cette Machine**, en bas de **Paramètres**, puis **Compte**, retire de nouveau de votre compte une Machine installée sur votre propre ordinateur.

Votre Machine vous indique quelle IA essaie de se connecter. Si elle ne peut pas l’identifier, elle indique l’origine de la demande : connectez-vous uniquement si vous venez de lancer cette action vous-même.

Choisissez ce qu’elle peut faire : **Lire** ou **Lecture et modification**. Si vous avez des comptes Travail et Personnel, choisissez ce qu’elle peut voir. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Se connecter**, ou sur **Annuler** pour refuser la connexion.

## App officielle ou adresse privée

L’app officielle est la solution la plus simple : une seule adresse pour tout le monde, et votre compte trouve votre Machine. Notre cloud transmet les demandes et ne stocke rien.

Avec votre adresse privée, tout est chiffré jusqu’à votre Machine. Le cloud se contente de transmettre les demandes et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez autorisée sur sa page peut accéder à votre Machine, avec les droits que vous avez choisis. Dans **Paramètres**, puis **Applis**, une IA connectée par l’app officielle porte la mention **App officielle**.

## Ce qu’elle peut voir

Une connexion ne voit que son espace. Travail comprend les tâches et les promesses de vos comptes professionnels, les personnes, les entreprises et les projets professionnels, ainsi que le brief d’équipe de votre Fleet Travail. Personnel comprend tout le reste. Le texte des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cette option, une IA voit seulement l’expéditeur, l’objet et la date des messages associés à une tâche.

Les fiches du Graph d’équipe de vos collègues ne sont jamais transmises à une IA externe.

## Messages

L’option **Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack, WhatsApp et vos autres chats. Elle est désactivée jusqu’à ce que vous l’activiez, soit sur la page de connexion, soit plus tard dans **Paramètres**, puis **Applis**. L’IA peut uniquement lire les messages : elle ne les envoie, ne les supprime et ne les marque jamais.

Elle ne lit que les messages de son espace. Certains messages ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les fils que The Machine a jugés sensibles (transactions, RH, questions juridiques, santé, argent), les fils que vous avez gardés privés et les messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les fils concernés, jamais leur contenu. Votre Machine transmet le texte comme une donnée, pour que l’IA ne suive pas les instructions écrites dans un message.

Tant que Messages est activé, les changements apportés au Graph par une IA avec **Lecture et modification** attendent votre accord. Appuyez sur **Appliquer** ou **Écarter** pour accepter ou écarter le changement dans **Activité**.

## Dans Paramètres

Ouvrez **Paramètres**, puis **Applis**, pour voir chaque IA qui s’est connectée, avec ses droits, son espace, sa date d’expiration et sa dernière utilisation. Vous pouvez activer ou désactiver **Messages** au même endroit. Appuyez sur **Modifier** pour changer ses droits, son espace ou la durée d’accès. Le prochain appel utilisera ces nouveaux paramètres. **Activité** répertorie tous les appels, y compris ceux qui ont été refusés. **Désactiver maintenant** suspend l’accès : toutes les connexions sont interrompues, mais l’historique est conservé. **Retirer** supprime l’IA ainsi que son historique.

Si vous vous reconnectez à la même IA, la nouvelle autorisation remplace la précédente.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les droits et la durée, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affiche qu’une seule fois. L’IA l’envoie sous la forme `Authorization: Bearer <key>`.

## Protéger votre compte

Tous les appels sont consignés, y compris ceux qui sont refusés. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion, donc une copie de ces données ne permet pas d’accéder à quoi que ce soit.
