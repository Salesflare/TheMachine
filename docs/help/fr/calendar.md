---
title: Calendrier
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: ae462ef9e7316cb6
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches à échéance ce jour-là et les tâches en attente le jour où elles reviennent,
- les points de suivi sur le travail que vous avez confié,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) repérés dans les e-mails de réservation et de billets.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ces événements ne donnent jamais lieu à une tâche. Les événements sur toute la journée et ceux qui durent plusieurs jours s’affichent comme des événements sur toute la journée, pour chacun des jours concernés. Dans **Agenda**, un voyage apparaît en premier chaque jour. Dans les vues **Semaine** et **Mois**, une seule barre s’étend sur les jours concernés, comme « Voyage à Lisbonne ».

Un projet commun donne lieu à une seule promesse, marquée « Avec » et suivie du nom de l’autre personne. Une promesse liée à une réunion qui a lieu ce jour-là avec cette même personne apparaît sur la ligne de la réunion.

**En retard** apparaît en premier. Une réunion associée à une tâche en cours affiche son statut : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous avez déjà répondu ou que son exécution l’a marquée comme terminée, ne s’affiche pas comme **Échéance**.

## Vue Agenda, Semaine ou Mois

- **Agenda** affiche chaque journée. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. La vue remonte jusqu’à une semaine avant la connexion de votre agenda. Une ligne en haut indique à partir de quel jour. Une fois son [historique](history.md) chargé, elle remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de passer d’une semaine ou d’un mois à l’autre. La vue choisie est mémorisée sur cet appareil.

Dans la grille hebdomadaire, les événements qui ont lieu à la même heure s’affichent côte à côte tout en restant lisibles. Les autres apparaissent sous la forme **+N**. Sélectionnez-les pour ouvrir cette journée dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : date et heure, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, renvoient vers leur page. **Ouvrir dans Google Calendar** (ou **Ouvrir dans Outlook**) ouvre la réunion dans l’application correspondante. La consultation n’apporte aucune modification.

Une salle de réunion réservée pour une réunion apparaît sous le lieu, jamais comme une personne ni dans votre Graph.

Un lien de réunion s’affiche sous le nom de son service, comme Zoom, Google Meet ou Teams, ou sous **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Lorsqu’une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking d’aéroport arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même déplacement sont regroupées dans un seul voyage, quelle que soit la boîte mail concernée : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet du retour. Les réservations sont regroupées lorsque leurs dates se chevauchent ou que l’une commence là où l’autre se termine.

Le voyage s’affiche sous la forme d’une seule barre sur les jours concernés. Ouvrez-le pour voir chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre siège.

Les billets de concert, de match, de festival ou de conférence créent un événement distinct, avec son lieu, son code de réservation, votre siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est marqué comme professionnel, sinon comme personnel. Les billets pour un événement qui a lieu pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique les éléments manquants, par exemple **Aucun hébergement réservé pour 2 nuits** ou l’absence de réservation entre l’aéroport et votre hôtel. Ces lignes sont grisées et marquées **Aucune réservation**. Si le voyage ne comprend aucun hébergement, aucune information sur les nuits ne s’affiche.

- Chaque ligne indique la provenance de la réservation, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche a été créée à partir de l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** permet de l’afficher.
- Une réservation modifiée met à jour sa ligne. Une réservation annulée est supprimée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.
- Une réservation pour une autre personne, comme le billet d’avion d’un collègue qui vous a été transféré, n’est pas ajoutée à vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour les autres, comme un e-mail transféré ou une réservation provenant d’un petit site, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques réservations à la fois, et attend si vous approchez de votre limite d’utilisation. Les e-mails de réservation de l’année conservée dans l’[historique](history.md) de votre Machine sont lus en arrière-plan une fois l’historique chargé.

## Notes de réunion et transcription

Les détails d’une réunion se composent de deux parties. **Notes** est le résumé : décisions et actions à effectuer. **Transcription** reprend mot pour mot ce qui a été dit. Elle est repliée par défaut et indique sa durée. **Afficher** permet de l’ouvrir.

Si le contenu ne se charge pas, l’application réessaie automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque partie dispose de ses propres commandes **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** au format Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, **Notes**, sous son formulaire, permet de les ouvrir.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes apparaissent dans Notes et sa transcription dans Transcript, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais le contenu que vous avez ajouté : si les deux sont présents, les deux s’affichent.

Des notes peuvent également être ajoutées à l’événement de réunion dans l’agenda après le début de la réunion, ou envoyées par e-mail par Zoom ou Gemini. Après la réunion, The Machine n’en crée des tâches que pour les prochaines étapes clairement définies. Si les mêmes notes sont reçues de deux façons, une seule tâche est créée, avec la réunion comme source : « Source : notes de la réunion ».

Une réunion avec une transcription et sans notes propose **Générer les notes**. The Machine rédige les notes à partir de la transcription : un bref résumé, les décisions et les actions à effectuer avec les personnes responsables, dans la langue de la réunion.

Le statut **Rédaction des notes…** s’affiche et la rédaction continue quand vous fermez la réunion. Pour une longue réunion, cela peut prendre quelques minutes et utilise votre propre modèle. Les notes indiquent **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple « ajoute cette transcription à la réunion de l’équipe d’aujourd’hui ». Une transcription est ajoutée à Transcript et un résumé à Notes. Dans Calendar, une réunion qui en contient affiche **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les actions de suivi de la réunion. Elles sont marquées comme professionnelles ou personnelles selon la réunion et ne sont transmises à votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails où que vous la trouviez : dans une chronologie, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas de page, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** en ajoute un (sur téléphone, sélectionnez **+** dans la barre supérieure) : choisissez l’agenda, un titre et l’horaire. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (cliquez deux fois).

**Où** suggère des lieux à mesure que vous saisissez du texte : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses fournies par [OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour rechercher des lieux. Sélectionnez un résultat ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou toute adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations quand vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un lieu de prise en charge. Les changements sont détaillés et ne sont appliqués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Aucune réunion pour l’instant ? Si aucun agenda n’est connecté, **Connecter votre agenda** ouvre Connexions. Vous pouvez connecter [Google Calendar](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche concernant le plus récent des deux. Elle peut rédiger un court message pour proposer de déplacer l’événement ou vous proposer de le refuser. Rien n’est envoyé avant votre approbation.

Les événements sur toute la journée, marqués comme libres ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Une tâche professionnelle indique uniquement qu’il y a un conflit : votre équipe ne voit donc jamais l’événement personnel. Vous seul voyez avec quel événement il entre en conflit.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une seule tâche : **Préparer la réunion**. Il s’agit d’un bref résumé :

- **Qui :** leur identité d’après votre Graph, avec des informations sur leur parcours lorsqu’elles sont disponibles.
- **Organisation :** les activités de leur entreprise qui comptent pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les propositions faites, ainsi que leur état d’avancement. Après la réunion, ces messages sont les sources de la tâche.
- **Promesses en cours :** ce que vous ou ces personnes devez encore faire.
- **Questions en suspens :** ce qui n’a pas encore de réponse.
- **À décider ou à apporter :** les points à trancher ou les éléments à apporter, ainsi que les sujets qui les intéresseront probablement.

La tâche est créée le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle sert uniquement à consulter les informations. Touchez **Fait** après l’avoir lue. Les promesses ou questions qui nécessitent une action ont leur propre tâche.

La tâche utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne d’une entreprise, elle effectue aussi une recherche rapide sur le Web à partir de son nom et de celui de son entreprise, puis affiche un lien à côté des résultats. Seuls son nom public, le nom de l’entreprise et son site Web sont envoyés à la recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours. Si l’option **Rechercher les contacts pro** est désactivée dans Paramètres, sous Sécurité, aucune recherche n’est effectuée.

S’il n’y a pas d’historique utile, aucune tâche n’est créée. Les réunions récurrentes, internes, personnelles ou refusées n’en génèrent pas. Si une réunion est déplacée, sa tâche est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas et celle d’une réunion annulée se ferme automatiquement.

Les détails de la réunion affichent sa tâche sous **Tâche**, accessible en une seule touche depuis le chat correspondant.
