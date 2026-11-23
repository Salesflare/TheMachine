---
title: Intercom
area: connections
summary: Les conversations avec vos clients dans votre espace Intercom. Elle ne répond qu’après votre envoi, en votre nom.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## Ce qu’elle lit

Les conversations avec vos clients dans votre espace Intercom : celles des 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. Elle lit aussi le nom de l’espace de travail et du collègue associés à la connexion.

## Ce qu’elle peut faire

Avec votre propre **Se connecter avec Intercom**, elle peut répondre en votre nom dans une conversation, mais uniquement après que vous avez appuyé sur **Envoyer** pour ce texte précis. Elle n’attribue, ne ferme et ne classe jamais les conversations, et n’y ajoute pas de notes. Une connexion Intercom partagée avec vous via votre Fleet ne fait que lire les conversations.

## Tâches provenant d’Intercom

Une tâche Intercom affiche le client, et **Lire le message** ouvre la conversation avec un lien vers celle-ci dans Intercom. Chaque message est affiché sous le nom de son auteur : le client d’un côté, votre équipe et son bot de l’autre, y compris lorsqu’un collègue ou une campagne a lancé la conversation. La réponse est envoyée dans cette conversation, sauf si vous demandez à l’envoyer par e-mail.

Seules les conversations qui vous sont attribuées, ou qui ne le sont encore à personne, deviennent des tâches. Lorsqu’un collègue prend une conversation dans Intercom, la tâche se ferme automatiquement, avec la possibilité d’utiliser **Annuler**. Sur une connexion Intercom partagée avec vous, vos conversations sont celles qui sont attribuées au collègue au nom duquel vous écrivez.

Une tâche Intercom se ferme aussi automatiquement lorsqu’un membre de l’équipe ferme la conversation dans Intercom, ou y répond sans que le client ait écrit depuis, si la tâche demandait uniquement une réponse. C’est aussi le cas si vous avez répondu juste avant la création de la tâche, avant que The Machine ne lise votre réponse. Une note, une mise en attente ou une réponse du bot ne compte jamais.

Lorsque votre Machine ne peut pas répondre dans Intercom (connexion partagée en lecture seule, réponses désactivées ou absence de connexion), la réponse est préparée par e-mail à la place. La tâche en indique la raison et vous demande **Envoyer plutôt par e-mail ?** Pour répondre dans Intercom, appuyez sur **Connecter votre propre Intercom** dans la tâche, puis connectez-vous. La tâche est alors réécrite sous forme de réponse dans Intercom. Rien n’est envoyé avant que vous ne l’envoyiez.

Votre propre connexion Intercom et une connexion partagée avec vous pour le même espace de travail ne lisent pas toutes les deux les conversations : la connexion partagée reste inactive et ses conversations sont transférées vers la vôtre, une seule fois chacune.

## Connecter Intercom

1. Dans le tableau de bord : **Connexions**, **Clients**, Intercom. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Intercom. Sur votre propre ordinateur, associez d’abord la Machine à votre compte.
2. Appuyez sur **Se connecter avec Intercom**.
3. Autorisez The Machine (créée par Salesflare) dans Intercom. Vous revenez ensuite à l’endroit où vous étiez.

Si vous vous connectez à un autre espace de travail, un deuxième compte Intercom est ajouté.

Intercom est toujours considéré comme professionnel, pour l’entreprise indiquée par le nom de son espace de travail.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Intercom, puis **Détails** et **Déconnecter**. La connexion cesse de lire les conversations. Les données déjà importées restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté d’Intercom sur la page de configuration.

## Désinstaller l’app dans Intercom

Dans Intercom, ouvrez Paramètres, Applications, Applications installées, puis supprimez The Machine.
