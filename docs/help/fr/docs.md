---
title: Microsoft OneDrive
area: connections
summary: Commentaires, mentions, modifications suivies et partages sur vos fichiers Word dans OneDrive et SharePoint. Les nouveaux documents et les modifications attendent votre accord.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: b06d8ca4f35e5a38
---
## Ce qu’elle lit

**Microsoft OneDrive** lit vos fichiers Word dans OneDrive et SharePoint, sur une Machine hébergée ou sur votre propre ordinateur. Il n’est pas nécessaire de connecter Outlook. Pour Google Docs, voir ci-dessous. Elle apporte des signaux :

- Les documents que quelqu’un partage avec vous.
- Les commentaires et réponses sur vos documents, ainsi que les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchronisation remonte à 7 jours. Chaque élément renvoie aux personnes et aux projets de votre [Graph](graph.md). Un commentaire qui nécessite votre intervention devient une tâche.

## Ce qu’elle peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document, uniquement pendant qu’elle travaille sur cette tâche.

Elle peut rédiger une réponse à un commentaire. Word ne permet pas de publier des réponses depuis l’extérieur, vous devez donc copier le brouillon dans Word.

Elle n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais un fichier et ne modifie jamais un document sans votre accord.

Pour l’utiliser uniquement pour effectuer des actions, désactivez **Apporte des signaux** sous **Détails**. Elle ne trouve et ne lit alors que les documents dont vos tâches ont besoin, et en crée de nouveaux.

## Créer et modifier des documents

Votre Machine peut rédiger un nouveau document ou modifier un document concerné par une tâche :

- Elle crée immédiatement un nouveau document quand une tâche ou une compétence le demande. Il est privé et enregistré dans votre propre OneDrive ou Google Drive. La tâche affiche **Ouvrir le document**. Le partage du document ou l’envoi de son lien attend votre accord.
- Elle prépare uniquement les modifications apportées à un document existant. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Une modification que vous demandez dans le chat de la tâche est appliquée immédiatement.
- Elle écrit uniquement dans le document tel que vous l’avez vu. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche vous l’indique. Demandez un nouveau brouillon.
- Dans Talk, elle lit à voix haute l’intégralité de la modification et attend un oui explicite.
- Si Microsoft ou Google refuse de créer un document, la tâche en indique la raison et affiche **Relire et créer** pour réessayer.

Elle peut remplacer et ajouter du texte, des paragraphes et des titres. Les tableaux, images, modifications suivies et champs restent inchangés.

Le document d’une tâche de travail est enregistré dans le compte de l’entreprise, jamais dans un compte personnel. Sur votre propre ordinateur, un compte Google connecté pour Gmail et ayant accès à Drive peut aussi créer de nouveaux documents Google Docs. Si aucun compte ne convient, la tâche vous indique quoi connecter pour le travail : Microsoft OneDrive ou Google Docs, si votre Machine peut l’utiliser.

Quand le document n’est pas la dernière étape, par exemple pour une réponse avec son lien, la tâche reste ouverte et rédige cette étape en attendant votre accord.

La modification est disponible dès la connexion. Une ancienne connexion qui permet uniquement la lecture affiche **Autoriser les modifications** dans **Connexions**. Appuyez dessus une fois, puis acceptez.

## Ce qu’elle vous demande

Microsoft vous demande un seul accord : lire et modifier vos fichiers, y compris ceux qui sont partagés avec vous. Chaque modification attend toujours votre accord dans la tâche correspondante. L’accès à vos e-mails et à votre agenda ne change pas.

Si vous retirez cet accord par la suite, Microsoft OneDrive affiche **En attente de votre accord pour lire les documents** dans **Connexions**.

## Connecter le service

Sur une Machine hébergée ou sur votre propre ordinateur associé à votre compte :

- Ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Microsoft OneDrive**.
- Appuyez sur **Se connecter avec Microsoft** et autorisez la lecture et la modification de vos fichiers.

Si Microsoft n’autorise pas la lecture, le service n’est pas ajouté. Si vous appuyez sur **Autoriser les modifications** et que Microsoft ne les autorise pas, la Machine vous l’indique.

## Google Docs

Sur une Machine hébergée, ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Google Docs**. Google vous demande l’autorisation d’accéder aux documents que vous lui indiquez, de les modifier et d’en créer de nouveaux. Il n’est pas nécessaire de connecter Gmail et l’accès à Gmail ne change pas.

Votre Machine peut ensuite :

- Lire un document Google Docs dont le lien figure dans les messages d’une tâche, uniquement pendant qu’elle travaille sur cette tâche.
- Préparer des modifications pour ce document. Chacune attend votre accord, comme indiqué ci-dessus.
- Créer de nouveaux documents privés dans votre Google Drive.

Elle ne recherche pas de documents dans votre Drive. Elle ne voit les commentaires, partages et suggestions que sur les documents qu’elle a créés. Pour accéder à davantage de documents, elle devrait avoir accès à l’ensemble de votre Drive, ce qu’elle ne demande pas.

Sur votre propre ordinateur, votre Machine peut créer un document Google Docs dans un compte Gmail connecté sur cet ordinateur et ayant déjà accès à Drive. Elle ne lit pas vos autres documents Google Docs ni leurs commentaires. **Documents et fichiers** l’affiche sous le nom Google Docs, avec ce compte. Elle peut aussi modifier un document qu’elle y a créé pour une tâche.

## Travail ou personnel

Elle suit le libellé Travail ou Personnel de sa connexion, comme pour les e-mails. Les documents professionnels peuvent être accessibles dans le Graph de votre équipe, selon vos [règles de partage](sharing-rules.md). Les documents personnels n’y sont jamais accessibles.

## Supprimer la connexion

Ouvrez **Connexions**, puis Microsoft OneDrive ou Google Docs, **Détails** et **Déconnecter**. La Machine cesse alors de lire les documents. Les éléments qu’elle a déjà importés restent disponibles. Sur une Machine hébergée, **Déconnecter ↗** ouvre votre page de configuration, qui conserve les informations de connexion.
