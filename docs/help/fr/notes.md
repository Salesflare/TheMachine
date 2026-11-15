---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, reliée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 88cfd4099bf27f38
---
Une note donne une vue d’ensemble d’un sujet : un voyage, votre maison, la façon dont les factures sont traitées. Les notes se trouvent dans le Graph, à côté des personnes, des organisations et des projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

Touchez **Nouvelle note** en haut de Notes. Donnez-lui un titre, puis touchez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** vous permet d’ajouter ce que vous voulez garder. Chaque ligne de texte devient sa propre ligne.

## Relier des personnes, des projets et d’autres notes

Saisissez @, puis quelques lettres d’un nom dans une ligne. Choisissez une personne, une organisation, un projet ou une note dans la liste. Son nom devient un lien. La page de l’élément lié affiche **Lié depuis** avec votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre les notes qu’elle contient. Pour déplacer une note, touchez **Modifier** et choisissez son emplacement sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, en crée une directement à cet endroit.

En haut de la page d’une note, vous voyez où elle se trouve, par exemple **Notes › Enfants**. Touchez n’importe quelle partie pour y accéder. Sur un téléphone, les notes intermédiaires sont regroupées dans ⋯.

## Notes créées par votre Machine

Votre Machine rédige aussi des notes à partir de vos messages et les tient à jour. Chaque ligne indique sa provenance, par exemple l’expéditeur de l’e-mail. Touchez-la pour ouvrir le message. Une ligne tirée de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**. Une réunion ou un rendez-vous dans votre calendrier ne constitue jamais une ligne à part : l’élément reste dans [Calendrier](calendar.md).

**Maison**, **Santé** et **Enfants** apparaissent seulement quand votre Machine a au moins deux éléments concrets à y ajouter, comme une facture ou une information qu’elle a apprise. En attendant, ces rubriques ne figurent pas dans la liste. Si elles se retrouvent à nouveau vides, elles disparaissent.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne, et votre Machine gardera vos changements lors de la mise à jour de la note. Supprimez une ligne ou une note, et elle ne réapparaîtra pas. Les notes créées par la suite sur le même sujet seront placées là où vous avez mis la première.

**Revenir à l’original** réaffiche les mots de votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi dans **Ce que j’ai appris** : il n’en existe ainsi qu’une seule version.

## Pages rédigées

Dès qu’une note contient au moins deux lignes tirées de vos messages ou de ce que votre Machine a appris, votre Machine rédige le contenu de la page en haut. Elle lit les conversations elles-mêmes, pas seulement leur sujet :

- Un bref résumé du sujet et de son état d’avancement.
- **Faits clés**, **Décisions**, **Points en suspens** et une **Chronologie**, uniquement s’il y a des éléments concrets à indiquer.
- Les lignes de la note figurent ensuite, numérotées sous **Sources**. Chaque phrase se termine par les numéros des lignes dont elle est tirée. Touchez un numéro pour accéder à la ligne correspondante.

La page est réécrite uniquement lorsque les lignes de la note changent, au maximum environ une fois par jour. Si ses sources ne contiennent aucun élément concret, il n’y a pas de page, seulement les lignes. Si vous supprimez une ligne, les informations qui en provenaient uniquement disparaissent aussi de la page. Dans la liste Notes, le début du résumé de chaque page apparaît sous le nom de la note.

Les projets et les organisations ont déjà leur propre page dans le Graph, avec leur description en haut. Les conversations à leur sujet sont ajoutées à cette page, et non à une note.

## Notes tirées de vos conversations

Votre Machine lit les conversations en entier et classe chacune dans la note correspondante : un fil d’e-mails de l’une de vos boîtes mail, un chat dans WhatsApp, Slack, Telegram, LinkedIn ou une autre application connectée, ou encore vos notes de réunion. Les messages d’un chat comptent comme une seule conversation jusqu’à ce que le chat reste inactif pendant deux jours.

- Une conversation à propos d’un projet ou d’une organisation du Graph est ajoutée à sa page, et non à une nouvelle note.
- Une conversation peut être classée dans une rubrique de **Maison**, **Santé** ou **Enfants**, dans l’une de vos notes, ou dans une note que votre Machine crée sous **Travail**, **Voiture**, **Impôts** ou un autre dossier.
- Votre Machine ne crée une note que pour un sujet qui compte au moins deux conversations, ou pour un sujet sur lequel vous avez écrit et qui est clairement toujours d’actualité.
- Chaque ligne correspond à une conversation, de la plus récente à la plus ancienne. Touchez une ligne pour ouvrir la conversation.

Votre Machine envoie à l’IA un court extrait de chaque conversation, sans les réponses citées ni les signatures. Chaque conversation est analysée une seule fois. Les nouveaux messages qu’elle reçoit y sont ensuite ajoutés.

Les e-mails de masse et les chats ne sont jamais ajoutés à une note ni envoyés à l’IA : spam, promotions, newsletters et autres e-mails de listes de diffusion, notifications automatiques, bots et canaux de diffusion. Une conversation à laquelle vous avez participé est tout de même prise en compte, tout comme les e-mails de réservation pour **Voyages** et **Événements**.

La première fois, votre Machine traite les trois derniers mois de conversations en quelques heures, en dehors de la nuit et uniquement si votre forfait IA dispose encore de capacité. Ensuite, elle classe les nouvelles conversations dès qu’il y en a dix en attente, ou dès qu’une conversation est en attente depuis une demi-journée.

## Voyages

Quand une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans votre boîte mail, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Chaque ligne du voyage indique le code de réservation, le siège et le billet, dans l’ordre chronologique, ainsi que les dates du voyage. Dans [Calendrier](calendar.md), le voyage apparaît sous forme d’une bande couvrant ces jours. Touchez-la pour ouvrir le voyage.

Votre Machine lit les détails de réservation fournis par les compagnies aériennes, les hôtels et les sites de réservation dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces détails ne crée pas de voyage. Les e-mails de réservation antérieurs, compris dans l’année d’[historique](history.md) conservée par votre Machine, sont lus en arrière-plan une fois cet historique importé, en commençant par vos boîtes mail personnelles. Si une ancienne confirmation est lue plus tard, elle est ajoutée au voyage existant.

Une réservation modifiée met sa ligne à jour. Une réservation annulée est supprimée. Si toutes les réservations d’un voyage sont annulées, le voyage est lui aussi supprimé.

## Événements

Quand des billets pour un concert, un match, un festival ou une conférence arrivent dans votre boîte mail, votre Machine ajoute l’événement sous **Événements**, avec une note par événement. Une ligne indique le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement affiche ses dates et apparaît sous forme de bande dans [Calendrier](calendar.md). Touchez-la pour ouvrir la note.

- Chaque ligne indique de qui viennent les billets, par exemple **De la part de Example Tickets**, et ouvre l’e-mail correspondant.
- Si l’e-mail des billets a créé une tâche, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Un événement réservé avec votre boîte mail professionnelle est classé dans Travail. Sinon, il est classé dans Personnel.

Votre Machine lit les détails des billets indiqués par les vendeurs dans leurs e-mails de confirmation, sans utiliser l’IA. Un e-mail qui ne contient pas ces détails ne crée pas d’événement. Une réservation annulée est supprimée. Si tous les billets d’un événement sont annulés, l’événement est lui aussi supprimé.

## Maison

Sous **Maison**, votre Machine conserve ce qu’elle sait de votre maison : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle d’énergie ou d’eau, est ajoutée avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture elle-même. Le montant et les détails de paiement restent sur cette page.
- Un abonnement que vous avez conservé est ajouté et ouvre sa tâche **Abonnements**. Les abonnements que vous avez résiliés ne figurent pas dans la liste.
- Les personnes ou organismes qui vous écrivent régulièrement au sujet de votre maison, comme votre fournisseur d’énergie, votre fournisseur Internet ou votre mairie, ont une ligne qui indique à quelle fréquence ils vous écrivent. Touchez-la pour ouvrir leur e-mail le plus récent.
- Les informations que votre Machine a apprises sur votre maison, comme la marque de votre lave-vaisselle, sont également ajoutées. Les modifier change aussi leur contenu dans **Ce que j’ai appris**.
- Si vous gardez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les éléments qui le concernent sont ajoutés à votre note. Votre Machine ne crée pas elle-même ce type de note.

Seules les factures, les abonnements et les e-mails personnels sont utilisés. Les notes Maison sont toujours personnelles. Votre Machine demande une fois à son IA d’examiner chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvelle information apprise afin de déterminer si l’élément concerne votre maison. Pour une facture, elle indique de qui elle vient, jamais le montant.

Vos conversations sont également ajoutées à ces notes, comme indiqué plus haut dans **Notes tirées de vos conversations**.

## Santé

Sous **Santé**, votre Machine conserve ce qu’elle sait de votre santé : **Rendez-vous**, **Résultats des tests**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture d’un médecin, d’un dentiste ou d’une pharmacie est ajoutée et ouvre sa tâche. Le montant reste sur cette page.
- Chaque e-mail de votre cabinet médical, d’un hôpital, d’un laboratoire ou de votre assurance maladie est ajouté sous forme de ligne datée avec son objet, pour que votre historique se constitue au fil du temps. Touchez la ligne pour ouvrir l’e-mail.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, sont également ajoutées. Les modifier change aussi leur contenu dans **Ce que j’ai appris**.
- Si vous avez votre propre note dans une rubrique, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, les éléments qui le concernent sont ajoutés à votre note.

Les notes Santé sont toujours personnelles, même si une facture est arrivée à votre adresse professionnelle. Votre Machine demande une fois à son IA d’examiner chaque nouvelle facture ou information apprise afin de déterminer si elle concerne votre santé.

## Enfants

Sous **Enfants**, votre Machine conserve ce qu’elle sait de vos enfants : **École**, **Activités**, **Garde d’enfants**, **Médecins et soins** et **Factures et frais**. Une baby-sitter ou une garderie est classée sous Garde d’enfants, jamais sous Médecins et soins. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur principal ou son jour de natation, sont ajoutées sous forme d’une ligne liée à sa page. Votre Machine considère une personne comme votre enfant lorsque la rubrique **Pour vous** l’indique, par exemple « fille » ou « fils ».
- Une facture d’école, de club ou de garde d’enfants est ajoutée et ouvre sa tâche. Le montant reste sur cette page.
- Chaque e-mail de l’école, d’un club ou d’un service de garde d’enfants, par exemple pour annoncer une sortie ou un changement de programme, est ajouté sous forme de ligne datée avec son objet. Tout ce qu’ils vous envoient est ainsi regroupé au même endroit. Touchez la ligne pour ouvrir l’e-mail.
- Si vous avez votre propre note pour un enfant dans une rubrique, par exemple une note pour Isla sous **École**, les éléments qui concernent cet enfant sont ajoutés à votre note.

Les notes Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Votre Machine demande une fois à son IA d’examiner chaque nouvel élément afin de déterminer s’il concerne vos enfants.

## Fusionner, supprimer et annuler

**Fusionner dans…**, dans le menu ⋯, déplace les lignes d’une note et les notes qu’elle contient dans une autre note. Votre Machine ajoutera désormais les nouveaux éléments à cette note. **Supprimer** efface une note. Ces deux actions affichent **Annuler** pendant un instant. C’est aussi le cas lorsque vous supprimez une ligne.

## À distinguer des notes de réunion

Les notes de réunion et les notes liées à une personne ou à une organisation restent à leur emplacement initial. Les notes présentées ici sont des pages à part entière.
