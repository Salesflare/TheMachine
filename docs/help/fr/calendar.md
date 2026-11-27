---
title: Agenda
area: calendar
summary: La semaine à venir au même endroit : réunions, tâches à échéance, tâches en attente et promesses.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py, trip_notes.py, event_notes.py, bookings.py
order: 1
translated: 4b5bc600fefb624c
---
## Ce que l’agenda affiche

Vos journées à partir d’aujourd’hui, avec :

- les réunions des agendas que vous avez connectés,
- les tâches arrivées à échéance ce jour-là et les tâches en attente qui reviennent ce jour-là,
- les suivis du travail que vous avez transféré,
- les promesses avec une date,
- les [voyages et événements](calendar.md#trips-and-events) issus de vos e-mails de réservation et de billets.

Une réunion présente dans deux agendas ne s’affiche qu’une fois. Un agenda qu’une personne a partagé avec vous affiche ses événements en grisé, avec son prénom. Ces événements ne donnent jamais lieu à une tâche. Les événements sur toute la journée ou sur plusieurs jours s’affichent comme événements sur toute la journée, pour chaque jour concerné. Dans l’Agenda, un voyage apparaît en premier pour chacun de ses jours. Dans les vues Semaine et Mois, il s’affiche sur une bande couvrant tous ses jours, par exemple « Voyage à Lisbon ».

Un projet convenu ensemble devient une seule promesse, indiquée par « Avec » et son nom. Une promesse liée à une réunion qui a lieu ce jour-là avec la même personne s’affiche sur la ligne de cette réunion.

**En retard** s’affiche en premier. Une réunion liée à une tâche encore ouverte affiche son état : **Préparation prête**, **En préparation** ou **Tâche**. Une tâche qui semble terminée (vous avez déjà répondu ou son traitement l’a trouvée terminée) ne s’affiche pas comme **Échéance**.

## Agenda, semaine ou mois

- **Agenda** affiche chaque journée. Faites défiler vers le bas pour voir les jours suivants, ou vers le haut (ou sélectionnez **Afficher les jours précédents**) pour voir les jours précédents. L’affichage remonte jusqu’à une semaine avant la connexion de votre agenda. Une ligne en haut indique à partir de quel jour. Une fois votre [historique](history.md) chargé, il remonte à environ un an.
- **Semaine** affiche une grille du lundi au dimanche. Sur téléphone, trois jours s’affichent.
- **Mois** affiche le mois entier. Sur ordinateur, jusqu’à trois éléments s’affichent par jour. Sur téléphone, des points s’affichent. Touchez un jour pour afficher sa liste.

**Aujourd’hui**, ‹ et ›, en haut de l’écran, permettent de passer d’une semaine ou d’un mois à l’autre. La vue choisie est mémorisée sur cet appareil.

Dans la grille de la semaine, les événements qui ont lieu en même temps s’affichent côte à côte, tout en restant lisibles. Les autres sont regroupés sous **+N**. Sélectionnez cette indication pour ouvrir la journée dans l’Agenda.

## Ouvrir un élément

Cliquez sur une ligne pour ouvrir le chat de la tâche, la promesse, le voyage ou l’événement, ou la réunion. Pour une réunion que vous ne pouvez pas modifier ici, par exemple celle d’une autre personne ou une réunion avec des invités, les détails s’affichent : date, lieu et participants. Les personnes connues de votre Graph, ainsi que les organisations et les projets associés à la réunion, sont des liens vers leur page. **Ouvrir dans Google Agenda** (ou **Ouvrir dans Outlook**) ouvre la réunion dans le service correspondant. La consultation n’apporte aucune modification.

Une salle réservée pour une réunion s’affiche sous le lieu, jamais comme une personne ou dans votre Graph.

Le lien vers une réunion affiche le nom de son service, comme Zoom, Google Meet ou Teams, ou **Appel vidéo**. Ouvrez la réunion pour la rejoindre.

## Voyages et événements

Lorsqu’une réservation de vol, d’hôtel, de location de vacances, de train, de bus, de ferry, de voiture de location, de taxi ou de stationnement à l’aéroport arrive dans vos e-mails, votre Machine l’ajoute à un voyage. Les réservations d’un même trajet sont regroupées dans un seul voyage, quelle que soit la boîte mail concernée : le train jusqu’à l’aéroport, les vols, la voiture, l’hébergement et le trajet retour. Les réservations sont regroupées lorsque leurs dates se chevauchent ou que l’une commence là où l’autre se termine.

Le voyage s’affiche sur une bande couvrant les jours concernés. Ouvrez-le pour voir chaque réservation dans l’ordre chronologique, avec ses horaires, son adresse, son code de réservation et le numéro de siège.

Les billets de concert, de match, de festival ou de conférence créent un événement, un par événement, avec son lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée au même événement. Un événement réservé depuis votre boîte mail professionnelle est indiqué comme professionnel, sinon comme personnel. Les billets pour un événement pendant un voyage sont ajoutés au voyage.

Pour un voyage à venir, votre Machine indique ce qui manque, par exemple **Aucun hébergement réservé pour 2 nuits**, ou l’absence de réservation entre l’aéroport et l’hôtel. Ces lignes sont en grisé et portent la mention **Aucune réservation**. Un voyage sans aucun hébergement n’indique rien sur les nuits.

- Chaque ligne indique l’expéditeur de la réservation, par exemple **Depuis Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche est liée à l’e-mail, par exemple pour payer les billets, **Ouvrir la tâche** permet de l’afficher.
- Une réservation modifiée met à jour la ligne correspondante. Une réservation annulée est supprimée. Lorsque toutes les réservations sont annulées, le voyage ou l’événement est également supprimé.
- Une réservation pour quelqu’un d’autre, comme le vol d’un collègue qui vous a été transféré, n’apparaît pas dans vos voyages.

La plupart des confirmations contiennent leurs détails dans un format que votre Machine peut lire sans IA. Pour les autres, comme un e-mail transféré ou un petit site de réservation, votre [modèle](model.md) lit les e-mails en arrière-plan, quelques-uns à la fois, et attend lorsque vous approchez de votre limite d’utilisation. Une fois votre [historique](history.md) chargé, les e-mails de réservation de l’année qu’il couvre sont également lus en arrière-plan.

## Notes et transcription de réunion

Les détails d’une réunion comportent deux sections. **Notes** est le résumé : décisions et actions à effectuer. **Transcription** reprend mot pour mot les échanges. Elle est repliée au départ et indique sa durée. Sélectionnez **Afficher** pour l’ouvrir.

Si le contenu ne se charge pas, un nouvel essai est effectué automatiquement pendant environ une demi-minute. Ensuite, touchez **Réessayer**.

Chaque section comporte ses propres boutons **Ajouter des notes** ou **Ajouter une transcription**, **Importer un fichier** Markdown ou texte, **Modifier** et **Retirer** (touchez deux fois). Le contenu ajouté à l’une reste dans cette section. Pour une réunion modifiable, sélectionnez **Notes** sous le formulaire pour ouvrir les notes.

Si [Zoom](zoom.md), [Google Meet](google-meet.md) ou [Granola](granola.md) est connecté, les notes du service s’affichent dans Notes et sa transcription dans Transcription. Elles portent la mention **De Zoom**, **De Google Meet** ou **Depuis Granola**. Elles ne remplacent jamais le contenu que vous avez ajouté. Si les deux sont présents, les deux s’affichent.

Des notes peuvent aussi être ajoutées à l’événement de calendrier de la réunion, après son début, ou envoyées par e-mail par Zoom ou Gemini. Une fois la réunion terminée, The Machine crée des tâches à partir de ces notes uniquement si elles indiquent clairement les prochaines étapes. Si les mêmes notes arrivent par deux moyens, une seule tâche est créée, avec la réunion comme source : « Source : notes de la réunion ».

Pour une réunion avec une transcription mais sans notes, le bouton **Générer les notes** s’affiche. The Machine rédige les notes à partir de la transcription : un court résumé, les décisions et les actions à effectuer avec les personnes responsables, dans la langue de la réunion.

Le statut **Rédaction des notes…** s’affiche et la rédaction continue même si vous fermez la réunion. Pour une longue réunion, comptez quelques minutes. La rédaction utilise votre propre modèle. Les notes indiquent **Rédigé par The Machine** et ne remplacent jamais celles que vous avez ajoutées.

The Machine peut également ajouter des notes. Demandez-le dans un chat de tâche, par exemple : « Ajoute cette transcription à la réunion d’équipe d’aujourd’hui ». La transcription est ajoutée dans Transcription et le résumé dans Notes. Dans l’Agenda, une réunion qui en contient affiche **Notes** ou **Transcription**.

The Machine lit les deux pour trouver les suivis de la réunion. Ils sont professionnels ou personnels, comme la réunion, et ne sont transmis à votre équipe que si la réunion l’est aussi.

Une réunion s’ouvre avec ces détails, quel que soit l’endroit où vous la trouvez : dans une chronologie, dans les résultats d’une recherche de messages ou comme source d’une tâche. **Invitation d’origine**, en bas, affiche l’invitation telle qu’elle a été reçue.

## Ajouter ou modifier un événement

Vous pouvez modifier votre propre agenda Google ici. Outlook et les autres agendas sont consultables uniquement. **Nouvel événement** permet d’en ajouter un (sur téléphone, il se trouve sous **+** dans la barre supérieure) : choisissez l’agenda, un titre et une heure. Cliquez sur un événement sans invités de cet agenda pour le modifier ou le **Supprimer** (touchez deux fois).

**Lieu** suggère des endroits au fur et à mesure de votre saisie : d’abord ceux que vous avez déjà utilisés et ceux de vos organisations, puis des adresses d’[OpenStreetMap](https://www.openstreetmap.org), une carte gratuite. Seuls les mots que vous saisissez sont envoyés pour la recherche. Choisissez une suggestion ou conservez votre propre texte.

**Inviter** permet d’ajouter des personnes de votre Graph ou n’importe quelle adresse e-mail. Cette option est disponible uniquement dans votre propre agenda. Les personnes invitées sont indiquées au-dessus du bouton, qui précise leur nombre : **Ajouter et inviter 2**. Google envoie les invitations lorsque vous touchez le bouton, pas avant. Sans invités, personne ne reçoit d’invitation ni de mise à jour.

Une tâche peut aussi proposer une modification, par exemple l’ajout d’une prise en charge. Les changements sont indiqués précisément. Seuls les boutons **Ajouter**, **Enregistrer** ou **Supprimer** les appliquent.

Pas encore de réunion ? Si aucun agenda n’est connecté, **Connecter votre agenda** ouvre les Connexions. Connectez [Google Agenda](google-calendar.md), [Outlook Calendar](microsoft.md) ou [un autre agenda](other-calendars.md).

## Conflits avec votre autre agenda

Lorsqu’une réunion professionnelle chevauche un événement de votre agenda personnel, ou inversement, The Machine crée une tâche à propos de l’événement le plus récent. Elle peut rédiger un court message pour le déplacer ou proposer de le refuser. Rien n’est envoyé tant que vous ne l’avez pas approuvé.

Un événement qui en chevauche plusieurs ne donne lieu qu’à une seule tâche, à son sujet. Un nouveau chevauchement s’y ajoute tant qu’elle est ouverte. Une fois la tâche terminée ou écartée, seul un événement créé ou modifié par la suite peut la faire réapparaître.

Les événements sur toute la journée, indiqués comme disponibles ou provisoires ne sont jamais pris en compte, et chaque conflit n’est signalé qu’une fois. Les lieux de travail, périodes de concentration et absences du bureau de Google ne sont pas pris en compte non plus. Il en va de même pour un bloc que vous avez créé et qui contient d’autres réunions, comme une journée au bureau : seules les réunions qu’il contient peuvent entrer en conflit. Un bloc sans autres participants ni réunions, comme un vol, peut tout de même entrer en conflit avec un événement auquel d’autres personnes participent.

Une tâche professionnelle indique seulement qu’il y a un conflit, afin que votre équipe ne voie jamais l’événement personnel. Vous seul voyez avec quel événement il entre en conflit : les deux premiers, puis le nombre d’autres événements concernés. Une tâche à laquelle vous n’avez rien fait se ferme automatiquement si son conflit concerne un autre événement ou s’il n’y en avait finalement pas.

## Préparez vos réunions

Avant une réunion avec des personnes extérieures à votre entreprise, The Machine crée une tâche : **Préparer** la réunion. Elle contient un bref résumé :

- **Qui :** qui sont ces personnes, d’après votre Graph, et des éléments sur leur parcours, lorsque ces informations sont connues.
- **Organisation :** l’activité de leur entreprise, ses clients et ses tarifs, si ces éléments sont importants pour la réunion.
- **Jusqu’ici :** les sujets abordés, les questions posées et les propositions faites, ainsi que leur état d’avancement. Après la réunion, ces messages deviennent les sources de la tâche.
- **Déjà convenu :**, **Modifié depuis :** et **Encore à faire :** les éléments issus des réunions précédentes avec les mêmes personnes, chaque ligne indiquant la réunion ou le message d’origine.
- **Promesses en cours :** ce que vous ou les autres devez encore faire, d’après les promesses sur votre Machine.
- **Questions en suspens :** les questions qui n’ont pas encore de réponse.
- **À décider ou à apporter :** les points à trancher ou les éléments à apporter, ainsi que les sujets qui les intéresseront probablement.

La tâche apparaît le matin d’un jour ouvré : le jour même si la réunion a lieu l’après-midi, sinon le jour ouvré précédent. Elle est à consulter : sélectionnez **Fait** après l’avoir lue. Les promesses ou les questions qui nécessitent une action font l’objet de leurs propres tâches.

Posez une question sur la réunion dans son chat ou ajoutez ce que vous savez. The Machine vous répond ou intègre votre note au résumé, par exemple dans **À décider ou à apporter**, et en tient compte. Rien n’est envoyé depuis un résumé.

Les réunions précédentes sont prises en compte si une personne extérieure y participe aussi, quel que soit leur titre ou l’adresse utilisée. The Machine lit les notes disponibles sur votre Machine : les vôtres, celles de votre application de réunion ou celles qui vous ont été envoyées par e-mail. À défaut, elle consulte la transcription ou les notes de l’événement de calendrier. Les notes les plus récentes ont plus de poids, et un point réglé depuis n’est pas indiqué comme étant encore en suspens.

Les notes et messages de l’[Historique](history.md) sont également pris en compte. Le résumé peut donc tenir compte des réunions qui ont eu lieu avant que vous commenciez à utiliser The Machine.

Un résumé professionnel ne consulte aucune note personnelle ni aucun contenu provenant de la Machine d’une autre personne. Il reste privé : il n’est pas transmis lors d’un transfert et ne peut pas être envoyé pour révision. Si aucune note n’est disponible, ces lignes n’apparaissent pas.

Le résumé utilise les informations déjà présentes sur votre Machine. Pour une première réunion avec une personne d’une entreprise, il consulte également la page d’accueil du site Web de cette entreprise.

Si la recherche Web est configurée sur votre Machine, elle effectue également une recherche rapide sur le nom de la personne et celui de son entreprise. Une Machine hébergée n’inclut pas cette fonctionnalité. Sur votre propre ordinateur, vous pouvez la configurer dans OpenClaw. Les résultats sont accompagnés d’un lien. Seuls le nom public de la personne, le nom de l’entreprise et son site Web sont transmis à la recherche, jamais vos messages. Les résultats sont réutilisés pendant 30 jours.

Ainsi, une première réunion que vous avez acceptée peut être accompagnée d’un résumé avant même que vous ayez échangé un mot : l’activité de l’entreprise, ce qu’elle représente pour vous et, si l’information est connue, l’identité de la personne. Si vous ne disposez que d’un prénom, les résultats de recherche ne sont conservés que s’ils désignent une seule personne. Si **Rechercher les contacts pro** est désactivé dans Paramètres, Sécurité, aucune recherche n’est effectuée.

Une réunion récurrente ne reçoit un résumé que s’il y a eu du nouveau depuis la dernière fois : un message, des notes ou une promesse. Le résumé présente les nouveautés, pas le contenu du précédent. Il apparaît une fois la réunion précédente terminée, pour deux réunions récurrentes par jour au maximum.

Une réunion avec uniquement votre équipe reçoit un résumé seulement si les notes de réunions précédentes font apparaître une décision en suspens, une action à effectuer ou une nouveauté. Ces éléments doivent provenir de la même série de réunions ou d’une réunion portant le même titre que l’une d’elles, jamais d’une autre réunion avec les mêmes collègues. The Machine ne présente pas vos collègues et ne recherche pas d’informations sur eux. Une réunion d’équipe classique n’a pas de résumé.

S’il n’y a rien d’utile à dire, aucune tâche n’est créée. Les réunions personnelles ou refusées n’en génèrent pas. Si une réunion est déplacée, sa tâche est conservée à la nouvelle heure. Une tâche écartée ne réapparaît pas, et celle d’une réunion annulée se ferme automatiquement.

Si une mise à jour modifie le contenu d’un résumé, les résumés ouverts des réunions à venir sont rédigés à nouveau une fois, avec les nouvelles informations. Leur titre, leurs sources et leur position dans votre liste restent inchangés. Un résumé que vous avez modifié, mis en attente ou fermé ne change pas. Il en va de même pour celui d’une réunion qui commence dans les prochaines minutes.

Les détails de la réunion affichent sa tâche sous **Tâche**. Touchez-la pour ouvrir son chat.
