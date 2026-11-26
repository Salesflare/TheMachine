---
title: Microsoft OneDrive
area: connections
summary: Commentaires, mentions et modifications suivies dans vos fichiers Word sur OneDrive. Les nouveaux documents et les modifications attendent votre accord.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: c8fca3cf0299e327
---
## Ce que la connexion lit

**Microsoft OneDrive** lit vos fichiers Word sur OneDrive, sur une Machine hébergée et sur votre propre ordinateur. Vous n’avez pas besoin de connecter Outlook. Pour Google Docs, consultez la section ci-dessous. La connexion récupère :

- Les commentaires et les réponses dans vos fichiers Word, ainsi que les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchronisation couvre les 7 derniers jours. Chaque élément renvoie aux personnes et aux projets de votre [Graph](graph.md). Un commentaire qui demande votre attention devient une tâche.

## Fichiers partagés avec vous

Microsoft ne les répertoriera plus à partir de novembre 2026. Les partages et les mentions dans le fichier d’une autre personne n’arriveront alors sur votre Machine que dans les e-mails envoyés par Microsoft. Connectez aussi [Outlook](microsoft.md) et laissez ces e-mails activés. Une tâche créée à partir d’un e-mail ouvre celui-ci, et son bouton ouvre le fichier. Les partages ou les mentions qui ne sont pas accompagnés d’un e-mail ne sont pas détectés.

## Ce que la connexion peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit uniquement ce document, et seulement pendant qu’elle traite la tâche. Elle peut lire les fichiers Word, PDF et texte.

Elle recherche aussi tous les types de fichiers dans votre propre OneDrive et vous fournit un lien. Elle ne recherche pas dans les sites SharePoint ni dans les fichiers partagés avec vous. Elle ne peut pas lire le texte d’un PDF numérisé.

Elle peut rédiger une réponse à un commentaire. Word ne permet pas de publier des réponses depuis l’extérieur, vous devez donc copier le brouillon dans Word.

Elle n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais de fichier et ne modifie jamais de document sans votre accord.

Pour l’utiliser uniquement pour effectuer des tâches, désactivez **Apporte des signaux** sous **Détails**. Elle ne repère et ne lit alors que les fichiers nécessaires à vos tâches, et en crée de nouveaux.

## Créer et modifier des documents

Votre Machine peut créer un document ou modifier un document lié à une tâche :

- Elle crée immédiatement un document quand la tâche ou une compétence le demande. Le document est privé et se trouve dans votre propre OneDrive ou Google Drive. La tâche affiche **Ouvrir le document**. Le partage du document ou l’envoi de son lien attend votre accord.
- Pour modifier un document existant, elle prépare les changements. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Si vous demandez une modification dans le chat de la tâche, elle l’effectue immédiatement.
- Elle écrit uniquement dans le document tel que vous l’avez vu. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche vous l’indique. Demandez un nouveau brouillon.
- Dans Talk, elle lit à voix haute l’intégralité des modifications et attend un oui explicite.
- Si Microsoft ou Google refuse de créer un document, la tâche vous en indique la raison et affiche **Relire et créer** pour réessayer.

Elle peut remplacer et ajouter du texte, des paragraphes et des titres. Dans Google Docs, elle peut aussi mettre en forme le texte : gras, italique, souligné, liens, titres, listes à puces et numérotées, et saut de page. **Relire les modifications** affiche chaque changement. Elle ne peut pas créer de tableaux. Les images, les modifications suivies et les champs restent tels quels.

Le document d’une tâche Travail est enregistré dans le compte de l’entreprise concernée, jamais dans un compte personnel. Sur votre propre ordinateur, un compte Google connecté pour Gmail et disposant d’un accès à Drive peut aussi recevoir de nouveaux documents Google Docs. Si aucun compte ne convient, la tâche vous indique quoi connecter pour le travail : Microsoft OneDrive, ou Google Docs si votre Machine peut l’utiliser.

Si le document n’est pas l’étape finale, par exemple s’il faut envoyer une réponse avec son lien, la tâche reste ouverte et prépare cette étape pour que vous la validiez.

La modification est incluse avec la connexion. Une ancienne connexion qui permet uniquement la lecture affiche **Autoriser les modifications** dans **Connexions**. Appuyez dessus une fois et acceptez.

## Ce que la connexion vous demande

Microsoft vous demande une seule autorisation : lire et modifier vos fichiers, y compris ceux qui sont partagés avec vous. Chaque modification attend toujours votre accord dans la tâche correspondante. L’accès à vos e-mails et à votre agenda ne change pas.

Si vous retirez cette autorisation par la suite, Microsoft OneDrive affiche **En attente de votre accord pour lire les documents** dans **Connexions**.

## Connecter Microsoft OneDrive

Sur une Machine hébergée ou sur votre propre ordinateur associé à votre compte :

- Ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Microsoft OneDrive**.
- Appuyez sur **Se connecter avec Microsoft** et autorisez la lecture et la modification de vos fichiers.

Si Microsoft n’autorise pas la lecture, la connexion n’est pas ajoutée. Si vous appuyez sur **Autoriser les modifications** et que Microsoft ne les autorise pas, un message vous l’indique.

## Google Docs

Sur une Machine hébergée, ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Google Docs**. Google vous demande l’autorisation de consulter et de modifier les documents que vous lui indiquez, et d’en créer de nouveaux. Vous n’avez pas besoin de connecter Gmail, et l’accès à Gmail ne change pas.

Votre Machine peut alors :

- Lire un document Google Docs lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle traite cette tâche.
- Préparer des modifications de ce document. Chacune attend votre accord, comme indiqué ci-dessus.
- Créer de nouveaux documents privés dans votre Google Drive.

Elle ne recherche pas dans votre Drive. Elle ne voit les commentaires, les partages et les suggestions que dans les documents qu’elle a créés. Il faudrait lui donner accès à l’intégralité de votre Drive pour qu’elle en voie davantage, mais elle ne le demande pas.

## Google Sheets et Slides

Si Google Docs affiche **Autoriser Sheets et Slides** dans **Connexions**, appuyez dessus et autorisez les deux. Google vous demande l’autorisation de consulter vos fichiers Sheets et Slides. Votre Machine ne peut pas les modifier.

Votre Machine peut alors aussi lire un fichier Google Sheets ou Slides lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle traite cette tâche :

- Dans une feuille de calcul, elle lit d’abord l’onglet ou les cellules liés, puis les autres onglets, dans la limite de 2 000 cellules. Une formule est affichée sous la forme de sa valeur. Les onglets masqués ne sont lus que s’ils sont liés ou demandés.
- Dans les présentations, elle lit le texte et les notes du présentateur, dans l’ordre. Les images et les graphiques ne sont pas lus.

Pour un fichier volumineux, indiquez dans le chat l’onglet, les cellules ou les diapositives concernés. Si un fichier est privé et appartient à quelqu’un d’autre, s’il a été supprimé ou s’il s’agit d’un fichier Excel ou PowerPoint, la tâche vous l’indique. Un lien Google Drive fonctionne de la même manière s’il mène à un fichier Google Docs, Sheets ou Slides.

## Google Docs sur votre propre ordinateur

Sur votre propre ordinateur, votre Machine peut créer un document Google Docs dans un compte Gmail auquel vous êtes connecté et qui a déjà accès à Drive. Elle ne lit pas vos autres documents Google Docs ni leurs commentaires. **Documents et fichiers** affiche Google Docs pour ce compte. Elle peut aussi modifier un document qu’elle y a créé pour une tâche.

Elle peut aussi lire un fichier Google Sheets ou Slides lié à une tâche ou collé dans son chat, si cette session Google dispose déjà d’un accès à Drive, Sheets ou Slides. Elle ne demande jamais d’accès supplémentaire à Google. Si Google refuse l’accès, activez l’API Google Sheets ou Slides dans le projet Google associé à cette session.

## Travail ou personnel

La connexion suit son étiquette Travail ou Personnel, comme pour les e-mails. Les documents professionnels peuvent être visibles dans le Graph de votre équipe, conformément à vos [règles de partage](sharing-rules.md). Les documents personnels ne le sont jamais.

## Supprimer la connexion

Ouvrez **Connexions**, puis Microsoft OneDrive ou Google Docs, **Détails** et **Déconnecter**. La connexion cesse de lire vos fichiers. Les informations qu’elle a déjà récupérées restent disponibles. Sur une Machine hébergée, **Déconnecter ↗** ouvre votre page de configuration, où la session est enregistrée.
