---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: b88647412222409d
---
Une note présente un sujet : un voyage, votre maison, la façon de gérer les factures. Les notes se trouvent dans le Graph, aux côtés des personnes, des organisations et des projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Créer une note

**Nouvelle note** en haut de la page Notes. Donnez-lui un titre, puis sélectionnez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous voulez garder. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Tapez @ suivi de quelques lettres d’un nom dans une ligne. Choisissez une personne, une organisation, un projet ou une note dans la liste. Son nom devient alors un lien. La page de l’élément lié affiche **Lié depuis** avec votre note.

## Notes imbriquées

Une note peut être placée sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre celles qui se trouvent dessous. Pour déplacer une note, sélectionnez **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci** dans le menu ⋯ en crée une juste en dessous.

## Notes conservées par votre Machine

Votre Machine rédige aussi des notes automatiquement à partir de vos messages et les met à jour. Chaque ligne indique sa source, par exemple l’expéditeur de l’e-mail : touchez-la pour ouvrir le message. Une ligne tirée de **Ce que j’ai appris** indique **D’après ce que j’ai appris**.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne : votre Machine gardera vos changements lors de la mise à jour de la note. Si vous supprimez une ligne ou une note, elle ne réapparaîtra pas. Les notes ajoutées plus tard sur le même sujet seront placées là où vous avez mis la première.

**Revenir à l’original** affiche de nouveau les mots de votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi sous **Ce que j’ai appris** : il n’en existe ainsi qu’une seule version.

## Voyages

Lorsqu’une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans vos e-mails, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même séjour figurent dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage indique, pour chaque ligne et dans l’ordre chronologique, le code de réservation, le siège et le billet, ainsi que les dates. Dans [Agenda](calendar.md), il apparaît sous forme d’une seule barre couvrant ces jours et ouvre le voyage.

Votre Machine lit les détails de réservation que les compagnies aériennes, les hôtels et les sites de réservation incluent dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces détails ne crée pas de voyage. Les e-mails de réservation antérieurs, datant de l’année couverte par l’[historique](history.md) conservé par votre Machine, sont traités en arrière-plan une fois cet historique chargé. Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Lorsque toutes les réservations d’un voyage sont annulées, le voyage est également supprimé.

## Événements

Lorsque des billets pour un concert, un match, un festival ou une conférence arrivent dans vos e-mails, votre Machine ajoute l’événement sous **Événements**, dans une note distincte. Une ligne indique le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement indique ses dates et apparaît sous forme d’une barre dans [Agenda](calendar.md), qui ouvre la note.

- Chaque ligne indique de qui viennent les billets, par exemple **De la part d’Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche a été créée à partir de l’e-mail des billets, par exemple pour les payer, **Ouvrir la tâche** permet de l’afficher.
- Un événement réservé avec votre adresse e-mail professionnelle est classé Travail. Sinon, il est classé Personnel.

Votre Machine lit les détails des billets inclus par les vendeurs dans leurs e-mails de confirmation, sans IA. Un e-mail qui ne contient pas ces détails ne crée pas d’événement. Une réservation annulée est supprimée. Si tous les billets d’un événement sont annulés, l’événement est également supprimé.

## Maison

Sous **Maison**, votre Machine conserve les informations qu’elle connaît sur votre logement : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle d’énergie ou d’eau, est ajoutée avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture ; son montant et les détails du paiement restent dans la tâche.
- Un abonnement que vous avez conservé est ajouté avec un lien vers sa tâche **Abonnements**. Les abonnements que vous avez résiliés ne sont pas affichés.
- Les informations que votre Machine a apprises sur votre logement, comme la marque de votre lave-vaisselle, sont aussi ajoutées sous forme de ligne. Les modifier les modifie également sous **Ce que j’ai appris**.
- Si vous gardez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations sur cet appareil sont ajoutées à votre note. Votre Machine ne crée pas elle-même ce type de note.

Seules les factures et les abonnements personnels sont utilisés, et les notes Maison sont toujours personnelles. Votre Machine demande une fois à son IA, pour chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvel élément appris, s’il concerne votre logement. Pour une facture, elle indique son expéditeur, jamais son montant.

## Santé

Sous **Santé**, votre Machine conserve les informations qu’elle connaît sur votre santé : **Rendez-vous**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Un rendez-vous dans votre agenda auquel vous vous rendez seul, comme chez le dentiste, est ajouté avec sa prochaine date ou sa dernière date. **Depuis votre agenda** permet de l’ouvrir.
- Une facture d’un médecin, d’un dentiste ou d’une pharmacie est ajoutée avec un lien vers sa tâche. Le montant reste dans la tâche.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, sont aussi ajoutées sous forme de ligne. Les modifier les modifie également sous **Ce que j’ai appris**.
- Votre propre note dans une rubrique, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, contient les informations sur ce sujet.

Les notes Santé sont toujours personnelles, même si une facture arrive sur votre adresse professionnelle. Votre Machine demande une fois à son IA, pour chaque nouveau rendez-vous, chaque nouvelle facture ou chaque nouvel élément appris, si cela concerne votre santé. Elle transmet le nom du rendez-vous, jamais son contenu ni la liste des autres personnes invitées.

## Enfants

Sous **Enfants**, votre Machine conserve les informations qu’elle connaît sur vos enfants : **École**, **Activités**, **Médecins et soins** et **Factures et frais**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur ou son jour de natation, sont ajoutées sous forme de ligne liée à sa page. Elle considère une personne comme votre enfant lorsque la rubrique **Pour vous** indique son lien avec vous, par exemple fille ou fils.
- Un événement dans votre agenda auquel vous vous rendez seul, comme une réunion de parents d’élèves, est ajouté avec sa prochaine date ou sa dernière date. **Depuis votre agenda** permet de l’ouvrir.
- Une facture de l’école, d’un club ou d’un service de garde est ajoutée avec un lien vers sa tâche. Le montant reste dans la tâche.
- Votre propre note pour un enfant dans une rubrique, par exemple une note sur Isla sous **École**, contient les informations sur cet enfant.

Les notes Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Votre Machine demande une fois à son IA, pour chaque nouvelle information, si elle concerne vos enfants.

## Fusionner, supprimer et annuler

**Fusionner dans…** dans le menu ⋯ déplace les lignes d’une note et les notes qui se trouvent dessous vers une autre note. Votre Machine ajoutera ensuite les nouvelles informations à cette note. **Supprimer** efface une note. Ces deux actions affichent **Annuler** pendant un instant, tout comme la suppression d’une ligne.

## À ne pas confondre avec les notes de réunion

Les notes de réunion et celles d’une personne ou d’une organisation restent à leur emplacement actuel. Les notes présentées ici sont des pages à part entière.
