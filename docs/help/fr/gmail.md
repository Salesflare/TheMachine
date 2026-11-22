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
## Ce qu’elle lit

Tous vos e-mails : ceux des 7 derniers jours au moment de la connexion, puis tous les nouveaux, envoyés comme reçus. Les e-mails que vous envoyez comptent aussi. Elle apprend ainsi votre façon d’écrire et les promesses que vous avez faites.

Les e-mails de type Promotions, newsletters, Mises à jour et Forums sont d’abord parcourus rapidement : expéditeur, objet et quelques mots, plusieurs à la fois. Si l’un d’eux est important, elle le lit en entier et peut en faire une tâche. Rien n’est ignoré sans avoir été consulté.

## Ce qu’elle peut envoyer

Un e-mail lié à une tâche, et seulement après votre approbation. **Faire** prépare un brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer maintenant**. **Se connecter avec Google** demande aussi à Google l’autorisation d’envoyer des e-mails. Avec votre propre app sur votre ordinateur, la connexion est en lecture seule jusqu’à ce que vous activiez vous-même l’envoi.

Dans l’écran de vérification, **De** ouvre un petit sélecteur si Gmail autorise cette boîte à envoyer des e-mails en tant qu’alias. Il affiche ceux que vous avez marqués **Les miens** dans Paramètres, [Vos adresses](settings.md#your-addresses). Une réponse à un e-mail reçu à cette adresse part de cet alias. Un nouvel e-mail part de l’adresse de votre boîte. Juste avant l’envoi, Gmail est interrogé à nouveau : si l’adresse n’est pas confirmée, rien n’est envoyé.

Une réponse est ajoutée au fil de discussion de l’e-mail auquel elle répond. Si elle part d’une autre de vos boîtes que celle qui a reçu l’e-mail, la tâche vous le signale avant l’envoi. La réponse est tout de même ajoutée à leur fil de discussion.

Après l’envoi d’une réponse, son fil quitte la boîte de réception et porte le libellé En attente pendant quelques jours (3, sauf indication contraire dans la tâche). Il réapparaît ensuite, ou plus tôt si quelqu’un répond. L’écran de vérification vous l’indique avant l’envoi. C’est votre boîte : si une réponse promet simplement que le travail sera fait, la tâche reste ouverte.

## Connecter Gmail

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup.
2. Sous **E-mail et agenda**, appuyez sur **Connecter Google**, puis connectez-vous. Sur la page de Google, le nom Salesflare apparaît, l’entreprise qui crée The Machine.
3. Gmail et Google Agenda sont connectés ensemble.

Vous vous êtes inscrit avec Google et avez autorisé Gmail et Google Agenda sur cette page ? Ils se connectent automatiquement. Les e-mails ne sont envoyés que lorsque vous appuyez sur Envoyer.

Vous pouvez aussi passer par le tableau de bord : **Connexions**, **E-mail**, choisissez Gmail, puis appuyez sur **Se connecter avec Google**. Une fois la connexion terminée, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois qu’il est [associé à votre compte](friends.md#a-machine-on-your-own-computer) :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **E-mail**, et choisissez Gmail.
2. Appuyez sur **Se connecter avec Google** et connectez-vous dans l’onglet qui s’ouvre. Gmail et Google Agenda sont connectés ensemble.

Si l’ordinateur n’est pas associé, ou si vous utilisez votre propre client OAuth Google, ouvrez **Utiliser votre propre app** sur cette page ou exécutez `assistant connect gmail`. Appuyez sur **Ouvrir Google**, connectez-vous, puis collez l’adresse vers laquelle Google vous redirige. Google Agenda associé à la même adresse est également connecté.

Un administrateur Google Workspace devra peut-être autoriser l’app dans la console d’administration.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse sur votre page de configuration. Gmail et Google Agenda sont alors déconnectés pour cette adresse, et votre Machine oublie la connexion. Vos autres Machines conservent la leur. Dans le tableau de bord, **Déconnecter ↗** sous Connexions vous mène à cette page. **Reconnecter** permet de vous connecter à nouveau sans quitter le tableau de bord.
- Sur votre propre ordinateur : ouvrez **Connexions**, puis Gmail, **Détails**, et appuyez sur **Déconnecter**. La lecture des e-mails s’arrête. Les données déjà importées restent. Si plus rien n’utilise cette connexion Google, votre Machine l’oublie. Vos autres Machines conservent la leur.

## Supprimer l’app de Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions aux applications et services tiers, et supprimez Salesflare (Connexion avec Google ou hébergement) ou votre propre app.
