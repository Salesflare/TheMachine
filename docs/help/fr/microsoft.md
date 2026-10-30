---
title: Microsoft Outlook et Calendar
area: connections
summary: Les e-mails et réunions Outlook, pour Microsoft 365 et Outlook.com. N’envoie un e-mail qu’après votre accord.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
---
## Ce qu’il lit

- **Outlook** : tous vos e-mails, les 7 derniers jours au moment de la connexion, puis tout ce qui est nouveau.
- **Outlook Calendar** : vos réunions, en lecture seule.

Les e-mails du dossier Autres et les newsletters ont d’abord droit à un coup d’œil rapide : expéditeur, objet et quelques mots, beaucoup à la fois. Quand l’un d’eux compte, il est lu en entier et peut devenir une tâche. Rien n’est écarté sans être vu.

## Ce qu’il peut envoyer et modifier

- Un e-mail depuis une tâche, seulement après votre accord dans l’aperçu.
- Une réponse arrive dans la conversation Outlook de l’e-mail auquel elle répond.
- Quand vous mettez en attente une tâche liée à un e-mail, les messages du fil vont dans un dossier Snoozed dans Outlook et reviennent en même temps que la tâche.

L’agenda n’est jamais modifié.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup.
2. Appuyez sur **Connecter Microsoft** et connectez-vous.
3. Si Microsoft demande l’accord d’un admin, envoyez ce lien à l’administrateur de votre Microsoft 365 : themachine.computer/m365-admin-consent. **Copier le lien** le copie. Dès son approbation, tout le monde dans votre organisation peut se connecter. Si c’est vous, appuyez sur **Je suis l’admin : approuver maintenant**.

Ou dans le tableau de bord : **Connexions**, **+ Ajouter**, choisissez Outlook et appuyez sur **Se connecter avec Microsoft**. Une fois terminé, vous revenez au tableau de bord. Besoin de l’approbation de votre administrateur ? Le même lien est sous le bouton, avec **Copier le lien**.

Sur votre propre ordinateur, une fois [associé à votre compte](fleet.md) : ouvrez **Connexions**, puis **+ Ajouter**, choisissez Outlook et appuyez sur **Se connecter avec Microsoft**. Les e-mails et l’agenda se connectent ensemble.

Avec votre propre app : ouvrez **Utiliser votre propre app** à cet endroit, ou lancez `assistant connect outlook` ou `assistant connect outlook_calendar`. Il utilise votre propre inscription d’app dans Microsoft Entra et un code de connexion. Il demande s’il doit aussi envoyer ce que vous approuvez.

## Le retirer

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté du compte sur votre page de configuration. Dans le tableau de bord, **Déconnecter ↗** dans Connexions vous y emmène. **Reconnecter** à cet endroit vous reconnecte sans quitter le tableau de bord.
- Sur votre propre ordinateur : **Connexions**, ouvrez le compte, **Détails**, puis **Déconnecter**.

## Le désinstaller chez Microsoft

Microsoft ne nous permet pas de révoquer une connexion, alors retirez-la aussi chez eux :

- Compte professionnel ou scolaire : myapps.microsoft.com
- Compte personnel : account.live.com/consent/Manage
