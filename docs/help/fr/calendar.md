---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: f3f41306aad03084
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches à échéance ce jour-là et les tâches en attente le jour où elles réapparaissent,
- les suivis sur le travail que vous avez transféré,
- les promesses datées,
- les [voyages et événements](calendar.md#trips-and-events) tirés des e-mails de réservation et de billetterie.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda qu’on a partagé avec vous affiche les événements de son propriétaire en grisé, avec son prénom. Ces événements ne créent jamais de tâche. Les événements sur toute la journée ou sur plusieurs jours s’affichent comme des événements sur toute la journée, pour chacun des jours concernés. Dans Agenda, un voyage apparaît en premier pour chacun de ses jours. Dans les vues Semaine et Mois, il apparaît sous forme d’une seule bande sur ces jours, par exemple « Voyage à Lisbonne ».

Un projet élaboré à deux correspond à une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse concernant une réunion prévue ce jour-là avec cette même personne apparaît sur la ligne de la réunion.

**En retard** apparaît en premier. Une réunion associée à une tâche ouverte affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut, ou sélectionnez **Afficher les jours précédents**, pour voir les jours précédents. L’affichage remonte jusqu’à une semaine avant la connexion de votre agenda, et une ligne en haut indique à partir de quel jour. Une fois votre [historique](history.md) chargé, il remonte jusqu’à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez-en un pour afficher la liste du jour.

**Aujourd’hui**, ‹ et › en haut permettent de parcourir les semaines ou les mois. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte et restent lisibles. Les autres apparaissent sous la forme **+N**. Sélectionnez cette indication pour ouvrir le jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de sa tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle de quelqu’un d’autre ou une réunion avec des invités, les détails s’affichent : quand, où et avec qui. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, sont des liens vers leurs pages. **Ouvrir dans Google Agenda** ou **Ouvrir dans Outlook** ouvre la réunion dans le service correspondant. La consultation n’apporte aucune modification.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ni dans votre Graph.

Un lien de réunion s’affiche avec le nom de son service, comme Zoom, Google Meet ou Teams, ou sous la forme **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand un e-mail de réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking d’aéroport arrive, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un seul voyage, quelle que soit la boîte mail concernée : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet retour. Les réservations sont regroupées si leurs dates se chevauchent ou si l’une commence là où l’autre se termine.

Le voyage s’affiche sous forme d’une seule bande sur les jours concernés. Ouvrez-le pour voir chaque réservation par ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre place.

Les billets de concert, de match, de festival ou de conférence créent un événement par manifestation, avec son lieu, le code de réservation, la place et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est marqué Travail, sinon il est marqué Personnel. Les billets pour un événement qui a lieu pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et l’hôtel. Ces lignes sont grisées et portent la mention **Aucune réservation**. Si le voyage ne comprend aucun hébergement, rien ne s’affiche à propos des nuits.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **Depuis Example Tickets**, et ouvre l’e-mail correspondant.
- Si l’e-mail a créé une tâche, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Si toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.
- Une réservation pour quelqu’un d’autre, par exemple le vol d’un collègue que l’on vous a transféré, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour celles qui n’en contiennent pas, comme un e-mail transféré ou une réservation sur un petit site, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques messages à la fois, et attend lorsque vous approchez de votre limite d’utilisation. Les e-mails de réservation de l’année conservée dans l’[historique](history.md) de votre Machine sont également lus en arrière-plan, une fois l’historique chargé.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à suivre. **Transcription** reprend les paroles mot pour mot. Elle est d’abord repliée, avec sa durée. **Afficher** permet de l’ouvrir.

Si les éléments ne se chargent pas, une nouvelle tentative est lancée automatiquement pendant environ une demi-minute. Après cela, touchez **Réessayer**.

Les notes et la transcription ont chacune leurs propres commandes **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** au format Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, **Notes** sous son formulaire permet de les ouvrir.

Lorsque [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais ce que vous avez ajouté : si les deux sont présentes, les deux s’affichent.

Les notes peuvent aussi être ajoutées à l’événement de la réunion dans l’agenda, une fois celle-ci commencée, ou envoyées par e-mail par Zoom ou Gemini. Une fois la réunion terminée, The Machine en crée des tâches uniquement pour les prochaines étapes clairement établies. Si les mêmes notes arrivent par deux moyens, elles ne créent qu’une seule tâche, dont la source est la réunion : « Source : notes de » la réunion.

Une réunion avec transcription, mais sans notes, affiche **Générer les notes**. The Machine les rédige à partir de la transcription : un résumé court, les décisions et les actions à suivre, avec les personnes chargées de les réaliser, dans la langue de la réunion.

La mention **Rédaction des notes…** s’affiche. La rédaction continue même si vous fermez la réunion. Une longue transcription peut prendre quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans une tâche, par exemple : « ajoute cette transcription au point d’équipe d’aujourd’hui ». Une transcription est ajoutée dans Transcription, un résumé dans Notes. Dans l’agenda, une réunion qui en contient affiche **Notes** ou **Transcription**.

The Machine lit les deux pour préparer le suivi de la réunion. Les tâches sont marquées Travail ou Personnel comme la réunion et ne sont envoyées à votre équipe que si la réunion l’est aussi.

Les détails d’une réunion sont accessibles partout où vous la trouvez : sur une chronologie, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un (sur téléphone, cette option se trouve sous **+** dans la barre supérieure) : choisissez l’agenda, un titre et un horaire. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

**Lieu** suggère des endroits au fil de votre saisie : ceux que vous avez déjà utilisés et vos organisations d’abord, puis des adresses d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour effectuer la recherche. Choisissez un lieu ou gardez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option n’est disponible que dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un lieu de prise en charge. Les changements sont indiqués en détail. Ils ne sont appliqués que si vous sélectionnez **Ajouter**, **Enregistrer** ou **Supprimer**.

Vous n’avez pas encore de réunions ? Si vous n’avez pas d’agenda, **Connecter votre agenda** ouvre Connexions : connectez [Google Agenda](google-calendar.md), [Outlook Agenda](microsoft.md) ou [un autre agenda](other-calendars.md).

## Chevauchements avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou l’inverse, The Machine crée une tâche à propos de l’événement le plus récent. Elle peut rédiger un court message pour le déplacer ou proposer de le décliner. Rien n’est envoyé tant que vous ne l’avez pas approuvé.

Les événements sur toute la journée, indiqués comme libres ou provisoires ne sont jamais pris en compte, et chaque chevauchement n’est signalé qu’une fois. Une tâche Travail indique simplement qu’il y a un conflit. Votre équipe ne voit donc jamais l’événement personnel. Vous seule voyez avec quel événement il entre en conflit.

## Préparer vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref compte rendu préparatoire :

- **Qui :** leur identité, d’après votre Graph, avec des éléments de leur parcours quand ces informations sont connues.
- **Organisation :** l’activité de leur entreprise, ses clients et ses tarifs, si ces informations sont utiles pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les offres faites, ainsi que l’état d’avancement. Après la réunion, ces messages apparaissent comme sources de la tâche.
- **Déjà convenu :**, **Modifié depuis :** et **Encore à faire :** les éléments issus des réunions précédentes avec les mêmes personnes. Chaque ligne indique la réunion ou le message dont elle provient.
- **Promesses en attente :** ce que vous ou ces personnes devez encore faire, d’après les promesses enregistrées sur votre Machine.
- **Questions en suspens :** les questions qui restent sans réponse.
- **À décider ou à apporter :** les points à régler ou les éléments à apporter, ainsi que ce qui les intéressera probablement.

La tâche arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle est uniquement destinée à être consultée. Sélectionnez **Fait** une fois que vous l’avez lue. Toute promesse ou question qui nécessite une action fait l’objet de sa propre tâche.

Les réunions précédentes sont prises en compte si elles réunissaient une personne extérieure et l’un des mêmes participants, quel que soit leur intitulé ou l’adresse utilisée. The Machine lit les notes disponibles sur votre Machine : les vôtres, celles de votre application de réunion ou celles reçues par e-mail. À défaut, elle lit la transcription ou les notes de l’événement dans l’agenda. Les notes les plus récentes comptent davantage, et un point réglé depuis n’est pas présenté comme étant toujours en suspens.

Les notes et les messages de l’[Historique](history.md) sont également pris en compte. Le compte rendu préparatoire peut ainsi intégrer les réunions antérieures à votre arrivée.

Un compte rendu préparatoire professionnel ne consulte aucune note personnelle ni aucun contenu provenant de la Machine d’une autre personne. Il reste privé : un transfert ne l’emporte jamais et il ne peut pas être envoyé pour examen. Sans notes, ces lignes n’apparaissent pas.

The Machine s’appuie sur les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne travaillant dans une entreprise, elle consulte également la page d’accueil du site de cette entreprise.

Si la recherche sur le Web est configurée sur votre Machine, elle effectue aussi une brève recherche sur le nom de la personne et son entreprise. Une Machine hébergée n’inclut pas cette fonctionnalité. Sur votre propre ordinateur, vous pouvez la configurer dans OpenClaw. Les résultats sont accompagnés d’un lien. Seuls le nom public de la personne, le nom de l’entreprise et son site Web sont transmis à la recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours.

Ainsi, une première réunion que vous avez acceptée peut avoir son compte rendu préparatoire avant même que vous ayez échangé un mot : l’activité de l’entreprise, ce que cela signifie pour vous et, si l’information est connue, l’identité de la personne. Si vous ne connaissez que son prénom, les résultats de recherche ne sont conservés que s’ils désignent une seule personne. Lorsque **Rechercher les contacts pro** est désactivé dans Paramètres, Sécurité, aucune recherche n’est effectuée.

Une réunion récurrente ne donne lieu à un nouveau compte rendu que s’il s’est passé quelque chose depuis la dernière fois : un message, des notes ou une promesse. Il indique les nouveautés, pas le contenu du compte rendu précédent. Il arrive une fois la réunion précédente terminée, avec un maximum de deux réunions récurrentes par jour.

S’il n’y a rien d’utile à signaler, aucune tâche n’est créée. Les réunions internes, personnelles ou déclinées n’en génèrent pas. Si une réunion est déplacée, sa tâche est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Lorsqu’une mise à jour modifie le contenu d’un compte rendu préparatoire, les comptes rendus des réunions à venir sont rédigés une nouvelle fois, sous leur nouvelle forme. Leur titre, leurs sources et leur place dans votre liste ne changent pas. Un compte rendu que vous avez modifié, mis en attente ou fermé reste tel quel, tout comme celui d’une réunion qui commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour ouvrir son chat.
