---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue seule, à intervalles réguliers, comme un récap du lundi sur vos affaires en cours. Elle ne fait que lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 3b0405616881de74
---
## En créer une

Ouvrez **Routines** dans la barre latérale et dites en une ligne ce qu’elle doit faire et quand : « chaque lundi à 9 h, fais le point sur mes affaires en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Puis appuyez sur **Ajouter**.

Sans horaire indiqué, elle se lance à 8 h. L’heure est celle de votre Machine. Le premier résultat lui donne un nom court.

**Ajouter** commence par lancer un test pour vous montrer le résultat avant que vous décidiez de la garder. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la lance à intervalles réguliers, **Modifier** essaie d’autres mots ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de la page Routines, **Ajouter** active une routine prête à l’emploi. Elle se lance tout de suite une fois, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Trouvailles d’occasion toutes les 3 heures, Abonnements et essais une fois par mois). Sa carte présente son texte comme celui de n’importe quelle routine, et **Modifier** permet de changer ses instructions ou son nom.

Quand vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), une ligne au-dessus de vos tâches indique combien vous en avez reçu et ce que la routine ferait, avec **Activer** et **Non merci**.

Tri du spam est proposé de la même façon quand au moins 5 e-mails ont été déplacés manuellement dans le spam en une semaine. **Activer** l’ajoute comme le fait **Ajouter** ici. Avec **Non merci**, la proposition ne revient plus. Un modèle que vous avez déjà utilisé ne sera jamais proposé de nouveau.

**Tri des newsletters** crée une tâche par espace (travail et personnel) avec les newsletters reçues la veille. Chacune propose **Garder** ou **Se désabonner**. Pour vous désabonner, la routine utilise le lien de désabonnement en un clic de la liste, ou envoie un e-mail de désabonnement depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne sur la page de la liste dans son propre navigateur. Si la page demande une connexion, un captcha ou de faire un choix, vous devez vous en occuper : la ligne l’indique avec **Ouvrir la page de désabonnement**.

Vous préférez ne pas recevoir de tâches pour une liste, mais garder ses e-mails ? Dans le chat de l’un de ses e-mails, dites : « Aucun e-mail de cette liste ne nécessite de tâche ».

Les reçus, commandes et avis de paiement sont exclus. Les e-mails reçus via une adresse de groupe, comme un Google Group, sont répertoriés sous le nom de leur expéditeur et ne vous désabonnent jamais du groupe. Si l’expéditeur n’a pas de fonction de désabonnement, la ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace avec les e-mails d’expéditeurs inconnus qui ressemblent à du spam. Chaque e-mail propose **Spam** ou **Pas du spam**. Outlook déplace les spams dans les courriers indésirables et Gmail les signale comme spam. La routine vérifie les e-mails toutes les heures : les spams sont donc généralement détectés avant que vous les voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Un compte Gmail connecté en lecture seule, comme sur une Machine hébergée, ne peut pas déplacer les e-mails dans le spam. Dans ce cas, **Spam** affiche un lien pour le signaler dans Gmail, et The Machine retient l’expéditeur comme spam. Si aucun compte e-mail n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. Une réponse commençant par « Re: » n’est considérée comme une conversation que dans un fil auquel vous avez participé. Si un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre messagerie, arrive de nouveau, il apparaît dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés dans le spam aident aussi la routine à repérer ceux qui leur ressemblent.

Rien ne change tant que vous ne confirmez pas dans la tâche. Appuyez sur le nom d’un expéditeur pour lire son e-mail : il reste non lu et rien ne change. Dans Tri du spam, les images provenant du Web ne se chargent pas, afin que l’expéditeur ne puisse pas voir que vous avez ouvert son e-mail. Les expéditeurs pour lesquels vous avez déjà fait un choix ne vous sont plus proposés. S’il n’y a pas de newsletters ou de spams à traiter dans la journée, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois votre choix fait pour chaque expéditeur, la tâche indique qu’elle est terminée et affiche **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour, dans une seule tâche, quelques articles de newsletter qui valent la peine d’être lus. Chacun indique en une ligne pourquoi il peut vous intéresser. Appuyez dessus pour lire l’e-mail ou utilisez **Ouvrir dans votre messagerie**. La routine ne prend en compte que les newsletters : jamais les e-mails de personnes, les reçus ou les expéditeurs dont vous vous êtes désabonné, ni les messages que vous avez déjà lus. Si aucun article ne sort du lot, aucune tâche n’est créée.

Elle apprend ce qui vous intéresse en fonction des éléments que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les avoir lus, ainsi que de vos choix **Plus comme ça** et **Moins comme ça** sur chaque sélection. Les sujets qu’elle recherche figurent sur la carte de la routine, sous **Plus de** et **Moins de**. Supprimez un sujet avec × ou ajoutez les vôtres. Les sujets en pointillés ont été détectés automatiquement. Chaque nouveau récap remplace celui qui est ouvert. Il n’envoie jamais de notification.

La routine ne lit que l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose une courte question à votre IA à leur sujet, dans la limite d’un quota quotidien pour réduire les coûts. **Changer le moment** permet de définir son horaire. Dès que vous modifiez ses instructions, elle fonctionne comme n’importe quelle routine basée sur vos propres instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts réguliers. Pour chaque personne, la tâche propose un court message rédigé dans le canal où vous échangez habituellement avec elle, par exemple son chat WhatsApp ou votre fil d’e-mails, et dans sa langue. Le message n’est envoyé que si vous le faites vous-même. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos agendas (les événements d’anniversaire et l’agenda Anniversaires de Google, consultés chaque matin même s’ils ne sont pas synchronisés, ainsi que l’agenda Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday sur une personne dans le Graph. Si aucun anniversaire n’a encore été enregistré, le résultat indique **Aucune information sur les anniversaires pour le moment** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche vous propose de consulter la page des anniversaires Facebook. Appuyez sur **Importer**. The Machine ouvre la page dans son navigateur, fait défiler la page jusqu’à ce que tous les mois soient chargés, puis récupère le nom et l’anniversaire de chaque ami. Elle indique combien de personnes ont été trouvées et lesquelles correspondent à des personnes dans votre Graph, d’après leur prénom et leur nom. Les noms partagés par plusieurs personnes sont ignorés et répertoriés.

Seul **Enregistrer** ajoute les informations sur la page de chaque personne : son anniversaire et sa photo de profil Facebook si elle n’en a pas encore. Un anniversaire ou une photo que vous avez définis restent inchangés, et une photo déjà présente n’est jamais remplacée. Aucune donnée n’est écrite sur Facebook.

La routine ne consulte pas de nouveau les anniversaires d’elle-même : c’est la tâche qui le fait avec **Importer à nouveau**. Le navigateur doit être connecté à Facebook. Si ce n’est pas le cas, appuyez sur **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois connecté, le navigateur consulte la page automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne sont associés à personne dans votre Graph sont comptabilisés, avec quelques noms affichés. **Ajouter … comme contacts personnels** les ajoute tous en une fois, même après avoir appuyé sur Enregistrer : chacun avec son nom et son anniversaire, jamais dans un Fleet Travail. Les personnes dont le nom est déjà associé à quelqu’un dans votre Graph, ou qui étaient associées à quelqu’un que vous avez définitivement supprimé, sont ignorées. Les rappels d’anniversaire ne concernent que les personnes à qui vous écrivez.

**Annuler** dans la tâche supprime exactement ces personnes, même après avoir appuyé sur **Importer à nouveau**.

**Abonnements et essais** consulte vos reçus, factures et avis de renouvellement une fois par mois et regroupe vos abonnements dans une tâche. Pour chacun, elle indique le coût, la date du prochain paiement et signale si un essai se termine ou si le prix augmente. Seuls les abonnements identifiés avec certitude sont affichés. Si aucun n’est détecté, aucune tâche n’est créée.

Choisissez **Garder** ou **Résilier** pour chaque abonnement. La routine ne vous interroge plus sur un abonnement gardé, sauf si son prix change. **Résilier** affiche la page de résiliation ou propose un brouillon demandant la résiliation, qui ne sera envoyé que si vous l’envoyez vous-même. Entre deux exécutions mensuelles, la routine vérifie chaque jour et crée une tâche lorsqu’un essai ou un renouvellement doit être facturé dans les 7 jours.

**Garder le contact** vous rappelle de temps en temps de prendre des nouvelles d’un proche, seulement s’il y a une vraie raison de le faire. Sur sa carte, choisissez les personnes concernées dans une courte liste de personnes avec qui vous échangez vous-même, dans les deux sens et depuis plusieurs mois. Supprimez une personne avec ×.

Un rappel n’est créé que si vous n’avez pas parlé à cette personne depuis bien plus longtemps que d’habitude et qu’il y a quelque chose de précis à lui dire : une nouvelle qu’elle a partagée, une promesse toujours en attente ou un message auquel vous n’avez jamais répondu. Une seule tâche indique la raison et propose un court message rédigé dans le canal où vous échangez habituellement avec cette personne, dans sa langue. Le message n’est envoyé que si vous le faites vous-même. S’il n’y a rien à dire, aucune tâche n’est créée.

La routine envoie au maximum deux rappels par semaine et un par personne par mois, et n’en envoie aucun à quelqu’un avec qui vous avez échangé récemment. **Pas nécessaire** sur un rappel allonge le délai avant le prochain rappel pour cette personne, et chaque fois que vous choisissez cette option, le délai s’allonge encore. La routine n’envoie jamais de notification et reste personnelle : elle n’est jamais partagée avec un Fleet Travail.

**Trouvailles d’occasion** surveille une recherche sur un site de seconde main, comme Marktplaats, Vinted, eBay ou Facebook Marketplace. Lancez une recherche sur le site avec les filtres voulus, copiez l’adresse des résultats et collez-la après avoir appuyé sur **Ajouter**. Vous pouvez ajouter des filtres avec vos propres mots, par exemple « moins de 300, dans un rayon de 30 km, pas “pour pièces” ». Chaque recherche constitue sa propre routine. Ajoutez-en une autre pour surveiller une autre recherche.

Toutes les 3 heures, The Machine ouvre la recherche dans son propre navigateur et repère les annonces qu’elle n’a pas encore vues. Le prix, la distance et les mots que vous avez exclus sont d’abord vérifiés par du code simple.

Chaque nouvelle annonce retenue est ouverte, puis votre IA évalue son état à partir de la photo et de la description, et le vendeur à partir de ses avis, de sa note et de l’ancienneté de son compte. Les annonces intéressantes sont regroupées dans une tâche, chacune avec sa photo, son titre, son prix et une évaluation en une ligne. Appuyez sur une annonce pour l’ouvrir dans le navigateur de The Machine.

Tant que cette tâche est ouverte, les nouvelles trouvailles s’ajoutent en tête de liste, le nombre d’annonces augmente et une nouvelle notification vous est envoyée, car les bonnes affaires partent vite. Marquez la tâche comme faite pour que la prochaine trouvaille crée une nouvelle tâche. Une exécution sans annonce intéressante ne change rien.

La routine reste raisonnable et peu coûteuse : une seule consultation de la recherche par exécution, au maximum 6 annonces ouvertes par exécution avec une pause entre chacune, et au maximum 40 annonces vérifiées par jour pour toutes vos recherches. Chaque vérification consiste en une courte question à votre IA avec une photo. Lors de la première exécution, les quelques annonces les plus récentes sont vérifiées, puis les autres sont considérées comme déjà vues. Les exécutions suivantes ne ramènent donc que les nouvelles annonces.

Si le site vous demande de vous connecter, affiche un test anti-robot ou bloque la consultation, une tâche vous l’indique avec **Ouvrir** pour afficher le site dans le navigateur de The Machine. Connectez-vous ou passez le test vous-même dans ce navigateur. La prochaine exécution consultera de nouveau le site. The Machine ne se connecte jamais à votre place et ne résout jamais les tests pour vous. Elle ne contacte jamais un vendeur, ne fait pas d’offre et n’achète rien.

**Modifier la recherche** sur la carte de la routine permet de remplacer l’adresse ou les filtres. **Changer le moment** permet de définir un autre rythme, par exemple « toutes les 6 heures ».

**Réachats** consulte les confirmations de commande des boutiques en ligne dans votre messagerie et repère les articles que vous achetez régulièrement, comme du café, de la nourriture pour animaux ou des vitamines. Lorsqu’un nouvel achat est probablement nécessaire, la routine crée une tâche qui indique l’article, la boutique, le dernier prix payé et la date de votre dernier achat. **Ouvrir dans la boutique** vous mène à la page de l’article pour que vous puissiez l’acheter vous-même. Rien n’est acheté à votre place.

Il faut au moins trois commandes du même article, à un rythme régulier. Un achat ponctuel ou un délai inhabituel ne crée donc aucune tâche. Pour l’instant, la routine consulte les boutiques qui utilisent Shopify. Votre IA ne lit que les nouveaux e-mails de commande de ces boutiques, avec une courte question par exécution. Ces tâches n’envoient jamais de notification. Une nouvelle commande de l’article clôt la tâche ouverte.

Tant que la routine d’un modèle conserve les instructions du modèle, elle s’exécute avec son propre code, sans utiliser votre forfait d’IA (Tri du spam répertorie d’abord en code les nouveaux e-mails d’expéditeurs inconnus et ne pose une courte question à votre IA que s’il y en a ; Garder le contact interroge votre IA uniquement sur les une ou deux personnes sélectionnées). Un nouveau nom ne change rien à cela. Dès que vous modifiez les instructions, la routine fonctionne comme n’importe quelle routine basée sur vos propres instructions.

Tri des newsletters et Tri du spam créent toujours une seule tâche avec un choix pour chaque e-mail. Si vous modifiez Anniversaires, la routine affiche son résultat et au maximum un brouillon, au lieu d’une tâche par personne. Dans **Modifier**, **Revenir au modèle** rétablit les instructions du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit ce dont elle a besoin, par exemple vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme une exécution réussie.

Les routines ne font que lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Elles ouvrent les pages trouvées dans ce qu’elles lisent ou dans une recherche, les adresses de pages simples et les sites connus, mais jamais une adresse inventée pour transporter ce qu’elles ont lu. Seul un modèle modifie les e-mails, et uniquement ce que vous confirmez dans sa tâche.

Quand une routine doit publier un message ou en envoyer un, elle s’arrête juste avant cette étape et affiche le brouillon, par exemple **Publication prévue sur X :**. Après une exécution réelle, le brouillon apparaît sous forme de tâche à approuver. Une exécution de test l’affiche simplement.

Son nom indique le sujet et l’endroit où le résultat sera publié, et **Depuis votre routine**, en dessous, ouvre la routine. Le bouton indique l’étape à effectuer, par exemple **Préparer une publication** : cette action prépare le contenu, mais ne publie rien. Vous le publiez à partir du résultat. Si The Machine ne peut pas le publier à votre place, le bouton du résultat ouvre la page où vous pouvez le faire.

La tâche apparaît d’abord dans l’espace du compte utilisé pour l’envoi, par exemple Travail pour le compte X de votre entreprise. Vous n’avez donc jamais à la déplacer.

Une exécution peut suivre vos [compétences](skills.md) activées, sélectionnées en fonction de la tâche de la routine. Seules les compétences pertinentes sont lues en entier. Le résultat les indique sous **Utilisées :**. Une compétence ne fait jamais envoyer de message ni modifier quoi que ce soit par une routine.

Vos routines se trouvent sous **Vos routines**, après les suggestions éventuelles. Un long résultat est réduit à un court aperçu. Appuyez sur **Afficher plus** ou sur l’aperçu pour l’ouvrir.

Chaque exécution connaît le résultat précédent et peut donc indiquer ce qui a changé depuis.

Après une exécution réussie, votre Machine peut créer une recette pour automatiser les étapes de lecture identiques à chaque fois, par exemple les e-mails ou les changements GitHub à consulter. Lors des exécutions suivantes, ces étapes sont d’abord effectuées avec du code simple. L’IA sélectionne ensuite les informations pertinentes et les rédige, en utilisant moins de jetons. Une recette ne fait que lire. Si elle ne fonctionne plus, la routine s’exécute normalement et corrige la recette. Vous la trouverez sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une fois. Chaque date donne lieu à une seule exécution, même après un redémarrage.

Les routines s’exécutent l’une après l’autre et attendent lorsque le quota de votre forfait d’IA est bas, comme tous les travaux en arrière-plan. **Lancer maintenant** démarre la routine tout de suite. Son résultat s’affiche sur la carte dès qu’il est prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et ce qu’elle fait. Son horaire et ses résultats restent inchangés. **Changer le moment** permet de définir un nouveau rythme avec vos propres mots, par exemple « tous les jours de la semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur ordinateur, Échap ou un clic à l’extérieur annule également les changements.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles instructions et affiche le résultat. La routine ne change pas tant que vous n’avez pas appuyé sur **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous appuyiez sur **Reprendre** sur la carte. Les routines en pause apparaissent sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne sont pas lancées ensuite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Quand vous utilisez **Demander des modifications** sur la tâche d’une routine ou que vous écrivez dans son chat, votre remarque peut concerner toutes les exécutions, par exemple « ne jamais utiliser d’émoji ». La tâche propose alors **Modifier aussi la routine**, sur la tâche et dans son chat, sous la réponse. Les changements apportés aux instructions de la routine sont affichés. La routine ne change que si vous appuyez sur **Modifier**. **Laisser ainsi** conserve les instructions actuelles. Une correction qui ne concerne que le brouillon n’entraîne aucune proposition.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez la routine avec vos propres mots et votre Machine se charge du reste.

Les utilisateurs avancés peuvent aussi exécuter leurs propres commandes sur leur Machine. Dans le menu ⋯, choisissez **Avancé : étapes de script**. **Modifier** affiche les étapes uniquement si la routine en contient. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel si le champ est vide), pendant la durée maximale indiquée en secondes. Le résultat affiché par la commande est transmis à la routine. Si les instructions sont vides, ce résultat constitue le résultat de la routine.

**Vérification** reçoit le résultat de la routine en entrée. Si elle se termine avec une erreur, le résultat indique **N’a pas marché** et affiche le message de la vérification. Une commande Récupérer les données qui échoue affiche le même message.

Une commande doit tenir sur une seule ligne et s’exécute sans shell : pas de tubes ni de variables. Les étapes de script vous appartiennent et ne sont définies que sur votre tableau de bord. Une exécution de test et **Essayer** exécutent aussi Récupérer les données et l’indiquent. Elles n’envoient toujours rien et ne conservent rien. Une routine n’envoie jamais rien : les étapes de script doivent donc uniquement lire.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit (sans jamais les modifier) et propose celles qui conviennent sous forme de routines, sous **Suggérée**. Chaque tâche a été exécutée une fois, ce qui vous permet de voir un vrai résultat.

La routine conserve vos corrections et exclut les éléments qu’une tâche a envoyés ou publiés. Si une tâche a exécuté un script ou lu les données recueillies par un script, celui-ci est ajouté à Récupérer les données. **Ajouter** crée une routine, et **Non merci** empêche toute nouvelle proposition pour cette tâche. Une tâche qui vous rappelait de faire quelque chose est plutôt proposée comme tâche récurrente dans la page Tâches.

Avant d’ajouter une suggestion, vous pouvez la modifier comme n’importe quelle routine avec **Modifier** et **Changer le moment** dans son menu ⋯. **Relancer** l’exécute tout de suite avec ses instructions actuelles pour afficher des résultats plus récents, par exemple après un week-end calme. Elle ne fait que lire, s’exécute une fois par appui et son nouveau résultat remplace l’ancien.

Trois suggestions au maximum peuvent être en attente à la fois. Après une semaine d’exécutions réussies, la routine demande **Désactiver l’ancienne tâche OpenClaw ?**. L’ancienne tâche est désactivée uniquement si vous appuyez sur **Désactiver**. Vous pouvez la réactiver dans OpenClaw. **Garder** laisse les deux tâches en cours.

## À partir de vos habitudes

Votre Machine repère aussi les tâches que vous effectuez régulièrement et les propose sous forme de routines, sous **Suggérée**, même sans OpenClaw. Elle recherche notamment :

- la même demande formulée au moins trois fois de suite, par exemple « fais le point sur les tickets de support ouverts » chaque lundi ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et des e-mails d’actualité reçus chaque semaine ;
- un canal Slack très actif où d’autres personnes écrivent chaque semaine ;
- des e-mails que vous transférez un par un à la même personne, comme les e-mails de l’école ou du club que vous transférez à votre partenaire : un récap hebdomadaire lui évite de devoir les transférer ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion indique ce qu’elle a repéré, par exemple « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines », et a été exécutée une fois pour vous présenter un vrai résultat. Vous pouvez par exemple créer un récap d’équipe, un résumé avant une réunion hebdomadaire, un récap du support ou du développement, un aperçu de vos chiffres ou un récap des newsletters que vous recevez.

La routine ne propose que des tâches propres à votre activité et clairement utiles : un récap d’actualités ne porte que sur vos propres newsletters, jamais sur des actualités générales. Si rien ne convient, aucune suggestion n’est proposée.

Elle vérifie vos habitudes une fois par jour au maximum et propose au plus une nouvelle routine par semaine, sans notification. **Non merci** empêche une suggestion de réapparaître. Les transferts et les réponses restent associés au compte utilisé pour les envoyer. Travail et Personnel ne sont donc jamais mélangés. Tout reste sur votre Machine. Une tâche que vous fermez régulièrement est plutôt proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue seule et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « chaque vendredi, indique-moi quelles affaires n’ont pas bougé ».
