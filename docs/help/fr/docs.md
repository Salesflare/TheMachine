---
title: Microsoft OneDrive
area: connections
summary: Commentaires, mentions et modifications suivies dans vos fichiers Word sur OneDrive. Les nouveaux documents et les modifications attendent votre accord.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: e931920c74158c98
---
## Ce que l’application lit

**Microsoft OneDrive** lit vos fichiers Word dans OneDrive, sur une Machine hébergée et sur votre ordinateur. Vous n’avez pas besoin de connecter Outlook. Pour Google Docs, voir ci-dessous. L’application importe :

- Les commentaires et les réponses dans vos fichiers Word, ainsi que les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchronisation remonte à 7 jours. Chaque élément renvoie aux personnes et aux projets de votre [Graph](graph.md). Un commentaire qui nécessite votre attention devient une tâche.

## Fichiers que d’autres personnes partagent avec vous

Microsoft cessera de les répertorier en novembre 2026. Les partages et les mentions dans le fichier d’une autre personne arriveront alors sur votre Machine uniquement dans les e-mails de Microsoft. Connectez aussi [Outlook](microsoft.md) et laissez ces e-mails activés. Une tâche créée à partir de l’un de ces e-mails ouvre celui-ci, et son bouton ouvre le fichier. Les partages et les mentions qui ne s’accompagnent pas d’un e-mail ne sont pas détectés.

## Ce que l’application peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document uniquement pendant qu’elle traite la tâche. Elle peut lire les fichiers Word, PDF et texte.

Elle recherche aussi des fichiers de tout type dans votre propre OneDrive et vous fournit leur lien. Elle ne recherche pas dans les sites SharePoint ni dans les fichiers partagés avec vous. Elle ne peut pas lire le texte d’un PDF numérisé.

Elle peut rédiger une réponse à un commentaire. Word ne permet pas de publier des réponses depuis l’extérieur, vous devez donc copier le brouillon dans Word.

Elle n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais un fichier et ne modifie jamais un document sans votre accord.

Pour l’utiliser uniquement pour effectuer des actions, désactivez **Apporte des signaux** sous **Détails**. Elle ne trouve et ne lit alors que les fichiers dont vos tâches ont besoin, et en crée de nouveaux.

## Créer et modifier des documents

Votre Machine peut créer un document ou modifier un document concerné par une tâche :

- Elle crée immédiatement un document si la tâche ou une compétence le demande. Le document est privé et enregistré dans votre propre OneDrive ou Google Drive. La tâche affiche **Ouvrir le document**. Le partager ou envoyer son lien attend votre accord.
- Pour modifier un document existant, elle prépare les changements. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Elle effectue immédiatement une modification que vous demandez dans le chat de la tâche.
- Elle écrit uniquement dans le document tel que vous l’avez vu. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche vous l’indique. Demandez un nouveau brouillon.
- En mode vocal, elle lit toute la modification à voix haute et attend un oui explicite.
- Si Microsoft ou Google refuse de créer un document, la tâche en indique la raison et affiche **Relire et créer** pour réessayer.

Elle peut remplacer du texte et ajouter du texte, des paragraphes et des titres. Dans Google Docs, elle peut aussi appliquer une mise en forme : gras, italique, soulignement, liens, titres, listes à puces et numérotées, et saut de page. **Relire les modifications** affiche chaque changement. Elle ne peut pas créer de tableaux, et les images, les modifications suivies et les champs restent tels quels.

Le document d’une tâche Travail est enregistré dans le compte de l’entreprise, jamais dans un compte personnel. Sur votre ordinateur, un compte Google connecté pour Gmail et disposant d’un accès à Drive peut aussi recevoir les nouveaux Google Docs. Si aucun compte ne convient, la tâche indique ce qu’il faut connecter pour le Travail : Microsoft OneDrive ou Google Docs, lorsque votre Machine peut l’utiliser.

Quand le document n’est pas la dernière étape, par exemple s’il faut répondre avec son lien, la tâche reste ouverte et prépare cette étape pour que vous puissiez l’approuver.

La modification est disponible dès la connexion. Une ancienne connexion qui permet uniquement la lecture affiche **Autoriser les modifications** dans **Connexions**. Appuyez dessus une fois et acceptez.

## Ce qui est demandé

Microsoft vous demande une seule autorisation : lire et modifier vos fichiers, y compris ceux qui sont partagés avec vous. Chaque modification attend toujours votre accord dans sa tâche. L’accès à vos e-mails et à votre agenda ne change pas.

Si vous retirez cette autorisation par la suite, Microsoft OneDrive affiche **En attente de votre accord pour lire les documents** dans **Connexions**.

## Connecter le service

Sur une Machine hébergée ou sur votre propre ordinateur associé à votre compte :

- Ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Microsoft OneDrive**.
- Appuyez sur **Se connecter avec Microsoft** et autorisez la lecture et la modification de vos fichiers.

Si Microsoft n’autorise pas la lecture, le service n’est pas ajouté. Si vous appuyez sur **Autoriser les modifications** et que Microsoft ne les autorise pas, un message vous l’indique.

## Google Docs

Sur une Machine hébergée, ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Google Docs**. Google vous demande l’autorisation d’accéder aux documents que vous lui indiquez, de les modifier et d’en créer. Vous n’avez pas besoin de connecter Gmail, et votre accès à Gmail ne change pas.

Votre Machine peut alors :

- Lire un Google Doc lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle traite cette tâche.
- Préparer des modifications pour ce document. Chacune attend votre accord, comme indiqué ci-dessus.
- Créer de nouveaux documents privés dans votre Google Drive.

Si plusieurs connexions Google Docs sont disponibles dans l’espace d’une tâche, votre Machine lit et modifie un fichier avec l’une d’elles, si celle-ci peut l’ouvrir et le modifier.

Elle ne recherche pas dans votre Drive. Elle voit les commentaires, les partages et les suggestions uniquement dans les documents qu’elle a créés. Pour accéder à davantage de documents, elle devrait accéder à l’ensemble de votre Drive, ce qu’elle ne vous demande pas.

## Google Sheets et Slides

Si Google Docs affiche **Autoriser Sheets et Slides** sous **Connexions**, appuyez dessus et autorisez les deux. Google vous demande d’autoriser votre Machine à accéder à vos fichiers Sheets et Slides. Elle ne peut pas les modifier.

Votre Machine peut alors aussi lire un fichier Google Sheet ou Slides lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle traite cette tâche :

- Dans une feuille de calcul, elle lit d’abord l’onglet ou les cellules liés, puis les autres onglets, jusqu’à 2 000 cellules. Une formule apparaît sous la forme de sa valeur. Les onglets masqués ne sont lus que s’ils sont liés ou si vous le demandez.
- Dans une présentation, elle lit le texte et les notes du présentateur, dans l’ordre. Les images et les graphiques ne sont pas lus.

### Modifier Sheets et Slides

Une fois que votre Machine peut les lire, Google Docs peut aussi afficher **Autoriser la modification de Sheets et Slides**. Appuyez dessus et autorisez les deux. Votre Machine peut alors modifier un fichier Sheet ou Slides lié à une tâche ou collé dans son chat, comme elle modifie un document : elle prépare uniquement la modification, **Relire les modifications** l’affiche, et rien n’est écrit avant que vous appuyiez sur **Enregistrer**.

- Dans une feuille de calcul : nouvelles valeurs pour des cellules d’un onglet, lignes ajoutées sous la dernière ligne ou nouvel onglet. Chaque cellule affiche son contenu avant et après. Les valeurs sont ajoutées sous forme de texte. Une formule est ajoutée comme formule uniquement si la tâche le demande.
- Dans une présentation : texte remplacé sur une diapositive, avec le texte avant et après, ou nouvelle diapositive avec un titre et du texte.
- Elle écrit uniquement dans le fichier tel que vous l’avez vu. Si quelqu’un a modifié ces cellules ou ces diapositives entre-temps, rien n’est écrit et la tâche vous l’indique.

La mise en forme, les graphiques, les images et les fichiers Excel ou PowerPoint restent tels quels.

Pour un fichier volumineux, précisez dans le chat l’onglet, les cellules ou les diapositives concernés. Si un fichier est privé à une autre personne, a été supprimé ou est un fichier Excel ou PowerPoint, la tâche vous l’indique. Un lien Google Drive fonctionne de la même façon s’il mène vers un fichier Google Doc, Sheet ou Slides.

## Google Docs sur votre ordinateur

Sur votre ordinateur, votre Machine peut créer un Google Doc dans un compte Gmail connecté à cet ordinateur qui dispose déjà d’un accès à Drive. Elle ne lit pas vos autres Google Docs ni leurs commentaires. **Documents et fichiers** l’affiche comme Google Docs sur ce compte. Elle peut aussi modifier un document qu’elle y a créé pour une tâche.

Elle lit aussi un fichier Google Sheet ou Slides lié à une tâche ou collé dans son chat, si cette connexion Google dispose déjà d’un accès à Drive, Sheets ou Slides. Elle ne demande jamais à Google d’accès supplémentaire et ne les modifie pas sur cet ordinateur. Si Google refuse, activez l’API Google Sheets ou Slides dans le projet Google de cette connexion.

## Travail ou personnel

Le service suit l’étiquette Travail ou Personnel de sa connexion, comme pour les e-mails. Les documents professionnels peuvent être partagés avec le Graph de votre équipe, conformément à vos [règles de partage](sharing-rules.md). Les documents personnels ne le sont jamais.

## Déconnecter le service

Ouvrez **Connexions**, puis Microsoft OneDrive ou Google Docs, **Détails** et **Déconnecter**. Le service cesse de lire les fichiers. Les éléments qu’il a déjà importés restent disponibles. Sur une Machine hébergée, **Déconnecter ↗** ouvre votre page de configuration, qui contient les informations de connexion.
