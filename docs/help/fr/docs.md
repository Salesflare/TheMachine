---
title: Microsoft OneDrive : fichiers Word dans OneDrive et SharePoint
area: connections
summary: Commentaires, mentions, modifications suivies et partages sur vos fichiers Word dans OneDrive et SharePoint, ainsi que les nouveaux documents privés, et les modifications que vous approuvez.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Ce qu’il lit

La connexion **Microsoft OneDrive** lit les fichiers Word dans OneDrive et SharePoint. Vous vous connectez avec Microsoft pour elle, avec ou sans Outlook connecté. Cela fonctionne sur une Machine hébergée et sur votre propre ordinateur associé à votre compte. Pour Google Docs, voir plus bas. Il récupère :

- Les documents que quelqu’un partage avec vous.
- Les commentaires et réponses sur vos documents, et les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchro remonte 30 jours en arrière. Chaque élément devient un événement, lié aux personnes et projets de votre [Graph](graph.md). Quand un commentaire a besoin de vous, il devient une tâche.

## Ce qu’il peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document uniquement, et seulement pendant qu’elle travaille sur cette tâche.

Il peut rédiger une réponse à un commentaire. Les fichiers Word ne permettent pas de publier une réponse depuis l’extérieur de Word, donc la réponse reste un brouillon à copier dans Word.

Il n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais un fichier et ne modifie jamais un document sans votre accord.

Une connexion de documents peut seulement agir : désactivez **Apporte des signaux** sous **Détails**, et elle ne fait que trouver et lire les documents dont vos to-dos ont besoin, et en créer de nouveaux. Une connexion Google sans accès à tout Drive lit les documents par leur lien, et ceux que votre Machine a créés.

## Créer et modifier des documents

Votre Machine peut écrire un nouveau document, ou modifier un document dont parle l’une de vos tâches :

- Un nouveau document, elle le crée tout de suite, quand la tâche ou une compétence demande d’en créer un : un document privé dans votre propre Google Drive ou OneDrive, partagé avec personne. La tâche l’affiche avec **Ouvrir le document**. Le partager, ou envoyer son lien à quelqu’un, attend votre accord.
- Une modification d’un document existant, elle la prépare seulement, chaque paragraphe avant et après. Touchez **Relire les modifications**, lisez, puis **Enregistrer**. Une modification que vous demandez dans le chat de la tâche, elle la fait tout de suite.
- Elle écrit une modification une seule fois, et seulement dans le document tel que vous l’avez vu. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche le dit. Demandez un nouveau brouillon.
- Dans Talk, elle lit toute la modification à voix haute et attend un oui clair.
- Si Google ou Microsoft refuse un nouveau document, la tâche dit ce qui a été refusé et affiche **Relire et créer** pour réessayer.

Elle remplace du texte, ajoute du texte et ajoute des paragraphes et des titres. Elle ne touche pas aux tableaux, images, modifications suivies et champs. Un nouveau document arrive dans votre Google Drive ou OneDrive et reste privé tant que vous ne le partagez pas.

Un nouveau document va dans un compte du domaine de la tâche : le document d’une tâche Travail dans le compte de cette entreprise, celui de la conversation quand c’est possible, jamais dans un compte perso. Sur votre propre ordinateur, un compte Google connecté pour Gmail qui a déjà accès à Drive peut aussi recevoir un nouveau Google Doc. Si aucun compte ne convient, la tâche indique **Connectez Google Docs ou Microsoft OneDrive pour Travail**.

Quand le document n’est pas la fin de la tâche, par exemple une réponse avec son lien, la tâche reste ouverte et prépare cette étape suivante pour votre OK.

Connecter Microsoft OneDrive l’autorise déjà : il n’y a pas d’étape à part. Une ancienne connexion Microsoft OneDrive qui ne fait que lire affiche **Autoriser les modifications** sur sa carte dans **Connexions**. Touchez-le une fois et acceptez.

## Ce qu’il demande

Microsoft OneDrive demande un seul accord à Microsoft, à part de votre connexion e-mail : lire et modifier vos fichiers, y compris ceux partagés avec vous dans OneDrive et SharePoint. Chaque modification attend quand même votre OK dans sa tâche. Vos accès e-mail et agenda restent tels quels. Sans Outlook, la connexion ne couvre que vos fichiers, jamais vos e-mails ni votre agenda.

Si cet accord est retiré plus tard, la carte Microsoft OneDrive indique **En attente de votre accord pour lire les documents**.

## Le connecter

Outlook n’a pas besoin d’être connecté.

- Machine hébergée : dans le tableau de bord, ouvrez **Connexions**, **+ Ajouter**, choisissez **Microsoft OneDrive** et appuyez sur **Se connecter avec Microsoft**. Microsoft vous demande d’autoriser la lecture et la modification de vos fichiers, puis vous revenez au tableau de bord.
- Votre propre ordinateur, associé à votre compte : ouvrez **Connexions**, **+ Ajouter**, choisissez **Microsoft OneDrive** et appuyez sur **Se connecter avec Microsoft**.

Il vérifie que la connexion peut lire les documents. Sans cet accord, il n’est pas ajouté. Si vous touchez **Autoriser les modifications** et que Microsoft ne les autorise pas, il le dit au lieu d’afficher Connecté.

## Google Docs

Google Docs ne peut pas encore être connecté. Les lire demande une autorisation Google que The Machine ne demande pas encore. Ce qui marche aujourd’hui :

- Sur votre propre ordinateur, votre Machine peut créer un nouveau Google Doc dans un compte Gmail connecté sur cet ordinateur qui a déjà accès à Drive. Elle ne lit pas vos autres Google Docs ni leurs commentaires.
- Une Machine hébergée ne peut pas encore utiliser Google Docs.

## Travail ou perso

Microsoft OneDrive suit l’étiquette travail ou perso de sa connexion, comme les e-mails. Les documents de travail peuvent rejoindre le Graph de votre équipe selon vos [règles de partage](sharing-rules.md). Les documents perso, jamais.

## Le retirer

Dans le tableau de bord : **Connexions**, ouvrez Microsoft OneDrive, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
