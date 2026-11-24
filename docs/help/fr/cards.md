---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre intervention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 32c3a3e62b74548f
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre intervention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, la dernière étape que vous avez confirmée, comme l’envoi d’un formulaire ou la résolution d’un problème, a abouti pendant votre absence. Elle reste là jusqu’à ce que vous touchiez **Compris**, pendant un jour au maximum. Votre téléphone en est aussi informé.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par ce qui arrive à échéance demain au plus tard. Chaque tâche porte l’un de ces statuts : **Préparée** (un brouillon ou un résultat est prêt. **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (elle nécessite d’abord votre décision ou une réponse. Si le travail ne peut pas continuer ou être utilisé sans une information que vous seul avez, comme un prix, un fait ou un choix, une ligne sous le titre le précise), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches sans nouveauté depuis une semaine sont repliées ici (voir ci-dessous).
- **En attente des autres** : les tâches dont la prochaine étape dépend de quelqu’un d’autre sont repliées ici (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, ainsi que celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec l’heure de fin, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. » Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. La tâche reste ouverte. » **Ouvrir** vous y conduit. La recherche retrouve une tâche à partir de son titre ou de son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain au plus tard s’affichent d’abord, suivies des questions de votre Fleet, des suivis d’un tableau, puis du reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine pense que la tâche est terminée, par exemple « PR #3451 a été fusionnée », mais qu’elle n’a pas encore été clôturée. **Rouvrir** la remet dans votre liste et votre Machine en tire des enseignements. Ces tâches ne sont jamais signalées comme en retard. Quand un message l’indique, la tâche se ferme automatiquement après un jour, avec **Annuler**. Sinon, elle attend que vous la **Marquer comme fait**.

Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi automatiquement. Une réponse qui indique qu’un fichier est joint alors qu’il ne l’est pas ne ferme pas la tâche.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, par exemple sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche le signale clairement : « Ce n’est pas Sam Lee. » Elle indique la personne par son adresse, jamais par le nom qu’elle a utilisé. Votre Machine vérifie le message auprès de la personne à l’adresse que vous connaissez déjà, jamais auprès de son auteur.

Une tâche qui attend toujours quelqu’un d’autre, pour une vérification ou une réponse par exemple, indique l’étape concernée sous **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est également le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si elle est dépassée. Elle précise alors qui doit encore répondre.

Quand une tâche dépend d’un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se ferme automatiquement avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier la tâche.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les nouvelles s’affichent en premier après quelques jours d’absence. Il n’y a pas de nouveauté si aucun nouveau message n’a été reçu et si vous n’avez rien fait sur la tâche, comme envoyer un message dans le chat, la modifier ou la mettre en attente. La consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque toutes les tâches de Plus anciennes comme inutiles après une seule confirmation, comme le fait **Pas nécessaire** pour une tâche à la fois, avec **Annuler**. Toute nouveauté sur une tâche la fait revenir dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine pose une fois la question : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve et la question ne sera plus posée. Sans réponse la semaine suivante, elle est repliée dans Revient plus tard. Elle n’est alors plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. Si vous l’ouvrez, envoyez un message dans son chat, la modifiez, la mettez en attente ou recevez un nouveau message, elle réapparaît.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut donner lieu à une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre intervention, votre Machine se met en veille devant une liste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, sa ligne l’indique, avec **Vérifier maintenant** en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur conservent le même choix. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’affichage complet. Une alerte concernant votre Machine elle-même, comme une partie qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire le récap, avec **Copier** pour le coller où vous voulez. Une fois ouvert ou après avoir touché son **×**, il reste sur tous vos appareils jusqu’au prochain récap.

S’il n’y a pas de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso ou uniquement pour la vue sélectionnée.

Une tâche liée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. L’option **Projet** sous **Détails** permet de modifier le projet ou de retirer la tâche du projet. Voir [Les tâches d’un projet](projects.md#a-project-s-to-dos).

L’option **Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les sources qu’elle peut lire et les moyens qu’elle peut utiliser pour envoyer des messages changent avec elle. **Annuler** dans la notification permet de la déplacer à nouveau.

Quand une tâche doit passer dans votre autre domaine pour continuer et que tous les messages concernés s’y trouvent, elle s’y déplace automatiquement et continue. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge avant que vous ne touchiez cette option. Une tâche que vous avez ajoutée sans choisir Travail ou Perso se déplace automatiquement dès qu’elle trouve sa place. En attendant, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez désignée comme Perso compte comme Perso. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille reçu à votre adresse professionnelle, est considérée comme Perso dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte personnelle ou une [promesse](promises.md) liée au travail, est considéré comme Travail dès le départ.

Une tâche que vous avez déplacée ou placée vous-même reste toujours à l’endroit que vous avez choisi. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais où elle répond : la réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une telle tâche Perso répond tout de même depuis l’adresse professionnelle qui a reçu l’e-mail et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

Quand au moins deux tâches vous attendent, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec le brouillon complet et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le processus. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un récap indique ce qui a été envoyé ou clôturé et ce qui est encore en préparation.

Les tâches qui vous posent une question ne sont pas incluses : elles attendent votre réponse, pas une action.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages quand elle en a reçu 40 ou quand le plus ancien message d’une personne est en attente depuis 15 minutes. Les newsletters, notifications et reçus sont inclus à la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications affiche « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre la section Vérifications sous Connexions. Si des tâches sont ouvertes, cette option se trouve en haut sur ordinateur. Une courte ligne n’apparaît que pendant une vérification, ou lorsqu’une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare ont leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle ne concerne que cette vérification : les tâches déjà dans votre liste restent inchangées. Si une nouvelle tâche attend un meilleur moment, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’auteur, l’objet ou les premiers mots, et la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « En copie uniquement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a fourni qu’une vague. Touchez un élément pour le lire avec les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Touchez l’option sous ces éléments pour afficher le reste. Un nombre après un nom, comme (3), indique combien de nouveaux messages ce chat contient. Une notification sur votre téléphone concernant un message déjà dans la liste ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour comprendre le contexte et repérer les promesses, mais ne sont pas de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni affichés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche indique la prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** vous permet de préciser ce qu’il faut changer : la façon de faire la tâche ou, une fois le brouillon prêt, ce qu’il faut modifier dans celui-ci. **Marquer comme fait** indique que la tâche est traitée : cette option est visible sur une tâche prête sans brouillon ou qui vous pose une question, et se trouve sinon en haut du menu **…**. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Faites glisser le message pour le supprimer ou déplacez-le hors de l’écran avec la souris pour le fermer plus rapidement. La modification est conservée.

Pour que la tâche soit faite autrement, indiquez-le dans son **Chat**. La réponse précise uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si une modification n’a pas pu être faite, comme celle d’une échéance, la réponse vous le signale.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la vérifier](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une fréquence définie](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** réaffiche une tâche clôturée. Elle réapparaît également automatiquement quand quelque chose de nouveau se produit, par exemple un nouveau message de la personne concernée, mais pas après votre propre réponse. La tâche indique alors quand elle est réapparue et est classée comme nouvelle. Son chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche qui indique le montant, l’échéance et les informations de paiement fournies sur la facture. Les factures payées automatiquement, par exemple par prélèvement ou avec une carte enregistrée, ne créent pas de tâche. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur qui confirme la réception du paiement, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’est utile que jusqu’à un moment donné, comme une confirmation à obtenir avant une réunion, se ferme automatiquement une fois ce moment passé. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les chats de groupe, et attend que Slack les ait lues. Quand un message ultérieur montre que la tâche est déjà terminée, par exemple que la personne a été sollicitée et a répondu oui, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez à nouveau sur **Envoyer** pour envoyer votre brouillon tel quel.

Quand un message plus récent modifie le plan, par exemple si une fête a lieu dans un autre endroit ou si une réservation est annulée, The Machine met elle-même ses tâches à jour. Une tâche toujours utile suit le nouveau plan. Si rien ne reste à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et en précise la raison. **Annuler** permet de la rétablir pendant un jour.

Lors de vos premières tâches, une courte astuce présente les actions importantes : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. Une astuce disparaît définitivement lorsque vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique qui attend depuis le plus longtemps votre réponse. Cette réponse est rédigée en premier, pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation si la tâche porte sur celle-ci, mais pas simplement parce qu’une personne y travaille, le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom ou une organisation affiche sa photo ou son logo si le Graph en a un, et ses initiales sinon. Un logo difficile à lire en petit, par exemple du texte blanc sur un fond transparent ou un long nom, affiche aussi l’initiale.

Parfois, une ligne discrète indique les informations manquantes, par exemple « Dernier contact il y a 12 jours par e-mail, aucun échange depuis ». Elle s’affiche lorsque le dernier échange avec la personne date d’il y a longtemps ou reste sans réponse, et précise les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Si un canal non connecté est mentionné, l’option Connecter à côté ouvre la page de connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si cela change. Une tâche terminée garde son titre et indique en dessous comment elle s’est terminée, par exemple « Terminé : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service concerné. Touchez-la pour lire le fil. Le brouillon affiche le logo du service auquel il est destiné, pour voir tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon s’appuie sur une contribution faite ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « Basé sur le message de Sam dans #ops ». Touchez-la pour lire le message. Ce message est remplacé lorsqu’une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, du plus ancien au plus récent : les messages précédant celui auquel la tâche se rapporte, puis les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message lié à la tâche porte la mention « Cette tâche » et s’ouvre directement. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste d’un fil d’e-mails est replié au-dessus et en dessous du message concerné.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification. Il porte la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, l’e-mail s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, les adresses en Cci ou une adresse de réponse différente. Il n’y a rien à afficher si aucun détail ne s’y ajoute.

Une réponse dans un fil Slack affiche aussi les messages qui précèdent le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche, que vous pouvez modifier en touchant l’un d’eux, votre dernière note et le résultat d’un agent de programmation. Touchez le titre pour ouvrir le chat. Une tâche terminée reste concise. Le message dont elle provient se trouve sous **Détails**.

Une tâche en attente indique un lien vers votre dernier message à la personne concernée, celui auquel vous attendez une réponse : « E-mail à Pat · mar. ».

## Créer une tâche soi-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, sous **+** sur téléphone ou avec `N`) ajoute une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, la tâche est classée selon les personnes et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue. L’icône du calendrier propose des dates rapides et **Choisir une date**.
- **Répéter** : la tâche revient selon une fréquence définie. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour retirer un fichier.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez ajouter uniquement des fichiers : elle complète la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour l’afficher en taille réelle.
