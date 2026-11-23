---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue seule à intervalles réguliers, comme un récapitulatif de vos affaires en cours chaque lundi. Elle se contente de lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: e0d519d5927cdde0
---
## En créer une

Dans la barre latérale, ouvrez **Routines** et indiquez en une ligne ce qu’elle doit faire et quand : « chaque lundi à 9 h, résume mes affaires en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Puis sélectionnez **Ajouter**.

Sans horaire, elle s’exécute à 8 h. L’heure dépend de l’horloge de votre Machine. La première fois qu’elle s’exécute, elle reçoit un nom court.

**Ajouter** commence par un essai pour vous montrer le résultat avant de l’enregistrer. Rien n’est envoyé ni sauvegardé. Ensuite, **Ajouter** la programme, **Modifier** essaie d’autres mots ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de la page Routines, **Ajouter** active une routine prête à l’emploi. Elle s’exécute tout de suite, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Trouvailles d’occasion toutes les 3 heures, Abonnements et essais une fois par mois). Sa carte affiche ses consignes, comme pour toute routine. **Modifier** permet de les changer ou de renommer la routine.

Quand vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (au moins 25 par semaine, provenant d’au moins 5 expéditeurs), un message au-dessus de vos tâches indique combien vous en avez reçu et ce que la routine ferait, avec les options **Activer** et **Non merci**.

Tri du spam est proposé de la même façon si vous avez déplacé manuellement au moins 5 e-mails dans le spam en une semaine. **Activer** l’ajoute comme **Ajouter** le fait ici. **Non merci** signifie que la proposition ne s’affichera plus. Un modèle que vous avez déjà utilisé ne vous sera jamais proposé.

**Tri des newsletters** crée une tâche par domaine (professionnel et personnel) qui rassemble les newsletters du jour précédent. Pour chacune, vous pouvez choisir **Garder** ou **Se désabonner**. La désinscription utilise le lien de désabonnement en un clic de la liste, ou envoie un e-mail de désabonnement depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne sur la page de la liste, dans son propre navigateur. Si cette page demande une connexion, un captcha ou un choix, vous devez vous en occuper. La ligne indique pourquoi, avec **Ouvrir la page de désabonnement**.

Les reçus, commandes et avis de paiement sont ignorés. Les e-mails reçus par l’intermédiaire d’une adresse de groupe, comme un Google Group, sont classés sous le nom de leur expéditeur. La routine ne vous désabonne jamais du groupe. Si l’expéditeur ne propose pas de désabonnement, la ligne affiche **Se désabonner soi-même**.

**Tri du spam** crée une tâche par domaine qui rassemble les e-mails d’expéditeurs inconnus ressemblant à du spam. Pour chacun, choisissez **Spam** ou **Pas du spam**. Outlook déplace les spams dans les courriers indésirables et Gmail les signale comme spam. La routine vérifie les messages toutes les heures, si bien que le spam est généralement repéré avant que vous ne le voyiez. Tant que la tâche est ouverte, les nouveaux spams y sont ajoutés.

Si Gmail est connecté en lecture seule, comme sur une Machine hébergée, les e-mails ne peuvent pas être déplacés dans le spam. Dans ce cas, **Spam** affiche un lien pour signaler l’e-mail dans Gmail, et The Machine mémorise l’expéditeur comme spam. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. Un « Re: » ne compte comme une conversation que dans un fil auquel vous avez participé. Si un e-mail provenant d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte de réception, arrive de nouveau, il apparaît dans la prochaine tâche avec la mention **Déjà signalé comme spam**. Les messages que vous avez déplacés vous-même dans le spam aident aussi la routine à repérer les e-mails similaires.

Rien ne change tant que vous ne confirmez pas dans la tâche. Touchez le nom d’un expéditeur pour lire son e-mail : il reste non lu et rien ne change. Depuis Tri du spam, les images provenant du Web ne se chargent pas, pour que l’expéditeur ne sache pas que vous avez ouvert le message. Les expéditeurs pour lesquels vous avez fait un choix ne vous seront pas proposés de nouveau. S’il n’y a eu aucune newsletter ou aucun spam pendant une journée, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Quand vous avez fait un choix pour chaque expéditeur, la tâche indique qu’elle est terminée et affiche **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour, dans une seule tâche, quelques articles de newsletters qui méritent votre attention. Chacun indique en une ligne pourquoi il vous intéresse. Touchez un article pour lire l’e-mail, ou sélectionnez **Ouvrir dans votre messagerie**. La routine ne consulte que les newsletters, jamais les e-mails de personnes, les reçus ou les messages d’expéditeurs dont vous vous êtes désabonné, ni les messages que vous avez déjà lus. Si aucun article ne se démarque, aucune tâche n’est créée.

La routine apprend ce qui vous intéresse à partir des messages que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les avoir lus, ainsi qu’à partir de vos choix **Plus comme ça** et **Moins comme ça** pour chaque article. Les sujets sélectionnés s’affichent sur la carte de la routine, sous **Plus de** et **Moins de**. Supprimez-en un avec × ou ajoutez les vôtres. Les sujets en pointillés ont été détectés par la routine. Un nouveau récap remplace celui qui est encore ouvert. Aucune notification n’est envoyée.

La routine lit uniquement l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose à votre IA une courte question à leur sujet, dans la limite d’un quota quotidien, pour réduire les coûts. **Changer le moment** permet de régler l’heure. Dès que vous modifiez les consignes, la routine fonctionne comme n’importe quelle routine et les suit.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts réguliers. Chaque tâche contient un court message de vœux rédigé dans le canal où vous échangez habituellement avec la personne, comme son chat WhatsApp ou votre fil d’e-mails, et dans sa langue. Le message n’est envoyé que lorsque vous l’envoyez vous-même. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos agendas (les événements d’anniversaire et l’agenda Anniversaires de Google, consultés chaque matin même s’ils ne sont pas synchronisés, ainsi que l’agenda Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday dans la fiche d’une personne du Graph. Si aucun anniversaire n’a encore été trouvé, le résultat affiche **Aucune info sur les anniversaires pour le moment** et indique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche vous propose de consulter la page des anniversaires de Facebook. Touchez **Importer**. The Machine ouvre la page dans son navigateur, fait défiler jusqu’à ce que tous les mois soient chargés, puis relève le nom et l’anniversaire de chaque ami. Elle indique combien d’anniversaires ont été trouvés et quelles personnes correspondent à des contacts de votre Graph, selon leur prénom et leur nom. Les noms associés à plusieurs personnes sont ignorés et répertoriés.

Seule l’option **Enregistrer** les ajoute, sur la fiche de chaque personne : l’anniversaire et la photo de profil Facebook, si la personne n’a pas encore de photo. Un anniversaire ou une photo que vous avez définis vous-même sont conservés, et une photo déjà présente n’est jamais remplacée. Aucune information n’est écrite sur Facebook.

La routine ne consulte pas Facebook de nouveau d’elle-même. Pour relancer l’importation, sélectionnez **Importer à nouveau** dans la tâche. Le navigateur doit être connecté à Facebook. Si ce n’est pas le cas, touchez **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois la session ouverte, la page est consultée automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent dans aucun contact de votre Graph sont comptabilisés, et quelques noms sont affichés. **Ajouter … comme contacts personnels** les ajoute tous en une seule fois, y compris après avoir sélectionné Enregistrer. Chaque contact est créé avec son nom et son anniversaire, et n’est jamais partagé avec une Fleet Travail. Une personne dont le nom figure déjà dans votre Graph, ou que vous avez supprimée définitivement, est ignorée. Les rappels d’anniversaire ne concernent toujours que les personnes à qui vous écrivez.

**Annuler** dans la tâche supprime précisément ces personnes, même après avoir sélectionné **Importer à nouveau**.

**Abonnements et essais** consulte une fois par mois vos reçus, factures et avis de renouvellement, puis rassemble vos abonnements dans une seule tâche. Pour chacun, vous voyez son prix, la date du prochain prélèvement et un indicateur si un essai se termine ou si le prix augmente. Seuls les abonnements identifiés avec certitude sont affichés. Si aucun n’est trouvé, aucune tâche n’est créée.

Pour chaque abonnement, choisissez **Garder** ou **Résilier**. La routine ne vous proposera plus un abonnement conservé, sauf si son prix change. **Résilier** affiche la page de résiliation ou un brouillon de message pour demander la résiliation. Le message n’est envoyé que lorsque vous l’envoyez vous-même. Entre deux vérifications mensuelles, la routine vérifie chaque jour et crée une tâche si un essai ou un renouvellement doit être facturé dans les 7 jours.

**Garder le contact** vous rappelle de temps à autre de reprendre contact avec un proche, uniquement lorsqu’il y a une bonne raison. Sur sa carte, choisissez les personnes concernées dans une courte liste de contacts avec lesquels vous échangez directement, dans les deux sens, depuis plusieurs mois. Supprimez une personne avec ×.

Un rappel n’apparaît que si vous n’avez pas parlé à la personne depuis bien plus longtemps que d’habitude et qu’il y a quelque chose de précis à lui dire : une nouvelle qu’elle vous a annoncée, une promesse en attente ou un message auquel vous n’avez jamais répondu. Une seule tâche indique la raison et contient un court message rédigé dans le canal où vous échangez habituellement avec la personne, dans sa langue. Le message n’est envoyé que lorsque vous l’envoyez vous-même. S’il n’y a rien à dire, aucune tâche n’est créée.

La routine envoie au maximum deux rappels par semaine, un par personne et par mois, et aucun à une personne avec qui vous avez échangé récemment. L’option **Pas nécessaire** sur un rappel allonge le délai avant un prochain rappel pour cette personne, et ce délai augmente à chaque fois. Aucune notification n’est envoyée, et cette routine reste personnelle : elle n’est jamais partagée avec une Fleet Travail.

**Trouvailles d’occasion** surveille une recherche sur un site de seconde main, comme Marktplaats, Vinted, eBay ou Facebook Marketplace. Effectuez une recherche avec les filtres souhaités, copiez l’adresse des résultats et collez-la après avoir sélectionné **Ajouter**. Si vous le souhaitez, ajoutez des filtres avec vos propres mots, comme « moins de 300, à moins de 30 km, pas “pour pièces” ». Chaque recherche correspond à une routine distincte. Ajoutez-en une autre pour surveiller une nouvelle recherche.

Toutes les 3 heures, la routine ouvre la recherche dans le navigateur de The Machine et repère les annonces qu’elle n’a pas encore vues. Le prix, la distance et les mots que vous avez exclus sont d’abord vérifiés avec du code simple.

Chaque nouvelle annonce qui passe ces vérifications est ouverte. Votre IA évalue son état à partir de la photo et de la description, et le vendeur à partir de ses avis, de sa note et de l’ancienneté de son compte. Les bonnes annonces sont regroupées dans une seule tâche, avec pour chacune une photo, un titre, un prix et une évaluation en une ligne. Touchez une annonce pour l’ouvrir dans le navigateur de The Machine.

Tant que la tâche est ouverte, les nouvelles trouvailles s’ajoutent en haut de la liste, le nombre augmente et une nouvelle notification vous est envoyée, car les bonnes affaires partent vite. Quand vous marquez la tâche comme faite, la prochaine trouvaille crée une nouvelle tâche. Si une vérification ne trouve rien d’intéressant, rien ne change.

La routine reste discrète et peu coûteuse : une seule lecture de la recherche par exécution, au maximum 6 annonces ouvertes à chaque fois avec une pause entre elles, et au maximum 40 annonces vérifiées par jour, toutes recherches confondues. Chaque vérification consiste en une courte question posée à votre IA avec une photo. Lors de la première exécution, les quelques annonces les plus récentes sont vérifiées et les autres sont considérées comme déjà vues. Les exécutions suivantes ne rapportent donc que les nouveautés.

Si le site vous demande de vous connecter, affiche un test anti-robot ou empêche la lecture, une tâche vous en informe et propose **Ouvrir** pour afficher la page dans le navigateur de The Machine. Connectez-vous ou effectuez le test vous-même dans le navigateur. La prochaine exécution relira la page. The Machine ne se connecte jamais à votre place, ne résout jamais les tests et ne contacte, n’enchérit sur ni n’achète jamais d’article auprès d’un vendeur.

**Modifier la recherche** sur la carte de la routine permet de changer l’adresse ou les filtres. **Changer le moment** permet de modifier la fréquence, par exemple « toutes les 6 heures ».

**Réachats** lit les confirmations de commande des boutiques en ligne dans vos e-mails et repère les articles que vous achetez régulièrement, comme du café, de la nourriture pour animaux ou des vitamines. Lorsqu’un nouvel achat est probablement nécessaire, la routine crée une tâche indiquant l’article, la boutique, le dernier prix et la date de votre dernier achat. **Ouvrir dans la boutique** affiche la page de l’article pour que vous puissiez l’acheter vous-même. Rien n’est acheté à votre place.

Il faut au moins trois commandes du même article à intervalles réguliers. Un achat ponctuel ou un intervalle inhabituel ne crée donc aucune tâche. Pour l’instant, la routine consulte les boutiques qui utilisent Shopify. Votre IA ne lit que les nouveaux e-mails de commande de ces boutiques et ne pose qu’une courte question par exécution. Ces tâches n’envoient jamais de notification. Une nouvelle commande de l’article clôt la tâche ouverte.

Tant que la routine d’un modèle conserve les consignes du modèle, elle s’exécute avec son propre code, sans utiliser votre forfait IA. (Tri du spam commence par répertorier en code les nouveaux e-mails d’expéditeurs inconnus, et ne pose une courte question à votre IA que s’il y en a. Garder le contact ne pose des questions que sur les une ou deux personnes sélectionnées.) Un nouveau nom ne change rien à cela. Dès que vous modifiez les consignes, la routine fonctionne comme n’importe quelle routine et les suit.

Tri des newsletters et Tri du spam continuent de créer une seule tâche avec un choix pour chaque e-mail. Une routine Anniversaires modifiée affiche son résultat et au maximum un brouillon, et non une tâche par personne. Dans **Modifier**, **Revenir au modèle** rétablit les consignes du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit ce dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme une réussite.

Les routines se contentent de lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Elles ouvrent des pages trouvées dans les contenus consultés ou dans une recherche, avec des adresses de page simples et des sites connus. Elles n’ouvrent jamais une adresse inventée pour transmettre ce qu’elles ont lu. Seul un modèle peut modifier des e-mails, et uniquement ce que vous confirmez dans sa tâche.

Quand le travail d’une routine comprend une publication ou un message, elle effectue toutes les étapes précédentes et affiche le brouillon, par exemple **Publier sur X ?**. Après une véritable exécution, le brouillon apparaît dans une tâche à approuver. Un essai affiche simplement le brouillon.

Le nom indique le sujet de la routine et l’endroit où elle s’exécute. **Depuis votre routine** ouvre la routine. Le bouton indique l’étape à effectuer, par exemple **Préparer une publication**. Cette option prépare le contenu, sans rien publier. Vous le publiez depuis le résultat. Si The Machine ne peut pas le publier pour vous, le bouton ouvre la page où vous pourrez le faire.

La tâche apparaît d’abord dans le domaine du compte depuis lequel le contenu sera envoyé, comme le domaine Travail pour le compte X de votre entreprise. Vous n’aurez donc jamais à la déplacer.

Une exécution peut suivre vos [compétences](skills.md) activées, sélectionnées selon le travail de la routine. Seules celles qui sont pertinentes sont consultées en entier. Le résultat les indique sous **Utilisées :**. Une compétence ne permet jamais à une routine d’envoyer ou de modifier quoi que ce soit.

Vos routines se trouvent sous **Vos routines**, après les suggestions. Les longs résultats sont réduits à un aperçu. **Afficher plus**, ou un toucher sur l’aperçu, permet de les ouvrir.

Chaque exécution connaît le résultat précédent et peut donc indiquer les changements survenus depuis.

Après une exécution réussie, votre Machine peut rédiger elle-même une recette pour les recherches identiques d’une exécution à l’autre, comme les e-mails ou les modifications GitHub à consulter. Lors des exécutions suivantes, cette recette les lit d’abord avec du code simple. L’IA se contente ensuite de sélectionner les éléments pertinents et de les rédiger, ce qui utilise moins de tokens. Une recette se contente de lire. Si elle cesse de fonctionner, la routine reprend la lecture automatiquement et corrige le problème. La recette apparaît sous **Avancé : étapes de script**, dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une seule fois. Chaque date ne donne lieu qu’à une exécution, même après un redémarrage.

Les routines s’exécutent l’une après l’autre et attendent lorsque votre forfait IA est presque épuisé, comme pour les autres tâches en arrière-plan. **Lancer maintenant** exécute la routine immédiatement. Le résultat s’affiche sur sa carte dès qu’il est prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et son fonctionnement. Son horaire et ses résultats précédents sont conservés. **Changer le moment** permet de définir une nouvelle fréquence avec vos propres mots, comme « chaque jour de semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur ordinateur, vous pouvez aussi annuler en appuyant sur Échap ou en cliquant à l’extérieur.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles consignes et affiche le résultat. La routine ne change pas tant que vous n’avez pas sélectionné **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous sélectionniez **Reprendre** sur sa carte. Les routines en pause apparaissent sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne seront pas lancées ensuite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Si vous sélectionnez **Demander des modifications** dans la tâche d’une routine ou écrivez dans son chat, et que votre remarque concerne toutes les exécutions, comme « ne jamais utiliser d’emoji », la tâche vous propose **Modifier aussi la routine**, dans la tâche et dans son chat, sous la réponse. Les modifications apportées aux consignes de la routine sont affichées. La routine ne change que si vous touchez **Modifier**. **Laisser ainsi** conserve la routine telle quelle. Une correction qui ne concerne que le brouillon n’affiche pas cette option.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez avec vos propres mots ce que la routine doit faire, et votre Machine s’occupe du reste.

Les utilisateurs avancés peuvent aussi exécuter leurs propres commandes sur leur Machine. Dans le menu ⋯, sélectionnez **Avancé : étapes de script**. **Modifier** affiche les étapes seulement si la routine en contient déjà. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel si le champ est vide), pendant le nombre de secondes indiqué au maximum. Le résultat de la commande est transmis à l’exécution pour qu’elle le traite. S’il n’y a pas de consignes, le résultat de la commande est affiché tel quel.

**Vérification** reçoit le résultat de l’exécution en entrée. Si la commande se termine par une erreur, le résultat affiche **N’a pas marché**, avec le message de la vérification. L’échec d’une commande Récupérer les données s’affiche de la même façon.

Une commande tient sur une seule ligne et s’exécute sans shell : les tubes et les variables ne sont pas pris en charge. Les étapes de script sont les vôtres et ne sont configurées que sur votre tableau de bord. Un essai et **Essayer** exécutent aussi Récupérer les données et l’indiquent. Rien n’est envoyé ni sauvegardé. Une routine n’envoie jamais rien, donc une étape de script doit se contenter de lire.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit sans jamais les modifier, puis propose celles qui peuvent devenir des routines, sous **Suggérée**. Chacune a déjà été exécutée une fois, pour vous montrer un résultat réel.

La routine conserve les corrections que vous avez apportées à la tâche et ignore ce qu’elle a envoyé ou publié. Si une tâche exécutait un script ou lisait des données recueillies par un script, celui-ci est repris comme étape Récupérer les données. **Ajouter** transforme la tâche en routine. **Non merci** signifie que cette tâche ne sera plus proposée. Une tâche qui vous rappelait de faire quelque chose est plutôt proposée comme tâche récurrente dans To-dos.

Avant d’ajouter une suggestion, les options **Modifier** et **Changer le moment** du menu ⋯ permettent de la modifier comme n’importe quelle routine. **Relancer** l’exécute avec ses consignes actuelles pour afficher des résultats plus récents, par exemple après un week-end calme. La routine se contente de lire, s’exécute une fois par sélection, et son nouveau résultat remplace l’ancien.

Trois suggestions au maximum peuvent être en attente. Après une semaine d’exécutions réussies, la routine demande **Désactiver l’ancienne tâche OpenClaw ?**. Elle ne la désactive que si vous sélectionnez **Désactiver**. Vous pourrez la réactiver dans OpenClaw. **Garder** laisse les deux tâches actives.

## En fonction de vos habitudes

Votre Machine repère aussi les tâches que vous effectuez régulièrement et les propose comme routines sous **Suggérée**, même sans OpenClaw. Elle recherche :

- la même demande répétée au moins trois fois de suite, comme « résume les tickets d’assistance en cours » chaque lundi ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- les newsletters et les e-mails d’actualité qui reviennent chaque semaine ;
- un canal Slack actif dans lequel d’autres personnes écrivent chaque semaine ;
- les e-mails que vous transférez un à un à la même personne, comme les messages de l’école et du club que vous envoyez à votre partenaire. Un récap hebdomadaire lui évite de recevoir tous ces transferts ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion indique ce qui a été repéré, comme « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a déjà été exécutée une fois pour vous montrer un résultat réel. Pensez à un récap d’équipe, à un briefing avant un appel hebdomadaire, à un résumé de l’assistance ou du développement, à un aperçu de vos chiffres ou à un récap des newsletters que vous recevez.

Seules les suggestions qui vous sont propres et qui sont clairement utiles sont proposées : un récap d’actualités portera uniquement sur vos newsletters, jamais sur des actualités génériques. Si rien ne correspond, aucune suggestion n’est proposée.

La routine vérifie les habitudes au maximum une fois par jour et propose au plus une nouvelle suggestion par semaine, sans envoyer de notification. **Non merci** empêche définitivement le retour de cette suggestion. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés, pour que Travail et Personnel ne soient pas mélangés. Tout reste sur votre Machine. Une tâche que vous clôturez régulièrement est plutôt proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue et vous présente automatiquement. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « chaque vendredi, indique-moi quelles affaires sont au point mort ».
