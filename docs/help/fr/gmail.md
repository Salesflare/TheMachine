---
title: Gmail
area: connections
summary: Lit vos e-mails et rédige des réponses dans votre style. N’envoie un e-mail qu’après votre approbation.
covers: connector:gmail
code: onboarding.py, google_api.py, next_actions.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google, Use your own app
order: 10
translated: f0565a7bf839f49f
---
## Ce qu’elle lit

Tous vos e-mails : ceux des 7 derniers jours au moment de la connexion, puis tous les nouveaux, envoyés et reçus. Les e-mails que vous envoyez comptent aussi, pour qu’elle apprenne votre style et les promesses que vous faites.

Les e-mails des catégories Promotions, newsletters, Mises à jour et Forums sont d’abord parcourus rapidement : expéditeur, objet et quelques mots, plusieurs à la fois. Si l’un d’eux est important, il est lu en entier et peut devenir une tâche. Aucun e-mail n’est ignoré sans être consulté.

## Ce qu’elle peut envoyer

Un e-mail créé à partir d’une tâche, et seulement après votre approbation. **Faire** prépare un brouillon ; **Vérifier et envoyer** l’ouvre, prêt à être modifié, et rien n’est envoyé avant que vous appuyiez sur **Envoyer maintenant**. **Se connecter avec Google** demande aussi à Google l’autorisation d’envoyer des e-mails. Avec votre propre app sur votre ordinateur, la connexion est en lecture seule jusqu’à ce que vous configuriez vous-même l’envoi.

Dans l’écran de vérification, **De** affiche une petite liste quand Gmail permet à cette boîte aux lettres d’envoyer des e-mails sous l’un de vos alias (l’un de ceux marqués **Les miens** dans **Paramètres**, [Vos adresses](settings.md#your-addresses)). Une réponse à un e-mail reçu sous cet alias est envoyée depuis celui-ci ; un nouvel e-mail est envoyé depuis l’adresse de votre boîte aux lettres. Juste avant l’envoi, Gmail est interrogé à nouveau : s’il ne confirme pas l’adresse, rien n’est envoyé.

Une réponse est ajoutée au fil de discussion de l’e-mail auquel elle répond. Si elle est envoyée depuis une autre de vos boîtes aux lettres que celle où l’e-mail a été reçu, la tâche vous l’indique avant l’envoi. La réponse apparaît tout de même dans le fil de discussion de votre correspondant.

Après l’envoi d’une réponse, son fil de discussion quitte votre boîte de réception et passe sous le libellé « En attente » pendant quelques jours (3, sauf indication contraire dans la tâche), puis revient, ou plus tôt si quelqu’un répond. Il ne reste jamais en attente au-delà de la date limite de la tâche : il revient le jour ouvré précédent, et s’il est dû aujourd’hui, il reste dans votre boîte de réception. L’écran de vérification vous l’indique avant l’envoi. C’est votre boîte aux lettres : une réponse qui ne fait que promettre le travail ne ferme pas la tâche.

## La connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup.
2. Sous **E-mail et Agenda**, appuyez sur **Connecter Google**, puis connectez-vous. Sur l’écran de Google, le nom Salesflare apparaît comme éditeur de The Machine.
3. Gmail et Google Agenda sont connectés ensemble.

Vous vous êtes inscrit avec Google et avez autorisé Gmail et Agenda sur cet écran ? Ils se connectent automatiquement. Un e-mail est envoyé uniquement lorsque vous appuyez sur Envoyer.

Vous pouvez aussi passer par le tableau de bord : **Connexions**, **E-mail**, sélectionnez Gmail, puis appuyez sur **Se connecter avec Google**. Une fois la connexion terminée, vous revenez au tableau de bord.

Sur votre propre ordinateur, une fois celui-ci [associé à votre compte](friends.md#a-machine-on-your-own-computer) :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **E-mail**, et sélectionnez Gmail.
2. Appuyez sur **Se connecter avec Google** et connectez-vous dans l’onglet qui s’ouvre. Gmail et Google Agenda sont connectés ensemble.

Si votre ordinateur n’est pas associé, ou si vous utilisez votre propre client OAuth Google, ouvrez **Utiliser votre propre app** à cet endroit, ou exécutez `assistant connect gmail`. Appuyez sur **Ouvrir Google**, connectez-vous, puis collez l’adresse vers laquelle Google vous redirige. Google Agenda associé à la même adresse est également connecté.

Un administrateur Google Workspace devra peut-être d’abord autoriser l’app dans la console d’administration.

## La déconnecter

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse, sur votre page de configuration. Gmail et Agenda sont alors déconnectés pour cette adresse, et votre Machine oublie la connexion. Vos autres Machines conservent la leur. Dans le tableau de bord, **Déconnecter ↗** sous **Connexions** vous amène à cette page. Vous pouvez vous reconnecter depuis cette page avec **Reconnecter**, sans quitter le tableau de bord.
- Sur votre propre ordinateur : ouvrez **Connexions**, sélectionnez Gmail, puis **Détails** et **Déconnecter**. La lecture des e-mails s’arrête. Les e-mails déjà importés sont conservés. Si aucune autre connexion n’utilise cet identifiant Google, il est oublié. Vos autres Machines conservent leur connexion.

## La supprimer de Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions aux applications et services tiers, et supprimez Salesflare (Se connecter avec Google ou Machine hébergée) ou votre propre app.
