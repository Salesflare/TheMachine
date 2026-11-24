---
title: Microsoft OneDrive
area: connections
summary: Commentaires, mentions et suivi des modifications dans vos fichiers Word sur OneDrive. Les nouveaux documents et les modifications attendent votre accord.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: d79388a1c8811d5f
---
## Ce qui est lu

**Microsoft OneDrive** lit vos fichiers Word dans OneDrive, sur une Machine hébergée ou sur votre propre ordinateur. Vous n’avez pas besoin de connecter Outlook. Pour Google Docs, voir ci-dessous. Il importe :

- Les commentaires et les réponses dans vos fichiers Word, ainsi que les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchronisation remonte à 7 jours. Chaque élément renvoie aux personnes et aux projets de votre [Graph](graph.md). Un commentaire qui nécessite votre attention devient une tâche.

## Fichiers partagés avec vous

Microsoft cessera de les répertorier en novembre 2026. Les partages et les mentions dans le fichier d’une autre personne ne parviendront alors à votre Machine que dans les e-mails de Microsoft. Connectez aussi [Outlook](microsoft.md) et laissez ces e-mails activés. Une tâche créée à partir de l’un de ces e-mails ouvre le message, et son bouton ouvre le fichier. Les partages et les mentions sans e-mail ne sont pas détectés.

## Ce qu’elle peut faire

Lorsqu’une tâche a besoin du texte d’un document, votre Machine lit ce document uniquement pendant qu’elle travaille sur cette tâche. Elle peut lire les fichiers Word, PDF et texte.

Elle recherche aussi tous les types de fichiers dans votre propre OneDrive et vous en donne le lien. Elle ne recherche pas dans les sites SharePoint ni dans les fichiers partagés avec vous. Elle ne peut pas lire le texte d’un PDF numérisé.

Elle peut rédiger une réponse à un commentaire. Word ne permet pas de publier des réponses depuis l’extérieur, vous devez donc copier le brouillon dans Word.

Elle n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais de fichier et ne modifie jamais un document sans votre accord.

Pour l’utiliser uniquement pour effectuer des actions, désactivez **Apporte des signaux** sous **Détails**. Elle ne trouve et ne lit alors que les fichiers nécessaires à vos tâches, et en crée de nouveaux.

## Créer et modifier des documents

Votre Machine peut créer un document ou modifier un document concerné par une tâche :

- Elle crée immédiatement un nouveau document lorsque la tâche ou une compétence le demande. Il est privé et se trouve dans votre OneDrive ou Google Drive personnel. La tâche affiche **Ouvrir le document**. Le partage du document ou l’envoi de son lien attend votre accord.
- Pour modifier un document existant, elle prépare les changements. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Elle effectue immédiatement les modifications que vous demandez dans le chat de la tâche.
- Elle écrit uniquement dans la version du document que vous avez consultée. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche vous l’indique. Demandez un nouveau brouillon.
- Dans Talk, elle lit toute la modification à voix haute et attend un oui explicite.
- Si Microsoft ou Google refuse de créer un document, la tâche en indique la raison et affiche **Relire et créer** pour réessayer.

Elle peut remplacer et ajouter du texte, des paragraphes et des titres. Les tableaux, les images, les modifications suivies et les champs restent inchangés.

Le document d’une tâche professionnelle est enregistré dans le compte de l’entreprise concernée, jamais dans un compte personnel. Sur votre propre ordinateur, un compte Google connecté pour Gmail et disposant d’un accès à Drive peut aussi créer de nouveaux documents Google Docs. Si aucun compte ne convient, la tâche indique ce qu’il faut connecter pour le travail : Microsoft OneDrive ou Google Docs, si votre Machine peut l’utiliser.

Lorsque le document n’est pas la dernière étape, par exemple s’il faut répondre avec son lien, la tâche reste ouverte et prépare cette étape pour que vous la validiez.

La modification est incluse lors de la connexion. Une ancienne connexion qui permet uniquement la lecture affiche **Autoriser les modifications** dans **Connexions**. Appuyez une fois dessus et acceptez.

## Ce qui vous est demandé

Microsoft vous demande une seule autorisation : lire et modifier vos fichiers, y compris ceux qui sont partagés avec vous. Chaque modification attend toujours votre accord dans la tâche correspondante. L’accès à vos e-mails et à votre agenda ne change pas.

Si vous retirez cette autorisation par la suite, Microsoft OneDrive affiche **En attente de votre accord pour lire les documents** dans **Connexions**.

## Connecter Microsoft OneDrive

Sur une Machine hébergée ou sur votre propre ordinateur associé à votre compte :

- Ouvrez **Connexions**, puis **Documents et fichiers**, et sélectionnez **Microsoft OneDrive**.
- Appuyez sur **Se connecter avec Microsoft** et autorisez la lecture et la modification de vos fichiers.

Si Microsoft n’autorise pas la lecture, la connexion n’est pas ajoutée. Si vous appuyez sur **Autoriser les modifications** et que Microsoft ne les autorise pas, un message vous l’indique.

## Google Docs

Sur une Machine hébergée, ouvrez **Connexions**, puis **Documents et fichiers**, et sélectionnez **Google Docs**. Google vous demande l’autorisation de consulter et modifier les documents que vous lui indiquez, ainsi que d’en créer. Vous n’avez pas besoin de connecter Gmail et votre accès à Gmail ne change pas.

Votre Machine peut alors :

- Lire un document Google Docs lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle travaille sur cette tâche.
- Préparer des modifications pour ce document. Chacune attend votre accord, comme indiqué ci-dessus.
- Créer de nouveaux documents privés dans votre Google Drive.

Elle ne recherche pas dans votre Drive. Elle ne voit les commentaires, les partages et les suggestions que sur les documents qu’elle a créés. Pour en voir davantage, elle devrait accéder à l’ensemble de votre Drive, ce qu’elle ne demande pas.

## Google Sheets et Slides

Si Google Docs affiche **Autoriser Sheets et Slides** sous **Connexions**, appuyez dessus et autorisez les deux applications. Google vous demande l’autorisation de consulter vos fichiers Sheets et Slides. Votre Machine ne peut pas les modifier.

Votre Machine peut alors aussi lire un fichier Google Sheets ou Slides lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle travaille sur cette tâche :

- Dans une feuille de calcul, elle lit d’abord l’onglet ou les cellules liés, puis les autres onglets, dans la limite de 2 000 cellules. Une formule apparaît sous forme de valeur. Les onglets masqués ne sont lus que s’ils sont liés ou si vous le demandez.
- Dans les diapositives, elle lit le texte et les notes du présentateur, dans l’ordre. Les images et les graphiques ne sont pas lus.

Pour un fichier volumineux, précisez dans le chat l’onglet, les cellules ou les diapositives concernés. Si le fichier est privé et appartient à quelqu’un d’autre, s’il a été supprimé ou s’il s’agit d’un fichier Excel ou PowerPoint, la tâche vous l’indique. Un lien Google Drive fonctionne de la même façon s’il mène à un fichier Google Docs, Sheets ou Slides.

## Google Docs sur votre propre ordinateur

Sur votre propre ordinateur, votre Machine peut créer un document Google Docs dans un compte Gmail qui y est connecté et dispose déjà d’un accès à Drive. Elle ne lit pas vos autres documents Google Docs ni leurs commentaires. **Documents et fichiers** affiche Google Docs associé à ce compte. Elle peut aussi modifier un document qu’elle y a créé pour une tâche.

Elle lit également un fichier Google Sheets ou Slides lié dans une tâche ou collé dans son chat, si cette session Google dispose déjà d’un accès à Drive, Sheets ou Slides. Elle ne demande jamais d’accès supplémentaire à Google. Si Google refuse, activez l’API Google Sheets ou Slides dans le projet Google de cette session.

## Travail ou personnel

Comme pour les e-mails, votre Machine suit le libellé Travail ou Personnel de la connexion. Les documents professionnels peuvent être accessibles au Graph de votre équipe, conformément à vos [règles de partage](sharing-rules.md). Les documents personnels ne le sont jamais.

## Déconnecter

Ouvrez **Connexions**, puis Microsoft OneDrive ou Google Docs, **Détails** et **Déconnecter**. La lecture s’arrête. Les éléments déjà importés sont conservés. Sur une Machine hébergée, **Déconnecter ↗** ouvre votre page de configuration, qui contient la session connectée.
