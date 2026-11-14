---
title: Gmail
area: connections
summary: Lit vos e-mails et rédige des réponses dans votre style. N’envoie un e-mail qu’après votre approbation.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: c1f2362cd496840e
---
## Ce que Gmail lit

Tous vos e-mails : ceux des 7 derniers jours au moment de la connexion, puis tous les nouveaux, reçus et envoyés. Les e-mails que vous envoyez comptent aussi, pour que votre assistante apprenne votre façon d’écrire et les promesses que vous avez faites.

Les e-mails des catégories Promotions, newsletters, Mises à jour et Forums sont d’abord parcourus rapidement : expéditeur, objet et quelques mots, plusieurs à la fois. Si l’un d’eux est important, il est lu en entier et peut devenir une tâche. Aucun e-mail n’est ignoré sans avoir été vu.

## Ce que Gmail peut envoyer

Un e-mail associé à une tâche, et uniquement après votre approbation. **Faire** prépare un brouillon ; **Vérifier et envoyer** l’ouvre, prêt à être modifié. Rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer maintenant**. **Se connecter avec Google** demande aussi à Google l’autorisation d’envoyer des e-mails. Avec votre propre app sur votre ordinateur, la connexion permet uniquement la lecture jusqu’à ce que vous activiez vous-même l’envoi.

Dans l’écran de vérification, **De** affiche un petit sélecteur si Gmail permet à cette boîte d’envoyer des e-mails en tant qu’alias de l’une de vos adresses (une adresse marquée **Les miens** dans les **Paramètres**, [Vos adresses](settings.md#your-addresses)). Une réponse à un e-mail reçu sur cet alias est envoyée depuis celui-ci ; un nouvel e-mail part de l’adresse de votre boîte. Juste avant l’envoi, Gmail est interrogé une nouvelle fois : si l’adresse n’est pas confirmée, rien n’est envoyé.

Une réponse est ajoutée au fil de l’e-mail auquel elle répond. Si elle part d’une autre de vos boîtes que celle qui a reçu l’e-mail, la tâche vous l’indique avant l’envoi. La réponse reste dans le fil de la personne.

Après l’envoi d’une réponse, son fil quitte votre boîte de réception et reçoit le libellé « En attente » pendant quelques jours (3, sauf indication contraire dans la tâche). Il revient ensuite dans votre boîte, ou plus tôt si quelqu’un répond. L’écran de vérification vous l’indique avant l’envoi.

## Connecter Gmail

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup.
2. Sous **E-mail et agenda**, appuyez sur **Connecter Google** et connectez-vous. L’écran de Google indique Salesflare, l’entreprise qui a créé The Machine.
3. Gmail et Google Calendar sont connectés ensemble.

Si vous vous êtes inscrit avec Google et avez autorisé Gmail et Calendar sur cet écran, les deux services se connectent automatiquement. L’envoi n’a lieu que lorsque vous appuyez sur **Envoyer**.

Vous pouvez aussi passer par le tableau de bord : **Connexions**, **E-mail**, choisissez Gmail, puis appuyez sur **Se connecter avec Google**. Une fois la connexion terminée, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois qu’il est [associé à votre compte](friends.md#a-machine-on-your-own-computer) :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **E-mail**, et choisissez Gmail.
2. Appuyez sur **Se connecter avec Google** et connectez-vous dans l’onglet qui s’ouvre. Gmail et Google Calendar sont connectés ensemble.

Si votre ordinateur n’est pas associé à votre compte, ou si vous utilisez votre propre client OAuth Google, ouvrez **Utiliser votre propre app** à cet endroit ou exécutez `assistant connect gmail`. Appuyez sur **Ouvrir Google**, connectez-vous, puis collez l’adresse vers laquelle Google vous redirige. Google Calendar associé à la même adresse est également connecté.

Un administrateur Google Workspace devra peut-être d’abord autoriser l’app dans la console d’administration.

## Déconnecter Gmail

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse sur votre page de configuration. Gmail et Calendar sont alors déconnectés pour cette adresse, et votre Machine oublie les informations de connexion. Vos autres Machines conservent les leurs. Dans le tableau de bord, **Déconnecter ↗** dans Connexions vous mène à cette page. **Reconnecter** vous permet de vous connecter à nouveau sans quitter le tableau de bord.
- Sur votre propre ordinateur : ouvrez **Connexions**, sélectionnez Gmail, appuyez sur **Détails**, puis sur **Déconnecter**. Gmail cesse alors d’être lu. Les données déjà importées sont conservées. Si cette connexion Google n’est utilisée par aucun autre service, elle est oubliée. Vos autres Machines conservent leurs connexions.

## Désinstaller l’app dans Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions aux applications et services tiers, et supprimez Salesflare (connexion avec Google ou Machine hébergée) ou votre propre app.
