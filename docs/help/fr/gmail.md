---
title: Gmail
area: connections
summary: Lit vos e-mails et rédige des réponses dans votre style. N’envoie un e-mail qu’après votre approbation.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: e06946aaa6ad0e1a
---
## Ce qu’elle lit

Tous vos e-mails : ceux des 7 derniers jours au moment de la connexion, puis tous les nouveaux e-mails reçus et envoyés. Les e-mails que vous envoyez comptent aussi, pour qu’elle apprenne votre façon d’écrire et ce que vous avez promis.

Les promotions, les newsletters et les e-mails des onglets Mises à jour et Forums sont d’abord examinés rapidement : expéditeur, objet et quelques mots, souvent plusieurs à la fois. Si l’un d’eux est important, elle le lit en entier et peut en faire une tâche. Aucun message n’est ignoré sans être examiné.

## Ce qu’elle peut envoyer

Un e-mail à partir d’une tâche, et uniquement après votre approbation. **Faire** prépare un brouillon ; **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Rien n’est envoyé avant que vous appuyiez sur **Envoyer maintenant**. **Se connecter avec Google** demande aussi à Google l’autorisation d’envoyer des e-mails. Avec votre propre app sur votre propre ordinateur, la connexion donne un accès en lecture seule jusqu’à ce que vous ajoutiez vous-même l’envoi.

Dans l’écran de vérification, **De** est un petit menu qui apparaît lorsque Gmail autorise cette boîte mail à envoyer des e-mails en tant qu’alias de l’une de vos adresses (une adresse marquée **Les miens** dans **Paramètres**, [Vos adresses](settings.md#your-addresses)). Une réponse à un e-mail reçu sur cet alias est envoyée depuis celui-ci ; un nouvel e-mail est envoyé depuis l’adresse de votre boîte mail. Juste avant l’envoi, Gmail est interrogé à nouveau : si l’adresse n’est pas confirmée, rien n’est envoyé.

Une réponse est ajoutée au fil de discussion de l’e-mail auquel elle répond. Si elle est envoyée depuis une autre de vos boîtes mail que celle qui a reçu l’e-mail, la tâche vous le signale avant l’envoi. La réponse est tout de même ajoutée à leur fil de discussion.

## Connecter Gmail

Sur une Machine hébergée :

1. Ouvrez votre page de configuration à l’adresse app.themachine.computer/setup.
2. Sous **Mail et calendrier**, appuyez sur **Connecter Google**, puis connectez-vous. Sur l’écran de Google, le nom Salesflare apparaît. C’est l’entreprise qui a créé The Machine.
3. Gmail et Google Calendar se connectent ensemble.

Vous vous êtes inscrit avec Google et avez autorisé Gmail et Google Calendar sur cet écran ? Ils se connectent automatiquement. Les e-mails ne sont envoyés que lorsque vous appuyez sur Envoyer.

Vous pouvez aussi passer par le tableau de bord : **Connexions**, **E-mail**, sélectionnez Gmail, puis appuyez sur **Se connecter avec Google**. Une fois la connexion terminée, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois celui-ci [associé à votre compte](friends.md#a-machine-on-your-own-computer) :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **E-mail**, et sélectionnez Gmail.
2. Appuyez sur **Se connecter avec Google** et connectez-vous dans l’onglet qui s’ouvre. Gmail et Google Calendar se connectent ensemble.

Si l’ordinateur n’est pas associé à votre compte ou si vous utilisez votre propre client OAuth Google, ouvrez **Utiliser votre propre app** à cet endroit ou exécutez `assistant connect gmail`. Appuyez sur **Ouvrir Google**, connectez-vous, puis collez l’adresse vers laquelle Google vous redirige. Google Calendar associé à la même adresse est également connecté.

Un administrateur Google Workspace devra peut-être d’abord autoriser l’app dans la console d’administration.

## Déconnecter Gmail

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse sur votre page de configuration. Gmail et Calendar sont alors déconnectés pour cette adresse, et votre Machine oublie les informations de connexion. Vos autres Machines les conservent. Dans le tableau de bord, **Déconnecter ↗** dans Connexions vous mène à cette page. **Reconnecter** vous permet de vous connecter à nouveau sans quitter le tableau de bord.
- Sur votre propre ordinateur : ouvrez **Connexions**, sélectionnez Gmail, puis **Détails** et **Déconnecter**. La lecture des e-mails s’arrête. Les e-mails déjà importés restent disponibles. Si aucun autre service sur cet ordinateur n’utilise cette connexion Google, il l’oublie. Vos autres Machines la conservent.

## Désinstaller l’app sur Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions aux applications et services tiers, et supprimez Salesflare (Se connecter avec Google ou hébergé) ou votre propre app.
