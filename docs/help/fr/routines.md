---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue automatiquement à intervalles réguliers, comme un récap de vos opportunités en cours chaque lundi. Elle ne fait que lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription
translated: 9c3559a910b9dd37
---
## En créer une

Dans la barre latérale, ouvrez **Routines**, puis indiquez en une ligne ce qu’elle doit faire et quand : « chaque lundi à 9 h, résume mes opportunités en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Puis sélectionnez **Ajouter**.

Sans horaire précisé, elle s’exécute à 8 h, selon l’horloge de votre Machine. La première fois qu’elle s’exécute, elle reçoit un nom court.

**Ajouter** lance d’abord un test, pour vous montrer le résultat avant que vous la gardiez. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** la programme à la fréquence choisie, **Modifier** permet d’essayer d’autres mots ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Dans **Modèles**, en bas de la page Routines, sélectionnez **Ajouter** pour activer une routine prête à l’emploi. Elle s’exécute immédiatement, puis chaque matin à 7 h 30 (le tri du spam, toutes les heures ; les abonnements et essais, une fois par mois). Sa carte affiche les instructions, comme pour n’importe quelle routine. **Modifier** permet de les changer ou de modifier son nom.

Quand vous recevez beaucoup de newsletters et que le tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), une ligne au-dessus de vos tâches indique combien vous en avez reçu et ce que la routine ferait. Elle propose **L’activer** ou **Non merci**.

Le tri du spam est proposé de la même façon si au moins 5 e-mails ont été déplacés manuellement vers les spams en une semaine. **L’activer** l’ajoute comme le fait **Ajouter** ici. Si vous sélectionnez **Non merci**, la proposition ne s’affichera plus. Un modèle que vous avez déjà utilisé ne vous sera jamais proposé.

**Tri des newsletters** crée une tâche par espace (professionnel et personnel) avec les newsletters reçues la veille. Pour chacune, vous pouvez sélectionner **Garder** ou **Se désabonner**. Le désabonnement utilise le lien en un clic de la liste, ou un e-mail de désabonnement envoyé depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne depuis la page de la liste, dans son propre navigateur. Si la page demande de vous connecter, de résoudre un captcha ou de faire un choix, vous devez vous en charger. La ligne en indique la raison et propose **Ouvrir la page de désabonnement**.

Les reçus, commandes et avis de paiement sont exclus. Les e-mails reçus via une adresse de groupe, comme un Google Group, sont classés sous le nom de leur auteur et ne vous désabonnent jamais du groupe. Si l’expéditeur n’a pas de lien de désabonnement, la ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace avec les e-mails d’expéditeurs inconnus qui semblent être des spams. Pour chacun, vous pouvez sélectionner **Spam** ou **Pas du spam**. Outlook déplace les spams dans le dossier Courrier indésirable et Gmail les signale comme spams. La vérification a lieu toutes les heures, les spams sont donc généralement repérés avant que vous ne les voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Avec un compte Gmail connecté en lecture seule, comme sur une Machine hébergée, les e-mails ne peuvent pas être déplacés vers les spams. Dans ce cas, **Spam** fournit un lien pour les signaler dans Gmail, et The Machine mémorise l’expéditeur comme spam. Si aucun compte de messagerie n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. Un « Re: » ne compte comme une conversation que dans un fil auquel vous avez participé. Si un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte de réception, arrive de nouveau, il apparaît dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés vers les spams aident aussi la routine à repérer les e-mails similaires.

Rien ne change tant que vous ne confirmez pas votre choix dans la tâche. Sélectionnez un expéditeur pour lire d’abord son e-mail : il reste non lu et rien ne change. Dans le tri du spam, les images provenant du Web ne se chargent pas, pour que l’expéditeur ne puisse pas savoir que vous avez ouvert l’e-mail. Vous ne serez pas sollicité à nouveau pour les expéditeurs dont vous avez déjà fait le choix. S’il n’y a pas de newsletter ou de spam un jour donné, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois que vous avez fait un choix pour chaque expéditeur, la tâche indique qu’elle est terminée et propose **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour, dans une seule tâche, quelques articles de newsletters qui valent la peine d’être lus. Une ligne indique pourquoi chacun peut vous intéresser. Sélectionnez un article pour lire l’e-mail, ou utilisez **Ouvrir dans votre messagerie**. La routine ne sélectionne que des newsletters, jamais des e-mails de personnes, des reçus ou des expéditeurs dont vous vous êtes désabonné, ni des e-mails déjà lus. Si rien ne se démarque, aucune tâche n’est créée.

Elle apprend ce qui vous intéresse en fonction des e-mails que vous ouvrez, marquez d’une étoile ou archivez sans les lire, ainsi que de vos choix **Plus comme ça** et **Moins comme ça** pour chaque sélection. Les sujets qu’elle privilégie figurent sur la carte de la routine, sous **Plus de** et **Moins de**. Pour en supprimer un, sélectionnez ×, ou ajoutez vos propres sujets. Les sujets en pointillés ont été appris automatiquement. Un nouveau récap remplace celui qui est encore ouvert et n’envoie jamais de notification.

La routine ne lit que l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose une courte question à votre IA à leur sujet, avec une limite quotidienne pour réduire les coûts. **Changer quand** permet de modifier l’horaire. Dès que vous modifiez les instructions, la routine s’exécute comme n’importe quelle autre, en suivant vos instructions.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts habituels. Pour chacun, un court message de vœux est rédigé dans le canal que vous utilisez habituellement avec cette personne, comme son chat WhatsApp ou votre fil d’e-mails, et dans sa langue. Le message n’est envoyé que si vous l’envoyez vous-même. Si personne ne fête son anniversaire ce jour-là, aucune tâche n’est créée.

Les anniversaires proviennent de vos calendriers (les événements d’anniversaire Google et le calendrier Anniversaires, consultés chaque matin même s’ils ne sont pas synchronisés, ainsi que le calendrier Anniversaires d’Outlook), de vos contacts Google sur une Machine auto-hébergée et d’un champ de date intitulé Birthday sur une personne du Graph. Si aucune de ces sources ne contient encore d’anniversaire, le résultat indique **Aucune info sur les anniversaires** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois les anniversaires activés, une tâche vous propose de consulter la page des anniversaires de Facebook. Sélectionnez **Importer** : The Machine ouvre la page dans son navigateur, fait défiler la page jusqu’à ce que tous les mois soient chargés, puis relève le nom et l’anniversaire de chaque ami. Elle indique combien d’anniversaires ont été trouvés et quelles personnes correspondent à des personnes de votre Graph, d’après leur prénom et leur nom. Les noms associés à plusieurs personnes sont ignorés et répertoriés.

Seul le bouton **Enregistrer** les ajoute, sur la page de chaque personne : l’anniversaire et la photo de profil Facebook, si la personne n’a pas encore de photo. Les anniversaires et les photos que vous avez ajoutés restent en place, et une photo déjà présente n’est jamais remplacée. Aucune information n’est écrite sur Facebook.

La routine ne consulte pas Facebook à nouveau automatiquement. Pour relancer l’importation, sélectionnez **Importer à nouveau** dans la tâche. Le navigateur doit être connecté à Facebook. Si ce n’est pas le cas, sélectionnez **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois la session ouverte, la page est consultée automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent pas dans votre Graph sont comptabilisés, et quelques noms sont affichés. **Ajouter … comme contacts personnels** les ajoute tous en une seule fois, y compris après avoir sélectionné Enregistrer. Chaque personne est ajoutée avec son nom et son anniversaire, sans jamais être partagée avec une Fleet professionnelle. Les personnes dont le nom figure déjà dans votre Graph, ou qui ont été supprimées définitivement, sont ignorées. Les rappels d’anniversaire ne concernent toujours que les personnes à qui vous écrivez.

Le bouton **Annuler** de la tâche supprime exactement ces personnes, même après avoir sélectionné **Importer à nouveau**.

**Abonnements et essais** consulte vos reçus, factures et avis de renouvellement une fois par mois et regroupe vos abonnements dans une seule tâche. Pour chacun, vous voyez son coût, la date du prochain prélèvement et un indicateur si un essai se termine ou si le prix augmente. Seuls les abonnements identifiés avec certitude sont affichés. Si aucun abonnement n’est trouvé, aucune tâche n’est créée.

Pour chaque abonnement, sélectionnez **Garder** ou **Résilier**. La routine ne vous demandera plus quoi faire pour un abonnement que vous gardez, sauf si son prix change. **Résilier** fournit la page de résiliation de l’abonnement ou un brouillon de demande de résiliation, qui ne sera envoyé que si vous l’envoyez vous-même. Entre deux exécutions mensuelles, la routine vérifie chaque jour et crée une tâche si un essai se termine ou si un renouvellement est prévu dans les 7 jours.

Tant que la routine d’un modèle conserve ses instructions, elle s’exécute avec son propre code, sans utiliser votre forfait IA (le tri du spam commence par répertorier en code les nouveaux e-mails provenant d’expéditeurs inconnus, et ne pose qu’une courte question à votre IA s’il y en a). Si vous modifiez son nom, elle conserve cette configuration. Dès que vous modifiez ses instructions, elle s’exécute comme n’importe quelle autre, en suivant vos instructions.

Le tri des newsletters et le tri du spam produisent toujours la même tâche, avec un choix pour chaque e-mail. Si vous modifiez la routine Anniversaires, elle affiche son résultat et, au maximum, un brouillon, au lieu de créer une tâche pour chaque personne. Dans **Modifier**, **Revenir au modèle** rétablit les instructions du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit les informations dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat est considérée comme un échec, jamais comme une tâche terminée.

Les routines ne font que lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Seul un modèle peut modifier des e-mails, et uniquement après votre confirmation dans sa tâche.

Quand une routine doit publier ou envoyer un message, elle effectue toutes les étapes précédentes et affiche le brouillon, par exemple **Publier sur X :**. Après une exécution réelle, le brouillon apparaît sous forme de tâche à approuver. Un test ne fait que l’afficher. Son nom indique le sujet et l’endroit où le contenu sera publié. Le bouton indique l’action, comme **Publier**, et le lien **Depuis votre routine** qui apparaît en dessous ouvre la routine.

La tâche est d’abord placée dans l’espace du compte depuis lequel elle sera envoyée, par exemple Professionnel pour le compte X de votre entreprise. Elle ne vous demande donc jamais de la déplacer.

Une exécution peut suivre vos [compétences](skills.md) activées, choisies en fonction de ce que fait la routine. Seules les compétences pertinentes sont lues en entier. Le résultat les répertorie sous **Utilisées :**. Une compétence ne peut jamais faire envoyer ou modifier quoi que ce soit par une routine.

Vos routines figurent sous **Vos routines**, après les suggestions éventuelles. Un résultat long est réduit à un bref aperçu. Sélectionnez **Afficher plus**, ou le résultat lui-même, pour l’ouvrir.

Chaque exécution connaît le dernier résultat et peut donc indiquer ce qui a changé depuis.

Après une exécution réussie, votre Machine peut créer une recette pour automatiser les lectures qui se répètent, comme les e-mails ou les modifications GitHub à examiner. Les exécutions suivantes commencent par lire ces éléments à l’aide de code simple. L’IA sélectionne ensuite ce qui compte et le rédige, avec moins de jetons. Une recette ne fait que lire. Si elle cesse de fonctionner, la routine s’exécute sans elle et la corrige. La recette apparaît sous **Avancé : étapes de script**, dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une fois. Chaque date ne donne lieu qu’à une seule exécution, même après un redémarrage.

Les routines s’exécutent une à la fois et attendent si le niveau d’utilisation de votre forfait IA est bas, comme toutes les tâches en arrière-plan. **Lancer maintenant** lance la routine immédiatement. Son résultat apparaît sur sa carte dès qu’il est prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et ses instructions. Ses horaires et ses résultats précédents sont conservés. **Changer quand** permet de définir une nouvelle fréquence avec vos propres mots, par exemple « chaque jour de semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur un ordinateur, vous pouvez aussi appuyer sur Échap ou cliquer en dehors pour annuler.

Dans **Modifier**, **Essayer** exécute une fois les nouvelles instructions et affiche le résultat. La routine reste inchangée tant que vous n’avez pas sélectionné **Enregistrer**.

**Mettre en pause** suspend les exécutions jusqu’à ce que vous sélectionniez **Reprendre**. Les routines en pause sont regroupées sous **En pause**, en bas de la page. Les exécutions manquées pendant la pause ne seront pas lancées ensuite. **Arrêter** met définitivement fin à une routine.

Quand vous utilisez **Demander des modifications** dans la tâche d’une routine, ou que vous écrivez dans son chat, et que votre demande concerne toutes les exécutions, par exemple « n’utilise jamais d’émojis », la tâche vous propose **Modifier aussi la routine**, sur la tâche et dans son chat, sous la réponse. Elle indique les changements apportés aux instructions de la routine. La routine ne change que si vous sélectionnez **Modifier**. **Laisser ainsi** conserve la routine telle quelle. Une correction qui ne concerne que ce brouillon ne déclenche pas cette proposition.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez avec vos propres mots ce que la routine doit faire et votre Machine s’occupe du reste.

Pour les utilisateurs avancés, une routine peut aussi exécuter vos propres commandes sur votre Machine. Dans le menu ⋯, sélectionnez **Avancé : étapes de script**. **Modifier** affiche les étapes uniquement si la routine en contient déjà. **Récupérer les données** exécute d’abord une commande dans son dossier (votre dossier personnel si le champ est vide), pendant la durée maximale indiquée en secondes. Le résultat affiché est transmis à l’exécution pour qu’elle l’utilise. Si aucune instruction n’est fournie, ce résultat constitue la réponse.

**Vérification** reçoit le résultat de l’exécution en entrée. Si la commande se termine avec une erreur, l’exécution affiche **N’a pas marché** et le message de la vérification. Une commande Récupérer les données qui échoue affiche le même message.

Une commande doit tenir sur une seule ligne et est exécutée sans shell : les tubes et les variables ne sont pas pris en charge. Les étapes de script vous appartiennent et ne sont configurables que sur votre tableau de bord. Un test ou une exécution avec **Essayer** lance aussi Récupérer les données et l’indique. Ces exécutions n’envoient et ne conservent toujours rien. Une routine n’envoie jamais rien, une étape de script doit donc se limiter à la lecture.

## Depuis vos tâches OpenClaw

Si vous avez créé des tâches planifiées dans OpenClaw, votre Machine les lit (sans jamais les modifier) et propose celles qui peuvent être converties en routines, sous **Suggérée**. Chacune a été exécutée une fois, vous pouvez donc voir un résultat réel.

Elle conserve vos corrections apportées à la tâche et ignore ce qu’elle a envoyé ou publié. Si une tâche a exécuté un script, ou lu les données collectées par une tâche de script, celui-ci est repris dans Récupérer les données. **Ajouter** la convertit en routine. **Non merci** signifie que cette tâche ne vous sera plus jamais proposée. Une tâche qui vous rappelait de faire quelque chose est plutôt proposée sous forme de tâche récurrente dans Tâches.

Avant d’ajouter une suggestion, utilisez **Modifier** et **Changer quand** dans son menu ⋯ pour la modifier comme n’importe quelle routine. **Relancer** l’exécute maintenant avec les instructions actuelles, pour obtenir un résultat plus récent, par exemple après un week-end calme. Elle ne fait que lire, ne s’exécute qu’une fois par sélection et son nouveau résultat remplace l’ancien.

Trois suggestions au maximum peuvent être en attente à la fois. Après une semaine d’exécutions réussies, la routine demande **Désactiver l’ancienne tâche OpenClaw ?**. Elle ne sera désactivée que si vous sélectionnez **Désactiver**. Vous pouvez la réactiver dans OpenClaw.

## À partir de vos habitudes

Votre Machine repère aussi les tâches que vous effectuez régulièrement et les propose sous **Suggérée**, même sans OpenClaw. Elle recherche notamment :

- la même demande au moins trois fois de suite, par exemple « résume les demandes d’assistance en cours » chaque lundi ;
- un e-mail que vous envoyez régulièrement, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et des e-mails d’actualités que vous recevez chaque semaine ;
- un canal Slack très actif dans lequel d’autres personnes écrivent chaque semaine ;
- des e-mails que vous transférez un par un à la même personne, par exemple des e-mails de l’école ou d’un club à votre partenaire. Un récap hebdomadaire lui évite de les transférer ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion indique ce qu’elle a repéré, par exemple « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a été exécutée une fois, vous pouvez donc voir un résultat réel. Pensez à un récap d’équipe, à un briefing avant un appel hebdomadaire, à un résumé des demandes d’assistance ou de développement, à un suivi de vos chiffres ou à un récap des newsletters que vous recevez.

Seules les suggestions qui vous sont propres et clairement utiles sont proposées : un récap d’actualités ne porte que sur vos propres newsletters, jamais sur des actualités génériques. Si rien ne correspond, aucune suggestion n’est proposée.

La routine vérifie vos habitudes une fois par jour au maximum et propose une seule nouvelle suggestion par semaine au maximum, sans notification. **Non merci** signifie que cette suggestion ne réapparaîtra pas. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés. Les espaces Professionnel et Personnel ne sont donc pas mélangés. Tout reste sur votre Machine. Une tâche que vous terminez régulièrement est plutôt proposée sous forme de tâche récurrente.

## Routines et tâches récurrentes

Une tâche récurrente (recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue automatiquement et dont elle vous présente le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « dis-moi chaque vendredi quelles opportunités sont au point mort ».
