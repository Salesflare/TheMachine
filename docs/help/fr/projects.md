---
title: Projets
area: graph
summary: Ce qui se passe, repéré dans vos messages ou ajouté manuellement, sur des tableaux avec des étapes comme les transactions dans un CRM.
code: graph.py, crm.py, dashboard.html
order: 4
translated: b42abbf107368175
---
Votre Machine nomme les projets en fonction du contenu de vos messages. Les messages qui semblent liés à un projet s’affichent comme « probablement liés ». Renommer un projet en lui donnant le nom d’un autre projet fusionne les deux. Vous pouvez aussi les gérer manuellement, comme des transactions dans un CRM.

## Ajouter un projet

**Nouveau projet** en haut d’un tableau, **+ Ajouter** sous une étape, **Nouveau projet** en haut de la liste, **+** dans la barre supérieure sur téléphone, ou depuis la page d’une personne ou d’une organisation.

Donnez-lui un nom, un tableau et une étape, une organisation (cherchez dans votre Graph ou **Ajouter** une nouvelle organisation), une valeur, une date de clôture prévue, des personnes et des notes. Les projets de votre Graph dont le nom est similaire s’affichent en premier.

## Modifier, gagner ou perdre un projet

- **Modifier** sur la page d’un projet, ou **Modifier** dans son menu **⋯** sur le tableau (ou appuyez sur E), permet de modifier tous les éléments ci-dessus.
- **Gagné** ou **Perdu**, avec la raison, pour une transaction : un projet avec une valeur ou une date de clôture prévue, ou sur un tableau qui en comporte une. Un projet gagné passe à la dernière étape du tableau, un projet perdu passe à « En suspens » ou « Refusé ». Les autres projets se terminent avec **Fait**. **Rouvrir** annule cette action.
- **Archiver** retire le projet du tableau et des listes. Un nouveau message à son sujet le réaffiche.
- **Supprimer** le retire définitivement. Ses messages et ses personnes sont conservés.

## Description

Une ou deux phrases sous le nom d’un projet pour expliquer de quoi il s’agit et où il en est. Votre Machine la rédige à partir des messages, tâches, promesses, faits et de l’étape du projet, puis la met à jour en cas de changement, par exemple à l’arrivée d’un nouveau message, lors d’un changement d’étape ou quand le projet est gagné ou perdu. Si elle n’a encore rien de précis à dire, aucune description ne s’affiche.

Modifiez-la sous **Description** dans **Modifier** sur la page du projet. Elle vous appartient alors : la mention « Modifié par vous » apparaît et votre Machine n’y touche plus. **La tenir à jour**, sous la description ou dans **Modifier**, lui redonne la main. Si vous enregistrez une description vide, aucune description ne s’affiche.

Pour un projet Work partagé, votre équipe ne voit la description que si tous les éléments sur lesquels elle s’appuie lui ont aussi été partagés. Votre propre modification reste visible uniquement par vous.

## Déplacer un projet

Faites-le glisser vers une autre étape ou, sur téléphone, utilisez **⋯**, puis **Déplacer vers**. Votre déplacement reste en place jusqu’à ce qu’un message plus récent le modifie.

**Étapes**, en haut d’un tableau, permet de choisir les étapes affichées pour chaque tableau. **Effacer** les affiche toutes à nouveau.

« 4 sans réponse depuis plus de 10 jours » sous une étape : appuyez dessus pour afficher uniquement ces projets sur le tableau et dans la liste. Appuyez à nouveau pour tout afficher.

## Scinder un projet

Quand un projet regroupe plusieurs sujets, **Scinder…** dans son menu **⋯** demande à votre Machine de créer deux à quatre projets, chacun avec un nom, une phrase expliquant de quoi il s’agit, et les fils de discussion, tâches et personnes qui lui correspondent. Rien ne change pour le moment : renommez les projets, déplacez des éléments vers une autre partie, laissez-les dans le projet ou retirez-les, puis confirmez.

Les nouveaux projets restent sur le même tableau et à la même étape, et sont partagés avec les mêmes personnes que le projet d’origine, jamais avec plus de personnes. La page indique ensuite en quoi le projet a été scindé, avec **Annuler**, qui rétablit tout comme avant.

## Les tâches d’un projet

Une tâche peut être rattachée à un seul projet. Votre Machine choisit le projet quand son fil de discussion ou les personnes concernées sont liés à un seul projet ouvert. Le nom du projet s’affiche alors sous le titre de la tâche. **Projet** sous **Détails** de la tâche, ou **Rattacher à un projet** dans le menu des commandes (Ctrl K), permet de modifier le projet ou de retirer la tâche du projet. Votre choix est conservé.

La page d’un projet répertorie ses tâches sous **Tâches**, avec les tâches ouvertes en premier. Le tableau indique leur nombre. Rattacher une tâche à un projet partagé ne partage rien de plus : votre équipe ne voit toujours que les éléments issus de messages partagés.

Une fois par semaine, votre Machine recherche les projets sans activité récente : rien de nouveau depuis au moins 10 jours, aucune tâche ouverte et aucune promesse en attente. Pour trois projets au maximum, elle ajoute une tâche avec une prochaine étape précise, comme « Envoyer à Sam le bon de commande signé », liée au message qui lui a permis de la créer. Si aucune étape claire ne se dégage, elle n’ajoute rien. Si vous écartez une suggestion, ce projet ne sera plus proposé pendant quatre semaines.

## L’organisation d’un projet

Chaque projet peut être lié à une organisation. Celle-ci apparaît sur la page du projet, dans la liste et sur le tableau, avec un lien.

Si personne n’en a choisi une, votre Machine la détermine à partir des personnes associées au projet et de ses messages, sans tenir compte de vos collègues. Elle ne le fait que si une organisation correspond clairement à l’autre partie : une adresse e-mail personnelle comme Gmail ne compte jamais, et un projet qui concerne plusieurs entreprises n’a pas d’organisation associée. Le formulaire du projet indique alors « D’après les personnes associées ».

Une vérification compare ensuite l’organisation avec le sujet du projet : si elle correspond uniquement à l’endroit où travaille une personne associée au projet (l’employeur d’un ami qui va à un concert, par exemple), elle est retirée.

Votre choix dans **Modifier** est toujours conservé, même si vous retirez l’organisation. **Même organisation que…** déplace les projets d’une organisation avec celle-ci, et **Séparer** les déplace à nouveau.

## Tableaux

Des projets d’un même type, répartis en étapes, comme un pipeline d’évaluation. **⋯** sur un tableau : **Modifier le tableau** (nom, étapes et projets associés), **Ouvrir sur ce tableau** et **Nouveau tableau**.

Les vérifications ajoutent les projets correspondants et les placent dans une étape. En cas d’incertitude, le tableau indique « 2 projets pourraient correspondre » : **Ajouter** ou **Exclure**. Cochez-en quelques-uns, ou **Tout sélectionner**, pour les traiter en une seule fois. Vous pouvez aussi utiliser **Annuler** juste après si vous changez d’avis. Si un projet regroupe plusieurs interlocuteurs, l’ajouter crée un projet par interlocuteur.

Un nouveau tableau, ou un tableau suggéré que vous enregistrez, parcourt une fois tout votre historique. Il crée un projet pour chaque organisation correspondante et place chacun dans une étape. L’en-tête indique « Parcours de votre historique… » pendant l’opération, puis le nombre de projets ajoutés et le nombre de projets qui attendent votre intervention. Un tableau réservé à vous garde les résultats pour vous uniquement.

**Relances…** dans le menu **⋯** d’un tableau permet de relancer automatiquement une personne qui ne répond pas. Consultez [Relances](follow-ups.md).

## Terminé quand

**Terminé quand**, sous **Modifier** sur n’importe quel projet, qu’il soit sur un tableau ou non, indique en termes simples ce qui permet de le terminer, ainsi que la preuve requise : **Une page en ligne** (The Machine ouvre le lien de leur message et vérifie qu’il renvoie vers vous) ou **Leur message**. Les vérifications proposent une option pour les inscriptions de partenaires.

Une vérification déplace un projet à la dernière étape uniquement si la preuve est fournie, avec un lien vers celle-ci sur sa page. Si le projet n’est sur aucun tableau, il est marqué comme terminé. Vous pouvez utiliser **Annuler** dans son menu **⋯**, sous Modifications récentes.

Si vous modifiez **Terminé quand** et que la preuve d’un projet terminé ne correspond plus, le projet est rouvert. Sa tâche est mise à jour en fonction de la nouvelle condition. Vous pouvez toujours le marquer manuellement comme **Fait** ou **Gagné**. La page indique aussi ce qui bloque le projet (aucune réponse depuis plus de 10 jours, promesse en retard) et ajoute une tâche à ce sujet s’il n’en a pas déjà une. La vérification a lieu chaque jour ouvré, même si aucun nouveau message n’est arrivé. Rien n’est envoyé sans votre accord.

## Pipeline

**Pipeline**, en haut d’un tableau, affiche la valeur totale des projets ouverts pour chaque étape et le montant dont la clôture est prévue chaque mois, selon leur date de clôture. Les projets gagnés, perdus ou en suspens ne sont pas considérés comme ouverts. Le montant des projets gagnés ce mois-ci est affiché séparément.

Les valeurs sont en euros, sauf si votre Machine utilise une autre devise. Avec **Propriétaire** dans Filtrer, seuls vos projets sont pris en compte.

## Le tableau d’un coéquipier

Dans **Équipe**, les tableaux que vos coéquipiers partagent s’affichent à côté des vôtres, en commençant par ceux qui contiennent le plus de vos projets. L’en-tête indique à qui appartient le tableau et avec qui il est partagé : avec toute l’équipe (« Tableau d’Ada, partagé avec l’équipe ») ou uniquement avec les coéquipiers choisis (« Ada a partagé ce tableau avec vous »).

Chaque projet indique la dernière activité et sa date : le dernier élément partagé avec l’équipe, ou son dernier déplacement si celui-ci est plus récent. Sur un tableau qui contient des projets de plusieurs coéquipiers, cette ligne indique aussi à qui appartient le projet (« par Ada »).

Un tableau de coéquipier peut afficher moins de projets que ce qu’il voit lui-même : un projet qu’il a gardé privé, ou qui contient une conversation personnelle, ne quitte jamais sa Machine. Une personne qui est dans ses contacts personnels n’apparaît pas dans les projets partagés. Sur votre propre tableau, l’en-tête indique « Partagé avec l’équipe » et le nombre de projets qui restent visibles uniquement par vous. Ces projets affichent un cadenas.

**Les miens**, **Pour moi** et **Tout** permettent de filtrer le contenu d’un tableau partagé, ainsi que la liste des projets de l’équipe associée. « Les miens » affiche les projets auxquels vous participez : un fil de discussion associé, un projet dont vous êtes propriétaire ou une tâche qui vous appartient et qui concerne le projet. « Pour moi » affiche les projets qui attendent votre intervention : une tâche ouverte à leur sujet ou un fil de discussion dont le dernier message vous était destiné.

Chaque projet s’affiche comme sur le tableau de son propriétaire, dans le même ordre : son organisation, le nombre de jours dans l’étape, la prochaine étape et « Sans réponse depuis N jours ». La prochaine étape ou la raison issue d’un message qui reste privé n’apparaît pas. Le reste d’une étape est regroupé sous **Afficher N de plus**. Rien de tout cela ne change ce qui est partagé.

Sur tous les tableaux, un projet qui porte le même nom que le tableau s’affiche sans le nom du tableau (« Annonces : Acme » s’affiche sous le nom « Acme » sur le tableau Annonces).
