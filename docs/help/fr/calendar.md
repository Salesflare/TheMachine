---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches mises en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: d6f800709c378338
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches arrivant à échéance ce jour-là et celles mises en attente, le jour où elles réapparaissent,
- les suivis des tâches que vous avez transférées,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) tirés des e-mails de réservation et de billetterie.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Les événements d’un agenda partagé avec vous sont affichés en grisé, avec le prénom de la personne qui l’a partagé. Ils ne génèrent jamais de tâche. Les événements qui durent toute la journée ou plusieurs jours sont affichés comme des événements d’une journée entière, pour chaque jour concerné. Dans l’Agenda, un voyage apparaît en premier pour chacun des jours qu’il couvre. Dans les vues Semaine et Mois, il s’affiche sous la forme d’une bande sur toute sa durée, par exemple « Voyage à Lisbonne ».

Un projet mené à deux donne lieu à une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion avec cette personne le même jour apparaît sur la ligne de la réunion.

**En retard** s’affiche en premier. Une réunion liée à une tâche en cours affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous avez déjà répondu ou que son exécution l’a marquée comme terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche les journées les unes à la suite des autres. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut (ou sélectionnez **Afficher les jours précédents**) pour voir les jours précédents. L’affichage remonte à une semaine avant la connexion de votre agenda. Une ligne en haut indique la date de début. Une fois votre [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte et restent lisibles. Les autres sont regroupés sous **+N**. Sélectionnez ce nombre pour ouvrir la journée dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : date et heure, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et projets liés à la réunion, renvoient vers leur page. **Ouvrir dans Google Agenda** (ou **Ouvrir dans Outlook**) permet de l’ouvrir dans le service correspondant. La consultation n’entraîne aucune modification.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Le lien d’une réunion indique le nom du service, par exemple Zoom, Google Meet ou Teams, ou **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking à l’aéroport arrive dans votre messagerie, votre Machine l’ajoute à un voyage. Les réservations liées à un même trajet sont réunies dans un seul voyage, quel que soit le compte de messagerie concerné : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet retour. Les réservations sont regroupées si leurs dates se chevauchent ou si l’une commence là où l’autre se termine.

Le voyage s’affiche sous la forme d’une bande sur toute sa durée. Ouvrez-le pour voir chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre place.

Les billets de concert, de match, de festival ou de conférence créent un événement, un par événement, avec le lieu, le code de réservation, votre place et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à celui-ci. Un billet réservé depuis votre messagerie professionnelle est classé dans Travail, sinon dans Personnel. Les billets pour un événement qui a lieu pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et l’hôtel. Ces lignes sont affichées en grisé et portent la mention **Aucune réservation**. Si aucun hébergement n’est réservé pour un voyage, rien n’est indiqué au sujet des nuits.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **Depuis Example Tickets**, et permet d’ouvrir l’e-mail correspondant.
- Si l’e-mail a généré une tâche, par exemple pour payer les billets, **Ouvrir la tâche** permet de l’afficher.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée disparaît. Lorsque toutes les réservations sont annulées, le voyage ou l’événement disparaît également.
- Une réservation pour quelqu’un d’autre, par exemple le vol d’un collègue qui vous a transféré son e-mail, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour les autres, comme un e-mail transféré ou une confirmation provenant d’un petit site de réservation, votre [modèle](model.md) lit les e-mails en arrière-plan, quelques-uns à la fois, et attend si vous approchez de votre limite d’utilisation. Les e-mails de réservation datant de l’année couverte par l’[historique](history.md) conservé par votre Machine sont lus en arrière-plan une fois l’historique chargé.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé, avec les décisions et les actions à effectuer. **Transcription** contient les propos échangés, mot pour mot. Elle est repliée au départ et indique sa durée. **Afficher** permet de la développer.

Si elles ne se chargent pas, un nouvel essai est lancé automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Les notes et la transcription ont chacune leurs boutons **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** au format Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste à cet endroit. Pour une réunion que vous pouvez modifier, le bouton **Notes** sous son formulaire permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, les notes s’affichent dans Notes et la transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais ce que vous avez ajouté. Si les deux versions sont présentes, elles s’affichent toutes les deux.

Les notes peuvent aussi être ajoutées à l’événement de la réunion dans l’agenda, après le début de la réunion, ou envoyées par e-mail par Zoom ou Gemini. Après la réunion, The Machine en tire des tâches uniquement si les prochaines étapes sont claires. Si les mêmes notes arrivent par deux moyens différents, elles ne créent qu’une seule tâche, dont la réunion est la source : « Source : notes de » la réunion.

Une réunion avec une transcription mais sans notes propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à effectuer, dans la langue de la réunion.

La mention **Rédaction des notes…** s’affiche. La rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela prend quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « ajoute cette transcription à la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcription, et un résumé dans Notes. Les réunions qui en contiennent affichent **Notes** ou **Transcription** dans l’Agenda.

The Machine lit les deux pour trouver les suites à donner à la réunion. Elles sont classées dans Travail ou Personnel, comme la réunion, et ne sont transmises à votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails où que vous la trouviez : dans une chronologie, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre agenda Google depuis cette page. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un (sur téléphone, appuyez sur **+** dans la barre supérieure) : choisissez l’agenda, un titre et un horaire. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

**Lieu** suggère des endroits au fil de la saisie : d’abord ceux que vous avez déjà utilisés et vos organisations, puis des adresses tirées d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour la recherche. Choisissez une suggestion ou conservez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2 personnes**. Google envoie les invitations lorsque vous appuyez sur ce bouton, pas avant. Sans invités, personne n’est invité ni informé d’une modification.

Une tâche peut également proposer une modification, par exemple l’ajout d’une prise en charge. Les changements sont détaillés. Ils ne sont appliqués que si vous choisissez **Ajouter**, **Enregistrer** ou **Supprimer**.

Vous n’avez pas encore de réunions ? Si aucun agenda n’est connecté, **Connecter votre agenda** ouvre les Connexions. Connectez [Google Agenda](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou l’inverse, The Machine crée une tâche à propos de l’événement le plus récent. Elle peut rédiger un court message pour le déplacer, ou proposer de le décliner. Rien n’est envoyé sans votre approbation.

Les événements d’une journée entière, indiqués comme disponibles ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Une tâche Travail indique seulement qu’il y a un conflit, pour que votre équipe ne voie jamais l’événement personnel. Vous seul voyez avec quel événement il entre en conflit.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Elle contient un bref résumé :

- **Qui :** qui sont ces personnes, d’après votre Graph, avec des éléments de leur parcours si ces informations sont connues.
- **Organisation :** l’activité de leur entreprise, ses clients et ses prix, si c’est utile pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les offres faites, ainsi que l’état d’avancement. Après la réunion, ces messages sont les sources de la tâche.
- **Décidé auparavant :**, **Changements depuis :** et **Encore à faire :** les résultats des réunions précédentes avec les mêmes personnes, chaque élément étant associé à la réunion ou au message dont il provient.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire, d’après les promesses enregistrées sur votre Machine.
- **Questions en suspens :** les questions qui attendent encore une réponse.
- **À décider ou à apporter :** les points à trancher ou les éléments à apporter, et ce qui pourrait les intéresser.

La tâche est créée le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle sert uniquement à consulter des informations. Une fois que vous l’avez lue, marquez-la **Fait**. Toute promesse ou question qui nécessite une action donne lieu à sa propre tâche.

Les réunions précédentes sont prises en compte si elles comptaient des participants extérieurs en commun, quel que soit leur intitulé ou l’adresse utilisée. The Machine lit les notes qu’elle trouve sur votre Machine : les vôtres, celles de votre application de réunion ou celles qui vous ont été envoyées par e-mail. À défaut, elle lit la transcription ou les notes de l’événement dans l’agenda. Les notes les plus récentes ont plus de poids, et un point réglé depuis n’est pas présenté comme étant toujours en suspens.

Les notes et les messages de l’[Historique](history.md) sont également pris en compte. Le résumé peut donc tenir compte des réunions qui ont eu lieu avant que vous commenciez à utiliser The Machine.

Un résumé professionnel ne contient aucune note personnelle ni aucun contenu provenant de la Machine de quelqu’un d’autre. Il reste privé : un transfert ne l’emporte pas et il ne peut pas être envoyé pour vérification. S’il n’y a pas de notes, les sections correspondantes n’apparaissent pas.

The Machine utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne d’une entreprise, elle consulte aussi la page d’accueil du site de l’entreprise.

Si un fournisseur de recherche Web est configuré dans OpenClaw (les Machines hébergées n’en ont pas), The Machine effectue aussi une brève recherche sur le nom de la personne et son entreprise. Les résultats sont accompagnés d’un lien. Seuls le nom public de la personne, le nom de l’entreprise et son site Web sont envoyés au moteur de recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours.

Une première réunion que vous avez acceptée peut donc donner lieu à un résumé avant même que vous ayez échangé un mot : l’activité de l’entreprise, ce que cela signifie pour vous et, si l’information est connue, l’identité de la personne. Si vous ne connaissez que son prénom, les résultats de la recherche ne sont conservés que s’ils désignent une seule personne. Si l’option **Rechercher les contacts pro** est désactivée (dans Paramètres, Sécurité), aucune recherche n’est effectuée.

Une réunion récurrente ne génère un résumé que s’il y a eu du nouveau depuis la dernière occurrence : un message, des notes ou une promesse. Le résumé indique les nouveautés, pas le contenu du résumé précédent. Il est créé une fois la réunion précédente terminée, avec un maximum de deux réunions récurrentes par jour.

S’il n’y a rien d’utile à dire, aucune tâche n’est créée. Les réunions internes, personnelles ou refusées ne donnent pas lieu à une tâche. Si une réunion est déplacée, sa tâche est conservée et indique le nouvel horaire. Une tâche écartée ne réapparaît pas, et la tâche d’une réunion annulée se ferme automatiquement.

Si une mise à jour modifie le contenu d’un résumé, les résumés des réunions à venir sont rédigés une nouvelle fois, dans leur nouvelle version. Leur titre, leurs sources et leur place dans votre liste ne changent pas. Un résumé que vous avez modifié, mis en attente ou fermé reste inchangé, tout comme celui d’une réunion qui commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour ouvrir son chat.
