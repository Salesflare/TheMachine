---
title: Gmail
area: connections
summary: Lit vos e-mails et rédige des réponses avec votre style. N’envoie un e-mail qu’après votre accord.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
---
## Ce qu’il lit

Tous vos e-mails : les 7 derniers jours au moment de la connexion, puis tout ce qui est nouveau, reçu et envoyé. Les e-mails que vous envoyez comptent aussi, pour apprendre votre façon d’écrire et ce que vous avez promis.

Les e-mails Promotions, newsletters, Mises à jour et Forums ont d’abord droit à un coup d’œil rapide : expéditeur, objet et quelques mots, beaucoup à la fois. Quand l’un d’eux compte, il est lu en entier et peut devenir une tâche. Rien n’est écarté sans être vu.

## Ce qu’il peut envoyer

Un e-mail depuis une tâche, et seulement après votre accord. **Faire** prépare un brouillon ; **Vérifier et envoyer** l’ouvre, prêt à être modifié, et rien ne part avant que vous appuyiez sur **Envoyer maintenant**. **Se connecter avec Google** demande aussi à Google le droit d’envoyer. Avec votre propre app sur votre propre ordinateur, la connexion est en lecture seule jusqu’à ce que vous ajoutiez l’envoi vous-même.

Une réponse arrive dans le fil de l’e-mail auquel elle répond. Si elle part d’une autre boîte que celle où l’e-mail est arrivé, la tâche l’indique avant l’envoi : chez eux, elle arrive quand même dans le même fil.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup.
2. Sous **E-mail et agenda**, appuyez sur **Connecter Google** et connectez-vous. L’écran de Google indique Salesflare, qui crée The Machine.
3. Gmail et Google Agenda se connectent ensemble.

Ou dans le tableau de bord : **Connexions**, **+ Ajouter**, choisissez Gmail et appuyez sur **Se connecter avec Google**. Une fois terminé, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois [associé à votre compte](fleet.md) :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez Gmail.
2. Appuyez sur **Se connecter avec Google** et connectez-vous dans l’onglet qui s’ouvre. Gmail et Google Agenda se connectent ensemble.

Sans association, ou avec votre propre client OAuth Google : ouvrez **Utiliser votre propre app** à cet endroit, ou lancez `assistant connect gmail`. Il utilise gog. Ouvrez l’adresse affichée et connectez-vous.

Un admin Google Workspace devra peut-être d’abord autoriser l’app, dans la console d’administration.

## Le retirer

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse sur votre page de configuration. Cela retire Gmail et l’agenda pour cette adresse et révoque la connexion chez Google. Dans le tableau de bord, **Déconnecter ↗** dans Connexions vous y emmène. **Reconnecter** à cet endroit vous reconnecte sans quitter le tableau de bord.
- Sur votre propre ordinateur : **Connexions**, ouvrez Gmail, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste. Quand plus rien n’utilise cette connexion Google, elle est révoquée chez Google.

## Le désinstaller chez Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions à des applications et services tiers, et retirez Salesflare (Se connecter avec Google, ou hébergé) ou votre propre app.
