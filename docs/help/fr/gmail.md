---
title: Gmail
area: connections
summary: Lit vos e-mails et rédige des réponses dans votre style. N’envoie un e-mail qu’après votre approbation.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: 0d8060f38f905576
---
## Ce que Gmail lit

Tous vos e-mails : ceux des 7 derniers jours au moment de la connexion, puis tous les nouveaux, reçus et envoyés. Les e-mails que vous envoyez comptent aussi. Gmail apprend ainsi votre façon d’écrire et ce que vous avez promis.

Les e-mails des catégories Promotions, newsletters, Mises à jour et Forums sont d’abord parcourus rapidement : expéditeur, objet et quelques mots, plusieurs à la fois. Si l’un d’eux est important, il est lu en entier et peut devenir une tâche. Aucun e-mail n’est ignoré sans avoir été vu.

## Ce que Gmail peut envoyer

Un e-mail associé à une tâche, et seulement après votre approbation. **Faire** prépare un brouillon. **Vérifier et envoyer** l’ouvre, prêt à être modifié, et rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer maintenant**. **Se connecter avec Google** autorise aussi Google à envoyer des e-mails. Si vous utilisez votre propre app sur votre propre ordinateur, la connexion est en lecture seule jusqu’à ce que vous activiez vous-même l’envoi.

Dans la vérification, **De** ouvre un petit sélecteur lorsque Gmail permet à cette boîte d’envoyer des e-mails avec l’un de vos alias, indiqué par **Les miens** dans les paramètres ([Vos adresses](settings.md#your-addresses)). Une réponse à un e-mail reçu sur cet alias est envoyée depuis celui-ci. Un nouvel e-mail est envoyé depuis l’adresse de votre boîte. Juste avant l’envoi, Gmail est interrogé une nouvelle fois. Si l’adresse n’est pas confirmée, rien n’est envoyé.

Une réponse est ajoutée au fil de discussion de l’e-mail auquel elle répond. Si elle est envoyée depuis une autre de vos boîtes que celle qui a reçu l’e-mail, la tâche vous l’indique avant l’envoi. La réponse est tout de même ajoutée à leur fil de discussion.

Après l’envoi d’une réponse, son fil de discussion quitte votre boîte de réception et porte le libellé En attente pendant quelques jours (3, sauf indication contraire dans la tâche). Il revient ensuite, ou plus tôt si quelqu’un répond. La vérification vous l’indique avant l’envoi. Votre boîte de réception reste sous votre contrôle : si une réponse se contente de promettre que le travail sera fait, la tâche reste ouverte.

## Connecter Gmail

Sur une Machine hébergée :

1. Ouvrez votre page de configuration à l’adresse app.themachine.computer/setup.
2. Sous **E-mail et agenda**, appuyez sur **Connecter Google** et connectez-vous. L’écran de Google indique Salesflare, l’entreprise qui crée The Machine.
3. Gmail et Google Calendar se connectent ensemble.

Vous vous êtes inscrit avec Google et avez autorisé Gmail et Calendar sur cet écran ? Ils se connectent automatiquement. L’envoi n’a lieu que lorsque vous appuyez sur Envoyer.

Vous pouvez aussi passer par le tableau de bord : **Connexions**, **E-mail**, sélectionnez Gmail, puis appuyez sur **Se connecter avec Google**. Une fois la connexion terminée, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois qu’il est [associé à votre compte](friends.md#a-machine-on-your-own-computer) :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **E-mail**, et sélectionnez Gmail.
2. Appuyez sur **Se connecter avec Google** et connectez-vous dans l’onglet qui s’ouvre. Gmail et Google Calendar se connectent ensemble.

Si votre ordinateur n’est pas associé à votre compte, ou si vous utilisez votre propre client OAuth Google, ouvrez **Utiliser votre propre app** à cet endroit, ou exécutez `assistant connect gmail`. Appuyez sur **Ouvrir Google**, connectez-vous, puis collez l’adresse vers laquelle Google vous redirige. Google Calendar associé à la même adresse se connecte aussi.

Un administrateur Google Workspace devra peut-être d’abord autoriser l’app dans la console d’administration.

## Déconnecter Gmail

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse sur votre page de configuration. Gmail et Calendar sont alors déconnectés pour cette adresse, et votre Machine oublie la connexion. Vos autres Machines conservent la leur. Dans le tableau de bord, **Déconnecter ↗** dans Connexions vous redirige vers cette page. **Reconnecter** à cet endroit vous permet de vous connecter à nouveau sans quitter le tableau de bord.
- Sur votre propre ordinateur : ouvrez **Connexions**, sélectionnez Gmail, puis **Détails** et **Déconnecter**. Gmail cesse alors de lire vos e-mails. Les données déjà importées sont conservées. Si aucun autre service n’utilise cette connexion Google, votre Machine l’oublie. Vos autres Machines conservent la leur.

## Désinstaller l’app de Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions aux applications et services tiers, et supprimez Salesflare (Se connecter avec Google ou hébergé) ou votre propre app.
