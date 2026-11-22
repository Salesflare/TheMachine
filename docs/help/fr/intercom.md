---
title: Intercom
area: connections
summary: Les conversations clients de votre espace de travail Intercom. Elle répond en votre nom uniquement après votre envoi.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 2cbee87e6d24c0a9
---
## Ce qu’elle lit

Les conversations clients de votre espace de travail Intercom : celles des 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. Elle lit aussi l’espace de travail et le nom du coéquipier associés à la connexion.

## Ce qu’elle peut faire

Avec votre propre connexion **Se connecter avec Intercom**, elle peut répondre en votre nom dans une conversation, uniquement après que vous avez appuyé sur **Envoyer** pour ce texte précis. Elle n’attribue, ne clôture et ne balise jamais les conversations, et n’y ajoute pas de notes. Une connexion Intercom partagée avec vous via votre Fleet ne fait que lire.

## Tâches issues d’Intercom

Une tâche issue d’Intercom indique le client. **Lire le message** ouvre la conversation et contient un lien vers celle-ci dans Intercom. La réponse est envoyée dans cette conversation, sauf si vous demandez un e-mail.

Seules les conversations qui vous sont attribuées, ou qui ne le sont encore à personne, deviennent des tâches. Lorsqu’un coéquipier en prend une dans Intercom, la tâche se ferme automatiquement et vous pouvez utiliser **Annuler**. Sur une connexion Intercom partagée avec vous, vos conversations sont celles attribuées au coéquipier au nom duquel vous écrivez.

Une tâche Intercom se ferme aussi automatiquement dès qu’un membre de l’équipe clôture la conversation dans Intercom, ou y répond et que le client n’a pas écrit depuis, si la tâche demandait uniquement une réponse. C’est aussi le cas si vous avez répondu juste avant la création de la tâche, avant que The Machine ne lise votre réponse. Une note, une mise en attente ou la réponse d’un bot ne compte jamais.

Lorsque votre Machine ne peut pas répondre dans Intercom (connexion partagée en lecture seule, réponses désactivées ou absence de connexion), le brouillon est envoyé par e-mail à la place. La tâche en indique la raison et vous demande **Envoyer plutôt par e-mail ?** Pour répondre dans Intercom, appuyez sur **Connectez votre propre Intercom** dans la tâche et connectez-vous. La tâche est alors recréée sous forme de réponse dans Intercom. Rien n’est envoyé avant que vous l’envoyiez.

Votre propre connexion Intercom et une connexion partagée avec vous pour le même espace de travail ne lisent pas toutes les deux : la connexion partagée reste inactive et ses conversations passent dans la vôtre, sans doublons.

## Connecter Intercom

1. Dans le tableau de bord : **Connexions**, **Clients**, Intercom. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Intercom. Sur votre propre ordinateur, associez d’abord la Machine à votre compte.
2. Appuyez sur **Se connecter avec Intercom**.
3. Autorisez The Machine (créée par Salesflare) dans Intercom. Vous reviendrez à la page de départ.

La connexion à un autre espace de travail ajoute un deuxième compte Intercom.

Intercom est toujours considéré comme professionnel, pour l’entreprise indiquée par le nom de son espace de travail.

## Supprimer Intercom

- Dans le tableau de bord : **Connexions**, ouvrez Intercom, puis **Détails** et **Déconnecter**. La lecture s’arrête. Les éléments déjà importés restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté d’Intercom sur la page de configuration.

## Désinstaller l’application dans Intercom

Dans Intercom, ouvrez **Paramètres**, **Applications**, **Applications installées**, puis supprimez The Machine.
