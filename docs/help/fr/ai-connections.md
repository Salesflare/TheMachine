---
title: Connecter d’autres IA
area: connections
summary: Permettez à Claude, ChatGPT, Cursor, Codex ou GBrain de lire vos tâches et votre Graph. Avec **Lecture et modification**, ces IA peuvent aussi faire des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 7681c632f712e93c
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, les briefs de votre équipe, ainsi que les personnes et les entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail et mettre à jour votre Graph : enregistrer un fait, corriger des informations, des champs et des tags, ou ajouter une ligne au résumé d’une personne.

Chaque changement apparaît dans **Activité**, avec **Annuler**. Elles ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent est marqué **IA :** avec leur nom. Votre Machine le considère comme une affirmation de leur part, jamais comme une instruction de votre part.

Un brouillon attend que vous le lisiez et que vous appuyiez vous-même sur Envoyer. Une IA connectée n’envoie rien et n’agit jamais à votre place.

## Ce qu’elle apprend de vous

Au début d’un chat, l’IA reçoit un bref résumé : qui vous êtes, vos règles principales et ce qui a changé depuis sa dernière visite. Elle peut aussi lire le contenu d’**Apprentissage** : vos règles, des faits généraux et votre façon d’écrire sur chaque canal. Elle peut ainsi écrire comme vous.

Avec **Lecture et modification**, elle peut enregistrer ce que vous décidez dans le chat. Un fait est ajouté immédiatement, avec **Annuler** dans **Activité**. Une règle influence le travail de votre Machine, alors elle reste dans **Apprentissage** jusqu’à ce que vous appuyiez sur **Approuver** ou **Écarter**. Elle ne modifie jamais votre façon d’écrire.

Un brouillon auquel il manque quelque chose, qui mentionne un fichier qu’elle n’a pas, ou qui ne contient que votre propre adresse est renvoyé à l’IA pour correction. Si une IA demande deux fois de suite la même tâche ou le même brouillon, vous n’en recevez qu’un seul.

## En connecter une

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine**, vous trouverez **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse** se trouvent l’adresse de l’app officielle, la même pour chaque Machine, `https://mcp.themachine.computer/mcp`, et **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, chacune avec l’option **Copier**.

Sur une Machine installée sur votre propre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page de votre compte s’ouvre : vérifiez que le même code s’y affiche, confirmez et choisissez un nom. Votre Machine s’associe automatiquement, sans redémarrer. Les deux méthodes nécessitent cette étape.

Votre Machine configure ensuite automatiquement son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans le répertoire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur Connecter. Avec les forfaits Team et Enterprise, un propriétaire doit l’ajouter dans les paramètres de l’organisation.

La compétence de The Machine indique à Claude quand utiliser votre Machine : d’abord le brief, puis vos règles et votre ton avant de rédiger quoi que ce soit. Appuyez sur **Télécharger**, à côté de **Compétence Claude**, puis dans Claude, ouvrez Customize, Skills et importez-la.

Pour utiliser une adresse dans Claude à la place, ouvrez Customize, Connectors, appuyez sur + Add, puis sur Add custom connector. Nommez-la The Machine, collez l’adresse, appuyez sur Continue, puis sur Add.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur Install plugin. Avec les forfaits Business et Enterprise, un administrateur devra peut-être d’abord l’autoriser.

L’app officielle permet de se connecter à une Machine hébergée et à une Machine installée sur votre propre ordinateur, une fois qu’elle a son adresse.

Pour votre adresse privée ou une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur +, puis sur Add custom MCP server. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement et appuyez sur Create as a plugin. Votre forfait ou espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’app officielle, l’IA vous demande de vous connecter à votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis approuvez la connexion sur la page de votre Machine. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. L’option **Dissocier cette Machine**, en bas de **Paramètres**, puis **Compte**, permet de retirer à nouveau de votre compte une Machine installée sur votre propre ordinateur.

Votre Machine indique quelle IA fait la demande. Si elle ne peut pas l’identifier, elle indique l’origine de la demande : ne vous connectez que si vous venez de lancer cette action vous-même.

Choisissez ce qu’elle peut faire : **Lire** ou **Lecture et modification**. Si vous avez des comptes Travail et Personnel, choisissez ce à quoi elle peut accéder. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Connecter**, ou sur **Annuler** pour refuser la demande.

## App officielle ou adresse privée

L’app officielle est la solution la plus simple : une seule adresse pour tout le monde, et votre compte trouve votre Machine. Notre cloud transmet les demandes et n’enregistre jamais leur contenu.

Avec votre adresse privée, tout est chiffré jusqu’à votre Machine. Le cloud se contente de transmettre les demandes et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez approuvée sur sa page peut accéder à votre Machine, avec les autorisations que vous avez choisies. Dans **Paramètres**, puis **Applis**, une IA connectée par l’app officielle porte la mention **App officielle**.

## Ce qu’elle voit

Une connexion ne donne accès qu’à son espace. L’espace Travail couvre les tâches et les promesses de vos comptes professionnels, les personnes, les entreprises et les projets professionnels, ainsi que le brief d’équipe de votre Fleet Travail. L’espace Personnel couvre le reste. Le contenu des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cette option, une IA ne voit les sources d’une tâche qu’à travers l’expéditeur, l’objet et la date.

Les fiches du Graph d’équipe de vos collègues ne sont jamais transmises à une IA externe.

## Messages

**Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack et WhatsApp, ainsi que vos autres chats. Cette option est désactivée jusqu’à ce que vous l’activiez, sur la page de connexion ou plus tard dans **Paramètres**, puis **Applis**. L’IA peut uniquement lire : elle n’envoie rien, ne supprime rien et ne marque rien.

Elle ne lit que les messages de son espace. Certains messages ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les fils que The Machine juge sensibles (transactions, RH, juridique, santé, argent), les fils que vous avez gardés privés et les messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les fils concernés, jamais leur contenu. Votre Machine transmet le contenu en le signalant comme une donnée, afin que l’IA ne suive pas les instructions écrites dans un message.

Tant que Messages est activé, les modifications du Graph par une IA avec **Lecture et modification** attendent votre accord. Appuyez sur **Appliquer** ou **Écarter** pour accepter ou refuser la modification dans **Activité**.

## Dans les paramètres

Ouvrez **Paramètres**, puis **Applis** pour voir chaque IA qui s’est connectée, avec ses autorisations, son espace, sa date d’expiration et sa dernière utilisation. Vous pouvez activer ou désactiver **Messages** ici. Appuyez sur **Modifier** pour changer ses autorisations, son espace ou la durée d’accès. Les changements s’appliquent à la prochaine demande. **Activité** répertorie chaque demande, y compris celles qui ont été refusées. **Désactiver maintenant** suspend l’accès : toutes les connexions sont interrompues, mais l’historique est conservé. **Retirer** supprime l’accès et l’historique.

Si vous vous reconnectez à la même IA, la nouvelle autorisation remplace l’ancienne. Si cette IA était déjà connectée, elle reste connectée avec les nouvelles autorisations. Une IA que vous utilisez reste connectée jusqu’à la date d’expiration. Si vous ne l’utilisez pas pendant 90 jours, vous devrez vous reconnecter.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les autorisations et la durée, puis appuyez sur **Créer la clé**. Copiez la clé immédiatement : elle ne s’affiche qu’une seule fois. L’IA l’envoie sous la forme `Authorization: Bearer <key>`.

## Protéger votre compte

Chaque demande est consignée, y compris celles qui sont refusées. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion : une copie de ses données ne permet donc pas d’accéder à votre compte.
