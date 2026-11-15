---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a32102a88a8b3856
---
Une note donne une vue d’ensemble d’un sujet : un voyage, votre maison, la façon de traiter les factures. Les notes se trouvent dans le Graph, à côté des Personnes, des Organisations et des Projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

Touchez **Nouvelle note** en haut de Notes. Donnez-lui un titre, puis touchez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous voulez conserver. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Tapez @ puis quelques lettres d’un nom dans une ligne. Choisissez une personne, une organisation, un projet ou une note dans la liste pour insérer son nom sous forme de lien. La page de l’élément lié affiche **Lié depuis**, avec votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : touchez la flèche à côté d’une note pour afficher celles qu’elle contient. Pour déplacer une note, touchez **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, en crée une à cet endroit.

## Notes que votre Machine conserve

Votre Machine rédige aussi des notes automatiquement à partir de vos messages et les tient à jour. Chaque ligne indique sa source, par exemple l’expéditeur de l’e-mail : touchez-la pour ouvrir le message. Une ligne provenant de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne, et votre Machine la gardera ainsi lors de sa mise à jour. Si vous supprimez une ligne ou une note, elle ne réapparaîtra pas. Les notes créées plus tard sur le même sujet iront là où vous avez placé la première.

**Revenir à l’original** réaffiche les propres mots de votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi sous **Ce que j’ai appris** : il n’en existe donc qu’une seule version.

## Voyages

Quand une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans votre boîte mail, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage indique le code de réservation, le siège et le billet pour chaque ligne, dans l’ordre chronologique, ainsi que ses dates. Dans [Agenda](calendar.md), il apparaît sous forme d’une seule barre couvrant ces journées et ouvre le voyage.

Votre Machine lit les détails de réservation que les compagnies aériennes, les hôtels et les sites de réservation indiquent dans leurs e-mails de confirmation. Un e-mail sans ces détails ne crée pas de voyage. Une réservation modifiée met sa ligne à jour, et une réservation annulée est supprimée. Lorsque toutes les réservations d’un voyage sont annulées, le voyage est lui aussi supprimé.

## Événements

Quand des billets pour un concert, un match, un festival ou une conférence arrivent dans votre boîte mail, votre Machine ajoute l’événement sous **Événements**, avec une note par événement. Une ligne indique le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement indique ses dates et apparaît sous forme de barre dans [Agenda](calendar.md), où il ouvre la note.

- Chaque ligne indique de qui proviennent les billets, par exemple **De la part de Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche provient de l’e-mail des billets, par exemple pour les payer, **Ouvrir la tâche** l’affiche.
- Un événement réservé depuis votre boîte mail professionnelle est classé Professionnel, sinon il est classé Personnel.

Votre Machine lit les détails des billets indiqués par les vendeurs dans leurs e-mails de confirmation, sans utiliser l’IA. Un e-mail sans ces détails ne crée pas d’événement. Une réservation annulée est supprimée. Lorsque tous les billets d’un événement sont annulés, l’événement est lui aussi supprimé.

## Maison

Sous **Maison**, votre Machine conserve ce qu’elle sait de votre logement : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle de l’énergie ou de l’eau, fait l’objet d’une ligne indiquant sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture elle-même ; le montant et les détails du paiement s’y trouvent.
- Un abonnement que vous avez conservé fait l’objet d’une ligne qui ouvre sa tâche **Abonnements**. Un abonnement que vous avez annulé n’apparaît pas dans la liste.
- Les informations que votre Machine a apprises sur votre logement, comme la marque de votre lave-vaisselle, apparaissent aussi sous forme de ligne. Les modifier les change également sous **Ce que j’ai appris**.
- Si vous gardez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations sur cet appareil vont dans votre note. Votre Machine ne crée pas elle-même de notes de ce type.

Seules les factures et les abonnements personnels sont pris en compte, et les notes Maison sont toujours personnelles. Votre Machine demande une fois à son IA si chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvel élément appris concerne votre logement. Pour une facture, elle lui indique l’émetteur, jamais le montant.

## Santé

Sous **Santé**, votre Machine conserve ce qu’elle sait de votre santé : **Rendez-vous**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Un rendez-vous dans votre agenda auquel vous allez seul, comme chez le dentiste, fait l’objet d’une ligne indiquant sa prochaine date ou, s’il est passé, sa dernière date. **Depuis votre agenda** l’ouvre.
- Une facture d’un médecin, d’un dentiste ou d’une pharmacie fait l’objet d’une ligne qui ouvre sa tâche. Le montant s’y trouve.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, apparaissent aussi sous forme de ligne. Les modifier les change également sous **Ce que j’ai appris**.
- Votre propre note dans une rubrique, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, recueille les informations concernant cette personne.

Les notes Santé sont toujours personnelles, même si une facture est arrivée à votre adresse professionnelle. Votre Machine demande une fois à son IA si chaque nouveau rendez-vous, chaque nouvelle facture ou chaque nouvel élément appris concerne votre santé. Pour un rendez-vous, elle lui indique son nom, jamais les notes ni les autres personnes invitées.

## Enfants

Sous **Enfants**, votre Machine conserve ce qu’elle sait de vos enfants : **École**, **Activités**, **Médecins et soins** et **Factures et frais**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur ou son jour de natation, apparaissent sous forme de ligne liée à sa page. Elle considère une personne comme votre enfant lorsque la mention **Pour vous** le précise, par exemple « fille » ou « fils ».
- Un événement dans votre agenda auquel vous allez seul, comme une réunion parents-professeurs, fait l’objet d’une ligne indiquant sa prochaine date ou, s’il est passé, sa dernière date. **Depuis votre agenda** l’ouvre.
- Une facture de l’école, d’un club ou d’un service de garde fait l’objet d’une ligne qui ouvre sa tâche. Le montant s’y trouve.
- Votre propre note pour un enfant dans une rubrique, par exemple une note pour Isla sous **École**, recueille les informations le concernant.

Les notes Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Votre Machine demande une fois à son IA si chaque nouvel élément concerne vos enfants.

## Fusionner, supprimer et annuler

**Fusionner dans…**, dans le menu ⋯, déplace les lignes d’une note et les notes qu’elle contient vers une autre note. Votre Machine ajoutera ensuite les nouveaux éléments à cette note. **Supprimer** efface une note. Ces deux actions affichent brièvement **Annuler**, tout comme la suppression d’une ligne.

## À ne pas confondre avec les notes de réunion

Les notes de réunion et les notes sur une personne ou une organisation restent à leur emplacement actuel. Les notes présentées ici sont des pages à part entière.
