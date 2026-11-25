---
title: Agenda
area: calendar
summary: Votre semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 9b7475608bb04e5c
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions de vos agendas connectés,
- les tâches à échéance ce jour-là et les tâches en attente qui reviennent ce jour-là,
- les suivis sur le travail que vous avez transféré,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) issus des e-mails de réservation et de billets.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ils ne génèrent jamais de tâche. Les événements sur une journée entière ou sur plusieurs jours s’affichent comme événements sur la journée entière, chaque jour concerné. Dans Agenda, un voyage apparaît en premier chaque jour où il a lieu. Dans les vues Semaine et Mois, il apparaît sous forme d’une bande sur les jours concernés, par exemple « Voyage à Lisbonne ».

Un projet commun compte comme une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion prévue ce jour-là avec cette même personne s’affiche sur la ligne de la réunion.

**En retard** s’affiche en premier. Une réunion avec une tâche ouverte indique son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée (vous y avez déjà répondu ou son exécution l’a trouvée terminée) ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. La vue remonte à la semaine précédant la connexion de votre agenda, et une ligne en haut indique à partir de quel jour. Une fois votre [historique](history.md) ajouté, elle remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, elle affiche trois jours.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher la liste de ses éléments.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte, tout en restant lisibles. Les autres sont indiqués par **+N**. Sélectionnez cette indication pour ouvrir ce jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, affiche ses détails : date et heure, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et projets associés à la réunion, renvoient vers leur page. **Ouvrir dans Google Agenda** (ou **Ouvrir dans Outlook**) sous ces éléments permet de l’ouvrir dans l’application correspondante. La consultation ne modifie rien.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Un lien de réunion affiche le nom du service correspondant, comme Zoom, Google Meet ou Teams, ou **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking à l’aéroport arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un voyage, quelle que soit votre boîte mail : le train jusqu’à l’aéroport, les vols, la voiture, le logement et le trajet retour. Les réservations sont regroupées lorsque leurs dates se chevauchent ou que l’une commence le jour où l’autre se termine.

Le voyage s’affiche sous forme d’une bande sur les jours concernés. Ouvrez-le pour afficher chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre place.

Les billets de concert, de match, de festival ou de conférence créent un événement, un par événement, avec son lieu, le code de réservation, votre place et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est classé dans Work, sinon dans Personal. Les billets pour un événement qui a lieu pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et votre hôtel. Ces lignes sont grisées et portent la mention **Aucune réservation**. Un voyage sans aucun hébergement n’indique rien au sujet des nuits.

- Chaque ligne indique l’origine de la réservation, par exemple **Depuis Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche provient de l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée disparaît. Lorsque toutes les réservations sont annulées, le voyage ou l’événement disparaît également.
- Une réservation au nom d’une autre personne, par exemple le vol d’un collègue que cette personne vous a transféré, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour les autres, par exemple un e-mail transféré ou une réservation provenant d’un petit site, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques-uns à la fois, et attend si vous approchez de votre limite d’utilisation. Les e-mails de réservation de l’année conservée dans l’[historique](history.md) de votre Machine sont lus en arrière-plan une fois cet historique ajouté.

## Notes et transcription de réunion

Les détails d’une réunion comprennent deux parties. **Notes** est le résumé : décisions et actions à effectuer. **Transcription** reprend mot pour mot les propos échangés. Elle est d’abord repliée et indique sa durée. **Afficher** permet de l’ouvrir.

Si les éléments ne se chargent pas, la tentative est relancée automatiquement pendant environ une demi-minute. Passé ce délai, sélectionnez **Réessayer**.

Chaque partie dispose de ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (sélectionnez deux fois). Le contenu de l’une reste dans cette partie. Pour une réunion modifiable, **Notes** sous le formulaire permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais les éléments que vous avez ajoutés : si les deux sont présents, les deux s’affichent.

Les notes peuvent aussi figurer dans l’événement correspondant de l’agenda, après le début de la réunion, ou arriver par e-mail depuis Zoom ou Gemini. Après la réunion, The Machine en tire des tâches uniquement si les prochaines étapes sont claires. Si les mêmes notes arrivent de deux façons, elles ne créent qu’une seule tâche, dont la réunion est la source : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à effectuer, dans la langue de la réunion.

Le message **Rédaction des notes…** s’affiche, et la rédaction continue même si vous fermez la réunion. Une réunion longue peut nécessiter quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple « ajoute cette transcription à la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcript, un résumé dans Notes. Dans l’agenda, une réunion qui contient l’un de ces éléments indique **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les suites à donner à la réunion. Elles sont classées Work ou Personal comme la réunion et ne sont transmises à votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails où que vous la trouviez : dans un fil chronologique, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine** en bas de page affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre agenda Google depuis cette page. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un (sur téléphone, sélectionnez **+** dans la barre supérieure) : choisissez l’agenda, un titre et un horaire. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (sélectionnez deux fois).

**Lieu** suggère des endroits au fur et à mesure de votre saisie : d’abord ceux que vous avez déjà utilisés et vos organisations, puis des adresses d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour effectuer la recherche. Sélectionnez une suggestion ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes qui recevront une invitation sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous sélectionnez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’une prise en charge. Les changements sont indiqués précisément. Seules les options **Ajouter**, **Enregistrer** ou **Supprimer** permettent de les appliquer.

Vous n’avez pas encore de réunion ? Sans agenda connecté, **Connecter votre agenda** ouvre Connexions. Vous pourrez connecter [Google Agenda](google-calendar.md), le [Calendrier Outlook](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Quand une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche au sujet de l’événement le plus récent. Elle peut rédiger un bref message pour le déplacer, ou proposer de le refuser. Rien n’est envoyé sans votre approbation.

Un événement qui chevauche plusieurs autres événements ne crée qu’une seule tâche, à son sujet. Tout nouveau chevauchement s’y ajoute tant que la tâche est ouverte. Une fois la tâche terminée ou écartée, seul un événement créé ou modifié par la suite peut la faire réapparaître.

Les événements sur une journée entière, marqués comme libres ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Les lieux de travail, plages de concentration et absences du bureau définis dans Google ne sont pas pris en compte non plus. Il en va de même pour un bloc que vous avez créé et qui contient d’autres réunions, par exemple une journée au bureau : seules les réunions qu’il contient peuvent entrer en conflit. Un bloc sans autre participant et sans réunion, comme un vol, entre toutefois en conflit avec un événement auquel d’autres personnes participent.

Une tâche Work indique seulement qu’il y a un conflit. Votre équipe ne voit donc jamais l’événement personnel. Vous seul voyez les événements concernés : les deux premiers, puis le nombre d’autres événements. Une tâche à laquelle vous n’avez pas donné suite se ferme automatiquement si le conflit concerne une autre tâche ou n’en était finalement pas un.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer la réunion**. Elle contient un bref récapitulatif :

- **Qui :** leur identité d’après votre Graph, ainsi que des éléments de leur parcours, si ces informations sont connues.
- **Organisation :** l’activité de leur entreprise, ses clients et ses tarifs, si c’est pertinent pour la réunion.
- **Jusqu’ici :** vos échanges, questions et propositions, ainsi que leur état d’avancement. Après la réunion, ces messages figurent parmi les sources de la tâche.
- **Déjà convenu :**, **Modifié depuis :** et **Encore à faire :** les éléments issus des réunions précédentes avec les mêmes personnes, chaque ligne indiquant la réunion ou le message dont elle provient.
- **Promesses en attente :** ce que vous ou ces personnes devez encore faire, d’après les promesses enregistrées sur votre Machine.
- **Questions en suspens :** les questions qui n’ont pas encore reçu de réponse.
- **À décider ou à apporter :** les points à régler ou les éléments à apporter, ainsi que les sujets qui les intéresseront probablement.

Elle arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle est uniquement destinée à être consultée. Sélectionnez **Fait** une fois que vous l’avez lue. Une promesse ou une question qui nécessite une action dispose de sa propre tâche.

Les réunions précédentes sont prises en compte si une personne extérieure participe aux deux, quel que soit leur intitulé ou l’adresse utilisée. La Machine lit les notes disponibles : les vôtres, celles de votre application de réunion ou celles qu’elle vous a envoyées par e-mail. À défaut, elle utilise la transcription ou les notes de l’événement dans l’agenda. Les notes les plus récentes comptent davantage, et un point réglé depuis n’est plus indiqué comme étant en suspens.

Les notes et les messages de l’[Historique](history.md) sont également pris en compte. Le récapitulatif peut donc mentionner des réunions antérieures à votre arrivée.

Un récapitulatif professionnel ne consulte aucune note personnelle ni aucun contenu provenant de la Machine d’une autre personne. Il reste privé : un transfert ne l’emporte pas avec lui et il ne peut pas être envoyé pour vérification. Sans notes, les sections concernées ne s’affichent pas.

Le récapitulatif s’appuie sur les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne d’une entreprise, il consulte également la page d’accueil du site Web de cette entreprise.

Si la recherche sur le Web est configurée sur votre Machine, une recherche rapide est aussi effectuée sur le nom de la personne et son entreprise. Une Machine hébergée n’en dispose pas. Sur votre propre ordinateur, vous pouvez la configurer dans OpenClaw. Les résultats sont accompagnés d’un lien. Seuls le nom public de la personne, le nom de l’entreprise et son site Web sont transmis à la recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours.

Une première réunion que vous avez acceptée peut ainsi avoir son récapitulatif avant même que vous ayez échangé un mot : l’activité de l’entreprise, ce que cela signifie pour vous et, si l’information est connue, l’identité des personnes. Si seul un prénom est disponible, les résultats de recherche ne sont conservés que s’ils désignent une seule personne. Si **Rechercher les contacts pro** est désactivé dans Paramètres, sous Sécurité, aucune recherche n’est effectuée.

Une réunion récurrente ne reçoit un récapitulatif que s’il y a du nouveau depuis la dernière occurrence : un message, des notes ou une promesse. Le récapitulatif indique les nouveautés, pas le contenu du précédent. Il arrive une fois la réunion précédente terminée, pour deux réunions récurrentes par jour au maximum.

S’il n’y a rien d’utile à signaler, aucune tâche n’est créée. Les réunions internes, personnelles ou refusées n’en génèrent pas. Si une réunion est déplacée, sa tâche est conservée à la nouvelle date. Une tâche écartée ne réapparaît pas et celle d’une réunion annulée se ferme automatiquement.

Si une mise à jour modifie le contenu d’un récapitulatif, les récapitulatifs déjà créés pour les réunions à venir sont rédigés à nouveau, une seule fois, dans leur nouvelle version. Leur titre, leurs sources et leur place dans votre liste restent inchangés. Un récapitulatif que vous avez modifié, mis en attente ou fermé reste tel quel. Il en va de même pour celui d’une réunion qui commence dans les prochaines minutes.

Dans les détails d’une réunion, sa tâche apparaît sous **Tâche**. Touchez-la pour ouvrir son chat.
