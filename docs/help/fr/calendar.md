---
title: Agenda
area: calendar
summary: La semaine à venir en un seul endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 479aa9c3fadda8bd
---
## Ce qui s’affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches dont l’échéance tombe ce jour-là et les tâches en attente, le jour où elles réapparaissent,
- les suivis du travail que vous avez transféré,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) tirés des réservations et billets reçus par e-mail.

Une réunion qui figure dans deux agendas ne s’affiche qu’une fois. Un agenda qu’on a partagé avec vous affiche les événements de son propriétaire en estompé, avec son prénom. Ces événements ne donnent jamais lieu à une tâche. Les événements sur une journée entière ou sur plusieurs jours s’affichent comme des événements sur toute la journée, chacun des jours concernés. Dans Agenda, un voyage apparaît en premier chaque jour. Dans les vues Semaine et Mois, il forme une seule bande sur les jours concernés, par exemple « Voyage à Lisbonne ».

Un projet élaboré à plusieurs correspond à une seule promesse, indiquée par « Avec » et le nom de l’autre personne. Une promesse liée à une réunion prévue ce jour-là avec cette même personne apparaît sur la ligne de la réunion.

**En retard** s’affiche en premier. Une réunion associée à une tâche ouverte l’indique : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée, parce que vous y avez déjà répondu ou que son exécution l’a trouvée terminée, ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque jour. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut pour les jours précédents, ou sélectionnez **Afficher les jours précédents**. L’affichage remonte à la semaine précédant la connexion de votre agenda, et une ligne en haut indique le premier jour affiché. Une fois son [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et › en haut de l’écran permettent de passer d’une semaine ou d’un mois à l’autre. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte et restent lisibles. Les autres sont regroupés sous **+N**. Sélectionnez ce nombre pour ouvrir le jour dans l’agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de sa tâche, la promesse, le voyage ou l’événement, ou la réunion. Si vous ne pouvez pas modifier une réunion ici, par exemple si elle appartient à quelqu’un d’autre ou si elle a des invités, ses détails s’affichent : quand et où elle a lieu, et qui y participe. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, renvoient vers leur page. **Ouvrir dans Google Agenda** ou **Ouvrir dans Outlook** permet de l’ouvrir dans l’application correspondante. La consultation n’apporte aucune modification.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ou dans votre Graph.

Le lien d’une réunion s’affiche sous le nom de son service, comme Zoom, Google Meet ou Teams, ou sous **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Quand un e-mail contient une réservation de vol, d’hôtel, de maison de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de parking à l’aéroport, votre Machine l’ajoute à un voyage. Les réservations liées à un même trajet sont regroupées dans un seul voyage, quel que soit le compte de messagerie concerné : le train jusqu’à l’aéroport, les vols, la voiture, le séjour et le trajet retour. Les réservations sont regroupées lorsque leurs dates se chevauchent ou que l’une commence à la fin de l’autre.

Le voyage s’affiche sous forme d’une seule bande sur les jours concernés. Ouvrez-le pour voir chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et votre siège.

Les billets de concert, de match, de festival ou de conférence créent un événement, un par événement, avec son lieu, son code de réservation, votre siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre compte professionnel est marqué comme professionnel, sinon il est personnel. Les billets pour un événement pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et l’hôtel. Ces lignes sont estompées et portent la mention **Aucune réservation**. Si aucun hébergement n’est réservé pour le voyage, rien ne s’affiche concernant les nuits.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **Depuis Exemple Billets**, et ouvre l’e-mail correspondant.
- Si une tâche découle de l’e-mail, par exemple payer les billets, **Ouvrir la tâche** l’affiche.
- Une réservation modifiée met à jour sa ligne. Une réservation annulée est supprimée. Quand toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.
- Une réservation pour quelqu’un d’autre, comme le vol d’un collègue qui vous a été transféré, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails sous une forme que votre Machine peut lire sans IA. Pour celles qui ne le sont pas, comme un e-mail transféré ou une réservation provenant d’un petit site, votre [modèle](model.md) lit l’e-mail en arrière-plan, quelques-uns à la fois, et attend si vous approchez de votre limite d’utilisation. Une fois l’historique chargé, les e-mails de réservation de l’année conservée dans votre [historique](history.md) sont également lus en arrière-plan.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux parties. **Notes** est le résumé : décisions et actions à entreprendre. **Transcription** reprend mot pour mot ce qui a été dit. Elle est repliée au départ, avec sa durée. **Afficher** permet de l’ouvrir.

Si les éléments ne se chargent pas, une nouvelle tentative est lancée automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque partie a ses propres options **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer**. Touchez deux fois pour retirer un élément. Le contenu ajouté à l’une reste dans celle-ci. Pour une réunion que vous pouvez modifier, l’option **Notes** sous le formulaire permet d’ouvrir les notes.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, ses notes s’affichent dans Notes et sa transcription dans Transcription, avec la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais ce que vous avez ajouté. Si les deux versions sont disponibles, elles s’affichent toutes les deux.

Les notes peuvent aussi être ajoutées à l’événement de la réunion dans l’agenda, après le début de celle-ci, ou reçues par e-mail depuis Zoom ou Gemini. Une fois la réunion terminée, The Machine en tire des tâches uniquement si elles correspondent clairement à des étapes à suivre. Si les mêmes notes arrivent par deux moyens, elles ne créent qu’une seule tâche, dont la réunion est la source : « Source : notes de la réunion ».

Une réunion avec une transcription, mais sans notes, propose **Générer les notes**. The Machine les rédige à partir de la transcription : un bref résumé, les décisions et les actions à entreprendre, dans la langue de la réunion.

Le statut **Rédaction des notes…** s’affiche. La rédaction continue même si vous fermez la réunion. Pour une longue réunion, cela prend quelques minutes et utilise votre propre modèle. Les notes portent la mention **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut aussi les ajouter. Demandez-le dans un chat de tâche, par exemple : « Ajoute cette transcription au compte rendu de la réunion d’équipe d’aujourd’hui ». Une transcription est ajoutée à Transcription, un résumé à Notes. Dans l’agenda, une réunion qui en contient affiche **Notes** ou **Transcription**.

The Machine lit les deux pour retrouver les actions à suivre après la réunion. Elles sont professionnelles ou personnelles, comme la réunion, et ne sont transmises à votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails, quel que soit l’endroit où vous la trouvez : sur une chronologie, dans une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle que vous l’avez reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont en lecture seule. **Nouvel événement** permet d’en ajouter un. Sur téléphone, l’option se trouve sous **+** dans la barre supérieure. Choisissez l’agenda, un titre et un horaire. Cliquez sur un événement sans invités dans cet agenda pour le modifier ou le **Supprimer**. Touchez deux fois pour le supprimer.

**Lieu** suggère des endroits à mesure que vous saisissez du texte : d’abord ceux que vous avez déjà utilisés et vos organisations, puis des adresses provenant d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots saisis sont envoyés pour la recherche. Choisissez une suggestion ou conservez votre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes qui recevront une invitation sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2 personnes**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’un lieu de prise en charge. Les changements sont indiqués précisément. Seule l’action **Ajouter**, **Enregistrer** ou **Supprimer** les applique.

Aucune réunion pour le moment ? Si aucun agenda n’est connecté, **Connecter votre agenda** ouvre les Connexions. Vous pouvez alors connecter [Google Agenda](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche au sujet de l’événement le plus récent. Elle peut rédiger un bref message pour le déplacer ou proposer de le décliner. Rien n’est envoyé avant votre approbation.

Un événement qui chevauche plusieurs autres événements ne crée qu’une seule tâche à son sujet. Un nouveau chevauchement est ajouté à cette tâche tant qu’elle est ouverte. Une fois la tâche terminée ou écartée, seul un événement créé ou modifié par la suite la fait réapparaître.

Les événements sur toute la journée, marqués comme disponibles ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Les lieux de travail, les plages de concentration et les périodes d’absence de Google ne sont pas pris en compte non plus. Il en va de même pour un bloc que vous avez créé et qui contient d’autres réunions, comme une journée au bureau : seules les réunions qu’il contient peuvent créer un conflit. Un bloc auquel personne d’autre ne participe et qui ne contient aucune réunion, comme un vol, crée tout de même un conflit avec un événement auquel d’autres personnes participent.

Une tâche professionnelle indique seulement qu’il y a un conflit, afin que votre équipe ne voie jamais l’événement personnel. Vous seul voyez ce qui entre en conflit : les deux premiers événements, puis le nombre d’autres événements concernés. Une tâche sur laquelle vous n’avez rien fait se ferme automatiquement si le conflit concerne une autre tâche ou s’il n’y avait finalement pas de conflit.

## Préparation de vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Il s’agit d’un bref compte rendu préparatoire :

- **Qui :** leur identité, d’après votre Graph, avec des informations sur leur parcours si elles sont connues.
- **Organisation :** l’activité de leur entreprise, ses clients et ses tarifs, si ces informations sont utiles pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les propositions faites, ainsi que leur état d’avancement. Après la réunion, ces messages deviennent les sources de la tâche.
- **Déjà convenu :**, **Modifications depuis :** et **Encore à faire :** les résultats des réunions précédentes avec les mêmes personnes. Chaque ligne indique la réunion ou le message dont elle provient.
- **Promesses en attente :** ce que vous ou ces personnes devez encore faire, d’après les promesses enregistrées sur votre Machine.
- **Questions ouvertes :** les questions qui n’ont pas encore de réponse.
- **À décider ou à apporter :** les points à régler ou les éléments à apporter, ainsi que les sujets qui les intéresseront probablement.

Le compte rendu préparatoire arrive le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Il suffit de le lire : la tâche passe à **Fait** une fois que vous l’avez lu. Une promesse ou une question qui nécessite une action a sa propre tâche.

Posez vos questions sur la réunion dans son chat ou ajoutez des informations : The Machine vous répond ou les intègre au compte rendu préparatoire, par exemple dans **À décider ou à apporter**, et en tient compte par la suite. Rien n’est envoyé depuis un compte rendu préparatoire.

Les réunions précédentes sont prises en compte dès qu’une personne extérieure participe aux deux réunions, quels que soient le titre de la réunion et l’adresse utilisée par cette personne. The Machine lit les notes disponibles sur votre Machine : les vôtres, celles de votre application de réunion ou celles qu’elle vous a envoyées par e-mail. À défaut, elle lit la transcription ou les notes de l’événement dans l’agenda. Les notes les plus récentes ont le plus de poids, et un point réglé depuis n’est plus indiqué comme ouvert.

Les notes et les messages de l’[Historique](history.md) sont aussi pris en compte. Le compte rendu préparatoire peut ainsi tenir compte des réunions qui ont eu lieu avant que vous commenciez à utiliser The Machine.

Un compte rendu préparatoire professionnel ne lit aucune note personnelle ni aucun contenu provenant de la Machine de quelqu’un d’autre. Son texte reste privé : il n’est jamais transmis avec un transfert et ne peut pas être envoyé pour révision. Si aucune note n’est disponible, ces lignes n’apparaissent pas.

The Machine utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne travaillant dans une entreprise, elle consulte aussi la page d’accueil du site de cette entreprise.

Si la recherche Web est configurée sur votre Machine, The Machine effectue aussi une brève recherche Web sur le nom de la personne et celui de son entreprise. Une Machine hébergée n’inclut pas cette fonction. Sur votre propre ordinateur, vous pouvez la configurer dans OpenClaw. Les résultats de la recherche sont accompagnés d’un lien. Seuls le nom public de la personne, le nom de l’entreprise et son site Web sont transmis au moteur de recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours.

Ainsi, le compte rendu préparatoire d’une première réunion que vous avez acceptée peut être prêt avant même que vous ayez échangé un mot : il indique l’activité de l’entreprise, ce que cela signifie pour vous et, si l’information est connue, l’identité de la personne. Si vous ne connaissez que son prénom, The Machine ne conserve les résultats de recherche que s’ils correspondent à une seule personne. Si **Rechercher les contacts pro** est désactivé dans Paramètres, Sécurité, aucune recherche n’est effectuée.

Une réunion récurrente donne lieu à un compte rendu préparatoire uniquement si quelque chose a changé depuis la dernière fois : un message, des notes ou une promesse. Il indique les nouveautés, pas le contenu du compte rendu précédent. Il est créé une fois la réunion précédente terminée, pour deux réunions récurrentes par jour au maximum.

S’il n’y a rien d’utile à indiquer, aucune tâche n’est créée. Les réunions internes, personnelles ou refusées ne donnent lieu à aucune tâche. Si une réunion est déplacée, sa tâche est conservée et son horaire est mis à jour. Une tâche écartée ne réapparaît pas. La tâche d’une réunion annulée se ferme automatiquement.

Si une mise à jour modifie le contenu d’un compte rendu préparatoire, les comptes rendus des réunions à venir qui sont encore ouverts sont réécrits une fois pour intégrer les nouvelles informations. Leur titre, leurs sources et leur place dans votre liste restent inchangés. Un compte rendu que vous avez modifié, mis en attente ou fermé reste tel quel, tout comme celui d’une réunion qui commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour ouvrir son chat.
