---
title: Microsoft OneDrive
area: connections
summary: Commentaires, mentions et modifications suivies dans vos fichiers Word sur OneDrive. Les nouveaux documents et les modifications attendent votre accord.
covers: connector:docs
code: connectors/docs.py, google_files.py, google_links.py, machine/app/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
translated: 057429e4c3b6408c
---
## Ce que l’intégration lit

**Microsoft OneDrive** lit vos fichiers Word sur OneDrive, sur une Machine hébergée ou sur votre propre ordinateur. Vous n’avez pas besoin de connecter Outlook. Pour Google Docs, consultez la section ci-dessous. L’intégration importe :

- Les commentaires et les réponses sur vos fichiers Word, ainsi que les commentaires qui vous mentionnent.
- Les modifications suivies dans vos fichiers Word.

La première synchronisation couvre les 7 derniers jours. Chaque élément renvoie aux personnes et aux projets de votre [Graph](graph.md). Un commentaire qui nécessite votre attention devient une tâche.

## Fichiers partagés avec vous

Microsoft cessera de les répertorier en novembre 2026. Les partages et les mentions dans le fichier d’une autre personne n’arriveront alors sur votre Machine que sous forme d’e-mails envoyés par Microsoft. Connectez aussi [Outlook](microsoft.md) et gardez ces e-mails activés. Une tâche créée à partir d’un de ces e-mails ouvre celui-ci, et le bouton qu’il contient ouvre le fichier. Un partage ou une mention sans e-mail ne sera pas détecté.

## Ce que l’intégration peut faire

Quand une tâche a besoin du texte d’un document, votre Machine lit ce document, uniquement pendant qu’elle traite la tâche. Elle peut lire les fichiers Word, PDF et texte.

Elle recherche aussi tous les types de fichiers dans votre propre OneDrive et vous fournit leur lien. Elle ne recherche ni dans les sites SharePoint ni dans les fichiers partagés avec vous. Elle ne peut pas lire le texte d’un PDF numérisé.

Elle peut rédiger une réponse à un commentaire. Word ne permet pas de publier une réponse depuis l’extérieur. Vous devez donc copier le brouillon dans Word.

Elle n’accepte jamais une suggestion, ne résout jamais un commentaire, ne partage jamais de fichier et ne modifie jamais un document sans votre accord.

Pour utiliser l’intégration uniquement pour effectuer des actions, désactivez **Apporte des signaux** sous **Détails**. Elle ne trouvera et ne lira alors que les fichiers nécessaires à vos tâches, et pourra en créer de nouveaux.

## Créer et modifier des documents

Votre Machine peut créer un document ou modifier un document lié à une tâche :

- Elle crée immédiatement un nouveau document si la tâche ou une compétence le demande. Le document est privé et se trouve dans votre OneDrive ou Google Drive personnel. La tâche affiche **Ouvrir le document**. Le partage du document ou l’envoi de son lien attend votre accord.
- Elle prépare les modifications apportées à un document existant. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Les modifications que vous demandez dans le chat de la tâche sont effectuées immédiatement.
- Elle écrit uniquement dans le document tel que vous l’avez consulté. Si quelqu’un l’a modifié entre-temps, rien n’est écrit et la tâche vous en informe. Demandez un nouveau brouillon.
- Dans Talk, elle lit à voix haute l’ensemble des modifications et attend votre accord explicite.
- Si Microsoft ou Google refuse de créer un document, la tâche en indique la raison et affiche **Relire et créer** pour réessayer.

Elle peut remplacer et ajouter du texte, des paragraphes et des titres. Dans Google Docs, elle peut aussi appliquer une mise en forme : gras, italique, souligné, liens, titres, listes à puces et numérotées, et saut de page. **Relire les modifications** affiche chaque modification. Elle ne peut pas créer de tableaux. Les images, les modifications suivies et les champs restent inchangés.

Le document d’une tâche professionnelle est enregistré dans le compte de l’entreprise, jamais dans un compte personnel. Sur votre propre ordinateur, un compte Google connecté à Gmail et disposant d’un accès à Drive peut aussi recevoir les nouveaux Google Docs. Si aucun compte ne convient, la tâche vous indique ce qu’il faut connecter pour le travail : Microsoft OneDrive ou Google Docs, si votre Machine peut l’utiliser.

Quand le document n’est pas la dernière étape, par exemple s’il faut envoyer une réponse avec son lien, la tâche reste ouverte et prépare cette étape pour que vous la validiez.

La modification est disponible dès la connexion. Une ancienne connexion qui permet uniquement la lecture affiche **Autoriser les modifications** dans **Connexions**. Appuyez dessus une fois et acceptez.

## Autorisations demandées

Microsoft vous demande une seule autorisation : lire et modifier vos fichiers, y compris ceux qui sont partagés avec vous. Chaque modification attend tout de même votre accord dans la tâche correspondante. L’accès à vos e-mails et à votre agenda ne change pas.

Si vous retirez cette autorisation par la suite, Microsoft OneDrive affiche **En attente de votre accord pour lire les documents** dans **Connexions**.

## Connecter l’intégration

Sur une Machine hébergée ou sur votre propre ordinateur associé à votre compte :

- Ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Microsoft OneDrive**.
- Appuyez sur **Se connecter avec Microsoft** et autorisez la lecture et la modification de vos fichiers.

Si Microsoft n’autorise pas la lecture, l’intégration n’est pas ajoutée. Si vous appuyez sur **Autoriser les modifications** et que Microsoft ne les autorise pas, un message vous l’indique.

## Google Docs

Sur une Machine hébergée, ouvrez **Connexions**, puis **Documents et fichiers**, et choisissez **Google Docs**. Google vous demande l’autorisation de consulter et de modifier les documents que vous lui indiquez, et d’en créer de nouveaux. Vous n’avez pas besoin de connecter Gmail, et l’accès à Gmail ne change pas.

Votre Machine peut alors :

- Lire un Google Doc lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle traite cette tâche.
- Préparer des modifications dans ce document. Chacune attend votre accord, comme indiqué ci-dessus.
- Créer de nouveaux documents privés dans votre Google Drive.

Elle ne recherche pas dans votre Drive. Elle ne voit les commentaires, les partages et les suggestions que sur les documents qu’elle a créés. Pour accéder à davantage de contenu, elle devrait accéder à l’ensemble de votre Drive, ce qu’elle ne demande pas.

## Google Sheets et Slides

Si Google Docs affiche **Autoriser Sheets et Slides** sous **Connexions**, appuyez dessus et autorisez les deux. Google vous demande d’autoriser votre Machine à consulter vos fichiers Sheets et Slides. Elle ne peut pas les modifier.

Votre Machine peut alors aussi lire un fichier Google Sheets ou Slides lié dans les messages d’une tâche ou collé dans son chat, uniquement pendant qu’elle traite cette tâche :

- Dans une feuille de calcul, elle lit d’abord l’onglet ou les cellules indiqués par le lien, puis les autres onglets, jusqu’à 2 000 cellules. Une formule apparaît sous la forme de sa valeur. Les onglets masqués ne sont lus que si le lien y renvoie ou si la tâche le demande.
- Dans une présentation, elle lit le texte et les notes du présentateur, dans l’ordre. Les images et les graphiques ne sont pas lus.

### Modifier Sheets et Slides

Une fois qu’elle les lit, Google Docs peut aussi afficher **Autoriser la modification de Sheets et Slides**. Appuyez dessus et autorisez les deux. Votre Machine pourra alors modifier un fichier Sheets ou Slides lié, comme elle modifie un document : elle prépare uniquement la modification, **Relire les modifications** l’affiche et rien n’est écrit tant que vous n’appuyez pas sur **Enregistrer**.

- Dans une feuille de calcul : nouvelles valeurs pour des cellules d’un onglet, lignes ajoutées après la dernière ligne ou nouvel onglet. Chaque cellule affiche son contenu avant et après. Les valeurs sont insérées comme du texte. Une formule n’est insérée comme telle que si la tâche le demande.
- Dans une présentation : remplacement du texte d’une diapositive, avec le texte avant et après, ou création d’une diapositive avec un titre et du texte.
- Elle écrit uniquement dans le fichier tel que vous l’avez consulté. Si quelqu’un a modifié ces cellules ou les diapositives entre-temps, rien n’est écrit et la tâche vous en informe.

La mise en forme, les graphiques, les images et les fichiers Excel ou PowerPoint restent inchangés.

Pour un fichier volumineux, indiquez dans le chat l’onglet, les cellules ou les diapositives concernés. Si le fichier est privé et appartient à quelqu’un d’autre, s’il a été supprimé ou s’il s’agit d’un fichier Excel ou PowerPoint, la tâche vous en informe. Un lien Google Drive fonctionne de la même façon s’il renvoie vers un fichier Google Docs, Sheets ou Slides.

## Google Docs sur votre propre ordinateur

Sur votre propre ordinateur, votre Machine peut créer un Google Doc dans un compte Gmail qui y est connecté et qui a déjà accès à Drive. Elle ne lit pas vos autres Google Docs ni leurs commentaires. **Documents et fichiers** affiche Google Docs pour ce compte. Elle peut aussi modifier un document qu’elle y a créé pour une tâche.

Elle lit également un fichier Google Sheets ou Slides lié dans une tâche ou collé dans son chat, si cette session Google dispose déjà d’un accès à Drive, Sheets ou Slides. Elle ne demande jamais d’autorisation supplémentaire à Google et ne les modifie pas. Si Google refuse l’accès, activez l’API Google Sheets ou Slides dans le projet Google associé à cette session.

## Travail ou personnel

Comme pour les e-mails, l’intégration suit le paramètre Travail ou Personnel de sa connexion. Les documents professionnels peuvent être transmis au Graph de votre équipe, selon vos [règles de partage](sharing-rules.md). Les documents personnels ne le sont jamais.

## Déconnecter l’intégration

Ouvrez **Connexions**, puis Microsoft OneDrive ou Google Docs, **Détails** et **Déconnecter**. L’intégration cesse alors de lire vos fichiers. Les éléments qu’elle a déjà importés sont conservés. Sur une Machine hébergée, **Déconnecter ↗** ouvre votre page de configuration, où se trouve la session.
