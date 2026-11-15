---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, reliée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 336e0f0dad44f19a
---
Une note donne une vue d’ensemble sur un sujet : un voyage, votre maison, la façon de traiter les factures. Les notes se trouvent dans le Graph, avec les personnes, les organisations et les projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

En haut de Notes, sélectionnez **Nouvelle note**. Donnez-lui un titre, puis sélectionnez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous voulez garder. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Dans une ligne, tapez @ suivi de quelques lettres d’un nom. Dans la liste, choisissez une personne, une organisation, un projet ou une note. Son nom apparaît alors sous forme de lien. La page de l’élément lié affiche **Lié depuis** avec votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, par exemple Électroménager sous Maison. Notes affiche les notes sous forme d’arborescence : la flèche à côté d’une note affiche celles qui se trouvent dessous. Pour déplacer une note, sélectionnez **Modifier**, puis choisissez son emplacement sous **Sous**. Dans le menu ⋯, **Nouvelle note sous celle-ci** en crée une à cet endroit.

En haut de la page d’une note, vous voyez son emplacement, par exemple **Notes › Enfants**. Touchez une partie pour y accéder. Sur un téléphone, les notes intermédiaires sont regroupées dans ⋯.

## Notes créées par votre Machine

Votre Machine rédige aussi des notes à partir de vos messages, et les tient à jour. Chaque ligne indique sa source, par exemple l’expéditeur de l’e-mail. Touchez-la pour ouvrir le message. Une ligne issue de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**. Une réunion ou un rendez-vous de votre calendrier n’apparaît jamais seul dans une note : il reste dans [Calendrier](calendar.md).

**Maison**, **Santé** et **Enfants** apparaissent uniquement lorsque votre Machine a au moins deux éléments concrets à y ajouter, comme une facture ou une information qu’elle a apprise. Jusque-là, ces notes ne figurent pas dans la liste. Si elles n’ont plus rien à afficher, elles disparaissent.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne, et votre Machine la gardera ainsi lors de sa mise à jour. Supprimez une ligne ou une note, et elle ne réapparaîtra pas. Les nouvelles notes sur le même sujet seront ajoutées à l’endroit où vous avez placé la première.

**Revenir à l’original** réaffiche les mots de votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi sous **Ce que j’ai appris**. Il n’en existe ainsi qu’une seule version.

## Voyages

Lorsqu’une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans votre boîte mail, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage affiche le code de réservation, le siège et le billet de chaque ligne, dans l’ordre chronologique, ainsi que ses dates. Dans [Calendrier](calendar.md), il apparaît sous forme d’une bande couvrant ces journées. Touchez-la pour ouvrir le voyage.

Votre Machine lit les détails de réservation que les compagnies aériennes, les hôtels et les sites de réservation incluent dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces informations ne crée pas de voyage. Les e-mails de réservation antérieurs, datant de l’année d’[historique](history.md) conservée par votre Machine, sont lus en arrière-plan une fois l’historique importé, en commençant par vos boîtes mail personnelles. Une confirmation plus ancienne lue ultérieurement est ajoutée au voyage déjà créé.

Une réservation modifiée met à jour sa ligne. Une réservation annulée est supprimée. Lorsque toutes les réservations d’un voyage sont annulées, le voyage disparaît aussi.

## Événements

Lorsque des billets pour un concert, un match, un festival ou une conférence arrivent dans votre boîte mail, votre Machine ajoute l’événement sous **Événements**, dans une note distincte. Une ligne indique le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement affiche ses dates et apparaît sous forme d’une bande dans [Calendrier](calendar.md). Touchez-la pour ouvrir la note.

- Chaque ligne indique la provenance des billets, par exemple **De Exemple Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche provient de l’e-mail des billets, par exemple pour les payer, **Ouvrir la tâche** l’affiche.
- Un événement réservé depuis votre boîte mail professionnelle est classé comme professionnel. Sinon, il est personnel.

Votre Machine lit, sans IA, les détails des billets que les vendeurs incluent dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces informations ne crée pas d’événement. Une réservation annulée est supprimée. Lorsque tous les billets d’un événement sont annulés, l’événement disparaît aussi.

## Maison

Sous **Maison**, votre Machine conserve ce qu’elle sait de votre maison : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle de l’électricité ou de l’eau, apparaît avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture. Le montant et les détails de paiement restent dans la tâche.
- Un abonnement que vous avez conservé apparaît avec une ligne qui ouvre sa tâche **Abonnements**. Un abonnement annulé n’est pas répertorié.
- Les personnes ou organismes qui vous écrivent régulièrement au sujet de votre maison, comme votre fournisseur d’énergie, votre opérateur Internet ou la mairie, apparaissent avec la fréquence de leurs messages. Touchez la ligne pour ouvrir leur e-mail le plus récent.
- Les informations que votre Machine a apprises sur votre maison, comme la marque de votre lave-vaisselle, apparaissent aussi sous forme de ligne. Les modifier change aussi le contenu sous **Ce que j’ai appris**.
- Si vous avez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations sur cet appareil sont ajoutées à votre note. Votre Machine ne crée pas elle-même de notes de ce type.

Seules les factures, les abonnements et les e-mails personnels sont utilisés. Les notes Maison sont toujours personnelles. Pour chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvelle information apprise, votre Machine interroge une fois son IA afin de déterminer si cela concerne votre maison. Pour une facture, elle indique l’expéditeur, mais jamais le montant.

Pour **Maison**, **Santé** et **Enfants**, votre Machine interroge aussi une fois son IA au sujet de chaque expéditeur de vos e-mails personnels. Elle lui transmet le nom de l’expéditeur, le nombre d’e-mails envoyés et les objets de ses e-mails les plus récents, dont les chiffres sont masqués. Elle ne transmet jamais les e-mails eux-mêmes. Un e-mail reçu deux fois, ou dans deux de vos boîtes mail, ne compte qu’une fois. Il en va de même pour une réponse ayant le même objet que le fil de discussion auquel elle appartient.

Les e-mails en nombre ne sont jamais ajoutés à ces notes ni transmis à l’IA : courriers indésirables, promotions, newsletters et autres messages de listes de diffusion, ainsi que les notifications automatiques sans possibilité de réponse. Les e-mails d’un fil auquel vous avez répondu sont tout de même comptés, tout comme les e-mails de réservation pour **Voyages** et **Événements**.

La première fois, votre Machine parcourt les e-mails de l’année écoulée en quelques heures, en dehors de la nuit et uniquement si votre forfait IA dispose de suffisamment de capacité. Ensuite, elle vérifie les nouveaux expéditeurs toutes les six heures.

## Santé

Sous **Santé**, votre Machine conserve ce qu’elle sait de votre santé : **Rendez-vous**, **Résultats des tests**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture d’un médecin, d’un dentiste ou d’une pharmacie apparaît sous forme de ligne qui ouvre la tâche correspondante. Le montant reste dans la tâche.
- Chaque e-mail de votre cabinet médical, d’un hôpital, d’un laboratoire ou de votre assurance santé apparaît sous forme de ligne datée avec son objet, pour que votre historique se constitue au fil du temps. Touchez la ligne pour ouvrir l’e-mail.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, apparaissent aussi sous forme de ligne. Les modifier change aussi le contenu sous **Ce que j’ai appris**.
- Votre propre note dans une rubrique, par exemple une note sur votre kiné sous **Rendez-vous**, reçoit les informations concernant ce sujet.

Les notes Santé sont toujours personnelles, même si une facture est arrivée à votre adresse professionnelle. Pour chaque nouvelle facture ou information apprise, votre Machine interroge une fois son IA afin de déterminer si cela concerne votre santé.

## Enfants

Sous **Enfants**, votre Machine conserve ce qu’elle sait de vos enfants : **École**, **Activités**, **Garde d’enfants**, **Médecins et soins** et **Factures et frais**. Une baby-sitter ou une garderie est classée sous Garde d’enfants, jamais sous Médecins et soins. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur ou son jour de natation, apparaissent sous forme de ligne liée à sa page. Une personne est considérée comme votre enfant si la mention **Pour vous** indique un lien de parenté, comme fille ou fils.
- Une facture de l’école, d’un club ou d’un service de garde apparaît sous forme de ligne qui ouvre la tâche correspondante. Le montant reste dans la tâche.
- Chaque e-mail de l’école, d’un club ou d’un service de garde, par exemple au sujet d’une sortie ou d’un changement de programme, apparaît sous forme de ligne datée avec son objet. Tous leurs messages sont ainsi regroupés au même endroit. Touchez la ligne pour ouvrir l’e-mail.
- Votre propre note sur un enfant dans une rubrique, par exemple une note sur Isla sous **École**, reçoit les informations concernant cet enfant.

Les notes Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Pour chaque nouvelle information, votre Machine interroge une fois son IA afin de déterminer si elle concerne vos enfants.

## Fusionner, supprimer et annuler

Dans le menu ⋯, **Fusionner dans…** déplace les lignes d’une note et les notes qui se trouvent dessous vers une autre note. Votre Machine ajoutera ensuite les nouvelles informations à cette note. **Supprimer** supprime une note. Ces deux actions, ainsi que la suppression d’une ligne, affichent **Annuler** pendant quelques instants.

## À ne pas confondre avec les notes de réunion

Les notes de réunion et celles concernant une personne ou une organisation restent à leur emplacement actuel. Les notes présentées ici sont des pages à part entière.
