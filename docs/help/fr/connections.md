---
title: Connexions
area: connections
summary: Vos sources en un seul endroit : l’état de chacune, en ajouter une, ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Leur état

L’onglet **Connexions** regroupe vos sources en **Mail et agenda**, **Chat** et **Autres sources**. Chacune indique son état : Connectée, En attente de la première synchro, Reconnexion automatique ou Besoin de votre aide. Ouvrez **Détails** pour voir les **Synchros récentes**, où sa synchro est décrite en mots simples (comme « À jour » ou « Première lecture »), et quoi faire.

## En ajouter une

Ouvrez **+ Ajouter** et choisissez une source. Elle demande ce dont elle a besoin, une question à la fois. **Annuler** arrête l’ajout. Une fois la source connectée, votre Machine redémarre pour commencer à la lire, puis ouvre la nouvelle carte, qui montre comment se passe sa première synchro. Sur une Machine hébergée, Google, Microsoft, Microsoft Word, Zoom, Stripe et Intercom se connectent ici : choisissez **Travail** ou **Perso**, connectez-vous et vous revenez à ce formulaire, qui montre où en est la connexion. GitHub, WhatsApp, Codex, Discussions Telegram et votre téléphone Android affichent leur code directement dans ce formulaire.

**Reconnecter** sur une source et dans **Vous attend** ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source compte comme travail (pour une entreprise que vous nommez) ou comme perso. Changez-le sous **Détails**. **Deviné** ne s’affiche que si votre Machine l’a déduit de l’adresse ; dès que vous choisissez, c’est votre choix. Les tâches de travail attendent vos jours de travail.

## En retirer une

Ouvrez la source, **Détails**, puis **Déconnecter**. Elle arrête de lire. Ce qu’elle a déjà récupéré reste. Sur une Machine hébergée, Google, Microsoft, Microsoft Word, Zoom et Stripe affichent **Déconnecter ↗**, qui ouvre votre page de configuration.

**Déconnecté récemment** liste les connexions Google, Microsoft et Zoom que vous avez retirées. **Supprimé, confirmé** signifie que Google a confirmé la déconnexion, ou pour Microsoft et Zoom qu’il ne reste aucune copie. **En attente** indique pourquoi, et votre Machine continue d’essayer.

## Identifiants enregistrés

Les sites qu’utilise le navigateur de votre Machine, comme LinkedIn ou X, peuvent enregistrer un identifiant : cochez **Enregistrer pour la prochaine fois** quand vous vous connectez. **Connexions aux sites** les liste ensuite. Quand un site déconnecte votre Machine, elle se reconnecte en un geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** en retire un.

## Revues

**Revues** montre comment votre Machine lit ce qui arrive : les exécutions récentes, et ce que chacune a trouvé. Voir [Revues en pause](reviews-paused.md).

Chaque connexion a son propre article dans cette section, avec ce qu’elle lit et ce qu’elle peut envoyer.
