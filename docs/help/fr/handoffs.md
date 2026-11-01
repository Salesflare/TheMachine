---
title: Transferts
area: fleet
summary: Transférez une tâche à la Machine d’un collègue, avec ce dont il a besoin. Relancez plus tard, ou reprenez-la.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
---
## Transférer une tâche

1. Sur la tâche, choisissez **Transférer à un collègue**.
2. Choisissez à qui, vérifiez ce qui part avec (retirez une partie avec ×) et ajoutez une note. Le texte commence par la tâche et son importance, tirées de la tâche, puis par sa provenance (son lien). Rien d’un compte Perso ou d’une autre entreprise ne part avec.
3. Envoyez-la. Sa Machine la lui montre comme une tâche.

Une conversation Intercom part avec sa place dans Intercom. Si leur Machine lit le même espace de travail Intercom, leur tâche est liée à cette conversation : **Lire le message** l’ouvre, le client y figure, et leur réponse repart dans Intercom. Sinon, la tâche renvoie quand même vers la conversation dans Intercom.

Pendant que vous attendez, la tâche se trouve sous **Revient plus tard**, « Chez Pat · en attente », avec une date de relance. **Relancer maintenant** demande où ça en est ; **Changer l’heure** déplace la relance.

Elle ne revient en haut que s’il y a quelque chose à décider : Pat a répondu, a refusé ou l’a marquée comme faite, le transfert a échoué, ou une échéance est arrivée. Une tâche due aujourd’hui est relancée quelques heures plus tard, une tâche due bientôt la veille ouvrée, une tâche urgente sans date le matin ouvré suivant, et toute autre après 3 jours ouvrés.

De retour pour une relance, elle indique « Toujours chez Pat · relancer ? » : Pat l’a encore, rien n’est revenu. **Relancer maintenant** ouvre le chat ; **Reprendre** et **Transférer à quelqu’un d’autre** sont à côté, et Marquer comme fait, Mettre en attente et Pas nécessaire sont sous Plus.

Le chat de la tâche indique quand elle est partie (« Transférée à la Machine de Pat · 14:02 ») et ce qui est revenu : acceptée, refusée (avec sa note) ou faite. Quand elle revient pour une relance sans réponse, « Pas encore de réponse de Pat » s’affiche sous cette ligne, avec **Marquer comme fait**, **Mettre en attente** et **Pas nécessaire** (pas de Faire : Pat l’a déjà). Pour lui faire signe ou la reprendre, dites-le dans le chat.

Si le transfert n’est pas parti, la tâche et son chat l’indiquent, avec **Réessayer**.

## La transférer plutôt à quelqu’un d’autre

Tant qu’un collègue l’a, la tâche l’indique en une ligne (« Chez Pat · en attente »), avec **Reprendre** et **Transférer à quelqu’un d’autre**. **Reprendre** vous la rend : la Machine de Pat est prévenue, et une réponse de Pat ne la déplace plus.

**Transférer à quelqu’un d’autre** ouvre le formulaire de transfert, pour quelqu’un qui ne l’a pas encore. Ou dites-le dans le chat de la tâche (« ça devrait aller à Kim »). Le nouveau transfert attend sur la tâche que vous le lisiez : « Toujours chez Pat jusqu’à l’envoi à Kim », avec **Vérifier le transfert à** Kim. Cela ouvre le formulaire avec le texte, au nom de Kim.

Une tâche va une seule fois à chaque coéquipier : tant que Pat l’a, la transférer de nouveau à Pat affiche « Pat a déjà cette tâche ».

**Reprendre à** Pat est activé par défaut ; désactivez-le pour que les deux l’aient. Rien ne part avant que vous choisissiez **Transférer**. Le chat indique alors « Reprise à Pat » et « Transférée à la Machine de Kim ». La Machine de Pat est prévenue aussi, et la tâche qu’elle avait créée pour Pat disparaît.

## Quand la personne refuse

Elle peut dire pourquoi : ce n’est pas pour elle, c’est déjà fait, ou pas le temps cette semaine. Choisissez alors **Le faire moi-même**, **Transférer à quelqu’un d’autre** ou **Marquer comme fait**.

## Quelqu’un en dehors du Network

Choisissez **Par e-mail** : votre Machine rédige un e-mail que vous envoyez. Pendant que vous tapez l’adresse, elle propose d’abord des collègues : les personnes de votre Fleet, puis celles du domaine de votre entreprise, puis ce que vous avez tapé avec ce domaine. Ajoutez une page de tâche pour qu’on puisse répondre en un geste : voir [Pages de tâche](task-pages.md).

Uniquement pour les tâches Travail. Cochez ce qui va dans l’e-mail : quelques lignes sur la tâche, son brouillon prêt, ses liens et fichiers. Seul ce que votre Team Graph partage avec l’équipe est proposé : le contenu Perso et Vous seul reste en dehors. **Préparer l’e-mail** place l’e-mail sur la tâche : lisez-le, puis envoyez-le depuis votre propre boîte comme tout e-mail. Aucun pixel de suivi.

La tâche indique alors "Transféré à <nom> par e-mail" et le suit comme une promesse jusqu’à ce que la personne réponde que c’est fait, ou que vous la marquiez faite. L’e-mail se termine par "Reprenez ceci dans votre propre Machine" : en s’inscrivant par ce lien, la personne peut rejoindre votre Fleet et la tâche passe sur sa Machine comme un transfert normal. Désactivez cette ligne dans **Paramètres**, sous Fleet.
