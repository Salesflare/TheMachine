---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue automatiquement à intervalles réguliers, comme le récap de vos ventes en cours chaque lundi. Elle se contente de lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: ed2171ef31eb6213
---
## En créer une

Ouvrez **Routines** dans la barre latérale et indiquez en une ligne ce qu’elle doit faire et quand : « tous les lundis à 9 h, récapitule mes ventes en cours » ou « chaque matin de semaine, liste les e-mails auxquels je dois encore répondre ». Puis sélectionnez **Ajouter**.

Sans horaire précisé, la routine se lance à 8 h, selon l’horloge de votre Machine. Lors de sa première exécution, elle reçoit un nom court.

**Ajouter** lance d’abord un essai pour vous montrer le résultat avant que vous décidiez de la garder. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la programme pour qu’elle s’exécute à intervalles réguliers, **Modifier** permet d’essayer une autre formulation ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de la page Routines, **Ajouter** active une routine prête à l’emploi. Elle s’exécute immédiatement, puis chaque matin à 7 h 30 (le tri du spam, toutes les heures ; les abonnements et essais, une fois par mois). Sa carte affiche sa formulation, comme pour n’importe quelle routine, et **Modifier** permet de changer cette formulation ou son nom.

Quand vous recevez beaucoup de newsletters et que le tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), une ligne au-dessus de vos tâches indique combien vous en avez reçues et ce que la routine ferait. Elle propose **L’activer** et **Non merci**.

Le tri du spam est proposé de la même façon si au moins 5 e-mails ont été déplacés manuellement vers le spam en une semaine. **L’activer** l’ajoute comme le fait **Ajouter** ici. Si vous sélectionnez **Non merci**, la routine ne vous sera plus proposée. C’est également le cas des modèles que vous aviez déjà utilisés.

**Tri des newsletters** crée une tâche par catégorie (travail et personnel) qui regroupe les newsletters de la journée écoulée. Pour chacune, vous pouvez choisir **Garder** ou **Se désabonner**. La désinscription utilise le lien de désabonnement en un clic de la liste, ou envoie un e-mail de désabonnement depuis votre adresse si l’envoi est activé. Sinon, The Machine vous désabonne depuis la page de la liste, dans son propre navigateur. Si vous devez vous connecter, répondre à un captcha ou faire un choix sur cette page, la ligne vous en indique la raison et propose **Ouvrir la page de désabonnement**.

Les reçus, commandes et avis de paiement sont ignorés. Les e-mails reçus via une adresse de groupe, comme un Google Group, sont répertoriés sous le nom de leur expéditeur, et la routine ne vous désabonne jamais du groupe. Si l’expéditeur ne propose pas de moyen de désabonnement, sa ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par catégorie qui regroupe les e-mails d’expéditeurs inconnus ressemblant à du spam. Pour chacun, vous pouvez choisir **Spam** ou **Pas du spam**. Outlook déplace les spams dans le dossier Courrier indésirable et Gmail les signale comme spam. La routine vérifie toutes les heures, donc les spams sont généralement repérés avant que vous ne les voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Si Gmail est connecté en lecture seule, comme sur une Machine hébergée, les e-mails ne peuvent pas être déplacés vers le spam. Dans ce cas, **Spam** affiche un lien pour le signaler dans Gmail, et The Machine retient que l’expéditeur est un spammeur. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. La mention « Re: » ne suffit à reconnaître une conversation que si vous avez participé au fil. Si un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte de réception, arrive de nouveau, il apparaît dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés vers le spam aident aussi la routine à repérer les e-mails similaires.

Rien ne change tant que vous ne confirmez pas votre choix dans la tâche. Touchez un expéditeur pour lire son e-mail au préalable : il reste non lu et rien ne change. Dans la tâche de tri du spam, les images provenant du Web ne se chargent pas, pour que l’expéditeur ne puisse pas savoir que vous avez ouvert l’e-mail. La routine ne vous redemande pas votre avis sur les expéditeurs pour lesquels vous avez déjà fait un choix. Si aucun newsletter ou spam n’arrive dans la journée, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois votre choix fait pour chaque expéditeur, la tâche indique qu’elle est terminée et affiche **Marquer comme fait**.

**Récap du jour** sélectionne en une seule tâche, une fois par jour, les quelques articles de newsletter qui valent la peine d’être lus. Chacun indique en une phrase pourquoi il peut vous intéresser. Touchez un article pour lire l’e-mail, ou sélectionnez **Ouvrir dans votre messagerie**. La routine ne sélectionne que des newsletters : jamais les e-mails de personnes, les reçus ou les expéditeurs dont vous vous êtes désabonné, ni les e-mails que vous avez déjà lus. Si aucun article ne sort du lot, aucune tâche n’est créée.

La routine apprend ce qui vous intéresse en fonction des e-mails que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les avoir lus, ainsi que de vos choix **Plus comme ça** et **Moins comme ça** pour chaque article. Les sujets qu’elle sélectionne figurent sur la carte de sa routine, sous **Plus de** et **Moins de**. Supprimez un sujet avec × ou ajoutez-en un vous-même. Les sujets en pointillés ont été repérés automatiquement. Un nouveau récap remplace celui qui est encore ouvert, et la routine n’envoie jamais de notification.

Elle lit uniquement l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose une courte question à votre IA à leur sujet, avec une limite quotidienne, pour limiter les coûts. **Changer quand** permet de modifier l’horaire. Une fois que vous avez modifié sa formulation, la routine fonctionne comme les autres et suit vos instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts habituels. Pour chacun, la routine prépare un court message dans le moyen de communication que vous utilisez généralement avec cette personne, comme son chat WhatsApp ou votre fil de discussion par e-mail, et dans sa langue. Le message ne part que si vous l’envoyez. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos calendriers (les événements d’anniversaire Google et le calendrier Anniversaires, consultés chaque matin même s’ils ne sont pas synchronisés, ainsi que le calendrier Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date nommé Birthday sur une personne dans le Graph. Si aucune de ces sources ne contient encore d’anniversaire, le résultat indique **Aucune information sur les anniversaires pour le moment** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois la routine Anniversaires activée, une tâche vous propose de consulter la page des anniversaires de Facebook. Touchez **Importer** et The Machine ouvre la page dans son navigateur, la fait défiler jusqu’à ce que tous les mois soient chargés, puis lit le nom et la date d’anniversaire de chaque ami. Elle indique combien de personnes elle a trouvées et lesquelles correspondent à des personnes dans votre Graph, en comparant leurs prénoms et noms. Les personnes dont le nom correspond à plusieurs profils sont ignorées et répertoriées.

Seule l’action **Enregistrer** les ajoute, sur la page de chaque personne : la date d’anniversaire et, si la personne n’a pas encore de photo, sa photo de profil Facebook. Les dates d’anniversaire et les photos que vous avez déjà ajoutées restent telles quelles, et une photo existante n’est jamais remplacée. Aucune information n’est ajoutée sur Facebook.

La routine ne consulte pas à nouveau la page toute seule : utilisez **Importer à nouveau** dans la tâche pour le faire. Le navigateur doit être connecté à Facebook. Si ce n’est pas le cas, touchez **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois connecté, la routine consulte la page automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent pas dans votre Graph sont comptabilisés et quelques noms sont affichés. **Ajouter … en tant que contacts personnels** les ajoute tous en une fois, même après avoir sélectionné **Enregistrer** : chacun avec son nom et sa date d’anniversaire, sans jamais les partager avec une Fleet professionnelle. Les personnes dont le nom figure déjà dans votre Graph, ou que vous avez définitivement supprimées, sont ignorées. Les rappels d’anniversaire ne concernent toujours que les personnes à qui vous écrivez.

L’action **Annuler** dans la tâche supprime exactement ces personnes, même si vous l’utilisez après avoir sélectionné **Importer à nouveau**.

**Abonnements et essais** examine vos reçus, factures et avis de renouvellement une fois par mois et regroupe vos abonnements dans une seule tâche. Pour chacun, la tâche indique son coût, la date du prochain paiement et signale les essais qui arrivent à leur terme ou les augmentations de prix. Seuls les abonnements identifiés avec certitude sont répertoriés. Si aucun n’est trouvé, aucune tâche n’est créée.

Pour chaque abonnement, choisissez **Garder** ou **Résilier**. La routine ne vous reposera pas la question pour un abonnement conservé, sauf si son prix change. **Résilier** fournit la page de résiliation ou un brouillon de message pour demander la résiliation, qui ne sera envoyé que si vous l’envoyez. Entre deux exécutions, la routine vérifie chaque jour et crée une tâche si un essai ou un renouvellement doit être facturé dans les 7 jours.

Tant que la routine d’un modèle conserve la formulation du modèle, elle s’exécute avec son propre code, sans utiliser votre forfait IA. Le tri du spam répertorie d’abord le nouveau courrier d’expéditeurs inconnus dans le code, puis ne pose une courte question à votre IA que s’il y a des messages à examiner. Si vous changez le nom, le modèle conserve son code. Une fois que vous modifiez la formulation, la routine fonctionne comme les autres et suit vos instructions.

Le tri des newsletters et le tri du spam créent toujours une seule tâche avec un choix pour chaque e-mail. Si vous modifiez la routine Anniversaires, elle affiche son résultat et au plus un brouillon, au lieu de créer une tâche par personne. **Revenir au modèle**, dans **Modifier**, rétablit la formulation du modèle.

## Fonctionnement des routines

À l’heure prévue, votre Machine lit les informations dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat est considérée comme un échec, et non comme une exécution terminée.

Les routines se contentent de lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Seul un modèle peut modifier des e-mails, et uniquement ce que vous confirmez dans sa tâche.

Si une routine doit publier un message ou en envoyer un, elle effectue toutes les étapes jusqu’à cette action, puis affiche le brouillon, par exemple **Publier sur X :**. Après une exécution réelle, le brouillon apparaît dans une tâche à approuver. Un essai ne fait que l’afficher. Son nom indique le sujet et l’endroit où le message sera publié, son bouton nomme l’action, comme **Publier**, et **Depuis votre routine**, juste en dessous, ouvre la routine.

La tâche apparaît d’abord dans la catégorie du compte utilisé pour l’envoi, par exemple Travail pour le compte X de votre entreprise, afin que vous n’ayez jamais besoin de la déplacer.

Une routine peut suivre vos [compétences](skills.md) activées, sélectionnées en fonction de la tâche à effectuer. Seules les compétences pertinentes sont lues en entier. Le résultat les répertorie sous **Utilisées :**. Une compétence ne permet jamais à une routine d’envoyer ou de modifier quoi que ce soit.

Vos routines figurent sous **Vos routines**, après les suggestions éventuelles. Si un résultat est long, il est réduit à un aperçu. **Afficher plus**, ou le fait de toucher le résultat, permet de l’ouvrir.

Chaque exécution connaît le résultat précédent et peut donc indiquer les changements depuis la dernière fois.

Après une exécution réussie, votre Machine peut écrire elle-même une recette pour les actions de lecture identiques à chaque fois, comme les e-mails à examiner ou les modifications à repérer dans GitHub. Lors des prochaines exécutions, la recette s’exécute d’abord en code simple. L’IA sélectionne ensuite les éléments pertinents et rédige le résultat, en utilisant moins de jetons. Une recette se contente de lire. Si elle cesse de fonctionner, la routine reprend la lecture automatiquement et corrige la recette. Celle-ci apparaît sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une seule fois. Chaque date donne lieu à une seule exécution, même après un redémarrage.

Les routines s’exécutent une par une et attendent que votre forfait IA ait suffisamment de capacité, comme toutes les tâches en arrière-plan. **Lancer maintenant** lance la routine immédiatement. Son résultat apparaît sur sa carte une fois prêt.

## Modifier ou arrêter une routine

Ces actions se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et son fonctionnement. Son horaire et ses résultats précédents sont conservés. **Changer quand** permet de définir un nouvel horaire en utilisant vos propres mots, comme « tous les jours de semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur ordinateur, vous pouvez aussi appuyer sur Échap ou cliquer à l’extérieur pour annuler.

Dans **Modifier**, **Essayer** exécute une fois la nouvelle formulation et en affiche le résultat. La routine reste inchangée jusqu’à ce que vous sélectionniez **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous sélectionniez **Reprendre** sur la carte. Les routines en pause apparaissent sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne seront pas lancées par la suite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez une routine pour en ajouter une autre.

Quand vous sélectionnez **Demander des modifications** dans la tâche d’une routine ou que vous écrivez dans son chat, si votre remarque concerne toutes les exécutions, comme « n’utilise jamais d’émoji », la tâche vous propose **Modifier aussi la routine**, dans la tâche et dans son chat, sous la réponse. La routine indique les changements apportés à sa formulation, et n’est modifiée que si vous touchez **Modifier**. **Laisser ainsi** conserve la routine en l’état. Une correction qui ne concerne que le brouillon n’entraîne aucune proposition.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez avec vos propres mots ce que la routine doit faire, et votre Machine s’occupe du reste.

Pour les utilisateurs expérimentés, une routine peut aussi exécuter vos propres commandes sur votre Machine : dans le menu ⋯, sélectionnez **Avancé : étapes de script**. **Modifier** n’apparaît que si la routine contient déjà des étapes. **Récupérer les données** exécute d’abord une commande dans son dossier, ou dans votre dossier personnel s’il n’est pas précisé, pendant la durée indiquée en secondes au maximum. Le résultat affiché est transmis à la routine. Si aucune instruction n’est fournie, ce résultat constitue la réponse.

**Vérification** reçoit le résultat de l’exécution en entrée. Si la commande renvoie une erreur, la routine indique **N’a pas marché** et affiche le message de vérification. Une erreur dans une commande de récupération des données s’affiche de la même façon.

Une commande doit tenir sur une ligne et s’exécute sans shell : pas de pipes ni de variables. Les étapes de script sont les vôtres et ne sont configurées que sur votre tableau de bord. Les exécutions d’essai et l’action **Essayer** exécutent aussi la commande de récupération des données, et vous le signalent. Elles n’envoient ni ne conservent rien. Une routine n’envoie jamais rien, donc une étape de script ne doit servir qu’à lire.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit (sans jamais les modifier) et propose celles qui conviennent comme routines sous **Suggérée**. Chacune a été exécutée une fois, ce qui vous permet de voir un vrai résultat.

La routine conserve les corrections que vous avez apportées à la tâche, mais exclut ce qu’elle a envoyé ou publié. Si une tâche exécutait un script ou lisait les données recueillies par une tâche de script, celui-ci est ajouté à **Récupérer les données**. **Ajouter** en fait une routine. **Non merci** empêche la tâche de vous être à nouveau proposée. Une tâche qui vous rappelait de faire quelque chose est proposée comme tâche récurrente dans Tâches.

Avant d’ajouter une suggestion, les options **Modifier** et **Changer quand** de son menu ⋯ permettent de la modifier comme n’importe quelle routine. **Relancer** l’exécute immédiatement avec sa formulation actuelle pour afficher des résultats plus récents, par exemple après un week-end calme. Elle se contente de lire, s’exécute une fois à chaque sélection et son nouveau résultat remplace l’ancien.

Vous pouvez avoir jusqu’à trois suggestions en attente à la fois. Après une semaine d’exécutions réussies, la routine vous demande **Désactiver l’ancienne tâche OpenClaw ?** Elle ne sera désactivée que si vous sélectionnez **Désactiver**. Vous pouvez la réactiver dans OpenClaw. **Garder** laisse les deux routines actives.

## À partir de vos habitudes

Votre Machine repère aussi les tâches que vous effectuez régulièrement et vous les propose comme routines sous **Suggérée**, même si vous n’utilisez pas OpenClaw. Elle recherche :

- une même demande formulée au moins trois fois de suite, comme « récapitule les tickets d’assistance en cours » tous les lundis ;
- un e-mail que vous envoyez à intervalles réguliers, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et des e-mails d’actualité qui arrivent chaque semaine ;
- un canal Slack très actif où d’autres personnes écrivent chaque semaine ;
- des e-mails que vous transférez un à un à la même personne, comme les e-mails de l’école ou du club que vous transférez à votre partenaire : un récap hebdomadaire lui évite de recevoir chaque transfert ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion indique ce que la routine a repéré, par exemple « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a été exécutée une fois, ce qui vous permet de voir un vrai résultat. Pensez au récap de votre équipe, à un résumé avant un appel hebdomadaire, à un récap de l’assistance ou du développement, à un aperçu de vos chiffres ou à un récap de vos newsletters.

La routine ne suggère que des choses qui vous sont propres et clairement utiles : un récap de l’actualité porte uniquement sur vos newsletters, jamais sur des actualités générales. Si aucune suggestion ne convient, rien ne vous est proposé.

Elle vérifie au maximum une fois par jour et propose au plus une nouvelle suggestion par semaine, sans envoyer de notification. **Non merci** empêche cette suggestion de revenir. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés, afin que Travail et Personnel ne soient pas mélangés. Toutes ces informations restent sur votre Machine. Une tâche que vous terminez régulièrement est proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue automatiquement et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « indique-moi chaque vendredi quelles ventes sont au point mort ».
