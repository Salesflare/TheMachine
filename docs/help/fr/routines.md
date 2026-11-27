---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue toute seule, à intervalles réguliers, comme le récap du lundi sur vos affaires en cours. Elle se contente de lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: 6d74cb93df1bf494
---
## En créer une

Ouvrez **Routines** dans la barre latérale et indiquez en une ligne ce qu’elle doit faire et quand : « tous les lundis à 9 h, récapitule mes affaires en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Puis appuyez sur **Ajouter**.

Sans heure précisée, elle s’exécute à 8 h. L’heure est celle de votre Machine. Lors de sa première exécution, elle reçoit un nom court.

**Ajouter** commence par lancer un test pour vous montrer le résultat avant de conserver la routine. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la fait s’exécuter à intervalles réguliers, **Modifier** essaie d’autres mots ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de la page Routines, **Ajouter** active une routine prête à l’emploi. Elle s’exécute une fois tout de suite, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Trouvailles d’occasion toutes les 3 heures, Abonnements et essais une fois par mois). Sa carte affiche ses instructions comme celles de n’importe quelle routine. **Modifier** permet de changer ses instructions ou son nom.

Si vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (25 ou plus en une semaine, envoyées par au moins 5 expéditeurs), une ligne au-dessus de vos tâches indique leur nombre et ce que la routine ferait, avec **Activer** et **Non merci**.

Tri du spam est proposé de la même façon si au moins 5 e-mails ont été déplacés manuellement dans le dossier Spam en une semaine. **Activer** l’ajoute comme le fait **Ajouter** ici. **Non merci** signifie que la suggestion ne sera plus proposée. Un modèle que vous avez déjà utilisé ne sera jamais proposé.

**Tri des newsletters** crée une tâche par espace, travail et personnel, avec les newsletters de la journée écoulée. Pour chacune, vous pouvez choisir **Garder** ou **Se désabonner**. Le désabonnement utilise le lien de désabonnement en un clic de la liste, ou envoie un e-mail de désabonnement depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne sur la page de la liste, dans son propre navigateur. Si vous devez vous connecter, passer un captcha ou faire un choix, la ligne vous indique pourquoi, avec **Ouvrir la page de désabonnement**.

Vous voulez seulement éviter de créer des tâches à partir d’une liste tout en continuant à recevoir ses e-mails ? Dans le chat de l’un de ses e-mails, dites « Rien de cette liste ne nécessite de tâche ».

Les reçus, les commandes et les avis de paiement sont exclus. Les e-mails envoyés via une adresse de groupe, comme un Google Group, sont associés à leur expéditeur et ne vous désabonnent jamais du groupe. Si l’expéditeur n’a pas de procédure de désabonnement, la ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace avec les e-mails d’expéditeurs inconnus qui semblent être du spam. Pour chacun, choisissez **Spam** ou **Pas du spam**. Outlook déplace les spams dans le dossier Courrier indésirable et Gmail les signale comme spam. La routine vérifie les e-mails toutes les heures. Les spams sont donc généralement détectés avant que vous ne les voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Un compte Gmail connecté en lecture seule, comme sur une Machine hébergée, ne peut pas déplacer les e-mails dans le dossier Spam. Dans ce cas, **Spam** affiche un lien pour le signaler dans Gmail, et The Machine mémorise que l’expéditeur est considéré comme du spam. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. Un « Re: » ne compte comme une conversation que dans un fil auquel vous avez participé. Si un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte de réception, arrive de nouveau, il apparaît dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés dans le dossier Spam aident aussi la routine à repérer les e-mails similaires.

Rien ne change tant que vous ne confirmez pas votre choix dans la tâche. Appuyez sur un expéditeur pour lire son e-mail : il reste non lu et rien ne change. Dans Tri du spam, les images provenant du Web ne se chargent pas, donc l’expéditeur ne peut pas savoir que vous avez ouvert l’e-mail. La routine ne vous demande plus votre avis sur les expéditeurs pour lesquels vous avez déjà fait un choix. Si une journée ne comporte ni newsletter ni spam, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois que vous avez fait un choix pour chaque expéditeur, la tâche indique qu’elle est terminée et affiche **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour les quelques articles de newsletter qui méritent votre attention, dans une seule tâche. Pour chacun, une courte phrase explique pourquoi il peut vous intéresser. Appuyez dessus pour lire l’e-mail ou choisissez **Ouvrir dans votre messagerie**. La routine ne prend en compte que les newsletters, jamais les e-mails de personnes, les reçus ou les expéditeurs dont vous vous êtes désabonné. Elle exclut aussi les e-mails que vous avez déjà lus. Si aucun article ne se démarque, aucune tâche n’est créée.

La routine apprend ce qui vous intéresse à partir des e-mails que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les lire, ainsi qu’avec **Plus comme ça** et **Moins comme ça** sur chaque sélection. Les sujets qu’elle sélectionne apparaissent sur la carte de la routine, sous **Plus de** et **Moins de**. Supprimez-en un avec × ou ajoutez les vôtres. Les sujets en pointillés ont été appris par la routine. Un nouveau récap remplace celui qui est ouvert. La routine n’envoie jamais de notification.

Elle lit uniquement l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose une courte question à votre IA à leur sujet, dans la limite d’un nombre quotidien, pour réduire les coûts. **Changer le moment** permet de choisir l’heure. Une fois ses instructions modifiées, la routine s’exécute comme n’importe quelle routine avec vos instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts réguliers. Chaque tâche contient un court message de vœux rédigé là où vous échangez habituellement avec la personne, par exemple dans son chat WhatsApp ou votre fil d’e-mails, dans sa langue. Le message est envoyé uniquement quand vous l’envoyez. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos agendas (les événements d’anniversaire et l’agenda Anniversaires de Google, lus chaque matin même s’ils ne sont pas synchronisés, ainsi que l’agenda Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday sur une personne dans le Graph. Si aucun anniversaire n’a encore été trouvé, le résultat indique **Aucune info sur les anniversaires** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche propose de lire la page des anniversaires Facebook. Appuyez sur **Importer**. The Machine ouvre la page dans son navigateur, fait défiler la page jusqu’à ce que tous les mois soient chargés, puis lit le nom et la date d’anniversaire de chaque ami. Elle indique le nombre d’anniversaires trouvés et les personnes qui correspondent, par leur prénom et leur nom, à des personnes de votre Graph. Les noms associés à plusieurs personnes sont ignorés et répertoriés.

Seul le bouton **Enregistrer** les ajoute, sur la page de chaque personne : la date d’anniversaire et, si la personne n’a pas encore de photo, sa photo de profil Facebook. Les anniversaires et les photos que vous avez déjà ajoutés sont conservés. Une photo déjà présente n’est jamais remplacée. Aucune information n’est écrite sur Facebook.

La routine ne relit pas la page automatiquement : **Importer à nouveau** dans la tâche permet de le faire. Le navigateur doit être connecté à Facebook. Sinon, appuyez sur **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois connecté, la routine lit la page toute seule. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent dans aucun Graph sont comptabilisés, avec quelques noms affichés. **Ajouter … comme contacts personnels** les ajoute tous en une fois, même après avoir appuyé sur Enregistrer : chaque personne est ajoutée avec son nom et sa date d’anniversaire, sans jamais être partagée avec un Fleet Travail. Les personnes dont le nom figure déjà dans votre Graph ou que vous avez supprimées définitivement sont ignorées. Les rappels d’anniversaire ne concernent que les personnes à qui vous écrivez.

Le bouton **Annuler** de la tâche supprime exactement ces personnes, même après avoir utilisé **Importer à nouveau**.

**Abonnements et essais** lit vos reçus, factures et avis de renouvellement une fois par mois, puis rassemble vos abonnements dans une tâche : leur prix, la date du prochain prélèvement et un indicateur si un essai se termine ou si le prix augmente. Seuls les abonnements identifiés avec certitude sont affichés. Si rien n’est trouvé, aucune tâche n’est créée.

Pour chaque abonnement, choisissez **Garder** ou **Résilier**. La routine ne vous demande plus votre avis sur un abonnement conservé, sauf si son prix change. **Résilier** affiche la page de résiliation ou un brouillon de message demandant la résiliation. Le message est envoyé uniquement quand vous l’envoyez. Entre deux exécutions, la routine vérifie chaque jour et crée une tâche si un essai ou un renouvellement est prévu dans les 7 jours.

**Garder le contact** vous rappelle de temps en temps de reprendre contact avec un proche, uniquement quand il y a une bonne raison de le faire. Sur sa carte, choisissez les personnes à inclure dans une courte liste de personnes avec qui vous échangez vous-même, dans les deux sens, depuis plusieurs mois. Supprimez une personne avec ×.

La routine vous relance uniquement si vous n’avez pas parlé à cette personne depuis bien plus longtemps que d’habitude et qu’il y a quelque chose de précis à lui dire : une nouvelle qu’elle vous a annoncée, y compris dans le récap de sa page, une promesse en attente ou un message auquel vous n’avez jamais répondu.

Si une nouvelle concerne une date à venir, comme un déménagement le mois prochain, la routine la réexamine juste après cette date, avec les derniers messages de la personne. Elle crée une seule tâche qui indique la raison et contient un court message rédigé là où vous échangez habituellement avec cette personne, dans sa langue. Le message est envoyé uniquement quand vous l’envoyez. Si vous n’avez rien à dire, aucune tâche n’est créée.

La routine envoie au maximum deux relances par semaine, une par personne et par mois, et aucune à une personne avec qui vous avez parlé récemment. **Pas nécessaire** sur une relance fait attendre plus longtemps avant de vous relancer pour cette personne. Ce délai s’allonge à chaque fois.

La routine n’envoie jamais de notification et reste personnelle : elle n’est jamais partagée avec un Fleet Travail, ne s’appuie jamais sur des informations professionnelles (ce qui arrive dans vos comptes Travail, ou une promesse ou un fait lié au travail) et rédige les messages dans une conversation hors du travail si vous en avez une.

**Trouvailles d’occasion** surveille une recherche sur un site de seconde main, comme Marktplaats, Vinted, eBay ou Facebook Marketplace. Lancez une recherche sur le site avec les filtres souhaités, copiez l’adresse des résultats et collez-la après avoir appuyé sur **Ajouter**. Si vous le souhaitez, ajoutez des filtres en précisant vos critères, par exemple « moins de 300, à moins de 30 km, pas “pour pièces” ». Chaque recherche est une routine distincte. Ajoutez-en donc une autre pour lancer une nouvelle recherche.

Toutes les 3 heures, la routine ouvre la recherche dans le navigateur de The Machine et repère les annonces qu’elle n’a pas encore vues. Le prix, la distance et les mots que vous avez exclus sont d’abord vérifiés par un code simple.

Chaque nouvelle annonce qui passe ces vérifications est ouverte. Votre IA évalue son état à partir de la photo et de la description, ainsi que le vendeur à partir de ses avis, de sa note et de l’ancienneté de son compte. Les annonces intéressantes sont rassemblées dans une tâche, chacune avec sa photo, son titre, son prix et un verdict en une ligne. Appuyez sur une annonce pour l’ouvrir dans le navigateur de The Machine.

Tant que la tâche est ouverte, les nouvelles trouvailles s’ajoutent en haut de la liste, le nombre augmente et la routine vous envoie une nouvelle notification, car les bonnes affaires partent vite. Marquez la tâche comme faite pour que la prochaine trouvaille commence une nouvelle tâche. Une exécution sans annonce intéressante ne change rien.

La routine reste discrète et peu coûteuse : une seule lecture de la recherche par exécution, au maximum 6 annonces ouvertes par exécution avec une pause entre chacune, et au maximum 40 annonces vérifiées par jour pour l’ensemble de vos recherches. Chaque vérification correspond à une courte question posée à votre IA avec une photo. La première exécution vérifie les quelques annonces les plus récentes et marque les autres comme vues. Les exécutions suivantes ne rapportent donc que les nouveautés.

Si le site vous demande de vous connecter, affiche une vérification anti-robot ou bloque la lecture, une tâche vous l’indique avec **Ouvrir** pour voir la page dans le navigateur de The Machine. Connectez-vous ou passez la vérification vous-même. La prochaine exécution relira la page. The Machine ne se connecte jamais à votre place, ne passe jamais une vérification à votre place et ne contacte jamais de vendeur, ne fait jamais d’offre et n’achète jamais rien.

**Modifier la recherche** sur la carte de la routine permet de changer l’adresse ou les filtres. **Changer le moment** permet de modifier la fréquence, par exemple « toutes les 6 heures ».

**Réachats** lit les confirmations de commande des boutiques en ligne dans vos e-mails et repère les produits que vous achetez régulièrement, comme du café, de la nourriture pour animaux ou des vitamines. Quand vous êtes susceptible d’en avoir bientôt besoin, la routine crée une tâche avec le produit, la boutique, le dernier prix payé et la date du dernier achat. **Ouvrir dans la boutique** vous mène à la page du produit pour que vous puissiez l’acheter vous-même. Rien n’est acheté à votre place.

La routine a besoin d’au moins trois commandes du même produit passées à intervalles réguliers. Un achat isolé ou un intervalle inhabituel ne crée donc aucune tâche. Pour le moment, elle lit les boutiques qui utilisent Shopify. Votre IA ne lit que les nouveaux e-mails de commande de ces boutiques, dans une courte question par exécution. Ces tâches n’envoient jamais de notification. Une nouvelle commande du produit clôt la tâche ouverte.

Tant que la routine d’un modèle conserve les instructions du modèle, elle s’exécute avec son propre code, sans utiliser votre forfait IA (Tri du spam liste d’abord en code les nouveaux e-mails d’expéditeurs inconnus et ne pose une courte question à votre IA que s’il y en a ; Garder le contact pose des questions uniquement sur les une ou deux personnes sélectionnées). Un nouveau nom ne change rien à cela. Une fois ses instructions modifiées, la routine s’exécute comme n’importe quelle routine avec vos instructions.

Tri des newsletters et Tri du spam créent toujours une seule tâche avec un choix pour chaque e-mail. Une routine Anniversaires modifiée affiche son résultat et au maximum un brouillon, au lieu de créer une tâche par personne. **Revenir au modèle** dans **Modifier** rétablit les instructions du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit les informations dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** avec une explication, ou **N’a pas marché** avec une explication. Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme une réussite.

Les routines se contentent de lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient aucun message, ne répondent pas, ne publient rien et ne modifient rien. Elles ouvrent des pages repérées dans ce qu’elles ont lu ou dans une recherche, des adresses de pages simples et des sites connus, mais jamais une adresse créée pour transmettre ce qu’elles ont lu. Seul un modèle peut modifier des e-mails, et uniquement ce que vous confirmez dans sa tâche.

Quand la tâche d’une routine doit se terminer par une publication ou un message, elle effectue tout jusqu’à cette étape et affiche le brouillon, par exemple **Publication à venir sur X :**. Après une exécution réelle, le brouillon vous est proposé dans une tâche à approuver. Une exécution de test affiche seulement le brouillon.

Son nom indique le sujet et l’endroit où le résultat sera publié. **Depuis votre routine** sous le nom ouvre la routine. Le bouton indique l’étape à effectuer, par exemple **Préparer une publication** : il prépare le contenu sans rien publier. Vous pouvez le publier depuis le résultat. Si The Machine ne peut pas le publier à votre place, le bouton ouvre la page où vous pouvez le faire.

La tâche est créée dans l’espace du compte depuis lequel le contenu sera envoyé, par exemple Travail pour le compte X de votre entreprise. Elle ne vous demandera donc jamais de la déplacer.

Une exécution peut suivre vos [compétences](skills.md) activées, sélectionnées en fonction de la tâche de la routine. Seules celles qui sont pertinentes sont lues en entier. Le résultat les répertorie sous **Utilisées :**. Une compétence ne permet jamais à une routine d’envoyer ou de modifier quoi que ce soit.

Vos routines apparaissent sous **Vos routines**, en dessous des suggestions. Les résultats longs sont réduits à un aperçu. **Afficher plus**, ou un appui sur le résultat, permet de l’ouvrir.

Chaque exécution connaît le dernier résultat et peut donc indiquer ce qui a changé depuis.

Après une exécution réussie, votre Machine peut créer elle-même une recette pour les lectures identiques à chaque exécution, par exemple les e-mails ou les modifications GitHub à consulter. Les exécutions suivantes commencent par ces lectures, effectuées avec un code simple. L’IA sélectionne uniquement les éléments importants et rédige le résultat, avec moins de jetons. Une recette se contente de lire. Si elle cesse de fonctionner, l’exécution reprend la lecture toute seule et corrige la recette. Celle-ci apparaît sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une fois. Chaque date ne donne lieu qu’à une seule exécution, même après un redémarrage.

Les routines s’exécutent une par une et attendent si l’utilisation de votre forfait IA est faible, comme pour toutes les tâches en arrière-plan. **Lancer maintenant** démarre la routine tout de suite. Le résultat s’affiche sur la carte dès qu’il est prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et ce qu’elle fait. Sa fréquence et ses résultats restent inchangés. **Changer le moment** permet de définir une nouvelle fréquence avec vos propres mots, par exemple « tous les jours de la semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur un ordinateur, vous pouvez aussi annuler en appuyant sur Échap ou en cliquant à l’extérieur.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles instructions et affiche le résultat. La routine reste inchangée tant que vous n’avez pas appuyé sur **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous choisissiez **Reprendre** sur la carte. Les routines en pause apparaissent sous **En pause**, sous vos routines. Les exécutions manquées pendant la pause ne seront pas lancées ensuite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Quand vous choisissez **Demander des modifications** dans la tâche d’une routine ou que vous écrivez dans son chat, et que votre remarque concerne toutes les exécutions, par exemple « n’utilise jamais d’emoji », la tâche vous propose **Modifier aussi la routine**. Cette option apparaît dans la tâche et dans son chat, sous la réponse. Elle indique les changements apportés aux instructions de la routine. La routine ne change que lorsque vous appuyez sur **Modifier**. **Laisser ainsi** ne change rien. Une correction qui concerne uniquement le brouillon ne donne lieu à aucune proposition.

## Avancé : étapes de script

Pas besoin de script : décrivez ce que la routine doit faire avec vos propres mots et votre Machine s’occupe du reste.

Pour les utilisateurs avancés, une routine peut aussi exécuter vos propres commandes sur votre Machine. Dans le menu ⋯, choisissez **Avancé : étapes de script**. **Modifier** affiche les étapes uniquement si la routine en contient déjà. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel s’il n’est pas précisé), pendant le nombre de secondes indiqué au maximum. Ce que la commande affiche est transmis à l’exécution, qui peut l’utiliser. Si aucune instruction n’est fournie, le résultat de la commande est affiché comme résultat de la routine.

**Vérification** reçoit le résultat en entrée après l’exécution. Si la commande se termine sur une erreur, la routine affiche **N’a pas marché** avec le message de la vérification. Une commande Récupérer les données qui échoue affiche le même message.

Une commande tient sur une ligne et s’exécute sans shell : pas de tube ni de variable. Vous êtes seul responsable des étapes de script, configurées uniquement sur votre tableau de bord. Une exécution de test ou **Essayer** exécute également Récupérer les données et l’indique. Rien n’est envoyé ni conservé. Une routine n’envoie jamais rien, donc une étape de script ne devrait faire que lire.

## À partir de vos tâches OpenClaw

Si vous avez créé des tâches planifiées dans OpenClaw, votre Machine les lit, sans jamais les modifier, et propose celles qui peuvent devenir des routines sous **Suggérée**. Chacune a été exécutée une fois. Vous pouvez donc voir un résultat réel.

La routine conserve vos corrections apportées à la tâche et exclut ce qu’elle a envoyé ou publié. Si une tâche exécutait un script ou lisait des données recueillies par un script, ces éléments sont repris dans Récupérer les données. **Ajouter** en fait une routine. **Non merci** permet de ne plus vous proposer cette tâche. Une tâche qui vous rappelait de faire quelque chose est plutôt proposée comme tâche récurrente sur la page Tâches.

Avant d’ajouter une suggestion, vous pouvez la modifier comme n’importe quelle routine avec **Modifier** ou **Changer le moment** dans le menu ⋯. **Relancer** l’exécute avec ses instructions actuelles pour afficher des résultats plus récents, par exemple après un week-end tranquille. Elle se contente de lire, s’exécute une fois par appui, et son nouveau résultat remplace l’ancien.

Vous pouvez avoir au maximum trois suggestions en attente. Après une semaine d’exécutions réussies, la routine vous demande **Désactiver l’ancienne tâche OpenClaw ?**. Elle est désactivée uniquement si vous appuyez sur **Désactiver**. Vous pouvez la réactiver dans OpenClaw. **Garder** laisse les deux tâches actives.

## À partir de vos habitudes

Votre Machine repère aussi les tâches que vous effectuez régulièrement et les propose comme routines sous **Suggérée**, même si vous n’utilisez pas OpenClaw. Elle repère :

- la même demande effectuée au moins trois fois de suite, comme « récapitule les tickets d’assistance ouverts » tous les lundis ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- les newsletters et les e-mails d’actualité reçus chaque semaine ;
- un canal Slack très actif auquel d’autres personnes écrivent chaque semaine ;
- les e-mails que vous transférez un par un à la même personne, comme ceux de l’école ou d’une association que vous envoyez à votre partenaire : un récap hebdomadaire lui évite de les transférer ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion indique ce que la routine a repéré, comme « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a déjà été exécutée une fois, vous pouvez donc voir un résultat réel. Pensez à un récap d’équipe, à un briefing avant un appel hebdomadaire, à un résumé de l’assistance ou du développement, à un suivi de vos chiffres ou à un récap des newsletters que vous recevez.

La routine propose uniquement des suggestions qui vous concernent directement et sont clairement utiles : un récap d’actualités ne porte que sur vos newsletters, jamais sur des actualités générales. Si rien ne correspond, aucune suggestion n’est proposée.

La routine vérifie vos habitudes au maximum une fois par jour et ajoute au maximum une suggestion par semaine, sans vous envoyer de notification. **Non merci** permet de ne plus afficher cette suggestion. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés. Travail et Personnel ne sont donc jamais mélangés. Tout reste sur votre Machine. Une tâche que vous clôturez régulièrement est plutôt proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue toute seule et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « tous les vendredis, indique-moi les affaires qui n’avancent plus ».
