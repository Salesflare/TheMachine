---
title: Docs : Word, OneDrive et SharePoint
area: connections
summary: Commentaires, mentions, modifications suivies et partages sur vos fichiers Word dans OneDrive et SharePoint. Google Docs viendra plus tard.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
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

Il n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais un fichier et ne modifie jamais un document sans votre accord.

## Créer et modifier des documents

Votre Machine peut écrire un nouveau document Word, ou modifier un document dont parle l’une de vos tâches. Elle n’écrit jamais d’elle-même :

- Elle prépare la modification dans la tâche. Un nouveau document s’affiche en entier. Une modification montre chaque paragraphe avant et après.
- Touchez **Relire et créer** ou **Relire les modifications**, lisez, puis **Créer** ou **Enregistrer**.
- Elle écrit une seule fois, et seulement dans le document tel que vous l’avez vu. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche le dit. Demandez un nouveau brouillon.
- Dans Talk, elle lit toute la modification à voix haute et attend un oui clair.

Elle remplace du texte, ajoute du texte et ajoute des paragraphes et des titres. Elle ne touche pas aux tableaux, images, modifications suivies et champs. Un nouveau document arrive dans votre OneDrive et reste privé tant que vous ne le partagez pas.

Pour l’activer, touchez **Autoriser les modifications** sur la carte Docs dans **Connexions**. Microsoft demande l’autorisation de modifier vos fichiers, à part de la lecture. Se reconnecter la conserve.

## Ce qu’il demande

La lecture des documents demande son propre accord, à part de votre connexion e-mail : Microsoft vous demande d’autoriser la lecture de vos fichiers, y compris ceux partagés avec vous dans OneDrive et SharePoint. Vos accès e-mail et agenda restent tels quels.

Si cet accord est retiré plus tard, la carte Docs indique **En attente de votre accord pour lire les documents**.

## Le connecter

Connectez d’abord Outlook pour cette adresse. Ensuite :

- Machine hébergée : dans le tableau de bord, ouvrez **Connexions**, **+ Ajouter**, choisissez **Documents** et appuyez sur **Se connecter avec Microsoft**. Microsoft vous demande d’autoriser la lecture de vos fichiers, puis vous revenez au tableau de bord.
- Votre propre ordinateur, associé à votre compte : ouvrez **Connexions**, **+ Ajouter**, choisissez **Documents** et appuyez sur **Se connecter avec Microsoft**.

Il vérifie que la connexion peut lire les documents. Sans cet accord, il n’est pas ajouté.

## Travail ou perso

Docs suit l’étiquette travail ou perso de sa connexion, comme les e-mails. Les documents de travail peuvent rejoindre le Graph de votre équipe selon vos [règles de partage](sharing-rules.md). Les documents perso, jamais.

## Le retirer

Dans le tableau de bord : **Connexions**, ouvrez Docs, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
