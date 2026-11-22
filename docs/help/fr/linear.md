---
title: Linear
area: connections
summary: Vos tickets Linear, mentions, commentaires, demandes de revue et échéances. Les commentaires, les changements de statut ou d’assignation et les nouveaux tickets attendent votre accord.
covers: connector:linear
code: connectors/linear.py, linear_writes.py
site: Sign in with Linear, Connect, More sources, Remove
translated: 1e16b6abdf4fefad
---
## Ce qu’elle lit

Votre boîte de réception Linear et les tickets qui vous sont attribués. Elle importe :

- Les tickets qui vous sont attribués : les nouveaux et ceux dont le statut, l’échéance ou le titre a changé. Quand un ticket est terminé ou annulé dans Linear, la tâche correspondante se ferme automatiquement. **Annuler** la rouvre.
- Les mentions de votre nom, ainsi que les commentaires et réponses sur les tickets que vous suivez.
- Les demandes de revue et les tickets ajoutés au triage.
- Les rappels d’échéance.

Chaque élément ne devient une tâche que lorsqu’il requiert votre attention, selon son contenu. Vos propres modifications ne sont jamais importées. La première synchronisation remonte à 7 jours. Les personnes sont associées à votre [Graph](graph.md) à l’aide de l’adresse e-mail que Linear affiche pour elles.

Pour l’utiliser uniquement pour agir, désactivez **Apporte des signaux** sous **Détails**.

## Ce qu’elle peut faire

Chacune de ces actions attend votre accord sur la tâche correspondante :

- Commenter le ticket concerné par la tâche, ou répondre dans le fil d’un commentaire. Le commentaire est publié en votre nom.
- Modifier le statut de ce ticket, en choisissant parmi ceux de son équipe.
- Attribuer le ticket à une personne de son équipe ou à vous-même.
- Créer un ticket dans l’une de vos équipes.

Elle ne supprime, n’archive ni ne déplace jamais un ticket vers une autre équipe.

## Connecter Linear

1. Dans le tableau de bord : **Connexions**, **+ Ajouter**, Linear. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Linear. Sur votre propre ordinateur, associez d’abord Linear à votre compte.
2. Appuyez sur **Se connecter avec Linear**, choisissez votre espace de travail et autorisez l’accès.
3. De retour dans The Machine, elle vérifie immédiatement la connexion et affiche le nom de l’espace de travail.

Pour ajouter un autre espace de travail, ajoutez Linear à nouveau. Choisissez **Travail** ou **Perso**, comme pour n’importe quelle connexion.

## Utiliser plutôt une clé API

Sous **Ou collez une clé API**, appuyez sur **Obtenir votre jeton**. Linear ouvre **Paramètres**, **Sécurité et accès** : créez une clé API personnelle, copiez-la, collez-la, puis appuyez sur **Connecter**. Sur votre propre ordinateur, `assistant connect linear` vous la demande aussi.

## Déconnecter Linear

- Dans le tableau de bord : **Connexions**, ouvrez Linear, puis **Détails** et **Déconnecter**. Les éléments déjà importés sont conservés.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Linear sur la page de configuration.

## Révoquer l’accès dans Linear

Dans Linear : **Paramètres**, **Sécurité et accès**, puis révoquez l’accès de The Machine dans les applications autorisées. Si vous avez collé une clé, révoquez-la sur la même page.
