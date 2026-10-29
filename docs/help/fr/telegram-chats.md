---
title: Discussions Telegram
area: connections
summary: Vos discussions et petits groupes Telegram, lus comme un appareil de votre propre compte. Elle ne répond qu’après votre accord.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## Ce qu’elle lit

Vos discussions privées et les groupes jusqu’à 50 personnes, comme un appareil connecté à votre propre compte Telegram, à la manière de Telegram Desktop. À la connexion, elle lit les 7 derniers jours, puis ce qui arrive.

Elle ne lit jamais les chaînes, les bots, les Messages enregistrés ni les messages de service de Telegram. Les discussions en sourdine et archivées sont aussi ignorées.

Elle ne touche pas à votre statut de lecture ni de présence : rien n’est marqué comme lu, et votre téléphone affiche toujours les nouveaux messages comme nouveaux.

C’est distinct de [Telegram](telegram.md), où votre propre bot vous envoie vos tâches.

## Ce qu’elle peut envoyer

Un texte dans une discussion qui existe déjà, seulement après votre accord sur la tâche. Les envois partent un par un, avec une pause entre chaque.

Si une tâche est arrivée par e-mail mais que vous parlez à cette personne sur Telegram, dites-le dans le chat de la tâche. The Machine trouve votre discussion existante avec elle et passe le brouillon sur Telegram, pour que vous le vérifiiez et l’envoyiez. Elle ne lance jamais de nouvelle discussion.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez Discussions Telegram.
2. Choisissez **Scanner un code QR dans Telegram sur votre téléphone**.
3. Sur votre téléphone, dans Telegram, ouvrez Paramètres, Appareils, **Link Desktop Device**, et scannez le code.
4. Si votre compte a un mot de passe cloud, saisissez-le quand il est demandé. Il va à Telegram et n’est jamais enregistré.

Vous configurez sur votre téléphone, sans second écran pour scanner ? Choisissez plutôt **Recevoir un code dans Telegram pour votre numéro**. Le formulaire indique où Telegram a envoyé le code : dans votre app Telegram sur un autre appareil, par SMS ou à votre e-mail de connexion. Pas de code ? Appuyez sur **Renvoyer le code**.

Sur votre propre ordinateur, il vous faut aussi votre propre ID d’app Telegram. Créez-en un sur [my.telegram.org](https://my.telegram.org), sous API development tools, et saisissez son api_id et son api_hash dans le formulaire.

Ou lancez `assistant connect telegram` dans un terminal et scannez le code qu’il y affiche.

## Quand elle s’arrête

- **Déconnectée de Telegram** : Telegram a mis fin à la connexion de cet appareil, ou vous l’avez déconnecté sur votre téléphone. Appuyez sur **Reconnecter** sur sa carte.
- **Telegram n’accepte plus l’ID d’app** : Telegram n’accepte plus l’ID d’app qu’utilise cette Machine. Rien n’est lu ni envoyé tant que vous n’appuyez pas sur **Reconnecter** pour ajouter votre propre ID d’app.

The Machine utilise pour cela l’API de Telegram. Telegram peut limiter ou mettre fin aux connexions d’apps comme elle.

## Photos

The Machine demande à Telegram les photos de profil des personnes de votre graph qui n’en ont pas, 50 par jour au maximum, via la même connexion qui lit vos chats, et seulement pour les personnes des chats qu’elle lit. Rien ne leur est envoyé. Une personne qui vous cache sa photo reste sans photo.

## La retirer

**Connexions**, ouvrez Discussions Telegram, **Détails**, puis **Déconnecter**. Votre Machine se déconnecte de Telegram et supprime ce qu’elle gardait pour Telegram.

Ou mettez-y fin sur votre téléphone : dans Telegram, ouvrez Paramètres, Appareils, appuyez sur The Machine et mettez fin à la session.
