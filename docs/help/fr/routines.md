---
title: Routines
area: cards
summary: Les tâches que votre Machine effectue seule, à intervalles réguliers, comme un récap du lundi sur vos affaires en cours. Elle se contente de lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, routine_templates.py, mail_cleanup.py, mail_cleanup_app.py, birthdays.py, birthdays_app.py, birthdays_facebook.py, birthdays_facebook_app.py, reading_digest.py, reading_digest_app.py, subscriptions.py, subscriptions_app.py, stay_in_touch.py, stay_in_touch_app.py, dashboard/routines-page.js, dashboard/todos-digest.js, dashboard/todos-cleanup.js, dashboard/todos-facebook-birthdays.js, dashboard/todos-facebook-people.js, dashboard/todos-subs.js
order: 10
keywords: routine, daily digest, interests, automation, scheduled, every week, every morning, report, suggested, digest, newsletter, birthday, facebook birthdays, import birthdays, subscriptions, free trial, renewal, cancel subscription, stay in touch, keep in touch, reach out, check in
translated: 2be351a9cef42215
---
## En créer une

Dans la barre latérale, ouvrez **Routines**, puis décrivez en une ligne ce qu’elle doit faire et quand : « tous les lundis à 9 h, fais le point sur mes affaires en cours » ou « chaque matin en semaine, liste les e-mails auxquels je dois encore répondre ». Puis appuyez sur **Ajouter**.

Sans horaire précisé, elle s’exécute à 8 h. L’heure est celle de votre Machine. À sa première exécution, elle prend un nom court.

**Ajouter** commence par un test, pour que vous puissiez voir le résultat avant de la garder. Rien n’est envoyé ni enregistré. Ensuite, **Ajouter** l’active selon le rythme choisi, **Modifier** permet d’essayer une autre formulation ou un nouveau nom, et **Annuler** la supprime.

## Modèles

Sous **Modèles**, en bas de la page Routines, **Ajouter** active une routine prédéfinie. Elle s’exécute immédiatement, puis chaque matin à 7 h 30 (Tri du spam toutes les heures, Abonnements et essais une fois par mois). Sa carte affiche sa formulation comme pour toute routine. **Modifier** permet de changer sa formulation ou son nom.

Quand vous recevez beaucoup de newsletters et que Tri des newsletters est désactivé (25 ou plus en une semaine, provenant d’au moins 5 expéditeurs), une ligne au-dessus de vos tâches indique combien vous en avez reçues et ce que la routine ferait, avec **L’activer** et **Non merci**.

Tri du spam est proposé de la même manière si au moins 5 e-mails ont été déplacés manuellement vers les spams en une semaine. **L’activer** l’ajoute comme le fait **Ajouter** ici. Avec **Non merci**, la proposition ne s’affiche plus. C’est aussi le cas d’un modèle que vous avez déjà eu.

**Tri des newsletters** crée une tâche par espace (travail et personnel), avec les newsletters reçues la veille. Pour chacune, vous pouvez choisir **Garder** ou **Se désabonner**. La désinscription utilise le lien en un clic de la liste, ou un e-mail de désinscription envoyé depuis votre adresse si l’envoi est activé. Sinon, The Machine se désabonne sur la page de la liste, dans son propre navigateur. Si une connexion, un captcha ou des choix sont nécessaires sur cette page, c’est à vous de vous en charger : la ligne vous en indique la raison, avec **Ouvrir la page de désabonnement**.

Les reçus, commandes et avis de paiement sont exclus. Les e-mails reçus via une adresse de groupe, comme un Google Group, sont répertoriés sous le nom de leur expéditeur. La routine ne vous désabonne jamais du groupe. Si l’expéditeur n’a pas de procédure de désabonnement, sa ligne indique **Se désabonner soi-même**.

**Tri du spam** crée une tâche par espace, avec les e-mails provenant d’expéditeurs inconnus qui ressemblent à du spam. Pour chacun, choisissez **Spam** ou **Pas du spam**. Outlook déplace les spams dans le dossier Courrier indésirable, et Gmail les signale comme spam. La routine vérifie chaque heure : les spams sont généralement repérés avant que vous les voyiez. Les nouveaux spams sont ajoutés à la même tâche tant qu’elle est ouverte.

Un compte Gmail connecté en lecture seule, comme sur une Machine hébergée, ne peut pas déplacer les e-mails vers les spams. Dans ce cas, **Spam** affiche un lien pour les signaler dans Gmail, et The Machine mémorise l’expéditeur comme spam. Si aucun compte e-mail n’est connecté, le modèle affiche **Connecter vos e-mails** à la place de **Ajouter**.

Un expéditeur est considéré comme inconnu si vous ne lui avez jamais écrit. Un « Re: » ne compte comme une conversation que dans un fil auquel vous avez participé. Si un e-mail d’un expéditeur que vous avez signalé comme spam, dans la tâche ou dans votre boîte mail, arrive de nouveau dans votre boîte de réception, il apparaît dans la tâche suivante avec la mention **Déjà signalé comme spam**. Les e-mails que vous avez vous-même déplacés vers les spams aident aussi la routine à repérer les e-mails similaires.

Rien ne change tant que vous ne confirmez pas votre choix dans la tâche. Appuyez sur le nom d’un expéditeur pour lire son e-mail avant de choisir : il reste non lu et rien ne change. Dans Tri du spam, les images provenant du Web ne se chargent pas, afin que l’expéditeur ne sache pas que vous avez ouvert l’e-mail. La routine ne vous redemande pas votre avis sur les expéditeurs pour lesquels vous avez déjà fait un choix. S’il n’y a aucune newsletter ou aucun spam un jour donné, aucune tâche n’est créée. Ces tâches n’envoient jamais de notification.

Une fois que vous avez choisi pour tous les expéditeurs, la tâche indique qu’elle est terminée et affiche **Marquer comme fait**.

**Récap du jour** sélectionne chaque jour, dans une seule tâche, quelques articles de newsletters qui méritent votre attention. Chacun est accompagné d’une courte explication sur son intérêt pour vous. Appuyez sur un article pour lire l’e-mail, ou sélectionnez **Ouvrir dans votre messagerie**. La routine ne concerne que les newsletters : jamais les e-mails de personnes, les reçus ou les expéditeurs dont vous vous êtes désabonné, et jamais les e-mails que vous avez déjà lus. Si aucun article ne sort du lot, aucune tâche n’est créée.

Elle apprend ce qui vous intéresse en fonction des articles que vous ouvrez, que vous marquez d’une étoile ou que vous archivez sans les avoir lus, ainsi que de vos choix **Plus comme ça** et **Moins comme ça** pour chaque article. Les sujets sélectionnés par la routine figurent sur sa carte sous **Plus de** et **Moins de**. Appuyez sur × pour en supprimer un, ou ajoutez vos propres sujets. Les sujets en pointillés ont été repérés automatiquement. Un nouveau récap remplace celui qui est ouvert, et la routine n’envoie jamais de notification.

Elle lit uniquement l’expéditeur, l’objet et le début de chaque nouvelle newsletter, puis pose une courte question à votre IA à leur sujet, dans la limite d’un quota quotidien pour réduire les coûts. **Changer quand** permet de définir l’heure. Si vous modifiez sa formulation, elle fonctionne comme n’importe quelle routine et suit votre formulation.

**Anniversaires** crée une tâche pour chaque proche dont c’est l’anniversaire aujourd’hui : les personnes à qui vous écrivez vous-même, comme vos amis, votre famille et vos contacts réguliers. Un court message de vœux est préparé dans le canal que vous utilisez habituellement avec la personne, par exemple son chat WhatsApp ou votre fil d’e-mails, dans sa langue. Il ne sera envoyé que si vous l’envoyez. Aucune tâche n’est créée les jours sans anniversaire.

Les anniversaires proviennent de vos calendriers (les événements d’anniversaire et le calendrier Anniversaires de Google, lus chaque matin même s’ils ne sont pas synchronisés, ainsi que le calendrier Anniversaires d’Outlook), de vos contacts Google sur une Machine hébergée par vos soins et d’un champ de date nommé Birthday dans une fiche du Graph. Si aucun de ces services ne contient encore d’anniversaire, le résultat indique **Aucune information sur les anniversaires pour le moment** et explique comment en ajouter.

**Importer les anniversaires depuis Facebook** : une fois Anniversaires activé, une tâche vous propose de lire la page des anniversaires de Facebook. Appuyez sur **Importer** et The Machine ouvre la page dans son navigateur, la fait défiler jusqu’à ce que tous les mois soient chargés, puis lit le nom et l’anniversaire de chaque ami. Elle indique combien d’anniversaires elle a trouvés et quels amis correspondent à des personnes de votre Graph, en comparant leur prénom et leur nom. Les noms associés à plusieurs personnes sont ignorés et répertoriés.

Seul **Enregistrer** les ajoute, sur la page de chaque personne : l’anniversaire et, si la personne n’a pas encore de photo, sa photo de profil Facebook. Les anniversaires et les photos que vous avez déjà renseignés restent inchangés, et une photo existante n’est jamais remplacée. Rien n’est écrit sur Facebook.

La routine ne relit pas la page automatiquement : **Importer à nouveau** dans la tâche le fait. Le navigateur doit être connecté à Facebook. Si ce n’est pas le cas, appuyez sur **Se connecter à Facebook** dans la tâche et connectez-vous. Une fois la session ouverte, la page est lue automatiquement. The Machine ne se connecte jamais à votre place.

Les amis qui ne figurent dans aucun Graph sont comptabilisés et quelques noms sont affichés. **Ajouter … comme contacts personnels** les ajoute tous en une fois, y compris après avoir appuyé sur Enregistrer : chacun avec son nom et son anniversaire, sans jamais les partager avec une Fleet de travail. Les personnes dont le nom figure déjà dans votre Graph, ou qui ont été supprimées définitivement, sont ignorées. Les rappels d’anniversaire ne concernent toujours que les personnes à qui vous écrivez.

**Annuler** dans la tâche supprime exactement ces personnes, même après avoir utilisé **Importer à nouveau**.

**Abonnements et essais** lit vos reçus, factures et avis de renouvellement une fois par mois, puis rassemble vos abonnements dans une seule tâche : leur coût, la date du prochain prélèvement et un indicateur si un essai se termine ou si le prix augmente. Seuls les abonnements identifiés avec certitude sont répertoriés. Si rien n’est trouvé, aucune tâche n’est créée.

Pour chaque abonnement, choisissez **Garder** ou **Résilier**. La routine ne vous demandera plus votre avis sur un abonnement conservé, sauf si son prix change. **Résilier** affiche la page de résiliation ou un brouillon demandant la résiliation, qui ne sera envoyé que si vous l’envoyez. Entre deux exécutions, la routine vérifie chaque jour et crée une tâche lorsqu’un essai ou un renouvellement sera facturé dans les 7 jours.

**Garder le contact** vous rappelle de temps en temps de prendre des nouvelles d’un proche, uniquement s’il y a une bonne raison de le faire. Sur sa carte, choisissez les personnes à inclure dans une courte liste de contacts avec qui vous échangez vous-même, dans les deux sens et depuis plusieurs mois. Appuyez sur × pour supprimer une personne.

La routine vous relance uniquement si vous n’avez pas parlé à la personne depuis beaucoup plus longtemps que d’habitude et que vous avez quelque chose de précis à lui dire : une nouvelle qu’elle vous a annoncée, une promesse en attente ou un message auquel vous n’avez jamais répondu. Une seule tâche indique la raison de la relance et propose un court message dans le canal que vous utilisez habituellement avec cette personne, dans sa langue. Le message ne sera envoyé que si vous l’envoyez. Si vous n’avez rien à lui dire, aucune tâche n’est créée.

La routine envoie au maximum deux relances par semaine et une par personne par mois. Elle ne relance pas une personne à qui vous avez parlé récemment. Si vous choisissez **Pas nécessaire** pour une relance, la prochaine attendra plus longtemps. Ce délai augmente à chaque fois. La routine n’envoie jamais de notification et reste personnelle : elle n’est jamais partagée avec une Fleet de travail.

Tant que la routine d’un modèle conserve la formulation du modèle, elle s’exécute avec son propre code, sans utiliser votre forfait IA (Tri du spam liste d’abord en code les nouveaux e-mails d’expéditeurs inconnus et ne pose une courte question à votre IA que s’il y en a ; Garder le contact ne pose de question qu’à propos des une ou deux personnes sélectionnées). Un nouveau nom ne change rien à cela. Si vous modifiez la formulation, la routine fonctionne comme n’importe quelle routine et suit votre formulation.

Tri des newsletters et Tri du spam aboutissent toujours à la même tâche, avec un choix pour chaque e-mail. Si vous modifiez Anniversaires, la routine affiche son résultat et au maximum un brouillon, pas une tâche par personne. **Revenir au modèle**, dans **Modifier**, rétablit la formulation du modèle.

## Fonctionnement d’une routine

À l’heure prévue, votre Machine lit les informations dont elle a besoin, comme vos messages, vos réunions et le Graph, puis affiche le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec une explication) ou **N’a pas marché** (avec une explication). Une exécution qui se termine sans résultat compte comme un échec, jamais comme une tâche terminée.

Les routines se contentent de lire : vos messages, des pages Web, GitHub et des sites comme X dans le navigateur. Elles n’envoient rien, ne répondent pas, ne publient rien et ne modifient rien. Seul un modèle peut modifier des e-mails, et uniquement ce que vous confirmez dans sa tâche.

Si une routine doit publier un message ou en envoyer un, elle effectue tout ce qui précède cette étape et affiche le brouillon, par exemple **Publierait sur X :**. Après une vraie exécution, le brouillon apparaît dans une tâche à approuver. Un test ne fait que l’afficher. Le nom de la tâche indique son sujet et sa destination, son bouton indique l’étape, par exemple **Publier**, et **Depuis votre routine**, juste en dessous, ouvre la routine.

La tâche s’affiche dans l’espace du compte depuis lequel le message sera envoyé, par exemple Travail pour le compte X de votre entreprise. Elle ne vous demande donc jamais de la déplacer.

Une exécution peut suivre vos [compétences](skills.md) activées, sélectionnées selon la tâche de la routine : seules les compétences pertinentes sont lues intégralement. Le résultat les répertorie sous **Utilisées :**. Une compétence ne peut jamais faire envoyer ou modifier quoi que ce soit par une routine.

Vos routines figurent sous **Vos routines**, après les éventuelles suggestions. Les résultats longs sont réduits à un aperçu. Appuyez sur **Afficher plus**, ou sur le résultat, pour l’ouvrir.

Chaque exécution connaît le résultat précédent et peut donc indiquer les changements depuis la dernière fois.

Après une exécution réussie, votre Machine peut créer elle-même une recette pour les lectures qui se répètent à l’identique, par exemple pour déterminer quels e-mails ou changements sur GitHub examiner. Lors des exécutions suivantes, elle commence par lire ces éléments en code simple. L’IA se contente alors de sélectionner les informations pertinentes et de rédiger le résultat, avec moins de jetons. Une recette ne fait que lire. Si elle cesse de fonctionner, l’exécution reprend automatiquement et la corrige. La recette apparaît sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’accumulent pas : seule la plus récente est lancée, une seule fois. Chaque date donne lieu à une seule exécution, même après un redémarrage.

Les routines s’exécutent une par une et attendent si le quota de votre forfait IA est bas, comme pour tous les travaux en arrière-plan. **Lancer maintenant** l’exécute immédiatement. Le résultat apparaît sur sa carte une fois prêt.

## Modifier ou arrêter une routine

Ces options se trouvent dans le menu ⋯ de la routine. **Modifier** permet de changer son nom et son fonctionnement. Son horaire et ses résultats précédents sont conservés. **Changer quand** permet de définir un nouveau rythme en quelques mots, par exemple « tous les jours de la semaine à 8 h ». Les deux options proposent **Enregistrer** et **Annuler**. Sur un ordinateur, vous pouvez aussi appuyer sur Échap ou cliquer à l’extérieur pour annuler.

Dans **Modifier**, **Essayer** exécute une fois la nouvelle formulation et affiche le résultat. La routine ne change pas tant que vous n’avez pas appuyé sur **Enregistrer**.

**Mettre en pause** arrête les exécutions jusqu’à ce que vous choisissiez **Reprendre** sur sa carte. Les routines en pause figurent sous **En pause**, après vos routines. Les exécutions manquées pendant la pause ne seront pas lancées ensuite. **Arrêter** met définitivement fin à une routine.

Vous pouvez avoir jusqu’à 20 routines, y compris celles en pause. Arrêtez-en une pour en ajouter une autre.

Si vous choisissez **Demander des modifications** dans la tâche d’une routine ou écrivez dans son chat, et que votre remarque s’applique à chaque exécution, par exemple « n’utilise jamais d’émojis », la tâche vous propose **Modifier aussi la routine**. Cette option apparaît dans la tâche et dans son chat, sous la réponse. La routine indique les modifications apportées à sa formulation et ne change que si vous appuyez sur **Modifier**. **Laisser ainsi** conserve la routine en l’état. Si la correction ne concerne que le brouillon, aucune option n’est proposée.

## Avancé : étapes de script

Aucun script n’est nécessaire : décrivez la routine avec vos propres mots et votre Machine s’occupe du reste.

Les utilisateurs avancés peuvent aussi exécuter leurs propres commandes sur leur Machine. Dans le menu ⋯, choisissez **Avancé : étapes de script**. **Modifier** n’affiche les étapes que si la routine en comporte déjà. **Récupérer les données** exécute d’abord une commande, dans son dossier (votre dossier personnel si celui-ci est vide), pendant la durée indiquée, en secondes, au maximum. Le résultat de la commande est transmis à l’exécution. Si aucune formulation n’est fournie, ce résultat devient le résultat de la routine.

**Vérification** reçoit le résultat de l’exécution en entrée. Si elle se termine avec une erreur, la routine affiche **N’a pas marché** avec le message de la vérification. Une commande Récupérer les données qui échoue affiche le même résultat.

Une commande tient sur une ligne et est exécutée sans shell : pas de tubes ni de variables. Vous êtes seul responsable des étapes de script, configurées uniquement sur votre tableau de bord. Un test ou **Essayer** exécute aussi Récupérer les données et l’indique. Rien n’est envoyé ni conservé. Une routine n’envoie jamais rien : une étape de script ne doit donc que lire.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit (sans jamais les modifier) et vous propose celles qui peuvent devenir des routines sous **Suggérée**. Elles ont été exécutées une fois : vous pouvez donc consulter un résultat réel.

La routine conserve vos corrections, mais ignore ce qui a été envoyé ou publié par la tâche. Si la tâche a exécuté un script ou lu des informations recueillies par un script, celui-ci est conservé comme étape Récupérer les données. **Ajouter** en fait une routine. **Non merci** permet de ne plus vous proposer cette tâche. Si une tâche vous rappelait de faire quelque chose, elle vous est proposée sous forme de tâche récurrente dans To-dos.

Avant d’ajouter une suggestion, vous pouvez la modifier comme n’importe quelle routine avec **Modifier** et **Changer quand**, dans son menu ⋯. **Relancer** l’exécute avec sa formulation actuelle pour afficher des résultats plus récents, par exemple après un week-end calme. Elle se contente de lire, s’exécute une fois par appui et son nouveau résultat remplace l’ancien.

Vous pouvez avoir jusqu’à trois suggestions en attente. Après une semaine d’exécutions réussies, la routine vous demande **Désactiver l’ancienne tâche OpenClaw ?** Elle ne la désactive que si vous appuyez sur **Désactiver**. Vous pouvez la réactiver dans OpenClaw. **Garder** laisse les deux routines en cours.

## D’après votre activité

Votre Machine repère aussi les tâches que vous effectuez régulièrement et vous les propose comme routines sous **Suggérée**, même sans OpenClaw. Elle recherche :

- la même demande au moins trois fois de suite, comme « fais le point sur les demandes d’assistance en cours » chaque lundi ;
- un e-mail envoyé régulièrement, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et des e-mails d’actualité qui arrivent chaque semaine ;
- un canal Slack très actif, où d’autres personnes écrivent chaque semaine ;
- des e-mails que vous transférez un par un à la même personne, comme des messages de l’école ou d’un club que vous transférez à votre partenaire : un récap hebdomadaire lui évite de recevoir chaque transfert ;
- la même demande à laquelle vous répondez régulièrement, comme une approbation mensuelle pour la même personne.

Chaque suggestion explique ce qu’elle a repéré, par exemple « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines ». Elle a été exécutée une fois : vous pouvez donc consulter un résultat réel. Vous pouvez par exemple créer un récap d’équipe, un bref compte rendu avant un appel hebdomadaire, un récap de l’assistance ou du développement, un suivi de vos chiffres ou un récap des newsletters que vous recevez.

La routine ne suggère que ce qui vous concerne spécifiquement et vous sera clairement utile : un récap d’actualité ne couvre que vos propres newsletters, jamais des actualités génériques. Si rien ne correspond, aucune suggestion n’est proposée.

Elle ne fait cette vérification qu’une fois par jour au maximum et ne propose pas plus d’une nouvelle suggestion par semaine, sans envoyer de notification. **Non merci** permet de ne plus afficher cette suggestion. Les transferts et les réponses restent associés au compte depuis lequel ils ont été envoyés : Travail et Personnel ne sont pas mélangés. Tout reste sur votre Machine. Une tâche que vous terminez régulièrement vous est plutôt proposée comme tâche récurrente.

## Routines et tâches récurrentes

Une [tâche récurrente](recurring.md) vous rappelle de faire quelque chose. Une routine est une tâche que votre Machine effectue seule et dont elle vous montre le résultat. Utilisez une tâche récurrente pour « payer le loyer le premier du mois » et une routine pour « chaque vendredi, indique-moi quelles affaires sont au point mort ».
