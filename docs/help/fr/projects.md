---
title: Projets
area: graph
summary: Ce qui se passe dans vos messages ou que vous ajoutez manuellement, organisé sur des tableaux avec des étapes, comme les affaires dans un CRM.
code: graph.py, crm.py, dashboard.html
order: 4
translated: 8ab2cc22d536a168
---
Votre Machine nomme les projets d’après le sujet de vos messages. Les messages qui semblent en faire partie sont indiqués comme « probablement lié ». Si vous renommez un projet avec le nom d’un autre projet, les deux fusionnent. Vous pouvez aussi les gérer manuellement, comme des affaires dans un CRM.

## Ajouter un projet

**Nouveau projet** en haut d’un tableau, **+ Ajouter** sous une étape, **Nouveau projet** en haut de la liste, **+** dans la barre supérieure sur téléphone, ou depuis la page d’une personne ou d’une organisation.

Donnez-lui un nom, un tableau et une étape, une organisation (cherchez dans votre Graph, ou **Ajouter** pour en créer une), une valeur, une date de clôture prévue, des personnes et des notes. Les projets déjà présents dans votre Graph avec un nom similaire s’affichent en premier.

## Modifier, gagner ou perdre un projet

- **Modifier** sur la page d’un projet, ou **Modifier** dans son menu **⋯** sur le tableau (ou appuyez sur E), permet de modifier tous les éléments ci-dessus.
- **Gagné** ou **Perdu**, avec la raison, pour une affaire : il s’agit d’un projet avec une valeur ou une date de clôture prévue, ou situé sur un tableau qui en comporte une. Gagné le déplace à la dernière étape du tableau, Perdu le déplace vers Au point mort ou refusé. Les autres projets se terminent avec **Fait**. **Rouvrir** annule cette action.
- **Archiver** le retire du tableau et des listes. Un nouveau message à son sujet le réactive.
- **Supprimer** le supprime définitivement. Ses messages et ses personnes restent.

## Description

Une ou deux phrases sous le nom du projet indiquent de quoi il s’agit et où il en est. Votre Machine les rédige à partir des messages, des tâches, des promesses, des faits et de l’étape du projet, puis les met à jour en cas de changement, par exemple à la réception d’un nouveau message, lors d’un changement d’étape ou après une victoire ou une défaite. Si rien de précis n’est encore à dire, aucune description ne s’affiche.

Modifiez-la dans **Description**, depuis **Modifier** sur le projet. Elle vous appartient alors : « Modifié par vous », et votre Machine n’y touche plus. **La tenir à jour**, sous la description ou dans **Modifier**, la confie de nouveau à votre Machine. Si vous l’enregistrez vide, aucune description ne s’affiche.

Pour un projet Travail partagé, votre équipe ne voit la description que si elle voit aussi tout ce sur quoi elle s’appuie. La modification que vous avez faite reste privée.

## Déplacer un projet

Faites-le glisser vers une autre étape ou, sur téléphone, utilisez **⋯**, puis **Déplacer vers**. Votre déplacement reste en place jusqu’à ce qu’un message plus récent le fasse changer d’étape.

**Étapes**, en haut d’un tableau, permet de choisir les étapes affichées, tableau par tableau. **Effacer** les affiche toutes de nouveau.

« 4 sans réponse depuis plus de 10 jours » sous une étape : touchez ce texte pour n’afficher que ces projets sur le tableau et dans la liste. Touchez-le de nouveau pour tout afficher.

## Scinder un projet

Quand un projet regroupe plusieurs sujets, **Scinder…** dans son menu **⋯** demande à votre Machine de créer deux à quatre projets, avec chacun un nom, une phrase de description et la répartition des fils de discussion, tâches et personnes. Rien ne change pour l’instant : renommez les projets, déplacez des éléments d’une partie à l’autre, laissez-les sur le projet ou retirez-les, puis confirmez.

Les nouveaux projets restent sur le même tableau et à la même étape, et sont partagés avec les mêmes personnes que le projet d’origine, jamais avec davantage de personnes. La page indique ensuite en quoi le projet a été scindé, avec **Annuler**, qui restaure tout.

## Tâches d’un projet

Une tâche peut appartenir à un seul projet. Votre Machine l’y associe lorsque son fil de discussion ou les personnes concernées appartiennent à un seul projet ouvert. Le nom du projet s’affiche alors sous le titre de la tâche. **Projet**, dans **Détails** de la tâche, ou **Rattacher à un projet** dans le menu des commandes (Ctrl K), permet de modifier cette association ou de la supprimer. Votre choix est conservé.

La page d’un projet affiche ses tâches dans **Tâches**, en commençant par celles qui sont ouvertes. Le tableau indique le nombre de tâches ouvertes. Associer une tâche à un projet partagé ne partage rien de plus : votre équipe ne voit toujours que ce qui provient de messages partagés.

Une fois par semaine, votre Machine recherche les projets inactifs : aucune nouveauté depuis au moins 10 jours, aucune tâche ouverte, aucune promesse. Pour trois projets au maximum, elle ajoute une tâche avec une prochaine étape précise, comme « Envoyer le bon de commande signé à Sam », associée au message dont elle est tirée. Si aucune étape claire ne se dégage, elle n’ajoute rien. Si vous écartez une suggestion, ce projet ne vous sera plus proposé pendant quatre semaines.

## Organisation d’un projet

Chaque projet peut être associé à une seule organisation. Celle-ci s’affiche sur sa page, dans la liste et sur le tableau, avec un lien.

Si personne n’en a choisi une, votre Machine l’associe en fonction des personnes du projet et de ses messages, sans tenir compte de vos collègues. Elle ne le fait que si une organisation est clairement l’autre partie : les adresses e-mail personnelles comme Gmail ne comptent jamais, et un projet qui concerne plusieurs entreprises reste sans organisation. Le formulaire du projet indique alors « D’après ses contacts ».

Elle attend aussi que vous ayez écrit à une personne de cette organisation ou que vous l’ayez rencontrée, pour qu’un e-mail d’un inconnu n’associe jamais son organisation à un projet.

Une vérification compare ensuite l’organisation au sujet du projet : si une organisation est seulement le lieu de travail d’une personne concernée (l’employeur d’un ami pour un concert, par exemple), elle est retirée.

Votre choix dans **Modifier** est toujours conservé, même si vous retirez l’organisation. **Même organisation que…** associe les projets d’une organisation, et **Séparer** les dissocie.

## Tableaux

Des projets de même type, organisés par étape, comme un pipeline d’évaluation. Le menu **⋯** d’un tableau propose **Modifier le tableau** (nom, étapes, projets associés), **Ouvrir sur ce tableau** et **Nouveau tableau**.

Les vérifications ajoutent les projets correspondants et les placent à une étape. En cas de doute, le tableau affiche « 2 projets pourraient être associés ici » : **Ajouter** ou **Exclure**. Cochez quelques projets ou **Tout sélectionner** pour les traiter en une fois. Vous pouvez aussi choisir **Annuler** juste après si vous changez d’avis. Lorsqu’un projet regroupe plusieurs interlocuteurs, il devient un projet par interlocuteur quand vous l’ajoutez.

Un nouveau tableau, ou un tableau suggéré que vous enregistrez, passe une fois en revue tout votre historique. Il crée un projet par organisation correspondante et place chacun à une étape. L’en-tête affiche « Analyse de votre historique… » pendant l’opération, puis indique le nombre de projets ajoutés et ceux qui attendent votre intervention. Un tableau visible par vous seul garde ses résultats privés.

**Relances…** dans le menu **⋯** d’un tableau permet de relancer automatiquement une personne qui ne répond pas. Voir [Relances](follow-ups.md).

## Terminé quand

**Terminé quand**, dans **Modifier** sur n’importe quel projet, avec ou sans tableau, indique en termes simples ce qui permet de le terminer et la preuve à fournir : **Une page en ligne** (The Machine ouvre le lien de leur message et vérifie qu’il renvoie vers vous) ou **Leur message**. Les vérifications proposent une option pour les fiches de partenaires.

Une vérification ne déplace un projet à la dernière étape qu’avec la preuve correspondante, liée sur sa page. Un projet sans tableau est plutôt marqué comme terminé, avec **Annuler** dans son menu **⋯**, sous Modifications récentes.

Si vous modifiez **Terminé quand** plus tard et que la preuve d’un projet terminé ne correspond plus, le projet est rouvert. Sa tâche suit la nouvelle condition. Vous pouvez toujours le marquer **Fait** ou **Gagné** manuellement. La page indique aussi ce qui le bloque (aucune réponse depuis plus de 10 jours, promesse en retard) et ajoute une tâche pour y remédier s’il n’en a pas. La vérification a lieu chaque jour ouvré, même si aucun nouveau message n’est arrivé. Rien n’est envoyé sans votre accord.

## Pipeline

**Pipeline**, en haut d’un tableau, additionne la valeur des projets ouverts à chaque étape et indique les clôtures prévues par mois, selon leurs dates de clôture. Les projets gagnés, perdus ou en suspens ne sont pas ouverts. Le total des projets gagnés ce mois-ci s’affiche séparément.

Les valeurs sont en euros, sauf si votre Machine est configurée dans une autre devise. Avec **Propriétaire** dans Filtrer, seuls vos projets sont comptabilisés.

## Tableau d’un collègue

Dans **Équipe**, les tableaux partagés par vos collègues s’affichent à côté des vôtres. Ceux qui contiennent le plus de vos projets apparaissent en premier. L’en-tête indique à qui appartient le tableau et avec qui il est partagé : toute l’équipe (« Tableau d’Ada, partagé avec l’équipe ») ou uniquement les collègues choisis (« Ada a partagé ce tableau avec vous »).

Chaque projet indique le dernier événement et sa date : la dernière ligne partagée avec l’équipe, ou le dernier déplacement s’il est plus récent. Sur un tableau contenant les projets de plusieurs collègues, cette ligne précise à qui appartient le projet (« par Ada »).

Un tableau de collègue peut contenir moins de projets que ce qu’il voit : un projet qu’il garde privé, ou qui contient une conversation personnelle, ne quitte jamais sa Machine. Une personne classée comme Personnel pour lui n’apparaît pas dans les projets partagés. Sur votre propre tableau, l’en-tête indique « Partagé avec l’équipe » et le nombre de projets qui restent privés. Ces projets affichent un cadenas.

**Les miens**, **M’attend** et **Tout** déterminent les projets affichés sur un tableau partagé et dans la liste des projets de l’équipe. Les miens correspond aux projets qui vous concernent : un fil de discussion, un projet dont vous êtes propriétaire ou une tâche à vous liée au projet. M’attend correspond aux projets qui attendent votre intervention : une tâche ouverte liée au projet ou un fil dont le dernier message vous a été envoyé.

Chaque projet s’affiche comme sur le tableau de son propriétaire, dans le même ordre : son organisation, le nombre de jours dans l’étape, la prochaine étape et « Sans réponse depuis N jours ». Une prochaine étape ou une raison provenant d’un message qui reste privé ne s’affiche pas. Le reste de l’étape est regroupé sous **Afficher N de plus**. Rien de tout cela ne change ce qui est partagé.

Sur tous les tableaux, un projet portant le nom de son tableau s’affiche sans ce nom (« Listings : Acme » devient « Acme » sur Listings).
