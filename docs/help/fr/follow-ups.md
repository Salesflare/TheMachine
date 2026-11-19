---
title: Relances
area: graph
summary: Relancez automatiquement les personnes qui ne répondent pas, pour tout un tableau ou un seul projet. Une confirmation vous est demandée, sauf indication contraire de votre part.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 0e7bdfb2c9b2deb5
---
Quand une personne sur un tableau ne répond plus, votre Machine rédige une relance à votre place, avec vos mots et dans la même conversation. Les relances sont désactivées jusqu’à ce que vous les activiez. Si une de vos compétences correspond au tableau, les brouillons en tiennent compte, y compris pour l’ordre des informations dans l’e-mail.

## Activer les relances

Sur un tableau, sélectionnez **⋯**, puis **Relances…**, et cochez **Relancer sans réponse**. Les relances concernent alors tous les projets de ce tableau. Vous pouvez aussi sélectionner **Relances désactivées** sous le nom du tableau, ou **Les relancer** dans une étape contenant des projets sans réponse depuis au moins 10 jours.

Pour un seul projet, sélectionnez **Relances…** dans son menu **⋯**, sur le tableau ou sur sa page. **Pour ce projet** permet de choisir **Activé**, **Désactivée** ou le paramètre du tableau. Le paramètre propre au projet prime sur celui du tableau.

## Paramètres

- Par défaut, attendez de 3 à 7 jours sans réponse. Une relance est rédigée après le délai le plus court et envoyée au plus tard à la fin du délai le plus long, même si votre quota d’utilisation est presque atteint.
- **Seulement les jours de travail** : aucun brouillon n’est rédigé et aucun message n’est envoyé pendant vos jours de congé (selon **Paramètres** > **Notifications** > **Heures de travail**). Les relances prévues ces jours-là attendent le prochain matin où vous travaillez. Cette option est activée pour Travail et désactivée pour Personnel.
- Par défaut, envoyez de 1 à 3 relances. La relance minimale est toujours envoyée, et les autres sont rédigées sous forme de brouillons. Quand votre Machine estime qu’il vaut mieux s’arrêter, le brouillon en indique la raison (« The Machine s’arrêterait ici : 9 e-mails sans réponse depuis août ») et n’est pas coché. Vous pouvez l’envoyer, l’ignorer ou choisir **Arrêter les relances ici**. Le nombre maximal de relances ne sera jamais dépassé.
- **Étapes** : **Toutes les étapes ouvertes** sont incluses, à l’exception de la dernière étape du tableau et de l’étape Au point mort ou refusé. **Personnaliser** permet d’activer ou de désactiver des étapes et de définir un délai propre à chacune.
- **Canaux** : les canaux connectés qui permettent d’envoyer des messages. Une relance est envoyée sur le même canal que le dernier message. **Changer de canal sans réponse** permet d’essayer le prochain canal autorisé.
- **Déplacer vers « Au point mort ou refusé » après la dernière** : cette option est activée si le tableau comporte cette ligne.

## Demander confirmation ou envoyer automatiquement

Par défaut, l’option **Me demander avant d’envoyer** est activée : les brouillons attendent dans vos tâches. **Envoyer sans demander** donne une autorisation permanente pour ce tableau ou ce projet. Tout cas inhabituel ou échec attend tout de même votre intervention, et le niveau de prudence demande toujours votre confirmation. Une relance n’est jamais envoyée deux fois. Les relances ne vous envoient aucune notification, ni par e-mail ni par notification push : leurs brouillons apparaissent dans votre liste et dans le récap du matin.

Juste avant l’envoi, la conversation est vérifiée une nouvelle fois. Si quelqu’un a écrit depuis la création du brouillon, celui-ci n’est pas envoyé : « Non envoyé : nouveau message dans la conversation ». La tâche affiche ce message, son auteur et sa date, avec **La lire** et **Refaire pour ce message**. Cette dernière option demande un nouveau brouillon qui tient compte du message.

## Vérifier les relances

Les relances d’un tableau sont regroupées dans une seule tâche, et non dans une tâche par e-mail. Pendant la rédaction des brouillons, la tâche indique « Rédaction de 3 relances… », puis « 8 relances prêtes pour les testeurs Alpha ».

**Vérifier** les affiche les unes sous les autres, au complet, pour que vous puissiez toutes les lire en faisant défiler la page. Les options **Envoyer**, **Modifier** et **Ignorer** s’affichent pour la relance en cours. Au clavier, les touches j et k (ou les flèches) permettent de passer d’une relance à l’autre, Entrée l’envoie, e permet de la modifier, s de l’ignorer (et de rétablir l’action), x de la cocher ou de la décocher, et c d’y apporter des modifications. **Envoyer tous les éléments cochés** envoie ceux qui sont encore cochés.

Chaque relance est accompagnée de son brouillon. Si la rédaction est impossible, la tâche indique ce qu’il faut d’abord (« Pas de brouillon. À préciser : le destinataire. ») et n’est pas cochée. **Rédiger** demande tout de même de créer le brouillon. Si un brouillon a plusieurs destinataires possibles, la tâche indique « Destinataire : à choisir au moment de l’envoi », et **Envoyer** vous demande de faire un choix.

**Ignorer** décoche un brouillon et le déplace en bas de la liste, avec la mention « Ignorée » et une option **Annuler**. Il est définitivement ignoré lorsque vous fermez la vérification. Une relance ignorée peut être rétablie avec **Récupérer**, dans les relances du projet ou dans sa tâche sous Fait, à condition qu’aucune relance plus récente n’ait été envoyée. La relance d’un seul projet est une tâche normale.

**Demander des modifications…** réécrit tous les brouillons cochés, ou seulement celui en cours, selon vos indications. Rien n’est envoyé et **Annuler la modification** restaure le texte précédent. Tant que la zone de saisie est ouverte ou qu’une réécriture est en cours, aucun message ne peut être envoyé. Tout brouillon modifié s’affiche de nouveau avant son envoi.

Lorsque plusieurs relances sont envoyées à la suite, y compris avec **Envoyer sans demander**, chaque boîte mail en envoie une toutes les 30 à 45 secondes. La tâche indique la progression : « Envoi de 3 sur 8… ». **Arrêter l’envoi** interrompt les envois restants. Un message déjà en cours d’envoi part tout de même, et les autres reviennent dans la vérification sous forme de brouillons, à envoyer plus tard (« Envoi interrompu. 1 envoyé, 11 conservés en brouillons. »).

## E-mails envoyés avant que votre Machine les lise

Les e-mails que vous avez envoyés depuis une autre application avant que votre Machine ne lise cette boîte mail sont également pris en compte. Elle lit la conversation elle-même, ou, si elle n’y arrive pas, les e-mails précédents cités dans votre dernier message. Ainsi, trois e-mails sans réponse comptent comme trois, et le délai « Sans réponse depuis » commence à partir du premier. Si vous avez déjà atteint le maximum, aucun autre brouillon n’est créé.

## Quand les relances s’arrêtent

Les relances s’arrêtent dès qu’une réponse est reçue, quand le projet est gagné, perdu, archivé ou déplacé dans une étape fermée, ainsi que lorsque vous mettez une relance en attente ou l’ignorez. Avant de rédiger un brouillon, votre Machine vérifie si la conversation contient un message plus récent. Elle ne relance donc pas quelqu’un qui a déjà répondu ailleurs.

**Mettre en pause**, dans **Relances…**, suspend les relances d’un tableau ou d’un projet sans les désactiver. Aucun brouillon n’est rédigé et aucun message n’est envoyé, aucun cycle ne se termine et les tâches de relance en cours restent ouvertes. Choisissez une date de reprise ou sélectionnez **Reprendre** quand vous le souhaitez. Le délai reprend là où il en était et les relances arrivées à échéance sont envoyées une par une. Le statut **En pause** s’affiche entre-temps.

Après la dernière relance sans réponse, le projet affiche « Aucune réponse après 3 relances » et passe à l’étape Au point mort ou refusé si cette option est activée. Si les relances sont arrêtées avant tout envoi, le projet affiche « Relances arrêtées » et reste dans son étape.

Si l’e-mail a été rejeté et que la personne a une autre adresse, la relance y est envoyée (« Adresse rejetée, envoi à <address> »). Si l’adresse d’un brouillon est rejetée avant son envoi, celui-ci est mis en attente : « Non envoyé : <address> a été rejetée ». Il est déplacé vers l’autre adresse de la personne et attend que vous sélectionniez **Envoyer**.

S’il n’y a pas d’autre adresse, les relances passent sur LinkedIn ou WhatsApp si ces canaux sont autorisés et que vous y échangez avec la personne. Sinon, elles s’arrêtent avec la mention « E-mail rejeté ». Si le projet est important, une tâche vous invite à trouver une nouvelle adresse.

## Où les voir

L’en-tête du tableau indique « Relances activées, prochaine relance jeu. ». Un projet du tableau affiche sa prochaine relance ou indique qu’une relance est prête. La page du projet répertorie les relances envoyées, y compris celles envoyées automatiquement.

Les relances sont mises en attente pendant que votre Machine est occupée ou proche de sa limite d’utilisation, puis rattrapées plus tard. Sur un tableau partagé, seule la Machine de la personne propriétaire du projet effectue les relances.
