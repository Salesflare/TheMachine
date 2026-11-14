---
title: Discussions Signal
area: connections
summary: Vos discussions et groupes Signal, lus comme un appareil relié à votre téléphone. Elle ne répond qu’après votre accord.
covers: connector:signal
code: onboarding.py, signal_setup.py, signal_mirror.py, signal_store.py, signal_send.py
keywords: Signal, linked device, QR code
translated: b85609009f246615
---
## Ce qu’elle lit

Vos discussions et groupes, comme un appareil relié à votre téléphone, à la manière de Signal Desktop. Signal ne donne aucun ancien message à un nouvel appareil relié : elle lit à partir du moment où vous la reliez.

Photos, messages vocaux et fichiers apparaissent comme ce qu’ils sont (« A envoyé une photo »), jamais avec leur contenu. Un média à vue unique ne garde aucun contenu. Les modifications et suppressions suivent ce qui s’est passé sur votre téléphone, et les messages éphémères quittent votre Machine quand leur délai est écoulé.

Les stories, réactions, appels et Note à soi-même sont ignorés. Rien n’est marqué comme lu.

## Ce qu’elle peut envoyer

Un texte dans une discussion qui existe déjà, seulement après votre accord sur la tâche. Une réponse cite le message auquel elle répond quand cela aide. Les envois partent un par un, avec une pause entre eux.

Si une tâche est arrivée par e-mail mais que vous parlez à cette personne sur Signal, dites-le dans la discussion de la tâche. The Machine trouve votre discussion existante avec elle et passe le brouillon sur Signal, pour que vous le relisiez et l’envoyiez. Elle ne commence jamais de nouvelle discussion.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez Discussions Signal.
2. Sur votre téléphone, dans Signal, ouvrez Paramètres, **Appareils reliés**, **Relier un nouvel appareil**, et scannez le code.

Il vous faut un second écran d’où scanner : Signal ne relie un appareil que par code QR. Ou lancez `assistant connect signal` dans un terminal et scannez le code qui s’y affiche.

Votre Machine garde les clés de l’appareil relié chez elle. Elles ne la quittent jamais.

## Quand elle s’arrête

Il utilise signal-cli, un client Signal non officiel. Votre Machine télécharge une version fixée et vérifie sa somme de contrôle avant de la lancer. Signal peut cesser de l’accepter à tout moment.

- **Signal a dissocié cette Machine** : vous l’avez retirée sur votre téléphone, ou Signal a mis fin à la liaison. Touchez **Reconnecter** dans **Connexions** et scannez un nouveau code.
- **Mettez à jour The Machine pour Signal** : Signal n’accepte plus le client Signal de cette Machine. Mettez à jour The Machine.

## La retirer

**Connexions**, ouvrez Discussions Signal, **Détails**, puis **Déconnecter**. Votre Machine supprime les clés et ce qu’elle gardait pour Signal. Retirez-la ensuite aussi sur votre téléphone : Signal, Paramètres, **Appareils reliés**, touchez The Machine et dissociez-la.
