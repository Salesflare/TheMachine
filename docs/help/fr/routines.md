---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue seule, à intervalles réguliers, comme un récap de vos affaires en cours le lundi. Elle fait uniquement de la lecture.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 57b97c44b031845f
---
## En créer une

Ouvrez **Routines** dans la barre latérale, puis indiquez en une ligne ce qu’elle doit faire et quand : « chaque lundi à 9 h, récapitule mes affaires en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Appuyez ensuite sur **Ajouter**.

Sans horaire précisé, elle s’exécute à 8 h. L’heure est celle de votre Machine. Son premier résultat lui donne un nom court.

**Ajouter** lance d’abord un test pour vous montrer le résultat avant que vous la gardiez. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la fait tourner à intervalles réguliers, **Modifier** essaie d’autres mots ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de Routines, **Ajouter** active une routine prête à l’emploi. Elle s’exécute immédiatement, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Trouvailles d’occasion toutes les 3 heures, Abonnements et essais une fois par mois). Sa carte affiche ses instructions comme pour n’importe quelle routine. **Modifier** permet de changer ses instructions ou son nom.

Quand vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), une ligne apparaît au-dessus de vos tâches. Elle indique le nombre de newsletters reçues et ce que la routine ferait, avec les options **Activer** et **Non merci**.

Tri du spam est proposé de la même manière lorsque 5 e-mails ou plus ont été déplacés manuellement dans le spam en une semaine. **Activer** l’ajoute comme le ferait **Ajouter** ici. **Non merci** signifie que la proposition ne réapparaîtra pas. Les modèles que vous avez déjà eus ne sont jamais proposés à nouveau.

**Tri des newsletters** crée une tâche par espace (travail et personnel) avec les newsletters reçues la veille. Chaque e-mail propose **Garder** ou **Se désabonner**. Le désabonnement utilise le lien en un clic de la liste ou, si l’envoi est activé, l’e-mail de désabonnement envoyé depuis votre adresse. Sinon, The Machine se désabonne sur la page de la liste, dans son propre navigateur. Si la page demande une connexion, un captcha ou des choix, vous devez vous en occuper. La ligne indique pourquoi, avec **Ouvrir la page de désabonnement**.

Vous préférez ne pas créer de tâches à partir d’une liste, tout en continuant à recevoir ses e-mails ? Écrivez « Cette liste ne contient rien qui nécessite une tâche » dans le chat de l’un de ces e-mails.

Les reçus, commandes et avis de paiement sont exclus. Les e-mails provenant d’une adresse de groupe, comme un groupe Google, sont classés sous le nom de leur auteur et ne vous désabonnent jamais du groupe. Si l’expéditeur ne propose pas de désabonnement, la ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace avec les e-mails d’expéditeurs inconnus qui ressemblent à du spam. Chaque e-mail propose **Spam** ou **Pas du spam**. Outlook déplace les spams dans les courriers indésirables et Gmail les signale comme spam. La routine vérifie les e-mails toutes les heures, le spam est donc généralement détecté avant que vous ne le voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Gmail connecté en lecture seule, comme sur une Machine hébergée, ne peut pas déplacer les e-mails dans le spam. Dans ce cas, **Spam** affiche un lien pour le signaler dans Gmail, et The Machine mémorise l’expéditeur comme spam. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. Un « Re: » ne compte comme une conversation que dans un fil auquel vous avez participé. Si un e-mail provenant d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre messagerie, arrive à nouveau, il figure dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez déplacés vous-même dans le spam aident aussi la routine à repérer les messages similaires.

Rien ne change tant que vous ne confirmez pas votre choix dans la tâche. Appuyez sur le nom d’un expéditeur pour lire l’e-mail d’abord : il reste non lu et rien ne change. Dans Tri du spam, les images provenant du Web ne se chargent pas. L’expéditeur ne peut donc pas savoir que vous avez ouvert l’e-mail. Les expéditeurs pour lesquels vous avez fait un choix ne vous sont plus proposés. Si aucun e-mail n’arrive pendant une journée, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois que vous avez fait un choix pour chaque expéditeur, la tâche indique qu’elle est terminée et propose **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour les quelques articles de newsletters qui méritent votre attention et les réunit dans une tâche. Une phrase explique pourquoi chacun vous intéresse. Appuyez sur un article pour lire l’e-mail ou utilisez **Ouvrir dans votre messagerie**. Seules les newsletters sont incluses, jamais les e-mails de personnes, les reçus ou les expéditeurs dont vous vous êtes désabonné, ni les e-mails que vous avez déjà lus. Si rien ne sort du lot, aucune tâche n’est créée.

La routine apprend ce qui vous intéresse en fonction des e-mails que vous ouvrez, que vous mettez en favori ou que vous archivez sans les lire, ainsi que des options **Plus comme ça** et **Moins comme ça** de chaque sélection. Les sujets qu’elle choisit figurent sur la carte de la routine, sous **Plus de** et **Moins de**. Supprimez un sujet avec × ou ajoutez les vôtres. Les sujets en pointillés ont été appris par la routine. Un nouveau récap remplace celui qui est ouvert. Aucune notification n’est envoyée.

La routine ne lit que l’expéditeur, l’objet et le début de chaque nouvelle newsletter. Elle pose une courte question à votre IA à leur sujet, dans la limite d’un quota quotidien, pour réduire les coûts. **Changer le moment** permet de définir l’heure. Si vous modifiez ses instructions, elle fonctionne comme n’importe quelle routine avec vos propres instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts réguliers. Une courte formule de vœux est rédigée dans l’espace où vous échangez habituellement avec cette personne, comme son chat WhatsApp ou votre fil de discussion par e-mail, dans sa langue. Elle est envoyée uniquement si vous l’envoyez. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos agendas (les événements d’anniversaire et l’agenda Anniversaires de Google, lus chaque matin même s’ils ne sont pas synchronisés, ainsi que l’agenda Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday sur une personne du Graph. Si aucune source ne contient encore d’anniversaire, le résultat indique **Aucune information sur les anniversaires** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche propose de lire la page des anniversaires de Facebook. Appuyez sur **Importer**. The Machine ouvre la page dans son navigateur, fait défiler la page jusqu’à ce que tous les mois soient chargés, puis lit le nom et l’anniversaire de chaque ami. Elle indique combien d’anniversaires ont été trouvés et quelles personnes correspondent à des contacts de votre Graph selon leur prénom et leur nom. Les noms correspondant à plusieurs personnes sont ignorés et répertoriés.

Seule l’option **Enregistrer** les ajoute, sur la page de chaque personne : son anniversaire et sa photo de profil Facebook si elle n’a pas encore de photo. Les anniversaires et photos que vous avez déjà ajoutés restent inchangés, et une photo existante n’est jamais remplacée. Aucune information n’est écrite sur Facebook.

La routine ne relit pas la page automatiquement. Pour le faire, utilisez **Importer à nouveau** dans la tâche. Le navigateur doit être connecté à Facebook. Sinon, appuyez sur **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois connecté, la page est lue automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent dans aucun Graph sont comptabilisés, avec quelques noms. **Ajouter … comme contacts personnels** les ajoute tous en une fois, y compris après avoir utilisé Enregistrer. Chaque contact est ajouté avec son nom et son anniversaire, et n’est jamais partagé avec une Fleet Travail. Les personnes dont le nom figure déjà dans votre Graph ou que vous avez supprimées définitivement sont ignorées. Les rappels d’anniversaire ne concernent toujours que les personnes à qui vous écrivez.

**Annuler** dans la tâche supprime précisément ces personnes, même après avoir utilisé **Importer à nouveau**.

**Abonnements et essais** lit une fois par mois vos reçus, factures et avis de renouvellement, puis réunit vos abonnements dans une tâche. Elle indique le prix de chacun, sa prochaine date de prélèvement et signale la fin d’un essai ou une hausse de prix. Seuls les abonnements identifiés avec certitude sont affichés. Si rien n’est trouvé, aucune tâche n’est créée.

Pour chaque abonnement, choisissez **Garder** ou **Résilier**. Un abonnement conservé ne vous est plus proposé, sauf si son prix change. **Résilier** affiche la page de résiliation ou un brouillon de message demandant la résiliation, qui ne sera envoyé que si vous l’envoyez. Entre deux exécutions, la routine vérifie chaque jour les essais et les renouvellements dont le prélèvement aura lieu dans les 7 jours et crée une tâche le cas échéant.

**Garder le contact** vous rappelle de temps en temps de reprendre contact avec un proche, uniquement s’il y a une bonne raison de le faire. Sur sa carte, choisissez les personnes concernées dans une courte liste de contacts avec qui vous échangez vous-même dans les deux sens depuis plusieurs mois. Supprimez une personne avec ×.

La routine vous relance uniquement si cela fait beaucoup plus longtemps que d’habitude que vous n’avez pas parlé à la personne et s’il y a quelque chose de précis à lui dire : une nouvelle qu’elle vous a annoncée, y compris dans le récap de sa page, une promesse toujours en attente ou un message auquel vous n’avez jamais répondu.

Si une nouvelle concerne une date à venir, comme un déménagement le mois prochain, la routine la vérifie de nouveau juste après cette date, en tenant compte des messages les plus récents. Elle crée une tâche avec la raison et un court message rédigé dans l’espace où vous échangez habituellement avec cette personne, dans sa langue. Le message est envoyé uniquement si vous l’envoyez. Si vous n’avez rien à dire, aucune tâche n’est créée.

La routine envoie au maximum deux relances par semaine, une par personne et par mois, et aucune à une personne avec qui vous avez échangé récemment. **Pas nécessaire** sur une relance retarde la prochaine pour cette personne, et chaque choix de ce type la retarde davantage. Aucune notification n’est envoyée. La routine reste personnelle : elle n’est jamais partagée avec une Fleet Travail et ne s’appuie jamais sur les informations reçues dans vos comptes professionnels.

**Trouvailles d’occasion** surveille une recherche sur un site de seconde main comme Marktplaats, Vinted, eBay ou Facebook Marketplace. Lancez une recherche avec les filtres souhaités, copiez l’adresse des résultats et collez-la après avoir appuyé sur **Ajouter**. Vous pouvez préciser les filtres en langage courant, par exemple « moins de 300, à moins de 30 km, pas de “pour pièces” ». Chaque recherche constitue une routine distincte. Ajoutez-en une autre pour en lancer une nouvelle.

Toutes les 3 heures, la routine ouvre la recherche dans le navigateur de The Machine et repère les annonces qu’elle n’a pas encore vues. Le prix, la distance et les termes à exclure sont d’abord vérifiés avec du code simple.

Chaque nouvelle annonce retenue est ouverte. Votre IA évalue l’état de l’article à partir de la photo et de la description, et celui du vendeur à partir de ses avis, de sa note et de l’ancienneté de son compte. Les bonnes annonces sont regroupées dans une tâche, chacune avec sa photo, son titre, son prix et une brève évaluation. Appuyez sur une annonce pour l’ouvrir dans le navigateur de The Machine.

Tant que la tâche est ouverte, les nouvelles trouvailles s’ajoutent en haut de la liste, le nombre augmente et vous recevez une nouvelle notification, car les bonnes affaires partent vite. Marquez la tâche comme faite pour que la trouvaille suivante en crée une nouvelle. Si une exécution ne trouve rien d’intéressant, rien ne change.

La routine reste raisonnable et peu coûteuse : une seule lecture de la recherche par exécution, au maximum 6 annonces ouvertes par exécution avec une pause entre chacune, et au maximum 40 annonces vérifiées par jour pour l’ensemble de vos recherches. Chaque vérification consiste en une courte question à votre IA accompagnée d’une photo. Lors de la première exécution, la routine vérifie les annonces les plus récentes et marque les autres comme déjà vues. Les exécutions suivantes ne récupèrent donc que les nouveautés.

Si le site vous demande de vous connecter, affiche une vérification anti-robot ou bloque la lecture, une tâche vous l’indique et propose **Ouvrir** pour afficher la page dans le navigateur de The Machine. Connectez-vous ou effectuez la vérification vous-même dans le navigateur. La lecture reprendra à la prochaine exécution. The Machine ne se connecte jamais à votre place et ne résout jamais de vérification pour vous. Elle ne contacte jamais de vendeur, ne fait jamais d’offre et n’achète jamais rien.

**Modifier la recherche** sur la carte de la routine permet de changer l’adresse ou les filtres. **Changer le moment** permet de choisir un autre rythme, comme « toutes les 6 heures ».

**Réachats** repère dans vos e-mails les confirmations de commande des boutiques en ligne et détecte les articles que vous achetez régulièrement, comme le café, la nourriture pour animaux ou les vitamines. Lorsqu’un nouvel achat est probablement nécessaire, la routine crée une tâche avec l’article, la boutique, le dernier prix et la date du dernier achat. **Ouvrir dans la boutique** affiche la page de l’article pour que vous puissiez l’acheter vous-même. Rien n’est acheté à votre place.

Il faut au moins trois commandes du même article à intervalles réguliers. Un achat ponctuel ou un intervalle inhabituel ne crée donc aucune tâche. Pour l’instant, la routine lit les e-mails des boutiques qui utilisent Shopify. Votre IA ne lit que les nouveaux e-mails de commande de ces boutiques, au moyen d’une courte question par exécution. Ces tâches n’envoient jamais de notification. Commander à nouveau l’article clôt la tâche en cours.

Tant que les instructions d’une routine de modèle n’ont pas été modifiées, elle s’exécute avec son propre code, sans utiliser votre forfait IA. Tri du spam répertorie d’abord en code les nouveaux e-mails d’expéditeurs inconnus, puis ne pose une courte question à votre IA que s’il y en a. Garder le contact pose des questions uniquement sur les une ou deux personnes sélectionnées. Si vous modifiez ses instructions, la routine fonctionne comme n’importe quelle routine avec vos propres instructions.

Tri des newsletters et Tri du spam créent toujours une tâche unique avec un choix pour chaque e-mail. Si vous modifiez Anniversaires, la routine affiche son résultat et au maximum un brouillon, et ne crée pas une tâche par personne. **Revenir au modèle**, dans **Modifier**, rétablit les instructions du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit ce dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** avec une explication, ou **N’a pas marché** avec une explication. Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme une exécution terminée.

Les routines font uniquement de la lecture : elles peuvent consulter vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Elles ouvrent les pages repérées dans les éléments consultés ou lors d’une recherche, les adresses de pages simples et les sites connus. Elles n’ouvrent jamais une adresse inventée pour y transmettre ce qu’elles ont lu. Seul un modèle peut modifier des e-mails, et uniquement ce que vous confirmez dans sa tâche.

Lorsqu’une routine doit publier un message ou en envoyer un, elle effectue toutes les étapes précédentes, puis affiche le brouillon, par exemple **Publication à venir sur X :**. Après une véritable exécution, le brouillon apparaît dans une tâche à approuver. Un test affiche uniquement le brouillon.

Son nom indique le sujet et l’endroit où il sera publié. L’option **Depuis votre routine**, en dessous, permet d’ouvrir la routine. Le bouton indique l’étape à effectuer, par exemple **Préparer une publication** : il prépare le contenu sans rien publier. Publiez-le depuis le résultat. Si The Machine ne peut pas le publier pour vous, le bouton ouvre la page où vous pourrez le faire.

La tâche apparaît d’abord dans l’espace du compte utilisé pour l’envoi, par exemple Travail pour le compte X de votre entreprise. Elle ne vous demande donc jamais de la déplacer.

Une routine peut suivre vos [compétences](skills.md) activées, choisies en fonction de ce qu’elle fait. Seules les compétences pertinentes sont lues en entier. Le résultat les répertorie sous **Utilisées :**. Une compétence ne fait jamais envoyer ou modifier quoi que ce soit à une routine.

Vos routines figurent sous **Vos routines**, après les suggestions éventuelles. Les longs résultats sont réduits à un aperçu. **Afficher plus**, ou un appui sur le résultat, permet de l’ouvrir.

Chaque exécution tient compte du résultat précédent et peut donc indiquer les changements survenus depuis.

Après une exécution réussie, votre Machine peut créer automatiquement une recette pour les lectures qui se répètent, comme les e-mails ou les changements GitHub à vérifier. Les exécutions suivantes commencent par lire ces éléments avec du code simple. L’IA sélectionne ensuite les informations pertinentes et les rédige avec moins de tokens. Une recette ne fait que lire. Si elle cesse de fonctionner, la routine reprend la lecture automatiquement et corrige le problème. La recette apparaît sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une fois. Chaque date donne lieu à une seule exécution, même après un redémarrage.

Les routines s’exécutent l’une après l’autre et attendent lorsque le quota de votre forfait IA est faible, comme tous les travaux en arrière-plan. **Lancer maintenant** lance la routine immédiatement. Le résultat apparaît sur sa carte une fois prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et son fonctionnement. Son horaire et ses résultats restent inchangés. **Changer le moment** permet de choisir un autre rythme en langage courant, comme « chaque jour de semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur un ordinateur, la touche Échap ou un clic à l’extérieur permet aussi d’annuler.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles instructions et affiche le résultat. La routine ne change pas tant que vous n’appuyez pas sur **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous appuyiez sur **Reprendre** sur la carte. Les routines en pause figurent sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne sont pas lancées par la suite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Lorsque vous utilisez **Demander des modifications** dans la tâche d’une routine, ou que vous lui écrivez dans le chat avec une remarque qui s’applique à chaque exécution, comme « ne jamais utiliser d’émojis », la tâche propose **Modifier aussi la routine**. Cette option apparaît dans la tâche et dans son chat, sous la réponse. Elle indique les changements prévus dans les instructions de la routine. La routine ne change que si vous appuyez sur **Modifier**. **Laisser ainsi** la laisse inchangée. Une correction qui concerne uniquement ce brouillon ne donne lieu à aucune proposition.

## Avancé : étapes de script

Aucun script n’est nécessaire. Décrivez simplement avec vos propres mots ce qu’une routine doit faire, et votre Machine s’occupe du reste.

Pour les utilisateurs avancés, une routine peut aussi exécuter vos propres commandes sur votre Machine. Dans le menu ⋯, choisissez **Avancé : étapes de script**. **Modifier** affiche les étapes uniquement si la routine en contient. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel si aucun dossier n’est indiqué), pendant la durée maximale définie en secondes. La sortie de la commande est transmise à la routine. Si aucune instruction n’est indiquée, la sortie devient le résultat.

**Vérification** reçoit le résultat en entrée après l’exécution. Si elle se termine avec une erreur, la routine affiche **N’a pas marché** et indique le message de vérification. Une commande Récupérer les données qui échoue affiche le même message.

Une commande doit tenir sur une seule ligne et s’exécute sans shell : pas de pipes ni de variables. Les étapes de script sont les vôtres et ne sont définies que sur votre tableau de bord. Un test et une exécution avec **Essayer** lancent aussi Récupérer les données et l’indiquent. Ils n’envoient ni n’enregistrent rien. Une routine n’envoie jamais rien, les étapes de script doivent donc se limiter à la lecture.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit sans jamais les modifier et vous propose celles qui peuvent devenir des routines, sous **Suggérée**. Chacune a déjà été exécutée une fois : vous pouvez donc consulter un vrai résultat.

La routine conserve les corrections apportées à la tâche et ignore ce qu’elle a envoyé ou publié. Si la tâche exécutait un script ou lisait les données collectées par un script, celui-ci est ajouté comme étape Récupérer les données. **Ajouter** crée une routine. **Non merci** signifie que la tâche ne sera plus proposée. Les tâches qui vous rappelaient de faire quelque chose sont plutôt proposées sous forme de tâches récurrentes dans la section Tâches.

Avant d’ajouter une suggestion, les options **Modifier** et **Changer le moment** de son menu ⋯ permettent de la modifier comme n’importe quelle routine. **Relancer** l’exécute avec ses instructions actuelles pour afficher des résultats plus récents, par exemple après un week-end calme. La routine ne fait que lire, s’exécute une fois par appui et remplace l’ancien résultat par le nouveau.

Trois suggestions au maximum peuvent être en attente à la fois. Après une semaine d’exécutions réussies, la routine demande **Désactiver l’ancienne tâche OpenClaw ?**. Elle ne sera désactivée que si vous appuyez sur **Désactiver**. Vous pourrez la réactiver dans OpenClaw. **Garder** laisse les deux tâches actives.

## En fonction de votre activité

Votre Machine repère aussi les activités que vous effectuez régulièrement et vous les propose sous forme de routines dans **Suggérée**, même sans OpenClaw. Elle repère :

- une même demande formulée au moins trois fois de suite, comme « récapitule les tickets d’assistance en cours » chaque lundi ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- les newsletters et les e-mails d’actualité reçus chaque semaine ;
- un canal Slack très actif où d’autres personnes écrivent chaque semaine ;
- les e-mails que vous transférez un par un à la même personne, comme ceux de l’école ou d’un club que vous transférez à votre partenaire : un récap hebdomadaire lui évite d’avoir à les transférer ;
- une même demande à laquelle vous répondez régulièrement, comme une validation mensuelle pour la même personne.

Chaque suggestion explique ce qu’elle a repéré, par exemple « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines », et a déjà été exécutée une fois pour vous montrer un vrai résultat. Pensez au récap d’équipe, au résumé avant un appel hebdomadaire, au récap de l’assistance ou du développement, au suivi de vos chiffres ou au récap des newsletters reçues.

La routine ne suggère que ce qui vous concerne directement et peut réellement vous être utile : un récap d’actualités porte uniquement sur vos propres newsletters, jamais sur un contenu générique. Si rien ne correspond, aucune suggestion n’est faite.

La routine vérifie votre activité au maximum une fois par jour et propose au maximum une nouvelle suggestion par semaine, sans notification. **Non merci** empêche définitivement la suggestion de réapparaître. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés. Les espaces Travail et Personnel ne sont donc pas mélangés. Tout reste sur votre Machine. Une tâche que vous terminez régulièrement est plutôt proposée sous forme de tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue seule et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « me dire chaque vendredi quelles affaires n’avancent plus ».
