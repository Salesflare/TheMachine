---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, dashboard/graph-notes.js
order: 8
translated: 59dd4e1951e7cc7d
---
Une note donne une vue d’ensemble d’un sujet : un voyage, votre maison, la façon de traiter les factures. Les notes se trouvent dans le Graph, avec les personnes, les organisations et les projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

En haut de Notes, sélectionnez **Nouvelle note**. Donnez-lui un titre, puis sélectionnez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous voulez garder. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Dans une ligne, saisissez @ et les premières lettres d’un nom. Choisissez une personne, une organisation, un projet ou une note dans la liste. Son nom devient alors un lien. La page de l’élément lié affiche **Lié depuis** avec votre note.

## Notes sous d’autres notes

Une note peut se trouver sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre celles qui se trouvent en dessous. Pour déplacer une note, sélectionnez **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, en crée une à cet endroit.

## Notes conservées par votre Machine

Votre Machine rédige aussi des notes à partir de vos messages et les tient à jour. Chaque ligne indique sa source, par exemple l’expéditeur de l’e-mail : touchez-la pour ouvrir le message. Une ligne issue de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne, et votre Machine la gardera ainsi lors de sa mise à jour. Supprimez une ligne ou une note, et elle ne réapparaîtra pas. Les notes créées plus tard sur le même sujet seront ajoutées à l’endroit où vous avez placé la première.

**Revenir à l’original** réaffiche les mots de votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi dans **Ce que j’ai appris**, pour qu’il n’en existe qu’une seule version.

## Voyages

Quand une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans votre messagerie, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage regroupe le code de réservation, le siège et le billet de chaque ligne, dans l’ordre chronologique, et indique ses dates. Dans [Agenda](calendar.md), il apparaît sous forme d’une bande couvrant ces jours et permet d’ouvrir le voyage.

Votre Machine lit les détails de réservation fournis par les compagnies aériennes, les hôtels et les sites de réservation dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces informations ne crée pas de voyage. Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Lorsque toutes les réservations d’un voyage sont annulées, le voyage est lui aussi supprimé.

## Maison

Sous **Maison**, votre Machine conserve ce qu’elle sait de votre maison : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle d’énergie ou d’eau, est ajoutée avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture elle-même. Le montant et les détails de paiement restent sur la facture.
- Un abonnement que vous avez conservé est ajouté et ouvre sa tâche **Abonnements**. Les abonnements annulés ne sont pas affichés.
- Les informations que votre Machine a apprises sur votre maison, comme la marque de votre lave-vaisselle, sont aussi ajoutées. Les modifier les change également sous **Ce que j’ai appris**.
- Si vous avez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations sur cet appareil sont ajoutées à votre note. Votre Machine ne crée pas elle-même de notes de ce type.

Seules les factures et les abonnements personnels sont utilisés, et les notes de Maison sont toujours personnelles. Votre Machine demande une seule fois à son IA, pour chaque nouvelle facture, nouvel abonnement ou nouvel élément appris, si cela concerne votre maison. Pour une facture, elle transmet l’identité de l’émetteur, jamais le montant.

## Santé

Sous **Santé**, votre Machine conserve ce qu’elle sait de votre santé : **Rendez-vous**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Un rendez-vous dans votre agenda auquel vous êtes la seule personne à vous rendre, comme un rendez-vous chez le dentiste, est ajouté avec sa prochaine date ou sa dernière date. **Depuis votre agenda** permet de l’ouvrir.
- Une facture d’un médecin, d’un dentiste ou d’une pharmacie est ajoutée et ouvre sa tâche. Le montant reste sur la facture.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, sont aussi ajoutées. Les modifier les change également sous **Ce que j’ai appris**.
- Votre propre note dans une rubrique, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, reçoit les informations qui le concernent.

Les notes de Santé sont toujours personnelles, même si une facture arrive sur votre adresse professionnelle. Pour chaque nouveau rendez-vous, nouvelle facture ou nouvel élément appris, votre Machine demande une seule fois à son IA si cela concerne votre santé. Pour un rendez-vous, elle transmet son nom, jamais ses notes ni l’identité des autres personnes invitées.

## Fusionner, supprimer et annuler

**Fusionner dans…**, dans le menu ⋯, déplace les lignes d’une note et les notes qui se trouvent sous celle-ci vers une autre note. À partir de là, votre Machine ajoute les nouvelles informations à cette note. **Supprimer** supprime une note. Ces deux actions affichent **Annuler** pendant un instant, tout comme la suppression d’une ligne.

## À ne pas confondre avec les notes de réunion

Les notes de réunion et les notes sur une personne ou une organisation restent à leur emplacement d’origine. Les notes présentées ici sont des pages indépendantes.
