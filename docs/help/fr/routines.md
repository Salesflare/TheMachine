---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue seule, à intervalles réguliers, comme un récap de vos affaires en cours chaque lundi. Elle fait uniquement de la lecture.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, secondhand.py, secondhand_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in, second-hand, secondhand, marketplace, listings, every 3 hours
translated: 3e6d9d8d446a5dde
---
## En créer une

Dans la barre latérale, ouvrez **Routines** et indiquez en une ligne ce qu’elle doit faire et quand : « tous les lundis à 9 h, récapitule mes affaires en cours » ou « chaque matin de semaine, liste les e-mails auxquels je dois encore répondre ». Puis sélectionnez **Ajouter**.

Si vous n’indiquez pas d’heure, la routine s’exécute à 8 h. L’heure dépend de l’horloge de votre Machine. La première exécution lui donne un nom court.

**Ajouter** lance d’abord un test pour vous montrer le résultat avant que vous ne gardiez la routine. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la programme à intervalles réguliers, **Modifier** essaie d’autres mots ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de la page Routines, **Ajouter** active une routine prête à l’emploi. Elle s’exécute tout de suite, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Trouvailles d’occasion toutes les 3 heures, Abonnements et essais une fois par mois). Sa carte affiche ses instructions, comme pour toute routine, et **Modifier** permet de les changer ou de modifier son nom.

Si vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), un message au-dessus de vos tâches indique combien vous en avez reçues et ce que la routine ferait, avec les options **L’activer** et **Non merci**.

Tri du spam est proposé de la même façon si au moins 5 e-mails ont été déplacés manuellement dans les spams au cours d’une semaine. **L’activer** l’ajoute comme le fait **Ajouter** ici. **Non merci** signifie que la routine ne sera plus proposée. Cela vaut aussi pour un modèle que vous avez déjà eu.

**Tri des newsletters** crée une tâche par espace (professionnel et personnel) avec les newsletters reçues au cours de la dernière journée. Pour chacune, vous pouvez choisir **Garder** ou **Se désabonner**. Le désabonnement utilise le lien prévu à cet effet en un clic dans la liste, ou envoie un e-mail de désabonnement depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne depuis la page de la liste dans son propre navigateur. Vous devez vous-même vous connecter, résoudre un captcha ou faire des choix sur cette page. La ligne explique pourquoi et propose **Ouvrir la page de désabonnement**.

Les reçus, les commandes et les avis de paiement sont ignorés. Les e-mails reçus par l’intermédiaire d’une adresse de groupe, comme un Google Group, sont classés sous le nom de leur expéditeur et ne vous désabonnent jamais du groupe. Si l’expéditeur ne propose pas de désabonnement, la ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace avec les e-mails d’expéditeurs inconnus qui semblent être du spam. Pour chaque e-mail, vous pouvez choisir **Spam** ou **Pas du spam**. Outlook déplace les spams dans le dossier Courrier indésirable et Gmail les signale comme spam. La routine vérifie toutes les heures, donc le spam est généralement repéré avant que vous ne le voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Gmail connecté en lecture seule, comme sur une Machine hébergée, ne peut pas déplacer les e-mails dans les spams. Dans ce cas, **Spam** affiche un lien pour les signaler dans Gmail, et The Machine mémorise l’expéditeur comme spam. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. « Re: » ne suffit à reconnaître une conversation que dans un fil auquel vous avez participé. Si un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte de réception, arrive de nouveau, il apparaît dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés dans les spams aident aussi la routine à repérer les e-mails similaires.

Rien ne change tant que vous n’avez pas confirmé dans la tâche. Touchez le nom d’un expéditeur pour lire son e-mail d’abord : il reste non lu et rien ne change. Dans Tri du spam, les images provenant du Web ne se chargent pas, afin que l’expéditeur ne puisse pas voir que vous avez ouvert son e-mail. Les expéditeurs pour lesquels vous avez fait un choix ne vous sont plus proposés. Si vous ne recevez ni newsletter ni spam un jour donné, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois que vous avez fait un choix pour chaque expéditeur, la tâche indique qu’elle est terminée et affiche **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour les quelques articles de newsletter qui méritent votre attention et les rassemble dans une tâche. Chaque article explique en une ligne pourquoi il vous intéresse. Touchez-le pour lire l’e-mail ou sélectionnez **Ouvrir dans votre messagerie**. Seules les newsletters sont prises en compte, jamais les e-mails de personnes, les reçus ou les expéditeurs dont vous vous êtes désabonné, ni les e-mails que vous avez déjà lus. Si rien ne ressort, aucune tâche n’est créée.

La routine apprend ce qui vous intéresse à partir des éléments que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les lire, ainsi qu’à partir de vos choix **Plus comme ça** et **Moins comme ça** sur chaque sélection. Les sujets qu’elle recherche apparaissent sur la carte de la routine, sous **Plus de** et **Moins de**. Touchez × pour supprimer un sujet ou ajoutez-en un vous-même. Les sujets en pointillés ont été appris automatiquement. Un nouveau récap remplace celui qui est ouvert et n’envoie jamais de notification.

La routine lit uniquement l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose à votre IA une seule question courte à leur sujet, dans une limite quotidienne, pour réduire les coûts. **Changer quand** permet de choisir l’heure. Dès que vous modifiez ses instructions, elle fonctionne comme n’importe quelle routine, selon vos instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts réguliers. Pour chacune, un court message de vœux est rédigé dans le canal où vous échangez habituellement, comme son chat WhatsApp ou votre fil d’e-mails, dans sa langue. Le message n’est envoyé que si vous l’envoyez vous-même. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos calendriers (les événements d’anniversaire et le calendrier Birthdays de Google, consultés chaque matin même s’ils ne sont pas synchronisés, ainsi que le calendrier Birthdays d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday sur une personne dans le Graph. Si aucune source ne contient encore d’anniversaire, le résultat indique **Aucune information sur les anniversaires pour le moment** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche vous propose de lire la page des anniversaires de Facebook. Touchez **Importer** et The Machine ouvre cette page dans son navigateur, fait défiler la page jusqu’à ce que tous les mois soient chargés, puis relève le nom et l’anniversaire de chaque ami. Elle indique combien d’anniversaires elle a trouvés et lesquels correspondent à des personnes de votre Graph d’après leur prénom et leur nom. Les noms associés à plusieurs personnes sont ignorés et répertoriés.

Seule l’option **Enregistrer** les ajoute, sur la page de chaque personne : l’anniversaire et, si la personne n’a pas encore de photo, sa photo de profil Facebook. L’anniversaire ou la photo que vous avez déjà renseignés restent inchangés, et une photo existante n’est jamais remplacée. Aucune information n’est écrite sur Facebook.

La routine ne lit pas à nouveau la page automatiquement. Pour cela, sélectionnez **Importer à nouveau** dans la tâche. Le navigateur doit être connecté à Facebook. Si ce n’est pas le cas, touchez **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois la session ouverte, la page est lue automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent dans le Graph de personne sont comptabilisés, et quelques noms sont affichés. **Ajouter … comme contacts personnels** les ajoute tous en une fois, même après avoir sélectionné Enregistrer : chacun avec son nom et son anniversaire, sans jamais les partager avec une Fleet Work. Les noms déjà associés à une personne dans votre Graph, ou à une personne que vous avez supprimée définitivement, sont ignorés. Les rappels d’anniversaire restent réservés aux personnes à qui vous écrivez.

L’option **Annuler** dans la tâche retire exactement ces personnes, même après avoir sélectionné **Importer à nouveau**.

**Abonnements et essais** analyse vos reçus, factures et avis de renouvellement une fois par mois et rassemble vos abonnements dans une seule tâche : le coût de chacun, sa prochaine date de facturation et un indicateur si un essai prend fin ou si le prix augmente. Seuls les abonnements dont la détection est certaine sont affichés. Si aucun n’est trouvé, aucune tâche n’est créée.

Choisissez **Garder** ou **Résilier** pour chaque abonnement. Un abonnement que vous gardez ne vous est plus proposé, sauf si son prix change. **Résilier** affiche la page de résiliation de l’abonnement ou un brouillon pour demander sa résiliation, qui ne sera envoyé que si vous l’envoyez vous-même. Entre deux exécutions, la routine vérifie chaque jour et crée une tâche lorsqu’un essai ou un renouvellement doit être facturé dans les 7 jours.

**Garder le contact** vous rappelle de temps en temps de reprendre contact avec un proche, uniquement lorsqu’il y a une vraie raison de le faire. Sur sa carte, choisissez les personnes concernées dans une courte liste de personnes avec qui vous échangez vous-même, dans les deux sens, depuis plusieurs mois. Touchez × pour supprimer une personne.

La routine vous relance uniquement si vous n’avez pas échangé depuis bien plus longtemps que d’habitude et qu’il y a quelque chose de précis à dire : une nouvelle que la personne a partagée, une promesse encore en attente ou un message auquel vous n’avez jamais répondu. Une seule tâche indique la raison et contient un court message rédigé dans le canal où vous échangez habituellement, dans sa langue. Le message ne sera envoyé que si vous l’envoyez vous-même. S’il n’y a rien à dire, aucune tâche n’est créée.

La routine envoie au maximum deux relances par semaine, une par personne et par mois, et aucune à une personne avec qui vous avez échangé récemment. **Pas nécessaire** sur une relance allonge le délai avant la prochaine relance à cette personne, et ce délai augmente à chaque fois. La routine n’envoie jamais de notification et reste personnelle : elle n’est jamais partagée avec une Fleet Work.

**Trouvailles d’occasion** surveille une recherche sur un site de vente d’occasion, comme Marktplaats, Vinted, eBay ou Facebook Marketplace. Faites une recherche avec les filtres souhaités, copiez l’adresse des résultats et collez-la après avoir sélectionné **Ajouter**. Si vous le souhaitez, ajoutez des filtres avec vos propres mots, par exemple « moins de 300, à moins de 30 km, pas “pour pièces” ». Chaque recherche est une routine distincte. Ajoutez-en une autre pour lancer une nouvelle recherche.

Toutes les 3 heures, The Machine ouvre la recherche dans son propre navigateur et repère les annonces qu’elle n’a pas encore vues. Le prix, la distance et les mots que vous avez exclus sont d’abord vérifiés à l’aide de code simple.

Chaque nouvelle annonce qui passe ces vérifications est ouverte. Votre IA évalue son état à partir de la photo et de la description, ainsi que le vendeur à partir de ses avis, de sa note et de l’ancienneté de son compte. Les bonnes annonces sont réunies dans une tâche, chacune avec sa photo, son titre, son prix et un verdict en une ligne. Touchez une annonce pour l’ouvrir dans le navigateur de The Machine.

Tant que la tâche est ouverte, les nouvelles trouvailles s’y ajoutent en haut, le nombre augmente et une nouvelle notification vous est envoyée, car les bonnes affaires partent vite. Lorsque vous marquez la tâche comme faite, la prochaine trouvaille crée une nouvelle tâche. Une exécution sans bonne trouvaille ne change rien.

La routine reste discrète et économique : une seule lecture de la recherche par exécution, au maximum 6 annonces ouvertes par exécution avec une pause entre chacune, et au maximum 40 annonces vérifiées par jour pour l’ensemble de vos recherches. Chaque vérification correspond à une question courte posée à votre IA avec une seule photo. La première exécution vérifie les quelques annonces les plus récentes et considère les autres comme déjà vues. Les exécutions suivantes ne montrent donc que les nouveautés.

Si le site vous demande de vous connecter, affiche un test anti-robot ou bloque la lecture, une tâche vous l’indique et propose **Ouvrir** pour accéder au site dans le navigateur de The Machine. Connectez-vous ou passez le test vous-même. La lecture reprendra à la prochaine exécution. The Machine ne se connecte jamais et ne résout jamais de test à votre place. Elle ne contacte jamais un vendeur, ne fait jamais d’offre et n’achète jamais rien.

**Modifier la recherche** sur la carte de la routine permet de remplacer l’adresse ou les filtres. **Changer quand** permet de choisir une autre fréquence, par exemple « toutes les 6 heures ».

Tant que la routine d’un modèle conserve ses instructions, elle s’exécute avec son propre code, sans utiliser votre forfait d’IA (Tri du spam liste d’abord en code les nouveaux e-mails d’expéditeurs inconnus et ne pose qu’une seule question courte à votre IA s’il y en a ; Garder le contact ne pose de question que sur les une ou deux personnes sélectionnées). Lui donner un nouveau nom ne change rien. Dès que vous modifiez ses instructions, elle fonctionne comme n’importe quelle routine, selon vos instructions.

Tri des newsletters et Tri du spam créent toujours une seule tâche avec un choix pour chaque e-mail. Si vous modifiez Anniversaires, la routine affiche son résultat et au maximum un brouillon, pas une tâche par personne. **Revenir au modèle** dans **Modifier** restaure ses instructions d’origine.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit ce dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme terminée.

Les routines font uniquement de la lecture : elles consultent vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient pas de messages, n’y répondent pas, ne publient rien et ne modifient rien. Seul un modèle peut modifier des e-mails, et uniquement ce que vous confirmez dans sa tâche.

Si une routine doit publier ou envoyer un message, elle effectue toutes les étapes précédant cette action et affiche le brouillon, par exemple **Publier sur X :**. Après une véritable exécution, le brouillon apparaît dans une tâche pour que vous puissiez l’approuver. Un test ne fait que l’afficher. Le nom de la tâche indique son sujet et sa destination, son bouton nomme l’action, par exemple **Publier**, et l’option **Depuis votre routine** en dessous ouvre la routine.

La tâche apparaît dans l’espace du compte utilisé pour l’envoi, par exemple dans Work pour le compte X de votre entreprise. Elle n’a donc jamais besoin d’être déplacée.

Une exécution peut suivre vos [compétences](skills.md) activées, choisies en fonction de ce que fait la routine. Seules celles qui sont pertinentes sont lues en entier. Le résultat les indique sous **Utilisées :**. Une compétence ne peut jamais faire envoyer ou modifier quoi que ce soit par une routine.

Vos routines se trouvent sous **Vos routines**, après les suggestions éventuelles. Les longs résultats sont repliés en un court aperçu. **Afficher plus**, ou un toucher sur le résultat, permet de l’ouvrir.

Chaque exécution connaît le résultat précédent et peut donc indiquer ce qui a changé depuis.

Après une exécution réussie, votre Machine peut écrire une recette pour automatiser les lectures qui se répètent, comme les e-mails ou les changements GitHub à examiner. Les exécutions suivantes commencent par les lire en code simple. L’IA sélectionne ensuite les éléments pertinents et les rédige, en utilisant moins de tokens. Une recette ne fait que lire. Si elle cesse de fonctionner, la routine lit les informations elle-même et corrige la recette. Vous la trouverez sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une seule fois. Chaque date ne donne lieu qu’à une exécution, même après un redémarrage.

Les routines s’exécutent une à la fois et attendent si l’utilisation de votre forfait d’IA est faible, comme pour toutes les tâches en arrière-plan. **Lancer maintenant** lance la routine tout de suite. Le résultat s’affiche sur sa carte lorsqu’il est prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et son fonctionnement. Sa fréquence et ses résultats précédents sont conservés. **Changer quand** permet de choisir une nouvelle fréquence avec vos propres mots, par exemple « tous les jours de semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur un ordinateur, la touche Échap ou un clic à l’extérieur annule également la modification.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles instructions et affiche le résultat. La routine reste inchangée tant que vous n’avez pas sélectionné **Enregistrer**.

**Mettre en pause** arrête les exécutions jusqu’à ce que vous sélectionniez **Reprendre** sur la carte. Les routines en pause se trouvent sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne seront pas lancées par la suite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Si vous sélectionnez **Demander des modifications** dans la tâche d’une routine ou écrivez dans son chat, et que votre remarque concerne toutes les exécutions, par exemple « n’utilise jamais d’émoji », la tâche vous propose **Modifier aussi la routine**, dans la tâche et dans son chat, sous la réponse. La routine indique les changements apportés à ses instructions. Elle ne change que si vous touchez **Modifier**. **Laisser ainsi** conserve la routine telle quelle. Une correction qui ne concerne que le brouillon ne déclenche aucune proposition.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez la routine avec vos propres mots et votre Machine s’occupe du reste.

Les utilisateurs avancés peuvent aussi faire exécuter leurs propres commandes sur leur Machine. Dans le menu ⋯, sélectionnez **Avancé : étapes de script**. **Modifier** n’affiche les étapes que si la routine en contient. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel si le champ est vide), pendant un maximum de la durée indiquée en secondes. Le résultat de la commande est transmis à l’exécution. Si aucune instruction n’est fournie, le résultat de la commande devient le résultat de l’exécution.

**Vérification** reçoit le résultat de l’exécution en entrée. Si elle se termine avec une erreur, l’exécution affiche **N’a pas marché** avec le message de la vérification. Une commande Récupérer les données qui échoue affiche le même résultat.

Une commande tient sur une seule ligne et s’exécute sans shell : pas de pipes ni de variables. Les étapes de script vous appartiennent et ne sont définies que sur votre tableau de bord. Un test ou une exécution **Essayer** lance aussi Récupérer les données et l’indique. Ces exécutions n’envoient et ne conservent toujours rien. Une routine n’envoie jamais rien. Une étape de script ne doit donc faire que lire.

## Depuis vos tâches OpenClaw

Si vous avez déjà créé des tâches planifiées dans OpenClaw, votre Machine les lit (elle ne les modifie jamais) et propose celles qui conviennent sous **Suggérée**, en tant que routines. Chacune a déjà été exécutée une fois, vous pouvez donc voir un résultat réel.

La routine conserve vos corrections apportées à la tâche et exclut ce qu’elle a envoyé ou publié. Si une tâche exécutait un script ou lisait des données collectées par une tâche script, ces éléments sont ajoutés à Récupérer les données. **Ajouter** la transforme en routine. **Non merci** empêche toute nouvelle proposition de cette tâche. Une tâche qui vous rappelait de faire quelque chose est proposée comme tâche récurrente dans To-dos.

Avant d’ajouter une suggestion, **Modifier** et **Changer quand** dans son menu ⋯ permettent de la modifier comme n’importe quelle routine. **Relancer** l’exécute immédiatement avec ses instructions actuelles pour obtenir des résultats plus récents, par exemple après un week-end calme. Elle ne fait que lire, ne s’exécute qu’une fois par toucher et son nouveau résultat remplace l’ancien.

Trois suggestions au maximum peuvent être en attente à la fois. Après une semaine d’exécutions réussies, la routine vous demande **Désactiver l’ancienne tâche OpenClaw ?**. Elle n’est désactivée que si vous touchez **Désactiver**. Vous pouvez la réactiver dans OpenClaw. **Garder** laisse les deux routines actives.

## À partir de vos habitudes

Votre Machine repère aussi les tâches que vous effectuez régulièrement et les propose comme routines sous **Suggérée**, même si vous n’utilisez pas OpenClaw. Elle recherche notamment :

- la même demande, au moins trois fois de suite, comme « récapitule les tickets d’assistance ouverts » tous les lundis ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et des e-mails d’actualité que vous recevez chaque semaine ;
- un canal Slack actif où d’autres personnes écrivent chaque semaine ;
- des e-mails que vous transférez un par un à la même personne, comme des messages de l’école ou du club à votre partenaire : un récap hebdomadaire lui évite de recevoir chaque transfert ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion indique ce qu’elle a repéré, par exemple « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a déjà été exécutée une fois, vous pouvez donc voir un résultat réel. Pensez à un récap d’équipe, à un briefing avant un appel hebdomadaire, à un résumé de l’assistance ou du développement, à un suivi de vos chiffres ou à un récap des newsletters que vous recevez.

La routine ne propose que des éléments qui vous concernent spécifiquement et sont clairement utiles : un récap d’actualités portera uniquement sur vos propres newsletters, jamais sur des actualités générales. Si rien ne convient, aucune suggestion n’est proposée.

La routine vérifie les habitudes au maximum une fois par jour et propose au maximum une nouvelle suggestion par semaine, sans envoyer de notification. **Non merci** empêche la suggestion concernée de réapparaître. Les transferts et les réponses restent associés au compte utilisé pour les envoyer. Les espaces professionnel et personnel ne sont donc pas mélangés. Tout reste sur votre Machine. Une tâche que vous clôturez régulièrement est plutôt proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue seule et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « chaque vendredi, indique-moi quelles affaires sont au point mort ».
