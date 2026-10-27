---
title: Le Graph
area: graph
summary: Les personnes, organisations et projets de vos messages, tenus à jour tout seuls.
covers: tab:people
code: graph.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, enrichment.py, dashboard.html
order: 1
---
Votre Machine dresse une carte des gens avec qui vous traitez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, et tout reste sur votre Machine.

## Personnes

Tous les gens avec qui vous êtes en contact, les plus proches d’abord. La page d’une personne commence par sa photo, son nom, son poste, son organisation et son lieu, puis une ligne sur votre relation (« Vous parlez chaque jour · dernière fois ven. 23 oct. · prochaine réunion mar. 27 oct. »). En dessous :

- **Contact** : ses téléphones et e-mails. Touchez-en un pour appeler ou écrire, ou **Copier** pour le copier.
- **Avec vous** : ce que cette personne est pour vous, contact Travail ou Perso, et votre Famille ou votre Fleet, avec **Voir dans Fleet**.
- **Aussi sur** : les autres endroits où vous lui parlez. **Slack** l’ouvre dans Slack, ou ouvre votre fil Slack le plus récent avec elle.
- Les **Personnes** et **Projets** dont elle fait partie, **En cours entre vous** (les promesses dans les deux sens, avec **Fait** et **Abandonner**), et sa **Chronologie**.

Les adresses et chats d’une personne sont réunis tout seuls quand il est clair qu’il s’agit de la même personne, comme un e-mail pro avec son adresse perso en copie.

Les onglets **Travail** et **Perso** n’affichent que ces contacts-là. **Télécharger le CSV**, dans le menu de tri, enregistre l’onglet ouvert sous forme de tableur, aussi pour Organisations et Projets.

### Chronologie

Chaque page de personne et d’organisation en a une, la plus récente d’abord : e-mails, réunions et leurs résumés Zoom, conversations Intercom (ouvertes ou fermées, avec **Ouvrir dans Intercom**), chats WhatsApp, Slack, LinkedIn et X, tâches, promesses et changements de projet. Les filtres en haut montrent une source à la fois. **Afficher plus** charge les plus anciens.

Les réunions à venir sont à part en haut, sous **À venir**, la plus proche d’abord. **Afficher tout ce qui est à venir** montre le reste. Une réunion présente dans plusieurs de vos agendas n’apparaît qu’une fois.

La chronologie d’une organisation contient les messages de ses membres et les conversations Intercom venant de son domaine. Vos chronologies sont à vous : le Graph de l’équipe ne montre que ce que vos règles de partage autorisent.

Si une page affiche **Impossible de charger cette page.**, appuyez sur **Réessayer**. Si cela continue, utilisez **Un problème ?** en bas de la page.

## Filtrer et trier

**Filtrer**, à côté des onglets dans Personnes, Organisations et Projets, réduit la liste par propriétaire, tag, tableau, étape, organisation, valeur et date de clôture prévue. Les personnes et organisations correspondent à travers leurs projets en cours.

Les filtres choisis s’affichent au-dessus de la liste, avec **Effacer**. Le menu de tri trie aussi par **Valeur** et **Date de clôture**. C’est votre Machine qui filtre, donc les longues listes restent rapides. Sur téléphone, les filtres s’ouvrent dans un panneau.

## Équipe

**Équipe**, à côté de Les miens, montre ce que vos coéquipiers partagent. Il a les mêmes onglets, le même menu de tri et les mêmes boutons **Nouvelle personne** ou **Nouvelle organisation** que Les miens. Ce que vous ajoutez est à vous. **Filtrer** le réduit par la personne qui a partagé, par organisation (Personnes) ou par état (Projets).

## Propriétaire

Dans une Fleet Travail, chaque personne, organisation et projet a un propriétaire : **Propriétaire** sous Avec vous sur sa page. C’est vous, sauf si vous choisissez quelqu’un de votre Fleet Travail. **Les miens**, à côté de Filtrer et sur un tableau, n’affiche que les vôtres. Une carte du tableau affiche le nom de son propriétaire. Chaque changement apparaît dans sa chronologie. Un élément partagé avec votre équipe emporte son propriétaire, selon les mêmes règles de partage que le reste.

## Champs et tags

Sous Champs, sur une personne, une organisation ou un projet, cliquez sur une valeur pour la changer : **Enregistrer** ou Entrée la garde, **Annuler** ou Échap laisse tel quel, **Retirer** la vide. **Gérer les champs** ajoute ou retire des champs : **Nouveau champ** en ajoute un pour tous les éléments de ce type, texte, nombre, date ou choix dans une liste. **Retirer** supprime un champ pour tous.

**+ Tag** ajoute un tag, comme VIP ou partenaire. **×** le retire. Les tags s’affichent dans les listes et **Filtrer** les retrouve. Un élément partagé avec votre équipe emporte ses champs et ses tags.

## Importer un tableur

**Importer un CSV…**, dans le menu de tri de Personnes, Organisations ou Projets, ajoute un tableur enregistré en CSV. Votre Machine devine quelle colonne correspond à quoi d’après les en-têtes et leur contenu. Vous pouvez corriger n’importe laquelle.

Quand votre modèle peut tourner, il vérifie aussi les colonnes, dans n’importe quelle langue et quelle que soit l’orthographe des en-têtes, avec une courte raison là où il a un doute. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire, sur votre Machine, comme pour une revue. Sans lui, la proposition tirée des en-têtes est conservée.

**Vérifier**, à côté des corrections suggérées, liste les corrections simples en avant/après : espaces en trop, noms en majuscules, numéros de téléphone au format international, fautes de frappe dans les e-mails (gmial.com), sites web réduits à leur domaine, dates et valeurs dans n’importe quel format (« €12k » donne 12000), plusieurs tags dans une cellule, une étape écrite autrement que sur le tableau, et la même ligne en double.

Décochez un type de correction ou une seule ligne pour la laisser telle quelle. Rien n’est corrigé sans être coché.

L’aperçu montre chaque ligne comme nouvelle, correspondant à un élément déjà dans votre Graph, ou ignorée, avec la raison. Une correspondance, c’est le même e-mail pour une personne (sinon le même nom dans la même organisation), le même site web ou le même nom pour une organisation, et le même nom pour un projet.

**Importer** ajoute les nouveaux et complète les correspondances. Une cellule vide ne change rien. **Annuler** juste après, ou **Annuler le dernier import** dans le menu de tri, défait le dernier import tant que ces éléments n’ont pas été modifiés depuis. Les corrections faites ensuite sont conservées : si Annuler devait en écraser une, il explique pourquoi au lieu de le faire. Le fichier reste sur votre Machine.

## Une organisation, plusieurs sites web

**⋯**, **Même organisation que…** sur la page d’une organisation l’intègre à une autre, avec ses personnes, projets et notes. **Ajouter un site web…** ajoute un autre de ses sites, comme son .io à côté de son .com : les personnes qui ont une adresse sur ce domaine la rejoignent, et ses informations sont recherchées pour chaque site web.

Ils sont listés sous **Sites web**, chacun avec **Séparer** pour annuler. Les modifications ultérieures de l’organisation réunie sont conservées. Les organisations qui semblent être des doublons apparaissent sous **Même organisation ?** : **Fusionner** ou **Pas la même**.

## Ajouter une personne ou une organisation

**Nouvelle personne** en haut de Personnes, **Nouvelle organisation** en haut d’Organisations, ou, sur téléphone, **+** dans la barre du haut. Donnez un nom, et pour une personne un e-mail et une organisation si vous les avez. Pour une organisation, son site web. Quand un élément similaire est déjà dans votre Graph, le formulaire le montre d’abord, pour que vous puissiez plutôt ouvrir celui-là. **Ajouter** ouvre la nouvelle page.

Une personne que vous ajoutez reste, même sans message pour l’instant. Son premier message la rejoint. Une organisation que vous avez ajoutée peut être supprimée depuis son menu **⋯** tant que personne n’en fait partie.

## À propos de vous

Vos propres adresses et numéros, alias compris, c’est toujours vous, jamais quelqu’un de votre Graph. Vous chercher vous-même, ou ajouter une personne avec une de vos adresses, ouvre **À propos de vous**, et un import ignore votre propre ligne.

À propos de vous liste vos adresses avec leur provenance. Modifiez-les dans **Paramètres**, sous Compte. Une personne créée auparavant à partir de votre propre adresse passe toute seule dans À propos de vous, avec une sauvegarde conservée sur votre Machine.

Pour envoyer votre propre fiche à un coéquipier ou un ami, choisissez **Partager mes coordonnées**. Voir [Partager un contact](share-contact.md).

## Photo

Cliquez sur la photo de la page d’une personne ou d’une organisation pour la changer : **Importer une photo**, choisissez-en une trouvée pour elle, ou **Retirer la photo**. Elle reste sur votre Machine.

## Notes

**Modifier**, sur la page d’une personne ou d’une organisation, contient un champ **Notes**, pour tout ce que vous voulez retenir. Les notes s’affichent sur la page et sont conservées lors des fusions.

## Modifier une personne

**Modifier**, en haut de sa page, change son nom, son poste, son organisation, son lieu, son LinkedIn, ses téléphones et e-mails, ce qu’elle est pour vous, et Travail ou Perso. **Enregistrer** garde les changements, **Annuler** laisse tout comme avant.

Vos modifications restent, même quand ses informations sont recherchées à nouveau ou qu’une revue lit autre chose, et après **Fusionner** et **Annuler**. Videz un champ pour reprendre la valeur trouvée. Un nom vide remet celui tiré de ses messages.

## Même personne ?

Quand deux personnes pourraient n’en faire qu’une, leur page demande s’il s’agit de la même personne, et Personnes les liste sous **Même personne ?**. **Fusionner** les réunit, avec tous leurs messages, notes, rôles et projets. **Pas la même** les garde séparées pour de bon.

**Tout fusionner** fusionne toutes les paires de la liste d’un coup, sauf celles que vous avez marquées **Pas la même**. **Annuler** juste après les sépare toutes à nouveau.

La page d’une personne fusionnée explique pourquoi sous **Fusionné à partir de**. **Annuler** les sépare à nouveau.

Pour réunir vous-même deux personnes, ouvrez l’une d’elles, puis **⋯**, **Même personne que…** et choisissez l’autre.

## Poste et photo

Les personnes qui ont une adresse d’entreprise reçoivent un poste, une photo, un LinkedIn et une ville, recherchés comme les [informations d’organisation](organization-data.md). Sur une Machine hébergée, seuls leur nom et le domaine de leur entreprise sont envoyés. Désactivez-le dans **Paramètres**, sous Sécurité : **Rechercher les contacts pro**.

Vos connexions complètent les informations au fil de leur travail, avec ce qu’elles lisent déjà et sans rien demander de plus : un poste, un téléphone et un fuseau horaire depuis Slack, une bio, un lieu et un site web depuis X, un titre et une photo depuis LinkedIn, et des postes depuis les contacts Google et Salesflare. Ce que la personne dit d’elle-même passe en premier. Survolez la ligne sous son nom pour voir d’où vient l’information. Tout reste sur votre Machine.

Les photos WhatsApp arrivent via votre synchronisation WhatsApp toujours active, quand elle le permet : jusqu’à 50 par jour, seulement pour les personnes déjà dans votre Graph. Rien ne leur est envoyé.

## Supprimer définitivement une personne

Sur sa page, ouvrez le menu ⋯ et choisissez **Supprimer définitivement…**, puis **Supprimer**. Cela la retire, avec ce que votre Machine sait d’elle : sa fiche, ses adresses, les informations trouvées, les messages échangés uniquement entre vous deux et les notes à son sujet. Les tâches qui la concernent restent, sans son nom. Elle ne sera pas ajoutée à nouveau. C’est irréversible.

## Qui est qui

Les rôles que votre Machine a lus dans vos messages, en attente de votre avis. **✓ Correct** en confirme un. **Modifier** ouvre sa page en mode Modifier. Elle apprend de vos modifications. Cette section n’apparaît que quand des rôles sont en attente.

## Dans une Fleet Travail

Le travail client est partagé avec les Machines de vos coéquipiers, et le leur apparaît dans la vôtre. Chaque fil indique **Équipe** ou **Vous seul**. Voir [Graph de l’équipe](team-graph.md).

## Organisations

Des entreprises, tirées des adresses et des noms de vos messages. Voir [Informations d’organisation](organization-data.md).

La page d’une organisation est construite comme celle d’une personne : son logo, son nom et son activité, une ligne sur votre relation, puis **Contact** (son site web et son LinkedIn), **Avec vous** (ce qu’elle est pour vous), les personnes qui y travaillent et sa **Chronologie**.

Ses **Projets** listent d’abord ceux en cours, chacun avec son étape. Leurs changements apparaissent dans sa chronologie. **Modifier**, en haut, change ses informations et ce qu’elle est pour vous. **Demander à la Fleet qui la connaît** trouve un moyen d’entrer en contact via votre Fleet.

Les e-mails des outils de préchauffage d’adresse sont mis de côté, sous « Masqué comme préchauffage », avec **Annuler** par domaine.

## Projets

Nommés par votre Machine d’après le sujet de vos messages. Les signaux qui semblent en faire partie s’affichent comme « En fait probablement partie ». Renommer un projet avec le nom d’un autre projet réunit les deux.

Ou gérez-les à la main, comme des affaires dans un CRM :

- **Nouveau projet** : en haut d’un tableau, **+ Ajouter** sous une étape, **Nouveau projet** en haut de la liste, **+** dans la barre du haut sur téléphone, ou depuis la page d’une personne ou d’une organisation. Donnez-lui un nom, un tableau et une étape, une organisation (cherchez dans votre Graph, ou **Ajouter** une nouvelle), une valeur, une date de clôture prévue, des personnes et des notes. Les projets similaires déjà dans votre Graph s’affichent d’abord.
- **Modifier** sur la page d’un projet, ou **Modifier** dans le **⋯** d’une carte du tableau (ou appuyez sur E sur une carte). Cela change tout ce qui précède.
- **Gagné** ou **Perdu**, avec la raison. Gagné le déplace vers la dernière étape du tableau, Perdu vers Bloqué ou refusé. **Rouvrir** annule.
- **Archiver** le retire du tableau et des listes. Un nouveau message à son sujet le fait revenir. **Supprimer** le retire pour de bon. Ses messages et ses personnes restent.
- Déplacez une carte en la faisant glisser, ou avec **⋯**, **Déplacer vers** sur téléphone. Votre déplacement tient jusqu’à ce qu’un message plus récent la déplace.
- **Étapes**, en haut d’un tableau, n’affiche que les étapes que vous choisissez, par tableau. **Effacer** les affiche toutes à nouveau.

### Les tâches d’un projet

Une tâche peut appartenir à un projet. Votre Machine le choisit quand son fil ou les personnes concernées sont sur un seul projet en cours, et la tâche l’affiche sous forme d’étiquette. Touchez **▾** sur l’étiquette, ou **Mettre dans un projet** dans le menu de commandes (Ctrl K), pour le changer ou le retirer. Votre choix est conservé.

La page d’un projet liste ses tâches sous **Tâches**, celles en cours d’abord, et sa carte sur le tableau indique combien sont en cours. Lier une tâche à un projet partagé ne partage rien de plus : votre équipe ne voit toujours que ce qui vient de messages partagés.

### L’organisation d’un projet

Chaque projet peut être lié à une organisation. Sa page, sa ligne et sa carte sur le tableau l’affichent, avec un lien vers elle.

Quand personne n’en a choisi, votre Machine la définit d’après les personnes du projet et ses messages, en laissant de côté vos collègues. Elle ne le fait que quand une organisation est clairement l’autre partie : un e-mail perso comme Gmail ne compte jamais, et un projet avec plusieurs entreprises reste sans organisation. Le formulaire du projet indique alors « D’après ses contacts ».

Votre choix dans **Modifier** est toujours conservé, même quand vous la retirez. **Même organisation que…** emmène les projets d’une organisation, et **Séparer** les ramène.

### Tableaux

Des projets d’un même type répartis en étapes, comme un pipeline d’évaluation. **⋯** sur un tableau : **Modifier le tableau** (nom, étapes, projets concernés), **Ouvrir sur ce tableau** et **Nouveau tableau**. Les revues continuent d’ajouter les projets qui correspondent et les placent dans une étape. En cas de doute, le tableau affiche « 2 projets pourraient aller ici » : **Ajouter** ou **Exclure**.

Cochez-en quelques-uns, ou **Tout sélectionner**, pour les traiter d’un coup, et **Annuler** juste après si vous changez d’avis. Un projet qui regroupe plusieurs interlocuteurs devient un projet par interlocuteur quand vous l’ajoutez.

**Pipeline**, en haut d’un tableau, additionne la valeur de ses projets en cours par étape, et ce qui devrait se conclure chaque mois d’après leurs dates de clôture. Les projets gagnés, perdus et bloqués ne sont pas en cours. Ce que vous avez gagné ce mois-ci s’affiche à part. Les valeurs sont en euros, sauf si votre Machine utilise une autre devise. **Les miens** ne compte que les vôtres.

Un nouveau tableau, ou un tableau suggéré que vous enregistrez, parcourt une fois tout votre historique. Il trouve les projets et organisations qui correspondent, crée un projet par organisation et place chacun dans une étape. L’en-tête affiche « Parcours de votre historique… » pendant le travail, puis combien de projets ont été ajoutés et combien attendent votre vérification. Un tableau Vous seul garde ce qu’il trouve pour vous seul.

### Le tableau d’un collègue

Dans **Équipe**, les tableaux que vos collègues partagent s’affichent à côté des vôtres, en commençant par ceux qui ont le plus de vos projets. Chaque carte indique ce qui s’est passé en dernier, avec sa date, comme sur le tableau de son propriétaire : la dernière ligne partagée avec l’équipe, sinon son dernier déplacement. Le nom du propriétaire n’apparaît que quand une étape a des cartes de plusieurs collègues ; quand une seule personne possède tout le tableau, l’en-tête le dit.

**Les miens**, **Pour moi** et **Tout** choisissent ce qu’un tableau partagé affiche. Les miens, c’est ce sur quoi vous êtes : un de ses fils, un projet que vous possédez ou avez vous-même, ou une de vos tâches à son sujet. Pour moi, c’est ce qui vous attend : une tâche ouverte à son sujet, ou un fil dont le dernier message vous était adressé.

Le reste d’une étape se replie dans **Afficher N de plus**. Les projets qui se ressemblent, comme une série d’essais « … évaluation CRM », se replient en une ligne avec un nombre ; touchez-la pour les ouvrir. Rien de tout cela ne change ce qui est partagé.

## Une tâche sur quelqu’un

**Nouvelle tâche**, dans le menu **⋯** d’une personne, d’une organisation ou d’un projet, crée une tâche à son sujet.

## Ce qu’on sait de quelqu’un

Sous Ce qu’on sait, chaque information a un menu :

- **Oublier** la supprime partout.
- Pas à son sujet la retire seulement de cette page.
