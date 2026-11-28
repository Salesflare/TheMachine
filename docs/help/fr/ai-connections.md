---
title: Connecter d’autres IA
area: connections
summary: Donnez à Claude, ChatGPT, Cursor, Codex ou GBrain accès à vos tâches et à votre Graph. Avec Lecture et modification, elles peuvent aussi apporter des changements que vous pouvez annuler.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 3a7200b2a076c274
---
## Ce qu’une autre IA peut faire

Claude, ChatGPT, Cursor, Codex, GBrain et d’autres IA peuvent se connecter à votre Machine. Elles peuvent lire vos tâches, vos promesses, les briefs de votre équipe et les personnes et entreprises de votre Graph.

Avec **Lecture et modification**, elles peuvent aussi ajouter une tâche ou un brouillon d’e-mail, et mettre à jour votre Graph : enregistrer un fait, corriger des informations, des champs ou des tags, ou ajouter une ligne au résumé d’une personne.

Chaque changement apparaît dans **Activité**, avec l’option **Annuler**. Elles ne fusionnent, ne suppriment et ne partagent jamais de fiches. Ce qu’elles enregistrent est marqué **IA :** suivi de leur nom. Votre Machine le considère comme une affirmation de leur part, jamais comme une instruction de votre part.

Un brouillon reste en attente jusqu’à ce que vous le lisiez et appuyiez vous-même sur **Envoyer**. Une IA connectée n’envoie rien et n’agit jamais à votre place.

## Ce qu’elle apprend de vous

Au début d’un chat, l’IA reçoit un bref résumé : qui vous êtes, vos règles principales et les changements intervenus depuis sa dernière visite. Elle peut aussi lire ce qui se trouve dans **Apprentissage** : vos règles, les faits généraux et votre façon d’écrire sur chaque canal. Elle écrit ainsi comme vous.

Avec **Lecture et modification**, elle peut enregistrer ce que vous décidez dans le chat. Un fait est enregistré immédiatement, avec l’option **Annuler** dans **Activité**. Une règle guide le travail de votre Machine, alors elle reste dans **Apprentissage** jusqu’à ce que vous appuyiez sur **Approuver** ou **Écarter**. Elle ne change jamais votre façon d’écrire.

Un brouillon auquel il manque des éléments à remplir, qui mentionne un fichier qu’elle n’a pas ou qui contient uniquement votre adresse est renvoyé à l’IA pour qu’elle le corrige d’abord. Si une IA demande deux fois de suite la même tâche ou le même brouillon, vous n’en recevez qu’un.

## En connecter une

Ouvrez **Paramètres**, puis **Applis**. Sous **Les applis The Machine** se trouvent **Ajouter dans ChatGPT** et **Ajouter dans Claude**. Sous **Ou ajoutez-la avec une adresse** se trouvent l’adresse unique de l’app officielle pour toutes les Machines, `https://mcp.themachine.computer/mcp`, et **Votre adresse**, `https://<your name>.mcp.themachine.computer/mcp`, chacune avec l’option **Copier**.

Sur une Machine installée sur votre ordinateur, appuyez d’abord sur **Configurer**, sous **Obtenir votre adresse**. Une page de votre compte s’ouvre : vérifiez que le code affiché est le même, confirmez et choisissez un nom. Votre Machine se connecte automatiquement, sans redémarrer. Cette étape est nécessaire dans les deux cas.

Votre Machine configure ensuite automatiquement son adresse sécurisée. Cela prend quelques minutes.

Pour Claude, appuyez sur **Ajouter dans Claude** ou ouvrez [The Machine dans l’annuaire de Claude](https://claude.ai/directory/the-machine), puis appuyez sur **Connecter**. Avec Team et Enterprise, une personne propriétaire doit l’ajouter dans les paramètres de l’organisation.

La compétence de The Machine indique à Claude quand utiliser votre Machine : d’abord le brief, puis vos règles et votre ton, avant de rédiger quoi que ce soit. Appuyez sur **Télécharger** à côté de **Compétence Claude**, puis dans Claude, ouvrez **Personnaliser**, **Compétences** et importez-la.

Pour utiliser une adresse dans Claude, ouvrez plutôt **Personnaliser**, **Connecteurs**, appuyez sur **+ Ajouter**, puis sur **Ajouter un connecteur personnalisé**. Nommez-le The Machine, collez l’adresse, appuyez sur **Continuer**, puis sur **Ajouter**.

Pour ChatGPT, appuyez sur **Ajouter dans ChatGPT** ou ouvrez [The Machine dans ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), puis appuyez sur **Installer le plugin**. Avec Business et Enterprise, une personne administratrice doit parfois d’abord l’autoriser.

L’app officielle permet de se connecter à une Machine hébergée, ainsi qu’à une Machine installée sur votre ordinateur une fois son adresse configurée.

Pour utiliser votre adresse privée ou une Machine qui n’est pas sur le Network, ajoutez plutôt un serveur MCP personnalisé dans ChatGPT : ouvrez chatgpt.com/plugins, appuyez sur **+**, puis sur **Ajouter un serveur MCP personnalisé**. Nommez-le The Machine, collez l’adresse et choisissez OAuth. Confirmez l’avertissement, puis appuyez sur **Créer en tant que plugin**. Votre forfait ou espace de travail doit autoriser les serveurs MCP personnalisés.

Avec l’app officielle, l’IA vous demande de vous connecter à votre compte The Machine. Si vous avez plusieurs Machines, choisissez celle-ci, puis autorisez la connexion sur la page de votre Machine. Avec l’adresse privée, l’IA se connecte directement à votre Machine.

Les IA sur un appareil de votre réseau privé (Tailscale), comme Claude Code ou Cursor, peuvent aussi utiliser l’adresse de votre tableau de bord suivie de `/mcp`. **Dissocier cette Machine**, en bas de **Paramètres**, **Compte**, retire également une Machine installée sur votre ordinateur de votre compte.

Votre Machine indique quelle IA essaie de se connecter. Si elle ne peut pas le savoir, elle indique l’origine de la demande : ne vous connectez que si vous venez de lancer cette action.

Choisissez ce qu’elle peut faire : **Lire** ou **Lecture et modification**. Si vous avez des comptes Travail et Personnel, choisissez ce qu’elle peut voir. Choisissez ensuite la durée : **1 jour**, **7 jours**, **30 jours** ou **1 an**. Appuyez sur **Connecter**, ou sur **Annuler** pour refuser la demande.

## App officielle ou adresse privée

L’app officielle est la solution la plus simple : une seule adresse pour tout le monde, et votre compte trouve votre Machine. Notre cloud transmet les demandes sans jamais enregistrer leur contenu.

Avec votre adresse privée, tout est chiffré jusqu’à votre Machine. Le cloud se contente de transmettre les demandes et ne peut pas les lire.

Dans les deux cas, c’est votre Machine qui décide. Seule une IA que vous avez autorisée sur sa page peut se connecter, avec les accès que vous avez choisis. Dans **Paramètres**, **Applis**, une IA connectée par l’app officielle est indiquée comme **App officielle**.

## Ce qu’elle voit

Une connexion ne voit que son périmètre. Travail comprend les tâches et les promesses de vos comptes professionnels, les personnes, les entreprises et les projets professionnels, ainsi que le brief d’équipe de votre Fleet Travail. Personnel comprend le reste. Le texte des messages reste sur votre Machine, sauf si vous activez **Messages** : sans cette option, une IA ne voit les sources d’une tâche qu’avec l’expéditeur, l’objet et la date.

Les fiches du Graph d’équipe de vos collègues ne sont jamais transmises à une IA externe.

## Messages

**Messages** permet à une IA de rechercher et de lire vos e-mails, vos messages Slack et WhatsApp, ainsi que vos autres chats. L’option reste désactivée tant que vous ne l’activez pas, sur la page où vous connectez l’IA ou plus tard dans **Paramètres**, **Applis**. L’IA peut uniquement lire : elle n’envoie rien, ne supprime rien et ne marque rien.

Elle ne lit que les messages de son périmètre. Certains messages ne sont jamais transmis : les codes à usage unique et les liens de connexion, les messages d’un tableau ou d’un projet **Vous seul**, les fils que The Machine a jugés sensibles (transactions, RH, juridique, santé, argent), les fils que vous avez gardés privés et les messages supprimés.

Chaque lecture apparaît dans son **Activité**, avec le nombre de messages et les fils concernés, jamais leur contenu. Votre Machine transmet le texte en tant que données, afin que l’IA ne suive pas les instructions écrites dans un message.

Tant que Messages est activé, les changements apportés au Graph par une IA autorisée pour **Lecture et modification** restent en attente de votre accord. Appuyez sur **Appliquer** ou **Écarter** pour accepter ou refuser le changement dans **Activité**.

## Événements

**Événements** permet à une IA comme ChatGPT de se lancer automatiquement quand quelque chose se produit : une nouvelle tâche, un brief de réunion pour le lendemain ou une promesse qui arrive à échéance le lendemain. Chaque événement reste désactivé jusqu’à ce que vous l’activiez sous **Modifier**. L’IA reçoit alors son titre et une courte explication, rien qu’elle ne puisse déjà lire, et jamais d’informations antérieures à l’événement.

Elle ne peut toujours rien envoyer, et ses changements apparaissent dans **Activité**, avec l’option **Annuler**. Désactiver un événement ou l’IA l’arrête immédiatement.

## Dans les paramètres

Ouvrez **Paramètres**, puis **Applis**, pour voir chaque IA connectée, avec ses accès, son périmètre, sa date d’expiration et sa dernière utilisation. Vous pouvez activer ou désactiver **Messages** au même endroit. Appuyez sur **Modifier** pour changer les accès, le périmètre ou la durée. La prochaine demande utilisera ces nouveaux paramètres. **Activité** répertorie chaque demande, y compris celles qui ont été refusées. **Désactiver maintenant** suspend l’IA : toutes ses sessions sont fermées, mais son historique est conservé. **Retirer** supprime l’IA et son historique.

Si vous vous reconnectez à la même IA, la nouvelle autorisation remplace la précédente. Si cette IA était déjà connectée ailleurs, elle reste connectée avec les nouveaux accès. Une IA que vous utilisez reste connectée jusqu’à la date d’expiration ; si vous ne l’utilisez pas pendant 90 jours, vous devrez vous reconnecter.

Une IA qui ne peut pas se connecter seule peut utiliser une clé. Sous **Ajouter une clé**, donnez-lui un nom, choisissez les accès et la durée, puis appuyez sur **Créer la clé**. Copiez la clé tout de suite : elle ne s’affichera qu’une seule fois. L’IA l’envoie sous la forme `Authorization: Bearer <key>`.

## Garder vos données en sécurité

Chaque demande est enregistrée, y compris celles qui sont refusées. Une connexion expirée ou désactivée est refusée jusqu’à ce que vous la modifiiez. Votre Machine ne conserve qu’une empreinte de chaque connexion : une copie de ses données ne permet donc pas d’accéder à quoi que ce soit.
