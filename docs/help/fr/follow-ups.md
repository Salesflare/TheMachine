---
title: Relances
area: graph
summary: Relancez automatiquement les personnes qui ne répondent pas, pour tout un tableau ou un seul projet. Une confirmation vous est demandée avant l’envoi, sauf indication contraire.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 7
translated: 76bea8f586963be1
---
Quand une personne ne répond plus dans un tableau, votre Machine rédige une relance à votre place, avec votre ton et dans la même conversation. Cette option est désactivée tant que vous ne l’activez pas. Si une de vos compétences correspond au tableau, les brouillons la suivent, notamment pour l’ordre des informations dans l’e-mail.

## L’activer

Dans un tableau, touchez **⋯**, puis **Relances…**, et cochez **Relancer sans réponse**. Cela s’applique à tous les projets du tableau. Vous pouvez aussi toucher **Relances désactivées** sous le nom du tableau, ou **Les relancer** dans une étape contenant des projets sans réponse depuis plus de 10 jours.

Pour un seul projet, touchez **Relances…** dans son menu **⋯**, sur le tableau ou sur sa page. **Pour ce projet** permet de choisir **Activé**, **Désactivé** ou le paramètre du tableau. Le paramètre du projet prime sur celui du tableau.

## Paramètres

- Attente : de 3 à 7 jours sans réponse par défaut. Une relance est rédigée après le délai le plus court et envoyée au terme du délai le plus long, même si votre utilisation est limitée.
- **Seulement les jours de travail** : aucun brouillon n’est rédigé ni envoyé pendant vos jours de congé (selon **Paramètres** > **Notifications** > **Heures de travail**). Les relances prévues ces jours-là attendent le prochain matin ouvré. Activé pour Travail, désactivé pour Personnel.
- Nombre de relances : de 1 à 3 par défaut. Le nombre minimum est toujours envoyé, et le reste est rédigé sous forme de brouillons. Si votre Machine pense qu’il vaut mieux s’arrêter, le brouillon indique pourquoi (« The Machine s’arrêterait ici : 9 e-mails sans réponse depuis août ») et n’est pas coché. Vous pouvez l’envoyer, l’ignorer ou choisir **Arrêter les relances ici**. Le nombre maximal ne sera jamais dépassé.
- **Étapes** : **Toutes les étapes ouvertes**, à l’exception de la dernière étape du tableau et de Au point mort ou refusé. **Personnaliser** permet d’activer ou de désactiver des étapes et de définir un délai propre à chacune.
- **Canaux** : les canaux connectés qui permettent d’envoyer des messages. Une relance est envoyée sur le même canal que le dernier message. **Changer de canal sans réponse** essaie le prochain canal autorisé.
- **Déplacer vers « Au point mort ou refusé » après la dernière** : activé si le tableau comporte cette ligne.

## Demander confirmation ou envoyer automatiquement

**Me demander avant d’envoyer** est le paramètre par défaut : les brouillons attendent dans vos tâches. **Envoyer sans demander** vaut accord permanent pour le tableau ou le projet concerné. Tout cas inhabituel ou tout échec attend tout de même votre intervention, et le niveau Prudent demande toujours confirmation. Une relance n’est jamais envoyée deux fois. Les relances ne vous envoient jamais de notification, ni par notification push ni par e-mail : leurs brouillons attendent dans votre liste et dans le récap du matin.

Juste avant l’envoi, la conversation est vérifiée à nouveau. Si quelqu’un a écrit depuis la création du brouillon, celui-ci n’est pas envoyé : « Non envoyé : nouveau message dans la conversation ». La tâche indique le contenu du message, son auteur et sa date, avec **La lire** et **Refaire pour ce message**. Cette dernière option demande un nouveau brouillon qui tient compte du message.

## Vérifier les relances

Les relances d’un tableau sont regroupées dans une seule tâche, et non dans une tâche par e-mail. Pendant la rédaction, elle indique « Rédaction de 3 relances… », puis « 8 relances prêtes pour Alpha testers ».

**Vérifier** affiche les relances les unes sous les autres, en entier, pour pouvoir toutes les lire en faisant défiler la page. **Envoyer**, **Modifier** et **Ignorer** s’affichent pour la relance en cours. Au clavier, les touches j et k (ou les flèches) permettent de passer d’une relance à l’autre, Entrée l’envoie, e la modifie, s l’ignore (et permet ensuite d’annuler), x la coche ou la décoche, et c permet de la modifier. **Envoyer tout ce qui est coché** envoie les relances toujours cochées.

Chaque relance est accompagnée de son brouillon. S’il est impossible de la rédiger, un message indique ce qu’il faut d’abord (« Aucun brouillon. À préciser d’abord : le destinataire. ») et elle n’est pas cochée. **Rédiger** demande tout de même la création du brouillon. Si plusieurs destinataires sont possibles, le message indique « Destinataire : à choisir au moment de l’envoi », et **Envoyer** vous demande de faire votre choix.

**Ignorer** décoche un brouillon et le déplace en bas de la liste, avec la mention « Ignoré » et l’option **Annuler**. Il est définitivement ignoré à la fermeture de la vérification. Un brouillon ignoré peut être rétabli avec **Récupérer**, dans les relances du projet ou dans sa tâche sous Fait, tant qu’aucune relance plus récente n’a été envoyée. La relance d’un projet seul est une tâche normale.

**Demander des modifications…** reformule tous les brouillons cochés ou seulement celui en cours, selon vos instructions. Rien n’est envoyé, et **Annuler la modification** restaure le texte précédent. Tant que le champ de demande est ouvert ou que la reformulation est en cours, rien ne peut être envoyé. Tout brouillon modifié s’affiche à nouveau avant l’envoi.

Lorsque plusieurs relances sont envoyées à la suite, y compris avec Envoyer sans demander, chaque boîte aux lettres en envoie une toutes les 30 à 45 secondes. La tâche indique l’avancement : « Envoi de 3 sur 8… ». **Arrêter l’envoi** interrompt les envois restants. Celui déjà en cours est envoyé, et les autres redeviennent des brouillons dans la vérification, prêts à être envoyés plus tard (« Envoi arrêté. 1 envoyé, 11 conservés en brouillon. »).

## E-mails envoyés avant que votre Machine ne lise la boîte aux lettres

Les e-mails que vous avez envoyés depuis une autre application avant que votre Machine ne lise cette boîte aux lettres sont également pris en compte. Elle lit la conversation elle-même ou, si elle n’y parvient pas, les e-mails précédents cités dans votre dernier message. Ainsi, trois e-mails sans réponse comptent comme trois, et le délai « Sans réponse depuis » commence à partir du premier. Si vous avez déjà atteint le nombre maximal, aucun autre brouillon n’est rédigé.

## Quand les relances s’arrêtent

Les relances s’arrêtent dès qu’une personne répond, que le projet est gagné, perdu, archivé ou déplacé vers une étape fermée, ou encore quand vous mettez une relance en attente ou l’ignorez. Avant de rédiger une relance, votre Machine vérifie si la conversation contient un nouveau message, pour éviter de relancer quelqu’un qui a déjà répondu ailleurs.

Une relance se clôt également si quelqu’un a déjà écrit à nouveau dans la même conversation. Une relance d’un autre projet n’est jamais prise en compte. Si votre Machine estime qu’une relance n’est pas nécessaire pour une autre raison, la tâche reste ouverte et indique pourquoi. C’est à vous de décider.

**Mettre en pause**, dans **Relances…**, suspend les relances d’un tableau ou d’un projet sans les désactiver : aucun brouillon n’est rédigé ni envoyé, aucun cycle ne se termine et les tâches de relance ouvertes restent ouvertes. Choisissez une date de reprise ou touchez **Reprendre** quand vous êtes prêt. Le délai reprend là où il s’était arrêté, et les relances échues sont traitées une par une. Le statut **En pause** s’affiche entre-temps.

Après la dernière relance sans réponse, le projet indique « Aucune réponse après 3 relances » et passe à Au point mort ou refusé si cette option est activée. Si les relances ont été arrêtées avant tout envoi, il indique « Relances arrêtées » et reste dans son étape.

Si l’e-mail a été rejeté et que la personne a une autre adresse, la relance y est envoyée (« Adresse rejetée, envoi à <address> »). Si l’adresse d’un brouillon est rejetée avant son envoi, celui-ci est mis en attente : « Non envoyé : <address> a rejeté le message ». Il est associé à l’autre adresse de la personne et attend que vous l’envoyiez.

Si aucune autre adresse n’est disponible, les relances passent à LinkedIn ou WhatsApp lorsque ces canaux sont autorisés et que vous échangez avec la personne dessus. Sinon, elles s’arrêtent avec le message « E-mail non distribué ». Si le projet est important, une tâche vous invite à trouver une nouvelle adresse.

## Où les retrouver

L’en-tête du tableau indique « Relances activées, prochaine relance jeudi ». Un projet du tableau affiche sa prochaine relance ou précise qu’une relance est prête. La page du projet répertorie les relances envoyées, y compris celles envoyées automatiquement.

Les relances attendent si votre Machine est occupée ou approche de sa limite d’utilisation, puis reprennent plus tard. Dans un tableau partagé, seule la Machine de la personne propriétaire du projet effectue les relances.
