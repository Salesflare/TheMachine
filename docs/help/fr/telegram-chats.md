---
title: Chats Telegram
area: connections
summary: Vos chats Telegram et petits groupes, lus comme sur un appareil connecté à votre compte. Les réponses ne sont envoyées qu’après votre approbation.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
translated: da17aef29a380002
---
## Ce qu’elle lit

Vos chats privés et groupes de 50 personnes maximum, comme sur Telegram Desktop, depuis un appareil connecté à votre compte Telegram. À la connexion, elle lit les 7 derniers jours de messages, puis les nouveaux messages.

Elle ne lit jamais les chaînes, les bots, les Messages enregistrés ni les messages de service de Telegram. Les chats mis en sourdine ou archivés sont également ignorés.

Elle ne modifie pas vos statuts « lu » ou « en ligne » : aucun message n’est marqué comme lu et votre téléphone continue d’afficher les nouveaux messages comme tels.

Cette connexion est distincte de [Telegram](telegram.md), où votre propre bot vous envoie vos tâches.

## Ce qu’elle peut envoyer

Un message texte dans un chat existant, uniquement après votre approbation sur la tâche. Les messages sont envoyés un par un, avec une pause entre chacun.

Si une tâche est arrivée par e-mail, mais que vous échangez avec cette personne sur Telegram, dites-le dans le chat de la tâche. The Machine trouve votre chat existant avec cette personne et remplace le brouillon par un message Telegram, que vous pourrez vérifier et envoyer. Elle ne commence jamais un nouveau chat.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez les chats Telegram.
2. Choisissez **Scanner un QR code avec Telegram sur un autre appareil**.
3. Sur votre téléphone, dans Telegram, ouvrez Paramètres, Appareils, **Associer un appareil de bureau**, puis scannez le code.
4. Si votre compte utilise un mot de passe cloud, saisissez-le lorsqu’on vous le demande. Il est envoyé à Telegram et n’est jamais enregistré.

Sur un téléphone, le formulaire propose d’abord **Recevoir un code sur votre numéro de téléphone**, car il est impossible de scanner un QR code depuis le même écran. Il indique où Telegram a envoyé le code : dans votre application Telegram sur un autre appareil, par SMS ou à votre adresse e-mail de connexion. Vous n’avez pas reçu de code ? Appuyez sur **Renvoyer le code**.

Sur votre propre ordinateur, vous avez également besoin de votre propre ID d’application Telegram. Créez-en un sur [my.telegram.org](https://my.telegram.org), dans les outils de développement API, puis renseignez son api_id et son api_hash dans le formulaire.

Vous pouvez aussi lancer `assistant connect telegram` dans un terminal et scanner le code qui s’affiche.

## En cas d’interruption

- **Déconnectée de Telegram** : Telegram a mis fin à la connexion de cet appareil, ou vous l’avez déconnecté sur votre téléphone. Appuyez sur **Reconnecter** dans **Connexions**.
- **Telegram n’accepte plus l’ID d’app** : Telegram n’accepte plus l’ID d’application utilisé par cette Machine. Rien n’est lu ni envoyé tant que vous n’avez pas appuyé sur **Reconnecter** et ajouté votre propre ID d’application.

Telegram peut limiter ou interrompre les connexions d’applications comme The Machine.

## Photos

The Machine demande à Telegram les photos de profil des personnes de votre Graph qui n’en ont pas, jusqu’à 50 par jour. Elle utilise la même connexion que pour lire vos chats, et ne le fait que pour les personnes présentes dans les chats qu’elle lit. Aucun message ne leur est envoyé. Les personnes qui vous cachent leur photo n’en auront toujours pas.

## La supprimer

Ouvrez **Connexions**, puis les chats Telegram, **Détails**, et enfin **Déconnecter**. Votre Machine se déconnecte de Telegram et supprime les données Telegram qu’elle a conservées.

Vous pouvez aussi mettre fin à la connexion sur votre téléphone : dans Telegram, ouvrez Paramètres, Appareils, appuyez sur The Machine, puis mettez fin à la session.
