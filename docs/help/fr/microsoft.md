---
title: Microsoft Outlook et Outlook Calendar
area: connections
summary: Les e-mails et réunions Outlook, pour Microsoft 365 et Outlook.com. Un e-mail n’est envoyé qu’après votre approbation.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## Ce que l’assistante lit

- **Outlook** : tous vos e-mails des 7 derniers jours au moment de la connexion, puis tous les nouveaux.
- **Outlook Calendar** : vos réunions, en lecture seule.

Les e-mails du dossier Autres et les newsletters sont d’abord parcourus rapidement : expéditeur, objet et quelques mots. Si l’un d’eux est important, il est lu en entier et peut devenir une tâche.

## Ce qu’elle peut envoyer et modifier

- Un e-mail lié à une tâche, uniquement après votre approbation. Il est envoyé depuis l’adresse propre à la boîte mail, et non depuis un alias.
- Une réponse est ajoutée à la conversation Outlook de l’e-mail auquel elle répond.
- Après l’envoi d’une réponse, les messages du fil sont déplacés dans un dossier En attente d’Outlook pendant quelques jours (3, sauf indication contraire dans la tâche), puis reviennent dans la boîte de réception, ou plus tôt si quelqu’un répond. Ils ne restent jamais à l’écart au-delà de l’échéance de la tâche. La vérification vous en informe avant l’envoi.

L’agenda n’est jamais modifié.

## Photos des collègues et des contacts

Microsoft est également invité à lire les profils de base des membres de votre organisation (nom, e-mail et photo) ainsi que vos contacts Outlook. Votre Machine utilise ces informations uniquement pour afficher les photos, les postes et les entreprises des personnes déjà présentes dans votre Graph, dans la limite de 200 photos par jour. Si une personne n’a pas de photo, une nouvelle vérification a lieu après 30 jours.

L’admin de votre organisation devra peut-être approuver les photos des collègues. Sans cette approbation, Outlook se connecte quand même, mais sans ces photos. Si un compte a été connecté avant cette mise à jour, une tâche apparaît : appuyez sur **Reconnecter**, ou sur **Pas nécessaire** pour la fermer définitivement. Un compte personnel (Outlook.com, Hotmail) n’a pas de collègues. La tâche concerne donc uniquement les photos des contacts.

## Connecter le compte

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup.
2. Appuyez sur **Connecter Microsoft**, puis connectez-vous.
3. Si Microsoft demande l’approbation d’un admin, envoyez le lien à l’admin Microsoft 365 de votre organisation (**Copier le lien**). Une fois l’approbation donnée, tout le monde dans votre organisation pourra se connecter. Si vous êtes admin, appuyez sur **Je suis admin : approuver maintenant**.

Vous pouvez aussi passer par le tableau de bord : **Connexions**, **E-mail**, choisissez Outlook, puis appuyez sur **Se connecter avec Microsoft**. Le lien destiné à l’admin se trouve juste sous le bouton.

Sur votre propre ordinateur, une fois qu’il est [associé à votre compte](friends.md#a-machine-on-your-own-computer), ouvrez **Connexions**, puis **E-mail**, choisissez Outlook et appuyez sur **Se connecter avec Microsoft**. Les e-mails et l’agenda se connectent ensemble. Après l’étape Microsoft, vous revenez dans **Connexions** sur votre tableau de bord.

Pour les équipes informatiques qui utilisent leur propre app Microsoft Entra : ouvrez **Utiliser votre propre app** à cet endroit, ou lancez `assistant connect outlook`.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté du compte sur votre page de configuration. Le bouton **Déconnecter ↗** dans Connexions vous y mène.
- Sur votre propre ordinateur : ouvrez **Connexions**, sélectionnez le compte, puis **Détails** et **Déconnecter**.

## Désinstaller l’app dans Microsoft

Microsoft ne nous permet pas de révoquer une connexion. Supprimez aussi l’app dans Microsoft :

- Compte professionnel ou scolaire : myapps.microsoft.com
- Compte personnel : account.live.com/consent/Manage
