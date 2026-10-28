---
title: Docs : Word, OneDrive et SharePoint
area: connections
summary: Commentaires, mentions, modifications suivies et partages sur vos fichiers Word dans OneDrive et SharePoint. Google Docs viendra plus tard.
covers: connector:docs
code: connectors/docs.py, next_actions.py, onboarding.py
site: More sources, Connect documents, Sign in with Microsoft
---
## Ce qu’il lit

Docs lit les fichiers Word dans OneDrive et SharePoint, avec la connexion Microsoft que vous avez déjà pour cette adresse. Cela fonctionne sur une Machine hébergée et sur votre propre ordinateur associé à votre compte. Google Docs viendra plus tard : la connexion Google de The Machine ne peut pas encore lire les documents. Il récupère :

- Les documents que quelqu’un partage avec vous.
- Les commentaires et réponses sur vos documents, et les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchro remonte 30 jours en arrière. Chaque élément devient un événement, lié aux personnes et projets de votre [Graph](graph.md). Quand un commentaire a besoin de vous, il devient une tâche.

## Ce qu’il peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document uniquement, et seulement pendant qu’elle travaille sur cette tâche.

Il peut rédiger une réponse à un commentaire. Les fichiers Word ne permettent pas de publier une réponse depuis l’extérieur de Word, donc la réponse reste un brouillon à copier dans Word.

Il ne modifie jamais un document, n’accepte jamais une suggestion, ne résout jamais un commentaire et ne partage jamais un fichier.

## Ce qu’il demande

La lecture des documents demande son propre accord, à part de votre connexion e-mail : Microsoft vous demande d’autoriser la lecture de vos fichiers, y compris ceux partagés avec vous dans OneDrive et SharePoint. Vos accès e-mail et agenda restent tels quels.

Si cet accord est retiré plus tard, la carte Docs indique **En attente de votre accord pour lire les documents**.

## Le connecter

Connectez d’abord Outlook pour cette adresse. Ensuite :

- Machine hébergée : sur votre page de configuration, ouvrez **Documents** sous **Plus de sources** et appuyez sur **Connecter les documents** à côté de cette adresse. Microsoft vous demande d’autoriser la lecture de vos fichiers.
- Votre propre ordinateur, associé à votre compte : ouvrez **Connexions**, **+ Ajouter**, choisissez **Documents** et appuyez sur **Se connecter avec Microsoft**.

Il vérifie que la connexion peut lire les documents. Sans cet accord, il n’est pas ajouté.

## Travail ou perso

Docs suit l’étiquette travail ou perso de sa connexion, comme les e-mails. Les documents de travail peuvent rejoindre le Graph de votre équipe selon vos [règles de partage](sharing-rules.md). Les documents perso, jamais.

## Le retirer

Dans le tableau de bord : **Connexions**, ouvrez Docs, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
