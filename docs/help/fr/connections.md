---
title: Connexions
area: connections
summary: Vos sources en un seul endroit : l’état de chacune, en ajouter une, ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Leur état

L’onglet **Connexions** regroupe vos sources en **Mail et agenda**, **Chat** et **Autres sources**. Chacune indique son état : Connectée, En attente de la première synchro, Reconnexion automatique ou Besoin de votre aide. Ouvrez **Détails** pour voir les **Synchros récentes**, où sa synchro est décrite en mots simples (comme « À jour » ou « Première lecture »), et quoi faire. Une synchro échouée qu’une synchro suivante a rattrapée s’affiche en gris ; seul un échec qui reste le dernier s’affiche comme un problème, avec l’heure du prochain essai.

Ses compteurs indiquent ce qu’elle a apporté, ce qui est arrivé ces dernières 24 h et ce qui n’est pas encore vérifié. Un agenda compte des événements : tous, ceux des 7 prochains jours et des dernières 24 h.

Sous son état, chaque source dit en une ligne ce qu’elle apporte et, quand elle peut agir, qu’elle ne le fait qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## En ajouter une

Ouvrez **+ Ajouter** et choisissez une source. Elle demande ce dont elle a besoin, une question à la fois. **Annuler** arrête l’ajout. Parti avant la fin ? Rouvrez **Connexions**, sur n’importe quel appareil, et vous reprenez à la même étape. Une fois la source connectée, votre Machine commence aussitôt à la lire et ouvre la nouvelle carte, qui montre comment se passe sa première synchro. Sur une Machine hébergée, Google, Microsoft, Microsoft OneDrive, Zoom, Stripe et Intercom se connectent ici : choisissez **Travail** ou **Perso**, connectez-vous et vous revenez à ce formulaire, qui montre où en est la connexion. GitHub, WhatsApp, Codex, Discussions Telegram et votre téléphone Android affichent leur code directement dans ce formulaire.

Une source déjà connectée l’indique dans la liste, avec son compte. Choisissez-la pour en ajouter une autre à côté : son formulaire le dit et renvoie vers celle que vous avez.

La liste est groupée (**Mail et agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), de A à Z dans chaque groupe.

**Suggéré pour vous** s’affiche en haut quand votre Machine voit une raison pour une source, avec cette raison en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages qui renvoient vers Google Docs, ou une configuration qui n’a pas abouti. Elle compte cela sur votre Machine ; rien n’en sort. Pas de raison, pas de section. Une source connectée n’est jamais suggérée.

**Reconnecter** sur une source et dans **Vous attend** ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source compte comme travail (pour une entreprise que vous nommez) ou comme perso. Changez-le sous **Détails**. **Deviné** ne s’affiche que si votre Machine l’a déduit de l’adresse ; dès que vous choisissez, c’est votre choix. Les tâches de travail attendent vos jours de travail.

Les e-mails et agendas Google et Microsoft suivent leur adresse quand elle est claire : un fournisseur comme Gmail ou Outlook.com, c’est Perso, le domaine de votre équipe, c’est Travail. Sinon, elle demande une fois, juste après la connexion. **Modifier** vous laisse choisir. Si les e-mails disent ensuite le contraire, la tâche **Tirez le meilleur de The Machine** demande une fois s’il faut le changer.

## Capacités

Une source peut apporter des signaux (ce qui arrive devient des to-dos), agir pour vos to-dos (lire un document quand l'un d'eux en a besoin, ou envoyer, répondre ou modifier quelque chose après votre OK), ou les deux. Avec les deux, **Détails** a un interrupteur pour chacune : **Apporte des signaux** et **Peut agir**. L'une reste activée. Pour arrêter les deux, déconnectez la source. Les réponses d'un chat répondent à ce qu'il apporte, donc un chat n'a que **Peut agir**.

Avec **Apporte des signaux** désactivé, elle ne se synchronise pas et sa carte n'affiche aucun compteur. Avec **Peut agir** désactivé, votre Machine ne lit jamais rien à la demande, ne rédige rien et ne modifie rien avec elle. Les sources d'avant ont les deux activées.

## En retirer une

Ouvrez la source, **Détails**, puis **Déconnecter**. Elle arrête de lire. Ce qu’elle a déjà récupéré reste. Sur une Machine hébergée, Google, Microsoft, Microsoft OneDrive, Zoom et Stripe affichent **Déconnecter ↗**, qui ouvre votre page de configuration.

**Déconnecté récemment** liste les connexions Google, Microsoft et Zoom que vous avez retirées. **Supprimé, confirmé** signifie que Google a confirmé la déconnexion, ou pour Microsoft et Zoom qu’il ne reste aucune copie. **En attente** indique pourquoi, et votre Machine continue d’essayer.

## Identifiants enregistrés

Les sites qu’utilise le navigateur de votre Machine, comme LinkedIn ou X, peuvent enregistrer un identifiant : cochez **Enregistrer pour la prochaine fois** quand vous vous connectez. **Connexions aux sites** les liste ensuite. Quand un site déconnecte votre Machine, elle se reconnecte en un geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** en retire un.

## Vérifications

**Vérifications** montre comment votre Machine lit ce qui arrive : les exécutions récentes, et ce que chacune a trouvé. Voir [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, avec ce qu’elle lit et ce qu’elle peut envoyer.
