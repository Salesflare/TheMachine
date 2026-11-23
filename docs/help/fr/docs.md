---
title: Microsoft OneDrive
area: connections
summary: Commentaires, mentions et modifications suivies dans vos fichiers Word sur OneDrive. Les nouveaux documents et les modifications attendent votre accord.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 41e5651f29782588
---
## Contenu consulté

**Microsoft OneDrive** lit vos fichiers Word dans OneDrive, sur une Machine hébergée ou sur votre propre ordinateur. Il n’est pas nécessaire de connecter Outlook. Pour Google Docs, consultez la section ci-dessous. Il importe :

- Les commentaires et les réponses dans vos fichiers Word, ainsi que les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchronisation remonte à 7 jours. Chaque élément renvoie aux personnes et aux projets de votre [Graph](graph.md). Un commentaire qui nécessite votre attention devient une tâche.

## Fichiers partagés avec vous

À partir de novembre 2026, Microsoft ne répertoriera plus ces fichiers. Les partages et les mentions dans les fichiers d’autres personnes n’arriveront alors sur votre Machine que dans les e-mails de Microsoft. Connectez aussi [Outlook](microsoft.md) et ne désactivez pas ces e-mails. Une tâche créée à partir de l’un de ces e-mails l’ouvre, et son bouton ouvre le fichier. Les partages et les mentions qui ne donnent pas lieu à un e-mail ne sont pas détectés.

## Ce que votre Machine peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document uniquement pendant qu’elle traite cette tâche. Elle peut lire les fichiers Word, PDF et texte.

Elle recherche aussi tous types de fichiers dans votre propre OneDrive et vous donne leur lien. Elle ne recherche pas dans les sites SharePoint ni dans les fichiers partagés avec vous. Elle ne peut pas lire le texte d’un PDF numérisé.

Elle peut rédiger une réponse à un commentaire. Word ne permet pas de publier des réponses depuis l’extérieur. Vous devez donc copier le brouillon dans Word.

Elle n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais de fichier et ne modifie jamais de document sans votre accord.

Pour l’utiliser uniquement pour effectuer des actions, désactivez **Apporte des signaux** sous **Détails**. Elle recherche et lit alors uniquement les fichiers nécessaires à vos tâches, et en crée de nouveaux.

## Créer et modifier des documents

Votre Machine peut créer un document ou modifier un document concerné par une tâche :

- Elle crée immédiatement un nouveau document si la tâche ou une compétence le demande. Il reste privé, dans votre propre OneDrive ou Google Drive. La tâche affiche **Ouvrir le document**. Le partage du document ou l’envoi de son lien attend votre accord.
- Elle prépare les modifications d’un document existant. Sélectionnez **Relire les modifications** pour voir chaque paragraphe avant et après, puis **Enregistrer**. Une modification que vous demandez dans le chat de la tâche est appliquée immédiatement.
- Elle écrit uniquement dans la version du document que vous avez consultée. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche vous en informe. Demandez un nouveau brouillon.
- Dans Talk, elle lit toute la modification à voix haute et attend votre accord explicite.
- Si Microsoft ou Google refuse de créer un document, la tâche en indique la raison et affiche **Relire et créer** pour réessayer.

Elle peut remplacer ou ajouter du texte, des paragraphes et des titres. Les tableaux, images, modifications suivies et champs restent inchangés.

Le document d’une tâche Travail est enregistré dans le compte de l’entreprise concernée, jamais dans un compte personnel. Sur votre propre ordinateur, un compte Google connecté à Gmail et ayant accès à Drive peut aussi servir à créer de nouveaux documents Google. Si aucun compte ne convient, la tâche vous indique ce qu’il faut connecter pour le travail : Microsoft OneDrive ou Google Docs, si votre Machine peut l’utiliser.

Si le document n’est pas la dernière étape, par exemple s’il faut envoyer une réponse avec son lien, la tâche reste ouverte et prépare cette étape pour que vous puissiez l’approuver.

La modification est incluse lors de la connexion. Une ancienne connexion qui permet seulement la lecture affiche **Autoriser les modifications** dans **Connexions**. Sélectionnez cette option une fois, puis acceptez.

## Autorisations demandées

Microsoft vous demande une seule autorisation : lire et modifier vos fichiers, y compris ceux qui sont partagés avec vous. Chaque modification attend toujours votre accord dans la tâche correspondante. L’accès à vos e-mails et à votre agenda ne change pas.

Si vous retirez ensuite cette autorisation, Microsoft OneDrive affiche **En attente de votre accord pour lire les documents** dans **Connexions**.

## Connecter Microsoft OneDrive

Sur une Machine hébergée ou sur votre propre ordinateur associé à votre compte :

- Ouvrez **Connexions**, puis **Documents et fichiers**, et sélectionnez **Microsoft OneDrive**.
- Sélectionnez **Se connecter avec Microsoft**, puis autorisez la lecture et la modification de vos fichiers.

Si Microsoft n’autorise pas la lecture, la connexion n’est pas ajoutée. Si vous sélectionnez **Autoriser les modifications** et que Microsoft ne les autorise pas, un message vous l’indique.

## Google Docs

Sur une Machine hébergée, ouvrez **Connexions**, puis **Documents et fichiers**, et sélectionnez **Google Docs**. Google vous demande l’autorisation de consulter et modifier les documents que vous lui indiquez, ainsi que d’en créer. Il n’est pas nécessaire de connecter Gmail et l’accès à Gmail ne change pas.

Votre Machine peut alors :

- Lire un Google Doc mentionné dans les messages d’une tâche, uniquement pendant qu’elle traite cette tâche.
- Préparer des modifications de ce document. Chacune attend votre accord, comme indiqué plus haut.
- Créer de nouveaux documents privés dans votre Google Drive.

Elle ne recherche pas dans votre Drive. Elle ne voit les commentaires, les partages et les suggestions que dans les documents qu’elle a créés. Pour en voir davantage, elle devrait accéder à l’ensemble de votre Drive, ce qu’elle ne demande pas.

Sur votre propre ordinateur, votre Machine peut créer un Google Doc dans un compte Gmail déjà connecté et disposant d’un accès à Drive. Elle ne lit pas vos autres Google Docs ni leurs commentaires. **Documents et fichiers** l’affiche sous le nom Google Docs, pour ce compte. Elle peut aussi modifier un document qu’elle y a créé pour une tâche.

## Travail ou personnel

La Machine suit la catégorie Travail ou Personnel de sa connexion, comme pour les e-mails. Les documents professionnels peuvent apparaître dans le Graph de votre équipe selon vos [règles de partage](sharing-rules.md). Les documents personnels n’y apparaissent jamais.

## Déconnecter

Ouvrez **Connexions**, puis Microsoft OneDrive ou Google Docs, **Détails** et **Déconnecter**. La Machine cesse de lire les documents. Le contenu déjà importé reste disponible. Sur une Machine hébergée, **Déconnecter ↗** ouvre votre page de configuration, où se trouvent les informations de connexion.
