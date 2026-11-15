---
title: Notes
area: graph
summary: Une page claire par sujet, comme un voyage ou votre maison, liée aux personnes et aux projets concernés.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, topic_notes.py, note_writer.py, folder_overview.py, memory_seed.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 1087ac0970878932
---
Une note donne une vue d’ensemble d’un sujet : un voyage, votre maison, la façon dont les factures sont traitées. Les notes se trouvent dans le Graph, à côté des personnes, des organisations et des projets. Elles restent sur votre Machine et ne sont pas partagées avec votre équipe.

## Commencer une note

En haut de Notes, sélectionnez **Nouvelle note**. Donnez-lui un titre, puis sélectionnez **Commencer la note** pour ouvrir sa page. **Ajouter une ligne** permet d’ajouter ce que vous voulez garder. Chaque ligne de texte devient une ligne distincte.

## Lier des personnes, des projets et d’autres notes

Saisissez @ et les premières lettres d’un nom dans une ligne. Choisissez une personne, une organisation, un projet ou une note dans la liste : son nom s’ajoute sous forme de lien. La page de l’élément lié affiche **Lié depuis** et le nom de votre note.

## Notes imbriquées

Une note peut se trouver sous une autre, par exemple Électroménager sous Maison. Notes les affiche sous forme d’arborescence : la flèche à côté d’une note ouvre celles qui se trouvent dessous. Pour déplacer une note, sélectionnez **Modifier**, puis choisissez où la placer sous **Sous**. **Nouvelle note sous celle-ci**, dans le menu ⋯, permet d’en créer une à cet endroit.

En haut de la page d’une note, vous voyez où elle se trouve, par exemple **Notes › Enfants**. Sélectionnez n’importe quelle partie pour y accéder. Sur un téléphone, les notes intermédiaires sont regroupées dans ⋯.

## Notes rédigées par votre Machine

Votre Machine rédige aussi des notes à partir de vos messages et les tient à jour. Chaque ligne indique sa source, par exemple l’expéditeur de l’e-mail. Sélectionnez-la pour ouvrir le message. Une ligne issue de **Ce que j’ai appris** porte la mention **D’après ce que j’ai appris**.

Une réunion ou un rendez-vous de votre calendrier n’apparaît jamais à lui seul dans une note : il reste dans [Calendrier](calendar.md). L’e-mail associé y reste aussi : l’invitation, les réponses, les mises à jour et les annulations.

**Maison**, **Santé** et **Enfants** apparaissent uniquement lorsque votre Machine a au moins deux éléments concrets à y ajouter, comme une facture ou une information qu’elle a apprise. Jusque-là, ces catégories ne figurent pas dans la liste. Si elles se retrouvent ensuite sans contenu, elles disparaissent.

Vos modifications sont toujours conservées. Si vous renommez une note, la déplacez, modifiez ses dates ou une ligne, votre Machine garde ces changements lorsqu’elle met la note à jour. Si vous supprimez une ligne ou une note, elle ne réapparaît pas. Les notes créées plus tard sur le même sujet sont placées au même endroit que la première.

**Revenir à l’original** réaffiche les mots de votre Machine. Modifier une ligne issue de ce que votre Machine a appris la modifie aussi sous **Ce que j’ai appris** : il n’en existe qu’une seule version.

## Pages rédigées

Dès qu’une note contient au moins deux lignes provenant de vos messages ou de ce que votre Machine a appris, votre Machine rédige le haut de sa page. Elle lit les conversations elles-mêmes, pas seulement leur sujet :

- Un bref résumé du sujet et de son état d’avancement.
- **Faits clés**, **Décisions**, **Points en suspens** et une **Chronologie**, uniquement lorsqu’il y a des éléments concrets à ajouter.
- Les lignes de la note suivent, numérotées sous **Sources**. Chaque phrase se termine par les numéros des lignes dont elle provient. Sélectionnez un numéro pour accéder à la ligne correspondante.

La page est réécrite uniquement lorsque les lignes de la note changent, au maximum environ une fois par jour. Si les sources ne contiennent aucun élément concret, la page n’est pas créée : seules les lignes s’affichent. Si vous supprimez une ligne, les éléments de la page qui en provenaient uniquement disparaissent aussi. Dans la liste Notes, le début du résumé de chaque page apparaît sous le nom de la note.

Les projets et les organisations ont déjà leur propre page dans le Graph, avec leur description en haut. Les conversations à leur sujet sont ajoutées à cette page, pas à une note.

## Vues d’ensemble

Une note qui contient d’autres notes, comme **Travail** ou **Maison**, affiche en haut une brève vue d’ensemble dès qu’au moins deux de ces notes contiennent des nouveautés : une ou deux phrases sur ce qui se passe, ainsi que quelques éléments qui ont évolué récemment ou qui arrivent bientôt. Chaque élément se termine par le nom de la note dont il provient. Sélectionnez ce nom pour ouvrir la note.

Cette vue est rédigée à partir des pages et des lignes les plus récentes des notes imbriquées, au maximum une fois par jour et uniquement si elles ont changé. Lorsqu’il n’y a rien de nouveau, aucune vue d’ensemble n’apparaît. Dans la liste Notes, le début de cette vue s’affiche sous le nom du dossier.

## Notes tirées de vos conversations

Votre Machine lit les conversations en entier et les classe dans la note correspondante : les fils d’e-mails de n’importe laquelle de vos boîtes de réception, les chats dans WhatsApp, Slack, Telegram, LinkedIn ou une autre application connectée, ainsi que vos notes de réunion. Les messages d’un chat sont considérés comme une seule conversation jusqu’à ce que le chat reste inactif pendant deux jours.

- Une conversation au sujet d’un projet ou d’une organisation dans votre Graph est ajoutée à sa page, pas à une nouvelle note.
- Une conversation peut être ajoutée à une catégorie de **Maison**, **Santé** ou **Enfants**, à l’une de vos notes, ou à une note créée par votre Machine sous **Travail**, **Voiture**, **Impôts** ou un autre dossier.
- Votre Machine ne crée une note que pour un sujet faisant l’objet d’au moins deux conversations, ou d’une conversation à laquelle vous avez participé et qui se poursuit clairement.
- Chaque ligne correspond à une conversation, de la plus récente à la plus ancienne. Sélectionnez-la pour ouvrir la conversation.

L’IA reçoit un court extrait de chaque conversation, sans les réponses citées ni les signatures. Chaque conversation est analysée une fois. Les nouveaux messages qui s’y ajoutent sont ensuite pris en compte.

Les e-mails et les chats de masse ne sont jamais ajoutés à une note ni envoyés à l’IA : les spams, les promotions, les newsletters et autres e-mails de listes de diffusion, les notifications envoyées depuis une adresse de type « no-reply », les bots et les chaînes de diffusion. Une conversation à laquelle vous avez participé est tout de même prise en compte, tout comme les e-mails de réservation pour **Voyages** et **Événements**.

La première fois, votre Machine parcourt les trois derniers mois en quelques heures, en dehors de la nuit et uniquement si votre forfait IA le permet. Ensuite, elle classe les nouvelles conversations dès qu’il y en a dix en attente, ou qu’une conversation attend depuis une demi-journée.

## Notes tirées de la mémoire OpenClaw

Si vous avez déjà utilisé OpenClaw, votre Machine lit une fois les pages thématiques de son dossier de mémoire, comme une page sur un voyage ou votre santé. Les informations utiles sont ajoutées à la note sur le sujet, ou à une nouvelle note. Chaque ligne indique la page dont elle provient, par exemple **Depuis vos pages mémoire · Lisbon**, avec sa date. Passez le curseur dessus pour voir l’emplacement de cette page.

Votre Machine ne modifie jamais ces pages et ignore les journaux quotidiens, les pages sur l’assistante elle-même et les dossiers marqués comme sensibles ou privés. Elle lit au maximum 80 pages, quelques-unes à la fois, puis ne les relit jamais.

## Voyages

Lorsqu’une réservation de vol, d’hôtel, de train, de bus, de ferry ou de voiture de location arrive dans vos e-mails, votre Machine l’ajoute à un voyage sous **Voyages**. Les réservations d’un même trajet sont regroupées dans un seul voyage : l’aller, l’hôtel et le retour. Le voyage indique le code de réservation, le siège et le billet de chaque ligne, dans l’ordre chronologique, ainsi que ses dates. Dans [Calendrier](calendar.md), il apparaît sous forme d’une seule barre sur ces jours. Sélectionnez-la pour ouvrir le voyage.

Votre Machine lit les détails de réservation fournis par les compagnies aériennes, les hôtels et les sites de réservation dans leurs e-mails de confirmation. Un e-mail qui ne les contient pas ne crée pas de voyage. Les e-mails de réservation antérieurs, datant de l’année couverte par l’[historique](history.md) conservé par votre Machine, sont analysés en arrière-plan une fois cet historique importé, en commençant par vos boîtes de réception personnelles. Si une ancienne confirmation est analysée plus tard, elle est ajoutée au voyage existant.

Une réservation modifiée met à jour la ligne correspondante, et une réservation annulée est supprimée. Si toutes les réservations d’un voyage sont annulées, le voyage est lui aussi supprimé.

## Événements

Lorsque des billets pour un concert, un match, un festival ou une conférence arrivent dans vos e-mails, votre Machine ajoute l’événement sous **Événements**, dans une note distincte. Une ligne indique le lieu, le code de réservation, le siège et le nombre de billets. Une deuxième commande pour le même événement est ajoutée à la même note. Comme un voyage, l’événement affiche ses dates et apparaît sous forme d’une barre dans [Calendrier](calendar.md). Sélectionnez-la pour ouvrir la note.

- Chaque ligne indique l’expéditeur des billets, par exemple **De Example Tickets**, et ouvre l’e-mail correspondant.
- Si une tâche provient de l’e-mail des billets, par exemple pour payer les billets, **Ouvrir la tâche** l’affiche.
- Un événement réservé depuis votre boîte de réception professionnelle est classé dans Travail. Dans les autres cas, il est classé dans Personnel.

Votre Machine lit les détails des billets que les vendeurs indiquent dans leurs e-mails de confirmation, sans utiliser l’IA. Un e-mail qui ne contient pas ces détails ne crée pas d’événement. Une réservation annulée est supprimée. Si tous les billets d’un événement sont annulés, l’événement est lui aussi supprimé.

## Maison

Sous **Maison**, votre Machine conserve les informations qu’elle connaît sur votre logement : **Factures et abonnements**, **Électroménager**, **Réparations et entretien** et **La Maison**. Une catégorie apparaît dès qu’elle contient au moins deux lignes.

- Une facture récurrente, comme celle d’énergie ou d’eau, apparaît avec sa fréquence et la date de la dernière facture. **Ouvrir la tâche** affiche la facture elle-même. Le montant et les détails du paiement restent dans la tâche.
- Un abonnement que vous avez conservé apparaît dans une ligne qui ouvre sa tâche **Abonnements**. Les abonnements annulés ne sont pas affichés.
- Les expéditeurs qui vous écrivent régulièrement au sujet de votre logement, comme votre fournisseur d’énergie, votre fournisseur Internet ou votre mairie, apparaissent avec la fréquence de leurs messages. Sélectionnez une ligne pour ouvrir leur e-mail le plus récent.
- Les informations que votre Machine a apprises sur votre logement, comme la marque de votre lave-vaisselle, apparaissent aussi sous forme de ligne. La modifier la modifie également sous **Ce que j’ai appris**.
- Si vous avez votre propre note dans une catégorie, par exemple une note sur votre lave-vaisselle sous **Électroménager**, les informations qui le concernent sont ajoutées à votre note. Votre Machine ne crée pas ce type de note elle-même.

Seules les factures, les abonnements et les adresses e-mail personnelles sont utilisés, et les notes Maison sont toujours personnelles. Votre Machine demande une fois à son IA, pour chaque nouvelle facture, chaque nouvel abonnement ou chaque nouvel élément appris, de déterminer si cela concerne votre logement. Pour une facture, elle indique l’expéditeur, jamais le montant.

Les conversations sont également ajoutées à ces notes, comme indiqué plus haut dans **Notes tirées de vos conversations**.

## Santé

Sous **Santé**, votre Machine conserve les informations qu’elle connaît sur votre santé : **Rendez-vous**, **Résultats des tests**, **Médecins et soins**, **Médicaments**, **Allergies et problèmes de santé** et **Factures et assurance**. Une catégorie apparaît dès qu’elle contient au moins deux lignes.

- Une facture d’un médecin, d’un dentiste ou d’une pharmacie apparaît dans une ligne qui ouvre la tâche correspondante. Le montant reste dans la tâche.
- Chaque e-mail de votre cabinet médical, d’un hôpital, d’un laboratoire ou de votre assureur santé apparaît sous forme de ligne datée avec son objet. Votre historique se constitue ainsi au fil du temps. Sélectionnez la ligne pour ouvrir l’e-mail.
- Les informations que votre Machine a apprises sur votre santé, comme une allergie, apparaissent aussi sous forme de ligne. La modifier la modifie également sous **Ce que j’ai appris**.
- Votre propre note dans une catégorie, par exemple une note sur votre kinésithérapeute sous **Rendez-vous**, reçoit les informations qui la concernent.

Les notes Santé sont toujours personnelles, même si une facture arrive à votre adresse professionnelle. Votre Machine demande une fois à son IA, pour chaque nouvelle facture ou chaque nouvel élément appris, de déterminer si cela concerne votre santé.

## Enfants

Sous **Enfants**, votre Machine conserve les informations qu’elle connaît sur vos enfants : **École**, **Activités**, **Garde d’enfants**, **Médecins et soins** et **Factures et frais**. Une baby-sitter ou une garderie est classée sous Garde d’enfants, jamais sous Médecins et soins. Une catégorie apparaît dès qu’elle contient au moins deux lignes.

- Les informations que votre Machine a apprises sur votre enfant, comme le nom de son professeur principal ou son jour de natation, apparaissent dans une ligne qui renvoie à sa page. Elle considère qu’une personne est votre enfant lorsque la rubrique **Pour vous** indique ce lien, par exemple fille ou fils.
- Une facture de l’école, d’un club ou d’un service de garde d’enfants apparaît dans une ligne qui ouvre la tâche correspondante. Le montant reste dans la tâche.
- Chaque e-mail de l’école, d’un club ou d’un service de garde d’enfants, par exemple au sujet d’une sortie ou d’un changement de programme, apparaît sous forme de ligne datée avec son objet. Tous leurs messages sont ainsi regroupés au même endroit. Sélectionnez la ligne pour ouvrir l’e-mail.
- Votre propre note pour un enfant dans une catégorie, par exemple une note pour Isla sous **École**, reçoit les informations qui le concernent.

Les notes Enfants sont toujours personnelles, même si l’école écrit à votre adresse professionnelle. Votre Machine demande une fois à son IA, pour chaque nouvel élément, de déterminer s’il concerne vos enfants.

## Fusionner, supprimer et annuler

**Fusionner dans…**, dans le menu ⋯, déplace les lignes d’une note et les notes imbriquées vers une autre note. À partir de là, votre Machine ajoute les nouveaux éléments à cette note. **Supprimer** efface une note. Les deux actions affichent **Annuler** pendant un moment, tout comme la suppression d’une ligne.

## Différence avec les notes de réunion

Les notes de réunion et les notes sur une personne ou une organisation restent à leur emplacement d’origine. Les notes présentées ici sont des pages à part entière.
