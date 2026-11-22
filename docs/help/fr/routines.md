---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue toute seule, à intervalles réguliers, comme le récap de vos affaires en cours chaque lundi. Elle se contente de lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, reorder.py, reorder_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js, dashboard/todos-reorder.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours, reorder, reorders, buy again, running low, order confirmation, shopify
translated: b5704836b00227a5
---
## En créer une

Dans la barre latérale, ouvrez **Routines** et indiquez en une phrase ce qu’elle doit faire et quand : « chaque lundi à 9 h, résume mes affaires en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Puis sélectionnez **Ajouter**.

Sans horaire indiqué, elle se lance à 8 h. L’heure est celle de votre Machine. Lors de sa première exécution, elle reçoit un nom court.

**Ajouter** commence par un essai pour vous montrer le résultat avant de l’enregistrer. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la programme selon le rythme choisi, **Modifier** essaie une autre formulation ou un nouveau nom, et **Annuler** l’abandonne.

## Modèles

Dans **Modèles**, en bas de la page Routines, **Ajouter** active une routine prête à l’emploi. Elle s’exécute tout de suite, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Trouvailles d’occasion toutes les 3 heures, Abonnements et essais une fois par mois). Sa carte affiche sa formulation comme celle de n’importe quelle routine. **Modifier** permet de changer son texte ou son nom.

Quand vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), une ligne au-dessus de vos tâches indique combien vous en avez reçues et ce que la routine ferait, avec **Activer** et **Non merci**.

Tri du spam est proposé de la même façon quand au moins 5 e-mails ont été déplacés manuellement dans le spam en une semaine. **Activer** l’ajoute comme le fait **Ajouter** ici. **Non merci** signifie que la proposition ne reviendra pas. C’est aussi le cas d’un modèle que vous avez déjà eu.

**Tri des newsletters** crée une tâche par espace (Travail et Perso) avec les newsletters reçues au cours de la dernière journée. Pour chacune, choisissez **Garder** ou **Se désabonner**. Le désabonnement utilise le lien en un clic de la liste, ou un e-mail de désabonnement envoyé depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne sur la page de la liste, dans son propre navigateur. Si cette page demande une connexion, un captcha ou un choix, c’est à vous de vous en occuper : la ligne vous en explique la raison, avec **Ouvrir la page de désabonnement**.

Les reçus, commandes et avis de paiement sont exclus. Les e-mails reçus via une adresse de groupe, comme un Google Group, sont indiqués sous le nom de leur auteur et ne vous désabonnent jamais du groupe. Si l’expéditeur ne propose pas de désabonnement, la ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace avec les e-mails d’expéditeurs inconnus qui ressemblent à du spam. Pour chacun, choisissez **Spam** ou **Pas du spam**. Outlook déplace les spams dans Courrier indésirable et Gmail les signale comme spam. La routine vérifie les e-mails toutes les heures, les spams sont donc généralement repérés avant que vous les voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Un compte Gmail connecté en lecture seule, comme sur une Machine hébergée, ne peut pas déplacer les e-mails dans le spam. Dans ce cas, **Spam** affiche un lien pour les signaler dans Gmail, et The Machine mémorise l’expéditeur comme spam. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. La mention « Re: » indique une conversation uniquement dans un fil auquel vous avez participé. Si vous recevez à nouveau un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte de réception, il apparaît dans la prochaine tâche avec l’indication **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés dans le spam aident aussi la routine à repérer les messages similaires.

Rien ne change avant que vous confirmiez votre choix dans la tâche. Touchez un expéditeur pour lire l’e-mail d’abord : il reste non lu et rien ne change. Dans Tri du spam, les images provenant du Web ne se chargent pas. L’expéditeur ne peut donc pas voir que vous avez ouvert l’e-mail. La routine ne vous demande plus votre avis sur les expéditeurs pour lesquels vous avez déjà choisi. Si vous ne recevez ni newsletter ni spam pendant une journée, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois que vous avez choisi pour tous les expéditeurs, la tâche indique qu’elle est terminée et propose **Marquer comme fait**.

**Récap du jour** sélectionne une fois par jour, dans une seule tâche, les quelques articles de newsletter qui valent la peine d’être lus. Chaque article est accompagné d’une phrase qui explique pourquoi il vous intéresse. Touchez-le pour lire l’e-mail ou choisissez **Ouvrir dans votre messagerie**. La routine ne traite que les newsletters, jamais les e-mails de personnes, les reçus ou les e-mails d’expéditeurs dont vous vous êtes désabonné, et jamais ceux que vous avez déjà lus. Si aucun article ne sort du lot, aucune tâche n’est créée.

La routine apprend ce qui vous intéresse d’après les e-mails que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les lire, ainsi que vos choix **Plus comme ça** et **Moins comme ça** pour chaque sélection. Les sujets qu’elle choisit apparaissent sur la carte de sa routine, sous **Plus de** et **Moins de**. Pour en supprimer un, touchez ×, ou ajoutez les vôtres. Les sujets en pointillés ont été trouvés par la routine. Un nouveau récap remplace celui qui est ouvert. Il n’envoie jamais de notification.

La routine lit uniquement l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose à votre IA une courte question à leur sujet, avec une limite quotidienne pour réduire les coûts. **Changer le moment** permet de choisir l’heure. Dès que vous modifiez son texte, elle fonctionne comme n’importe quelle routine, à partir de vos instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts habituels. Chaque tâche inclut un court message de vœux, rédigé dans l’endroit où vous échangez habituellement avec cette personne, comme son chat WhatsApp ou votre fil d’e-mails, dans sa langue. Le message n’est envoyé que si vous l’envoyez. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos agendas (les événements d’anniversaire de Google et l’agenda Anniversaires, consultés chaque matin même s’ils ne sont pas synchronisés, ainsi que le calendrier Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday sur une personne dans le Graph. Si aucun anniversaire n’est encore renseigné, le résultat indique **Pas encore d’informations sur les anniversaires** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche vous propose de consulter la page des anniversaires de Facebook. Touchez **Importer** et The Machine ouvre la page dans son navigateur, fait défiler la page jusqu’à ce que tous les mois soient chargés, puis relève le nom et l’anniversaire de chaque ami. La routine indique combien de dates elle a trouvées et quelles personnes correspondent à celles de votre Graph, d’après leur prénom et leur nom. Les noms associés à plusieurs personnes sont ignorés et signalés dans la liste.

Seul **Enregistrer** les ajoute, sur la page de chaque personne : la date d’anniversaire et, pour les personnes sans photo, leur photo de profil Facebook. Une date d’anniversaire ou une photo que vous avez renseignée reste inchangée, et une photo existante n’est jamais remplacée. Aucune information n’est écrite sur Facebook.

La routine ne relit pas la page toute seule : c’est **Importer à nouveau** dans la tâche qui le fait. Vous devez être connecté à Facebook dans le navigateur. Si ce n’est pas le cas, touchez **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois connecté, la routine consulte la page automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent dans aucun Graph sont comptabilisés, avec quelques noms. **Ajouter … comme contacts personnels** les ajoute tous en une fois, y compris après avoir sélectionné Enregistrer : la routine ajoute leur nom et leur anniversaire, sans jamais les partager avec une Fleet Travail. Les personnes dont le nom figure déjà dans votre Graph, ou qui y figuraient avant d’être supprimées définitivement, sont ignorées. Les rappels d’anniversaire ne concernent que les personnes à qui vous écrivez.

**Annuler** dans la tâche supprime précisément ces personnes, même après avoir sélectionné **Importer à nouveau**.

**Abonnements et essais** consulte une fois par mois vos reçus, factures et avis de renouvellement, puis regroupe vos abonnements dans une seule tâche : le prix de chacun, la date du prochain paiement et un indicateur si un essai prend fin ou si le prix augmente. La routine ne répertorie que les abonnements dont elle est sûre. Si elle n’en trouve aucun, aucune tâche n’est créée.

Pour chacun, choisissez **Garder** ou **Résilier**. La routine ne vous reparle pas d’un abonnement que vous gardez, sauf si son prix change. **Résilier** vous dirige vers la page de résiliation ou crée un brouillon pour demander la résiliation. Le message ne sera envoyé que si vous l’envoyez. Entre deux vérifications mensuelles, la routine vérifie chaque jour si un essai ou un renouvellement sera facturé dans les 7 jours et crée une tâche si c’est le cas.

**Garder le contact** vous rappelle de temps en temps de prendre des nouvelles d’un proche, uniquement s’il y a une vraie raison de le faire. Sur sa carte, choisissez les personnes concernées dans une courte liste de personnes avec qui vous échangez vous-même, dans les deux sens, depuis plusieurs mois. Touchez × pour retirer une personne.

Un rappel n’est envoyé que si vous n’avez pas parlé à la personne depuis bien plus longtemps que d’habitude et qu’il y a quelque chose de précis à lui dire : une nouvelle qu’elle vous a donnée, une promesse encore en suspens ou un message auquel vous n’avez jamais répondu. Une seule tâche vous indique la raison et propose un court message rédigé dans l’endroit où vous échangez habituellement avec cette personne, dans sa langue. Le message ne sera envoyé que si vous l’envoyez. S’il n’y a rien à dire, aucune tâche n’est créée.

La routine envoie au maximum deux rappels par semaine et un par personne par mois, et n’en envoie aucun à une personne avec qui vous avez parlé récemment. **Pas nécessaire** sur un rappel allonge le délai avant le prochain rappel pour cette personne, puis l’allonge encore à chaque fois. La routine n’envoie jamais de notification et reste personnelle : elle n’est jamais partagée avec une Fleet Travail.

**Trouvailles d’occasion** surveille une recherche sur un site de seconde main comme Marktplaats, Vinted, eBay ou Facebook Marketplace. Lancez une recherche sur le site avec les filtres voulus, copiez l’adresse des résultats et collez-la après avoir sélectionné **Ajouter**. Vous pouvez aussi ajouter des filtres avec vos propres mots, par exemple « moins de 300, à moins de 30 km, sans “pour pièces” ». Chaque recherche a sa propre routine. Ajoutez-en une autre pour votre prochaine recherche.

Toutes les 3 heures, The Machine ouvre la recherche dans son propre navigateur et repère les annonces qu’elle n’a pas encore vues. Le prix, la distance et les mots à exclure sont d’abord vérifiés par du code simple.

Chaque nouvelle annonce qui passe ces filtres est ouverte. Votre IA évalue son état d’après la photo et la description, ainsi que le vendeur d’après ses avis, sa note et l’ancienneté de son compte. Les annonces intéressantes sont regroupées dans une seule tâche, avec leur photo, leur titre, leur prix et un avis en une ligne. Touchez une annonce pour l’ouvrir dans le navigateur de The Machine.

Tant que la tâche est ouverte, les nouvelles trouvailles s’ajoutent en haut, le nombre d’annonces augmente et une nouvelle notification vous est envoyée, car les bonnes affaires partent vite. Marquez la tâche comme faite pour que la prochaine trouvaille crée une nouvelle tâche. Si une vérification ne trouve rien d’intéressant, rien ne change.

La routine reste discrète et peu coûteuse : une seule lecture de la recherche par vérification, au maximum 6 annonces ouvertes par vérification avec une pause entre chacune, et au maximum 40 annonces vérifiées par jour pour l’ensemble de vos recherches. Chaque vérification consiste en une courte question à votre IA avec une photo. Lors de la première vérification, la routine examine les quelques annonces les plus récentes et considère le reste comme déjà vu. Les suivantes ne vous montrent donc que les nouveautés.

Si le site demande une connexion, affiche un test anti-robot ou bloque la lecture, une tâche vous l’indique, avec **Ouvrir** pour consulter la page dans le navigateur de The Machine. Connectez-vous ou passez le test vous-même. La prochaine vérification relira la page. The Machine ne se connecte jamais à votre place, ne résout jamais de test et ne contacte jamais de vendeur, ne fait aucune enchère et n’achète rien.

**Modifier la recherche** sur la carte de la routine permet de saisir une nouvelle adresse ou de nouveaux filtres. **Changer le moment** permet de choisir un autre rythme, comme « toutes les 6 heures ».

**Réachats** repère les confirmations de commande de boutiques en ligne dans vos e-mails et détecte les achats que vous répétez, comme le café, la nourriture pour animaux ou les vitamines. Lorsqu’un nouvel achat est probablement nécessaire, la routine crée une tâche avec l’article, la boutique, le dernier prix et la date du dernier achat. **Ouvrir dans la boutique** vous mène à la page de l’article pour que vous puissiez l’acheter vous-même. Rien n’est acheté à votre place.

La routine a besoin d’au moins trois commandes du même article à intervalles réguliers. Un achat ponctuel ou un intervalle inhabituel ne crée donc pas de tâche. Pour le moment, elle consulte les boutiques qui utilisent Shopify. Votre IA ne lit que les nouveaux e-mails de commande de ces boutiques, au moyen d’une courte question par vérification. Ces tâches n’envoient jamais de notification. Une nouvelle commande du même article ferme la tâche ouverte.

Tant que le texte d’une routine de modèle n’est pas modifié, elle s’exécute avec son propre code, sans utiliser votre forfait IA (Tri du spam répertorie d’abord en code les nouveaux e-mails d’expéditeurs inconnus et ne pose une courte question à votre IA que si elle en trouve ; Garder le contact ne pose des questions qu’à propos d’une ou deux personnes sélectionnées). Un nouveau nom ne change rien à cela. Dès que vous modifiez le texte, la routine fonctionne comme n’importe quelle autre, à partir de vos instructions.

Tri des newsletters et Tri du spam créent toujours une seule tâche avec un choix pour chaque e-mail. Si vous modifiez Anniversaires, la routine affiche son résultat et un seul brouillon au maximum, et non une tâche par personne. Dans **Modifier**, **Revenir au modèle** rétablit le texte du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit les informations dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme une réussite.

Les routines se contentent de lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Elles ouvrent les pages trouvées dans ce qu’elles lisent ou dans une recherche, les adresses de pages simples et les sites connus, jamais une adresse inventée pour transporter ce qu’elles ont lu. Seul un modèle modifie les e-mails, et uniquement ce que vous confirmez dans sa tâche.

Quand une routine doit publier ou envoyer un message, elle effectue tout jusqu’à cette étape et affiche le brouillon, par exemple **Publication sur X :**. Après une véritable exécution, le brouillon apparaît dans une tâche que vous pouvez approuver. Un essai ne fait que l’afficher. Son nom indique le sujet et l’endroit où le contenu sera publié, et son bouton décrit l’étape, comme **Publier**. **Depuis votre routine**, en dessous, ouvre la routine.

La tâche apparaît dans l’espace du compte depuis lequel le contenu sera envoyé, par exemple Travail pour le compte X de votre entreprise. Elle ne vous demande donc jamais de la déplacer.

Une routine peut suivre vos [compétences](skills.md) activées, sélectionnées selon son objectif : seules celles qui sont pertinentes sont lues en entier. Le résultat les indique sous **Utilisées :**. Une compétence ne fait jamais envoyer ni modifier quoi que ce soit à une routine.

Vos routines figurent sous **Vos routines**, après les suggestions éventuelles. Les longs résultats sont repliés en un bref aperçu. Touchez **Afficher plus** ou le résultat pour l’ouvrir.

Chaque exécution connaît le résultat précédent et peut donc indiquer ce qui a changé depuis.

Après une exécution réussie, votre Machine peut rédiger elle-même une recette pour les vérifications qui se répètent, par exemple les e-mails ou les changements GitHub à consulter. Lors des exécutions suivantes, le code simple commence par les lire. L’IA sélectionne ensuite les éléments importants et les rédige, en utilisant moins de jetons. Une recette se contente de lire. Si elle ne fonctionne plus, la routine fait la lecture elle-même et la corrige. La recette apparaît sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une seule fois. Chaque date ne donne lieu qu’à une exécution, même après un redémarrage.

Les routines s’exécutent l’une après l’autre et attendent si l’utilisation de votre forfait IA est faible, comme pour toutes les tâches en arrière-plan. **Lancer maintenant** démarre la routine tout de suite. Le résultat s’affiche sur sa carte lorsqu’il est prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** change son nom et son objectif. Son horaire et ses résultats précédents restent inchangés. **Changer le moment** permet de définir un nouveau rythme avec vos propres mots, comme « chaque jour de la semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur un ordinateur, Échap ou un clic à l’extérieur annule aussi l’opération.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles instructions et affiche le résultat. La routine ne change pas tant que vous n’avez pas sélectionné **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous sélectionniez **Reprendre** sur la carte. Les routines en pause sont regroupées sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne sont pas lancées ensuite. **Arrêter** met fin définitivement à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Quand vous utilisez **Demander des modifications** dans la tâche d’une routine, ou que vous écrivez dans son chat, si votre commentaire concerne toutes les exécutions, comme « ne mets jamais d’émoji », la tâche vous propose **Modifier aussi la routine**, dans la tâche et dans son chat, sous la réponse. Elle vous indique les changements apportés au texte de la routine. Celle-ci n’est modifiée que lorsque vous touchez **Modifier**. **Laisser ainsi** ne change rien. Une correction qui concerne uniquement le brouillon ne donne lieu à aucune proposition.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez avec vos propres mots ce que la routine doit faire, et votre Machine s’occupe du reste.

Pour les utilisateurs avancés, une routine peut aussi exécuter vos propres commandes sur votre Machine. Dans le menu ⋯, sélectionnez **Avancé : étapes de script**. **Modifier** affiche les étapes seulement si la routine en contient. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel s’il n’est pas renseigné), pendant la durée indiquée en secondes au maximum. Le résultat de la commande est transmis à la routine. Si vous ne fournissez aucune instruction, ce résultat est celui de la routine.

**Vérification** utilise le résultat de l’exécution comme entrée. Si la commande se termine avec une erreur, la routine indique **N’a pas marché** et affiche le message de la vérification. Une commande de récupération des données qui échoue affiche le même message.

Une commande doit tenir sur une ligne et s’exécute sans shell : pas de tuyaux ni de variables. Vous gérez vous-même les étapes de script, qui ne sont définies que sur votre tableau de bord. Un essai et une exécution avec **Essayer** lancent aussi la récupération des données et vous le signalent. Ils n’envoient ni n’enregistrent rien. Une routine n’envoie rien : une étape de script doit donc se contenter de lire.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit sans jamais les modifier et propose celles qui conviennent comme routines, sous **Suggérée**. Chacune a été exécutée une fois, vous voyez donc un résultat réel.

La routine conserve vos corrections et exclut ce qu’elle a envoyé ou publié. Si une tâche exécutait un script ou lisait des informations récupérées par un script, celui-ci est ajouté comme étape **Récupérer les données**. **Ajouter** en fait une routine. **Non merci** empêche toute nouvelle proposition de cette tâche. Une tâche qui vous rappelait de faire quelque chose est plutôt proposée comme tâche récurrente dans la section Tâches.

Avant d’ajouter une suggestion, **Modifier** et **Changer le moment**, dans son menu ⋯, permettent de la modifier comme n’importe quelle routine. **Relancer** l’exécute immédiatement avec son texte actuel pour afficher des résultats plus récents, par exemple après un week-end calme. Elle se contente de lire, s’exécute une fois par sélection et son nouveau résultat remplace l’ancien.

Trois suggestions au maximum peuvent être en attente. Après une semaine d’exécutions réussies, la routine demande **Désactiver l’ancienne tâche OpenClaw ?** Elle n’est désactivée que si vous sélectionnez **Désactiver**. Vous pouvez la réactiver dans OpenClaw. **Garder** laisse les deux tâches actives.

## D’après votre activité

Votre Machine repère aussi les tâches que vous effectuez à intervalles réguliers et les propose comme routines sous **Suggérée**, même si vous n’utilisez pas OpenClaw. Elle cherche notamment :

- la même demande faite au moins trois fois de suite, comme « résume les tickets d’assistance en cours » chaque lundi ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et des e-mails d’actualité reçus chaque semaine ;
- un canal Slack très actif où d’autres personnes écrivent chaque semaine ;
- des e-mails que vous transférez un par un à la même personne, comme ceux de l’école ou d’un club à votre partenaire : un récap hebdomadaire lui évite de recevoir chaque transfert ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour une même personne.

Chaque suggestion indique ce que la routine a repéré, par exemple « Demande faite 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a déjà été exécutée une fois : vous voyez donc un résultat réel. Vous pouvez par exemple créer un récap d’équipe, un résumé avant un appel hebdomadaire, un récap de l’assistance ou du développement, un suivi de vos chiffres ou un récap des newsletters que vous recevez.

La routine ne suggère que des tâches qui vous sont propres et clairement utiles : un récap de l’actualité ne concerne que vos propres newsletters, jamais un récap générique. Si rien ne convient, aucune suggestion n’est affichée.

La routine vérifie au maximum une fois par jour et propose au plus une nouvelle suggestion par semaine, sans notification. **Non merci** empêche cette suggestion de revenir. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés, pour que Travail et Perso ne se mélangent pas. Toutes ces données restent sur votre Machine. Une tâche que vous fermez à intervalles réguliers est plutôt proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue toute seule et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « chaque vendredi, indique-moi quelles affaires sont au point mort ».
