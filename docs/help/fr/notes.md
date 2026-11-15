---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a71c5e46042cddd0
---
Une note présente un sujet : un voyage, votre maison, la façon dont les factures sont gérées. Les notes se trouvent dans le Graph, à côté des personnes, des organisations et des projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

Touchez **Nouvelle note** en haut de Notes. Donnez-lui un titre, puis touchez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** ajoute ce que vous souhaitez conserver. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Tapez @ puis quelques lettres d’un nom dans une ligne. Choisissez une personne, une organisation, un projet ou une note dans la liste : son nom apparaît sous forme de lien. La page de l’élément lié affiche **Lié depuis** avec votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, comme Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre les notes qui se trouvent dessous. Pour déplacer une note, touchez **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, permet d’en créer une directement à cet endroit.

En haut de la page d’une note, vous voyez où elle se trouve, par exemple **Notes › Enfants**. Touchez une partie du chemin pour y accéder. Sur téléphone, les notes intermédiaires sont regroupées dans ⋯.

## Notes créées par votre Machine

Votre Machine rédige aussi des notes automatiquement à partir de vos messages et les tient à jour. Chaque ligne indique sa provenance, par exemple qui a envoyé l’e-mail. Touchez-la pour ouvrir le message. Une ligne tirée de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**.

Une réunion ou un rendez-vous de votre calendrier n’apparaît jamais à lui seul dans une note : il reste dans [Calendrier](calendar.md). Son e-mail aussi : l’invitation, les réponses, les mises à jour et les annulations.

**Maison**, **Santé** et **Enfants** n’apparaissent qu’une fois que votre Machine a au moins deux éléments concrets à y ajouter, comme une facture ou une information apprise. Jusque-là, ces catégories ne figurent pas dans la liste. Si elles se retrouvent ensuite vides, elles disparaissent.

Vos modifications sont toujours conservées. Renommez une note, déplacez-la, modifiez ses dates ou une ligne : votre Machine conserve ces changements lorsqu’elle met la note à jour. Supprimez une ligne ou une note, et elle ne réapparaîtra pas. Les notes créées par la suite sur le même sujet seront placées là où vous avez mis la première.

**Revenir à l’original** réaffiche les mots de votre Machine. Si vous modifiez une ligne issue de ce que votre Machine a appris, elle est aussi modifiée sous **Ce que j’ai appris** : il n’y en a qu’une seule version.

## Pages rédigées

Dès qu’une note contient au moins deux lignes issues de vos messages ou de ce que votre Machine a appris, votre Machine rédige le haut de sa page. Elle lit les conversations elles-mêmes, et pas seulement leur sujet :

- Un bref résumé du sujet et de son état d’avancement.
- **Faits clés**, **Décisions**, **Points en suspens** et une **Chronologie**, uniquement lorsqu’il y a des éléments concrets à mentionner.
- Les lignes de la note suivent, numérotées sous **Sources**. Chaque phrase se termine par les numéros des lignes dont elle est tirée. Touchez un numéro pour accéder à la ligne correspondante.

La page est réécrite uniquement lorsque les lignes de la note changent, au maximum environ une fois par jour. Si ses sources ne contiennent aucun élément concret, la page n’apparaît pas : seules les lignes sont affichées. Si vous supprimez une ligne, les informations qui en provenaient uniquement disparaissent aussi de la page. Dans la liste Notes, le début du résumé de chaque page apparaît sous le nom de la note.

Les projets et les organisations ont déjà leur propre page dans le Graph, avec une description en haut. Les conversations qui les concernent sont ajoutées à cette page, et non à une note.

## Notes tirées de vos conversations

Votre Machine lit les conversations en entier et les classe dans la note correspondante : un fil d’e-mails de l’une de vos boîtes mail, un chat dans WhatsApp, Slack, Telegram, LinkedIn ou une autre application connectée, et vos notes de réunion. Les messages d’un chat comptent comme une seule conversation jusqu’à ce que le chat reste inactif pendant deux jours.

- Une conversation à propos d’un projet ou d’une organisation dans votre Graph est ajoutée à sa page, et non à une nouvelle note.
- Une conversation peut être ajoutée à une rubrique de **Maison**, **Santé** ou **Enfants**, à une note que vous avez créée, ou à une note que votre Machine crée dans **Travail**, **Voiture**, **Impôts** ou un autre dossier.
- Votre Machine ne crée une note que pour un sujet qui compte au moins deux conversations, ou pour un sujet au sujet duquel vous avez écrit et qui est clairement toujours d’actualité.
- Chaque ligne correspond à une conversation, de la plus récente à la plus ancienne. Touchez une ligne pour ouvrir la conversation.

Votre Machine envoie à l’IA un court extrait de chaque conversation, sans les réponses citées ni les signatures. Chaque conversation est analysée une seule fois, puis les nouveaux messages qui s’y ajoutent la complètent.

Les e-mails groupés et les chats ne sont jamais ajoutés à une note ni envoyés à l’IA : spam, promotions, newsletters et autres e-mails de listes, notifications sans réponse, bots et canaux de diffusion. Une conversation à laquelle vous avez participé compte quand même, tout comme les e-mails de réservation pour **Voyages** et **Événements**.

La première fois, votre Machine parcourt les trois derniers mois en quelques heures, en dehors de la nuit et uniquement si votre forfait IA a encore de la capacité. Ensuite, elle classe les nouvelles conversations lorsque dix sont en attente, ou lorsqu’une conversation est en attente depuis une demi-journée.

## Voyages

Lorsqu’une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans votre boîte mail, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet figurent dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage indique le code de réservation, le siège et le billet pour chaque ligne, dans l’ordre chronologique, ainsi que ses dates. Dans [Calendrier](calendar.md), il apparaît sous forme de bande couvrant ces jours. Touchez-la pour ouvrir le voyage.

Votre Machine lit les détails de réservation que les compagnies aériennes, les hôtels et les sites de réservation incluent dans leurs e-mails de confirmation. Un e-mail qui ne contient pas ces informations ne crée pas de voyage. Les e-mails de réservation reçus auparavant, pendant la période de [l’historique](history.md) conservé par votre Machine, sont lus en arrière-plan une fois cet historique importé, en commençant par vos boîtes mail personnelles. Une ancienne confirmation lue ultérieurement est ajoutée au voyage déjà créé.

Une réservation modifiée met à jour sa ligne, et une réservation annulée est supprimée. Si toutes les réservations d’un voyage sont annulées, le voyage est également supprimé.

## Événements

Lorsque des billets pour un concert, un match, un festival ou une conférence arrivent dans votre boîte mail, votre Machine ajoute l’événement sous **Événements**, dans une note distincte. Une ligne indique où il a lieu, avec le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement affiche ses dates et apparaît sous forme de bande dans [Calendrier](calendar.md). Touchez-la pour ouvrir la note.

- Chaque ligne indique de qui viennent les billets, par exemple **De la part de Example Tickets**, et ouvre cet e-mail.
- Si une tâche provient de l’e-mail des billets, par exemple pour payer les billets, **Ouvrir la tâche** permet de l’afficher.
- Un événement réservé depuis votre boîte mail professionnelle est classé dans Travail. Sinon, il est classé dans Personnel.

Votre Machine lit les détails des billets que les vendeurs incluent dans leurs e-mails de confirmation, sans utiliser l’IA. Un e-mail qui ne contient pas ces informations ne crée pas d’événement. Une réservation annulée est supprimée. Si tous les billets d’un événement sont annulés, l’événement est également supprimé.

## Maison

Sous **Maison**, votre Machine conserve les informations qu’elle connaît sur votre domicile : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme une facture d’énergie ou d’eau, est ajoutée avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** permet d’afficher la facture elle-même. Le montant et les détails du paiement y restent.
- Un abonnement que vous avez conservé est ajouté et ouvre sa tâche **Abonnements**. Les abonnements que vous avez résiliés ne sont pas répertoriés.
- Les personnes et organismes qui vous écrivent régulièrement au sujet de votre domicile, comme votre fournisseur d’énergie, votre fournisseur d’accès à Internet ou la mairie, sont ajoutés avec la fréquence de leurs messages. Touchez une ligne pour ouvrir leur e-mail le plus récent.
- Les informations que votre Machine a apprises au sujet de votre domicile, comme la marque de votre lave-vaisselle, sont également ajoutées. Si vous les modifiez, elles changent aussi sous **Ce que j’ai appris**.
- Si vous avez votre propre note dans une rubrique, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations à son sujet sont ajoutées à votre note. Votre Machine ne crée pas elle-même de notes de ce type.

Seuls les e-mails, factures et abonnements personnels sont utilisés, et les notes de Maison sont toujours personnelles. Pour chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvelle information apprise, votre Machine interroge son IA une seule fois pour déterminer si cela concerne votre domicile. Pour une facture, elle indique de qui elle vient, jamais son montant.

Vos conversations sont également ajoutées à ces notes, comme indiqué plus haut dans **Notes tirées de vos conversations**.

## Santé

Sous **Santé**, votre Machine conserve les informations qu’elle connaît sur votre santé : **Rendez-vous**, **Résultats des tests**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Une facture d’un médecin, d’un dentiste ou d’une pharmacie est ajoutée sous forme de ligne qui ouvre sa tâche. Le montant y reste.
- Chaque e-mail de votre cabinet médical, d’un hôpital, d’un laboratoire ou de votre assurance santé est ajouté sous forme de ligne datée avec son objet, pour que votre historique se constitue au fil du temps. Touchez la ligne pour ouvrir l’e-mail.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, sont également ajoutées. Si vous les modifiez, elles changent aussi sous **Ce que j’ai appris**.
- Si vous avez votre propre note dans une rubrique, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, les informations à son sujet y sont ajoutées.

Les notes de Santé sont toujours personnelles, même si une facture a été envoyée à votre adresse professionnelle. Pour chaque nouvelle facture ou information apprise, votre Machine interroge son IA une seule fois afin de déterminer si cela concerne votre santé.

## Enfants

Sous **Enfants**, votre Machine conserve les informations qu’elle connaît sur vos enfants : **École**, **Activités**, **Garde d’enfants**, **Médecins et soins** et **Factures et frais**. Une baby-sitter ou une garderie est classée sous Garde d’enfants, jamais sous Médecins et soins. Une rubrique apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur principal ou son jour de natation, sont ajoutées sous forme de ligne liée à sa page. Votre Machine considère une personne comme votre enfant lorsque son champ **Pour vous** l’indique, par exemple « fille » ou « fils ».
- Une facture de l’école, d’un club ou d’un service de garde d’enfants est ajoutée sous forme de ligne qui ouvre sa tâche. Le montant y reste.
- Chaque e-mail de l’école, d’un club ou d’un service de garde d’enfants, par exemple une note concernant une sortie ou un changement de programme, est ajouté sous forme de ligne datée avec son objet. Tout ce qu’ils envoient est ainsi regroupé au même endroit. Touchez une ligne pour ouvrir l’e-mail.
- Si vous avez votre propre note pour un enfant dans une rubrique, par exemple une note sur Isla sous **École**, les informations à son sujet y sont ajoutées.

Les notes d’Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Pour chaque nouvel élément, votre Machine interroge son IA une seule fois afin de déterminer s’il concerne vos enfants.

## Fusionner, supprimer et annuler

**Fusionner dans…** dans le menu ⋯ déplace les lignes d’une note et les notes qu’elle contient dans une autre note. À partir de là, votre Machine ajoute les nouvelles informations à cette note. **Supprimer** efface une note. Ces deux actions affichent **Annuler** pendant un instant, tout comme la suppression d’une ligne.

## Différence avec les notes de réunion

Les notes de réunion et les notes sur une personne ou une organisation restent à leur emplacement initial. Les notes présentées ici sont des pages à part.
