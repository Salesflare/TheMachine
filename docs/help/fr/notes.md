---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 8e27b2c69f77196d
---
Une note présente un sujet : un voyage, votre maison, la façon dont les factures sont réglées. Les notes se trouvent dans le Graph, aux côtés des personnes, des organisations et des projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Créer une note

**Nouvelle note** en haut de Notes. Donnez-lui un titre, puis appuyez sur **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous voulez garder. Chaque ligne de texte devient une ligne à part.

## Lier des personnes, des projets et d’autres notes

Tapez @ et quelques lettres d’un nom dans une ligne. Choisissez une personne, une organisation, un projet ou une note dans la liste. Son nom apparaît sous forme de lien. La page de l’élément lié affiche **Lié depuis**, avec votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre les notes imbriquées. Pour déplacer une note, appuyez sur **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, en crée une à cet endroit.

En haut de la page d’une note, vous voyez où elle se trouve, par exemple **Notes › Enfants**. Appuyez sur une partie du chemin pour y accéder. Sur un téléphone, les notes intermédiaires sont regroupées dans ⋯.

## Notes conservées par votre Machine

Votre Machine rédige aussi des notes automatiquement à partir de vos messages, et les tient à jour. Chaque ligne indique sa provenance, par exemple l’expéditeur de l’e-mail. Appuyez dessus pour ouvrir le message. Une ligne tirée de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**. Une réunion ou un rendez-vous de votre calendrier n’apparaît jamais seul dans une note : il reste dans [Calendrier](calendar.md).

**Maison**, **Santé** et **Enfants** apparaissent uniquement quand votre Machine a au moins deux éléments concrets à y ajouter, comme une facture ou une information qu’elle a apprise. D’ici là, ces notes ne figurent pas dans la liste. Si elles n’ont plus rien à afficher, elles disparaissent.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne : votre Machine la garde ainsi lors de sa mise à jour. Supprimez une ligne ou une note, et elle ne réapparaîtra pas. Les notes ajoutées plus tard sur le même sujet seront placées au même endroit que la première.

**Revenir à l’original** réaffiche le texte rédigé par votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi dans **Ce que j’ai appris** : il n’en existe qu’une seule version.

## Voyages

Quand une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans votre messagerie, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Chaque ligne du voyage indique le code de réservation, le siège et le billet, dans l’ordre chronologique, et le voyage affiche ses dates. Dans [Calendrier](calendar.md), il apparaît sous forme de bandeau sur ces jours. Appuyez dessus pour ouvrir le voyage.

Votre Machine lit les détails de réservation que les compagnies aériennes, les hôtels et les sites de réservation incluent dans leurs e-mails de confirmation. Un e-mail sans ces détails ne crée pas de voyage. Les e-mails de réservation antérieurs à la période d’[historique](history.md) conservée par votre Machine sont lus en arrière-plan, une fois cet historique importé, en commençant par vos messageries personnelles.

Une modification de réservation met à jour sa ligne, et une annulation la supprime. Lorsque toutes les réservations d’un voyage sont annulées, le voyage disparaît aussi.

## Événements

Quand des billets pour un concert, un match, un festival ou une conférence arrivent dans votre messagerie, votre Machine ajoute l’événement sous **Événements**, dans une note dédiée. Une ligne indique le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement affiche ses dates et apparaît sous forme de bandeau dans [Calendrier](calendar.md). Appuyez dessus pour ouvrir la note.

- Chaque ligne indique l’expéditeur des billets, par exemple **De la part de Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche provient de l’e-mail des billets, par exemple pour les payer, **Ouvrir la tâche** l’affiche.
- Un événement réservé depuis votre messagerie professionnelle est classé comme professionnel. Sinon, il est personnel.

Votre Machine lit les détails des billets inclus par les vendeurs dans leurs e-mails de confirmation, sans utiliser l’IA. Un e-mail sans ces détails ne crée pas d’événement. Une réservation annulée est supprimée. Si tous les billets d’un événement sont annulés, l’événement disparaît aussi.

## Maison

Sous **Maison**, votre Machine conserve ce qu’elle sait de votre logement : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle d’énergie ou d’eau, est ajoutée avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture elle-même ; le montant et les détails de paiement y restent.
- Un abonnement que vous avez conservé est ajouté et ouvre sa tâche **Abonnements**. Les abonnements résiliés ne sont pas affichés.
- Les personnes ou organismes qui vous écrivent régulièrement au sujet de votre logement, comme votre fournisseur d’énergie, votre opérateur Internet ou la mairie, sont ajoutés avec la fréquence de leurs messages. Appuyez sur une ligne pour ouvrir leur e-mail le plus récent.
- Les informations que votre Machine a apprises sur votre logement, comme la marque de votre lave-vaisselle, sont également ajoutées. Les modifier les modifie aussi dans **Ce que j’ai appris**.
- Si vous conservez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations sur cet appareil sont ajoutées à cette note. Votre Machine ne crée pas elle-même ce type de note.

Seuls les e-mails, factures et abonnements personnels sont utilisés, et les notes Maison sont toujours personnelles. Votre Machine demande une fois à son IA si chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvel élément appris concerne votre logement. Pour une facture, elle transmet l’identité de l’expéditeur, jamais le montant.

Pour **Maison**, **Santé** et **Enfants**, votre Machine demande aussi une fois à son IA d’examiner chaque nouvel expéditeur de vos e-mails personnels. Elle lui transmet le nom de l’expéditeur, le nombre d’e-mails envoyés et les sujets les plus récents, avec les numéros masqués, mais jamais le contenu des e-mails.

La première fois, elle parcourt les e-mails de l’année écoulée en quelques heures, en dehors de la nuit et uniquement si votre forfait IA a encore de la capacité. Ensuite, elle examine les nouveaux expéditeurs toutes les six heures.

## Santé

Sous **Santé**, votre Machine conserve ce qu’elle sait de votre santé : **Rendez-vous**, **Résultats des tests**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture d’un médecin, d’un dentiste ou d’une pharmacie est ajoutée et ouvre sa tâche. Le montant reste dans la tâche.
- Chaque e-mail de votre cabinet médical, d’un hôpital, d’un laboratoire ou de votre assurance maladie apparaît sous forme de ligne datée avec son sujet. Votre historique s’enrichit au fil du temps. Appuyez sur une ligne pour ouvrir l’e-mail.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, sont également ajoutées. Les modifier les modifie aussi dans **Ce que j’ai appris**.
- Si vous avez une note personnelle dans une rubrique, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, les informations à son sujet sont ajoutées à cette note.

Les notes Santé sont toujours personnelles, même si une facture arrive sur votre adresse professionnelle. Votre Machine demande une fois à son IA si chaque nouvelle facture ou chaque nouvel élément appris concerne votre santé.

## Enfants

Sous **Enfants**, votre Machine conserve ce qu’elle sait de vos enfants : **École**, **Activités**, **Garde d’enfants**, **Médecins et soins** et **Factures et frais**. Une baby-sitter ou une garderie est classée sous Garde d’enfants, jamais sous Médecins et soins. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur principal ou le jour de son cours de natation, sont ajoutées sous forme de ligne liée à sa page. Elle considère une personne comme votre enfant lorsque la mention **Pour vous** l’indique, par exemple « fille » ou « fils ».
- Une facture de l’école, d’un club ou d’un service de garde d’enfants est ajoutée et ouvre sa tâche. Le montant reste dans la tâche.
- Chaque e-mail de l’école, d’un club ou d’un service de garde d’enfants, comme la lettre hebdomadaire ou un message au sujet d’une sortie, apparaît sous forme de ligne datée avec son sujet. Tous leurs messages sont ainsi regroupés au même endroit. Appuyez sur une ligne pour ouvrir l’e-mail.
- Si vous avez une note personnelle pour un enfant dans une rubrique, par exemple une note pour Isla sous **École**, les informations à son sujet sont ajoutées à cette note.

Les notes Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Votre Machine demande une fois à son IA si chaque nouvel élément concerne vos enfants.

## Fusionner, supprimer et annuler

**Fusionner dans…**, dans le menu ⋯, déplace les lignes d’une note et les notes qu’elle contient vers une autre note. Votre Machine ajoute ensuite les nouveaux éléments à cette autre note. **Supprimer** efface une note. Ces deux actions affichent **Annuler** pendant un instant. C’est aussi le cas lorsqu’une ligne est supprimée.

## Différentes des notes de réunion

Les notes de réunion et les notes sur une personne ou une organisation restent à leur emplacement d’origine. Les notes présentées ici sont des pages à part entière.
