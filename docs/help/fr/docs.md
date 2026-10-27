---
title: Google Docs et Word
area: connections
summary: Commentaires, mentions, suggestions de modification et partages sur vos fichiers Google Docs ou Word. Il lit, et ne publie une réponse à un commentaire qu’avec votre accord.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
---
## Ce qu’il lit

Docs utilise la connexion Google ou Microsoft que vous avez déjà pour cette adresse. Il récupère :

- Les documents que quelqu’un partage avec vous.
- Les commentaires et réponses sur vos documents, et les commentaires qui vous mentionnent.
- Les suggestions de modification sur vos Google Docs, et les modifications suivies dans vos fichiers Word.

La première synchro remonte 30 jours en arrière. Chaque élément devient un événement, lié aux personnes et projets de votre [Graph](graph.md). Quand un commentaire a besoin de vous, il devient une tâche.

## Ce qu’il peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document uniquement, et seulement pendant qu’elle travaille sur cette tâche.

Il peut rédiger une réponse à un commentaire. Sur Google Docs, la réponse attend dans la tâche : appuyez sur **Relire et publier**, vérifiez-la, puis **Publier maintenant**. Rien n’est publié avant. Les fichiers Word ne permettent pas de publier une réponse depuis l’extérieur de Word, donc ces réponses restent des brouillons à copier dans Word.

Il ne modifie jamais un document, n’accepte jamais une suggestion, ne résout jamais un commentaire et ne partage jamais un fichier.

## Ce qu’il demande

La lecture des documents demande son propre accord, à part de votre connexion e-mail. Vos accès Gmail et agenda restent tels quels.

- Google : accès en lecture seule à vos fichiers Drive et à leurs commentaires. Publier des réponses demande un accord de plus, que vous pouvez ignorer.
- Microsoft : accès en lecture à vos fichiers, y compris ceux partagés avec vous dans OneDrive et SharePoint.

Si cet accord est retiré plus tard, la carte Docs indique **En attente de votre accord pour lire les documents**.

## Le connecter

Sur une Machine hébergée, Docs apparaît sous **+ Ajouter** dès que votre page de configuration le propose.

Sur votre propre ordinateur :

1. Connectez d’abord Gmail ou Outlook pour cette adresse.
2. Ouvrez **Connexions**, puis **+ Ajouter**, choisissez Docs et saisissez cette adresse. Ou lancez `assistant connect docs`.
3. Il vérifie que votre connexion peut lire les documents. Sans cet accord, il n’est pas ajouté.

## Travail ou perso

Docs suit l’étiquette travail ou perso de sa connexion, comme les e-mails. Les documents de travail peuvent rejoindre le Graph de votre équipe selon vos [règles de partage](sharing-rules.md). Les documents perso, jamais.

## Le retirer

Dans le tableau de bord : **Connexions**, ouvrez Docs, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
