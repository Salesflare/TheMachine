---
title: Microsoft Outlook et Outlook Calendar
area: connections
summary: E-mails et réunions Outlook pour Microsoft 365 et Outlook.com. Un e-mail n’est envoyé qu’après votre approbation.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: c10bf70a327b8ec0
---
## Ce qu’elle lit

- **Outlook** : tous vos e-mails, ceux des 7 derniers jours lorsque vous vous connectez, puis tous les nouveaux.
- **Outlook Calendar** : vos réunions, en lecture seule.

Les e-mails dans Autres et les newsletters font d’abord l’objet d’un rapide coup d’œil : expéditeur, objet et quelques mots. Si l’un d’eux est important, il est lu en entier et peut devenir une tâche.

## Ce qu’elle peut envoyer et modifier

- Un e-mail à partir d’une tâche, uniquement après votre approbation. Il est envoyé depuis l’adresse propre à la boîte mail, pas depuis un alias.
- Une réponse est ajoutée à la conversation Outlook de l’e-mail auquel elle répond.
- Après l’envoi d’une réponse, les messages du fil de discussion sont déplacés dans un dossier En attente d’Outlook pendant quelques jours (3, sauf indication contraire dans la tâche), puis reviennent dans la boîte de réception, ou plus tôt si quelqu’un répond. La vérification vous l’indique avant l’envoi.

L’agenda n’est jamais modifié.

## Photos des collègues et des contacts

Microsoft est également invité à lire les profils de base de votre organisation (nom, adresse e-mail et photo), ainsi que vos contacts Outlook. Votre Machine les utilise uniquement pour afficher les photos, les fonctions et les entreprises des personnes déjà présentes dans votre Graph, dans la limite de 200 photos par jour. Si une personne n’a pas de photo, une nouvelle vérification a lieu après 30 jours.

L’administrateur de votre organisation devra peut-être approuver les photos des collègues. Sans cette approbation, Outlook se connecte quand même, mais sans ces photos. Pour un compte connecté avant cette modification, une tâche s’affiche : appuyez sur **Reconnecter** ou sur **Pas nécessaire** pour la fermer définitivement. Un compte personnel (Outlook.com, Hotmail) n’a pas de collègues : la tâche vous demande donc uniquement les photos de vos contacts.

## Connecter Outlook

Sur une Machine hébergée :

1. Ouvrez votre page de configuration à l’adresse app.themachine.computer/setup.
2. Appuyez sur **Connecter Microsoft** et connectez-vous.
3. Si Microsoft demande l’approbation d’un administrateur, envoyez le lien à votre administrateur Microsoft 365 (**Copier le lien**). Une fois l’approbation donnée, tout le monde dans votre organisation peut se connecter. Si vous êtes l’administrateur, appuyez sur **Je suis l’administrateur : approuver maintenant**.

Vous pouvez aussi accéder au tableau de bord : **Connexions**, **E-mail**, choisissez Outlook, puis appuyez sur **Se connecter avec Microsoft**. Le lien pour l’administrateur se trouve juste sous le bouton.

Sur votre propre ordinateur, une fois celui-ci [associé à votre compte](friends.md#a-machine-on-your-own-computer) : ouvrez **Connexions**, puis **E-mail**, choisissez Outlook et appuyez sur **Se connecter avec Microsoft**. Les e-mails et l’agenda sont connectés ensemble. Après la connexion à Microsoft, vous revenez à **Connexions** dans votre tableau de bord.

Pour les équipes informatiques qui utilisent leur propre application Microsoft Entra : ouvrez **Utiliser votre propre app** à cet endroit ou exécutez `assistant connect outlook`.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté du compte sur votre page de configuration. **Déconnecter ↗** dans Connexions vous y mène.
- Sur votre propre ordinateur : ouvrez **Connexions**, sélectionnez le compte, puis **Détails** et **Déconnecter**.

## Désinstaller l’application sur Microsoft

Microsoft ne nous permet pas de révoquer une connexion. Vous devez donc aussi la supprimer ici :

- Compte professionnel ou scolaire : myapps.microsoft.com
- Compte personnel : account.live.com/consent/Manage
