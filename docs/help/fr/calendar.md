---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches arrivant à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 7f9f9d9e9a502b7d
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches arrivant à échéance ce jour-là et les tâches en attente, le jour où elles reviennent,
- les suivis des tâches transférées,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) trouvés dans vos e-mails de réservation et de billets.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ces événements ne donnent jamais lieu à une tâche. Les événements sur une journée entière ou plusieurs jours s’affichent comme tels, pour chaque jour concerné. Dans Agenda, un voyage apparaît en premier pour chacun de ses jours. Dans les vues Semaine et Mois, il apparaît sous la forme d’une seule bande sur toute sa durée, comme « Voyage à Lisbonne ».

Un projet élaboré ensemble donne lieu à une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion qui a lieu ce jour-là avec la même personne apparaît sur la ligne de cette réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche en cours affiche son statut : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son traitement l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Vue Agenda, Semaine ou Mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou touchez **Afficher les jours précédents**, pour voir les jours précédents. La vue remonte jusqu’à la semaine précédant la connexion de votre agenda, avec une ligne en haut indiquant le premier jour affiché. Une fois l’[historique](history.md) importé, elle remonte à environ un an.
- **Semaine** affiche une grille, du lundi au dimanche. Sur un téléphone, trois jours s’affichent.
- **Mois** affiche tout le mois. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu au même moment s’affichent côte à côte, tout en restant lisibles. Les autres sont regroupés sous **+N**. Touchez cette indication pour ouvrir la journée dans la vue Agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou avec des invités, les détails s’affichent : date et heure, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, sont des liens vers leur page. Le bouton **Ouvrir dans Google Agenda** (ou **Ouvrir dans Outlook**) situé en dessous ouvre la réunion dans l’application correspondante. La consultation ne modifie rien.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Un lien de réunion s’affiche sous le nom de son service, comme Zoom, Google Meet ou Teams, ou sous **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Lorsqu’une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking à l’aéroport arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un voyage, quel que soit le compte de messagerie concerné : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet de retour. Les réservations sont regroupées lorsque leurs dates se chevauchent ou que l’une commence à la fin de l’autre.

Le voyage s’affiche sous la forme d’une seule bande sur toute sa durée. Ouvrez-le pour voir chaque réservation par ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre place.

Les billets de concert, de match, de festival ou de conférence créent un événement, un par événement, avec son lieu, le code de réservation, votre place et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre adresse professionnelle est classé Travail. Sinon, il est classé Personnel. Les billets pour un événement qui a lieu pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et votre hôtel. Ces lignes sont grisées et marquées **Aucune réservation**. Si le voyage ne comporte aucun hébergement, rien n’est indiqué au sujet des nuits.

- Chaque ligne indique l’origine de la réservation, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche provient de l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne. Une réservation annulée est supprimée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est lui aussi supprimé.
- Une réservation au nom d’une autre personne, comme le vol d’un collègue qu’on vous a transféré, n’est pas ajoutée à vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour celles qui n’en contiennent pas, comme un e-mail transféré ou une réservation faite sur un petit site, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques-uns à la fois, et attend si vous approchez de votre limite d’utilisation. Les e-mails de réservation de l’année couverte par l’[historique](history.md) conservé par votre Machine sont lus en arrière-plan une fois cet historique importé.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à mener. **Transcription** reprend mot pour mot ce qui a été dit. Elle est repliée au départ et indique sa durée. Touchez **Afficher** pour l’ouvrir.

Si elles ne se chargent pas, une nouvelle tentative se lance automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque partie dispose de ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais le contenu que vous avez ajouté. Si les deux sont présents, ils s’affichent tous les deux.

Des notes peuvent aussi être ajoutées à l’événement de calendrier de la réunion, après son début, ou envoyées par e-mail par Zoom ou Gemini. Après la réunion, The Machine crée des tâches à partir de ces notes, mais seulement si elles indiquent clairement les prochaines étapes. Lorsque les mêmes notes arrivent par deux voies différentes, elles ne créent qu’une seule tâche, dont la source est la réunion : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine rédige les notes à partir de la transcription : un bref résumé, les décisions et les actions à mener, dans la langue de la réunion.

Le statut **Rédaction des notes…** s’affiche et la rédaction continue même si vous fermez la réunion. La rédaction d’une longue transcription prend quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple « ajoute cette transcription aux notes de la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée à Transcription, un résumé à Notes. Dans Agenda, une réunion contenant des notes ou une transcription porte la mention **Notes** ou **Transcription**.

The Machine lit les deux pour préparer les suivis de la réunion. Ils sont classés Travail ou Personnel, comme la réunion, et ne sont transmis à votre équipe que si la réunion l’est aussi.

Les détails d’une réunion s’affichent chaque fois que vous l’ouvrez, que ce soit depuis une chronologie, une recherche de messages ou la source d’une tâche. L’option **Invitation d’origine** en bas de page affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier ici votre propre agenda Google. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** en ajoute un (sur téléphone, l’option se trouve sous **+** dans la barre supérieure) : choisissez l’agenda, un titre et l’horaire. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

Le champ **Lieu** suggère des endroits au fur et à mesure de la saisie : d’abord ceux que vous avez utilisés et vos organisations, puis des adresses trouvées sur [OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour effectuer la recherche. Choisissez une suggestion ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option n’est disponible que dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un trajet pour aller chercher quelqu’un. Le détail des changements s’affiche. Seule votre action **Ajouter**, **Enregistrer** ou **Supprimer** les applique.

Pas encore de réunions ? Sans agenda, **Connecter votre agenda** ouvre Connexions, où vous pouvez connecter [Google Agenda](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou l’inverse, The Machine crée une tâche au sujet de l’événement le plus récent. Elle peut rédiger un bref message pour demander à le déplacer ou proposer de le décliner. Rien n’est envoyé avant votre approbation.

Un événement qui chevauche plusieurs autres n’entraîne qu’une seule tâche, à son sujet. Un nouveau chevauchement s’y ajoute tant que la tâche est en cours. Une fois la tâche terminée ou écartée, seul un événement créé ou modifié par la suite la fait réapparaître.

Les événements sur une journée entière, les événements indiqués comme disponibles et les événements provisoires ne sont jamais pris en compte. Chaque conflit n’est signalé qu’une fois. Les lieux de travail, plages de concentration et absences du bureau de Google ne sont pas pris en compte non plus. Il en va de même pour vos propres plages contenant d’autres réunions, comme une journée au bureau : seules les réunions qui s’y trouvent peuvent entrer en conflit. Une plage sans autre personne ni réunion, comme un vol, peut tout de même entrer en conflit avec un événement auquel participent d’autres personnes.

Une tâche Travail indique seulement qu’il y a un conflit. Votre équipe ne voit donc jamais l’événement personnel. Vous seul voyez ce qui entre en conflit avec lui : les deux premiers éléments, puis le nombre d’autres éléments. Une tâche sur laquelle vous n’avez rien fait se ferme automatiquement si son conflit concerne une autre tâche ou s’il n’y avait finalement pas de conflit.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref compte rendu préparatoire :

- **Qui :** leur identité, d’après votre Graph, avec des informations sur leur parcours si elles sont disponibles.
- **Organisation :** l’activité de leur entreprise, ses clients et ses tarifs, si ces informations sont pertinentes pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les propositions faites, ainsi que l’état d’avancement. Ces messages deviennent les sources de la tâche après la réunion.
- **Déjà convenu :**, **Changements depuis :** et **Encore à faire :** les éléments des réunions précédentes avec les mêmes personnes, chaque ligne indiquant la réunion ou le message dont elle provient.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire, d’après les promesses sur votre Machine.
- **Questions en suspens :** les questions qui restent sans réponse.
- **À décider ou à apporter :** les points à régler ou les éléments à apporter, et ce qui pourrait les intéresser.

Le compte rendu arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Il est à consulter : il est marqué **Fait** une fois que vous l’avez lu. Une promesse ou une question qui nécessite une action donne lieu à sa propre tâche.

Posez une question sur la réunion dans son chat ou ajoutez ce que vous savez : The Machine vous répond ou intègre votre note au compte rendu, par exemple dans **À décider ou à apporter**, et en tient compte. Rien n’est envoyé depuis un compte rendu préparatoire.

Les réunions précédentes sont prises en compte lorsqu’une personne extérieure y a participé, quels que soient leur titre et l’adresse qu’elle a utilisée. The Machine lit les notes présentes sur votre Machine : les vôtres, celles de votre application de réunion ou celles qui vous ont été envoyées par e-mail. À défaut, elle lit la transcription ou les notes de l’événement de calendrier. Les plus récentes ont davantage de poids, et un point réglé depuis n’est plus indiqué comme étant en suspens.

Les notes et messages de l’[Historique](history.md) sont aussi pris en compte. Le compte rendu peut ainsi tenir compte des réunions qui ont eu lieu avant que vous commenciez à utiliser The Machine.

Un compte rendu professionnel ne consulte aucune note personnelle ni aucun contenu provenant de la Machine d’une autre personne. Il reste privé : il n’est pas transféré lors d’un transfert et ne peut pas être envoyé pour révision. Si aucune note n’est disponible, les sections correspondantes n’apparaissent pas.

The Machine utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne travaillant dans une entreprise, elle consulte aussi la page d’accueil du site Web de cette entreprise.

Elle effectue également une brève recherche sur le Web à partir du nom de cette personne et de son entreprise. Sur une Machine hébergée, la recherche utilise votre compte ChatGPT ou Claude et consomme une petite partie de votre forfait. Sur votre propre ordinateur, elle utilise le moteur de recherche que vous avez configuré dans OpenClaw, ou votre compte si vous activez cette option (`meeting_prep_signin_search` dans `config.json`). Un moteur configuré est toujours prioritaire.

Seuls le nom public de cette personne, le nom de son entreprise et son site Web sont transmis pour la recherche, jamais vos messages. Les résultats sont accompagnés d’un lien et réutilisés pendant 30 jours. Avec ChatGPT, le modèle indique le lien sans le vérifier : ouvrez-le avant de vous fier aux informations. Le chat de la tâche affiche **A cherché sur le web**.

Ainsi, pour une première réunion que vous avez acceptée, le compte rendu peut être prêt avant même que vous ayez échangé un mot : il présente l’activité de l’entreprise, ce que cela implique pour vous et, si l’information est disponible, l’identité de votre interlocuteur. Si vous ne connaissez que son prénom, les résultats de recherche ne sont conservés que s’ils désignent une seule personne. Si l’option **Rechercher les contacts pro** est désactivée dans Paramètres, Sécurité, aucune recherche ni consultation n’est effectuée.

Une réunion récurrente ne donne lieu à un compte rendu que s’il y a du nouveau depuis la dernière fois : un message, des notes ou une promesse. Le compte rendu indique les nouveautés, sans reprendre celui de la dernière réunion. Il arrive une fois la réunion précédente terminée, pour deux réunions récurrentes par jour au maximum.

Une réunion avec votre seule équipe ne donne lieu à un compte rendu que si les notes précédentes de la même série, ou du même titre avec au moins une personne en commun, contiennent un point qui vous concerne : une action que vous devez encore effectuer, une question qui vous est adressée, une décision qui reste à prendre ou une promesse que vous avez faite. Les actions qui incombent uniquement à des collègues ne sont pas prises en compte. The Machine ne recherche pas d’informations sur vos collègues. Le compte rendu arrive si possible le matin même de la réunion.

S’il n’y a rien d’utile à indiquer, aucune tâche n’est créée. Les réunions personnelles et celles que vous avez déclinées ne donnent lieu à aucun compte rendu. Si une réunion est déplacée, sa tâche est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Si une mise à jour modifie le contenu d’un compte rendu, les comptes rendus des réunions à venir encore ouverts sont réécrits une fois, avec le nouveau contenu. Leur titre, leurs sources et leur place dans votre liste restent inchangés. Un compte rendu que vous avez modifié, mis en attente ou fermé reste tel quel. C’est aussi le cas si la réunion commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**, à un toucher de son chat.
