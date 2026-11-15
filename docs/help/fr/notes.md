---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, home_notes.py, dashboard/graph-notes.js
order: 8
translated: 4a6b4d56a8d9b93f
---
Une note est une vue d’ensemble d’un sujet : un voyage, votre maison, la façon dont les factures sont payées. Les notes se trouvent dans le Graph, à côté des Personnes, des Organisations et des Projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

En haut de Notes, sélectionnez **Nouvelle note**. Donnez-lui un titre, puis sélectionnez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous voulez conserver. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Dans une ligne, saisissez @ suivi de quelques lettres d’un nom. Choisissez une personne, une organisation, un projet ou une note dans la liste : son nom devient un lien. La page de l’élément lié affiche **Lié depuis** avec votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre celles qui se trouvent dessous. Pour déplacer une note, sélectionnez **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, en crée une à cet endroit.

## Les notes que votre Machine conserve

Votre Machine rédige aussi des notes automatiquement à partir de vos messages et les tient à jour. Chaque ligne indique sa source, par exemple l’expéditeur de l’e-mail : touchez-la pour ouvrir le message. Une ligne tirée de **Ce que j’ai appris** indique **D’après ce que j’ai appris**.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne, et votre Machine la gardera ainsi lors de sa mise à jour. Supprimez une ligne ou une note : elle ne réapparaîtra pas. Les notes ajoutées par la suite sur le même sujet seront placées là où vous avez mis la première.

**Revenir à l’original** réaffiche les mots utilisés par votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi dans **Ce que j’ai appris**, afin qu’il n’en existe qu’une seule version.

## Voyages

Lorsqu’une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans vos e-mails, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage indique le code de réservation, le siège et le billet de chaque ligne, dans l’ordre chronologique, ainsi que ses dates. Dans [Calendrier](calendar.md), il apparaît sous forme d’une bande couvrant ces jours et ouvre le voyage.

Votre Machine lit les détails de réservation indiqués par les compagnies aériennes, les hôtels et les sites de réservation dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces détails ne crée pas de voyage. Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Lorsque toutes les réservations d’un voyage sont annulées, le voyage est lui aussi supprimé.

## Maison

Sous **Maison**, votre Machine conserve ce qu’elle sait sur votre maison : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle de l’énergie ou de l’eau, apparaît avec sa fréquence et la date de la dernière réception. **Ouvrir la tâche** affiche la facture elle-même ; le montant et les détails de paiement s’y trouvent.
- Un abonnement que vous avez conservé apparaît et ouvre sa tâche **Abonnements**. Un abonnement résilié n’est pas affiché.
- Les informations que votre Machine a apprises sur votre maison, comme la marque de votre lave-vaisselle, apparaissent aussi sous forme de ligne. Les modifier les modifie également dans **Ce que j’ai appris**.
- Si vous avez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations sur cet appareil seront ajoutées à votre note. Votre Machine ne crée pas elle-même de notes de ce type.

Seules les factures et les abonnements personnels sont utilisés, et les notes Maison sont toujours personnelles. Votre Machine interroge son IA une fois pour chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvel élément appris, afin de déterminer si cela concerne votre maison. Pour une facture, elle indique son émetteur, jamais le montant.

## Fusionner, supprimer et annuler

**Fusionner dans…**, dans le menu ⋯, déplace les lignes d’une note et les notes imbriquées dans une autre note. À partir de là, votre Machine ajoutera les nouvelles informations à cette note. **Supprimer** efface une note. Dans les deux cas, ainsi que lors de la suppression d’une ligne, **Annuler** s’affiche pendant un instant.

## À ne pas confondre avec les notes de réunion

Les notes de réunion et les notes associées à une personne ou à une organisation restent là où elles se trouvaient. Les notes présentées ici sont des pages à part entière.
