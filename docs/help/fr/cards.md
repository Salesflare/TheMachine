---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre intervention, prête à recevoir votre accord. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fcb9a016c9af8551
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement si quelque chose nécessite votre intervention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un ticket, a abouti pendant votre absence. Elle reste là jusqu’à ce que vous touchiez **Compris**, au maximum un jour, et votre téléphone en est aussi informé.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par ce qui arrive à échéance d’ici demain. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (elle nécessite d’abord votre décision ou votre réponse ; quand le travail ne peut pas avancer ou être utilisé sans une information que vous seul avez, comme un prix, un fait ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, les messages [à envoyer plus tard](send-later.md) et ceux qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard, jusqu’à lundi. » Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. La tâche reste ouverte. » **Ouvrir** permet d’y accéder. La recherche retrouve une tâche par son titre ou son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou à échéance d’ici demain, puis les questions de votre Fleet, les suivis d’un tableau, puis le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et quand elle est terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain apparaissent d’abord, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine considère la tâche comme terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et permet à votre Machine d’en tirer des enseignements. Ces tâches ne sont jamais signalées comme en retard. Si un message l’indique, la tâche se clôture automatiquement après un jour, avec **Annuler**. Sinon, elle attend que vous choisissiez **Marquer comme fait**.

Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement. Une réponse indiquant qu’un fichier est joint alors qu’il ne l’est pas ne clôture pas la tâche.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, par exemple sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le nom affiché est celui associé à l’adresse réelle, jamais celui utilisé par l’expéditeur. Votre Machine vérifie ce type de message auprès de la personne à l’adresse que vous avez déjà, jamais auprès de l’expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple pour une révision ou une réponse, indique l’étape sous **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après une question que vous avez renvoyée : la tâche revient le matin avant son échéance, à l’échéance si elle est plus tard dans la journée, ou le lendemain matin une fois l’échéance passée. Elle indique alors qui doit encore répondre.

Lorsqu’une tâche porte sur un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** indique ce résultat sous **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche qui n’a rien de nouveau depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les tâches récentes apparaissent en premier après quelques jours d’absence. Rien de nouveau signifie qu’il n’y a pas de nouveau message et que vous n’avez rien fait sur la tâche, comme envoyer un message dans le chat, la modifier ou la mettre en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires toutes les tâches de Plus anciennes après une seule confirmation, comme le fait **Pas nécessaire** pour chacune d’elles, avec **Annuler**. Tout nouvel élément sur une tâche la ramène dans Pour vous.

Une tâche à laquelle personne n’a touché pendant une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve et la question ne réapparaît plus. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et elle n’est plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. Le fait de l’ouvrir, d’envoyer un message dans le chat, de la modifier, de la mettre en attente ou de recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet inactif sans tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre intervention, votre Machine fait une pause et affiche une liste vide. Pendant une vérification, elle se réveille et l’indique. Si une vérification a échoué ou tarde, une ligne le signale, avec **Vérifier maintenant** en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’une catégorie. Votre téléphone et votre ordinateur affichent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, par exemple un composant qui redémarre sans cesse, ne relève ni du Travail ni du Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre catégorie : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le dernier récap du matin ou du soir et son contenu, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire ce récap, puis **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou que vous touchez son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne indique **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso, ou uniquement pour la catégorie sélectionnée.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet** sous **Détails** permet de modifier le projet ou de retirer la tâche du projet. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche dans votre autre domaine. Les éléments qu’elle peut lire et envoyer sont déplacés avec elle. **Annuler** dans la note permet de la ramener à son emplacement précédent.

Lorsqu’une tâche doit passer dans votre autre domaine pour avancer et que tous les messages concernés s’y trouvent, elle y est déplacée automatiquement et le travail continue. Sinon, **Déplacer vers Travail** apparaît, et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès que son domaine est identifié. D’ici là, elle n’est classée ni dans Travail ni dans Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise, et une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est classée dans Perso dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte personnelle ou une [promesse](promises.md) liée au travail, est classé dans Travail dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, mais pas où la réponse est envoyée : elle est toujours envoyée dans la conversation concernée, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche classée dans Perso répond tout de même depuis l’adresse professionnelle à laquelle son e-mail a été envoyé. Elle n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec le brouillon complet et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie l’élément affiché, `S` le met en attente, `→` le passe et Échap arrête le processus. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, le récapitulatif indique ce qui a été envoyé ou clôturé, ainsi que ce qui est encore en préparation.

Une tâche qui vous pose une question n’est pas incluse : elle attend votre réponse, pas un toucher.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux éléments dès que 40 messages sont en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont inclus lors de la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, afin que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à une heure d’inactivité. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher **Détails**, qui ouvre Vérifications sous Connexions. Si des tâches sont ouvertes, l’option apparaît en haut de la liste sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou tarde. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification ayant lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle concerne uniquement cette vérification : les tâches déjà présentes dans votre liste restent inchangées. Si une nouvelle tâche attend un moment plus approprié, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Touchez la ligne pour afficher chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle aucune tâche n’était nécessaire, par exemple « En copie uniquement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a fourni qu’une vague. Touchez un élément pour le lire avec le contexte de la conversation.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir la suite. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié n’apparaît qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour comprendre le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails de The Machine qui vous sont adressés, comme le récap du matin ou un avis de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche indique la prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qui doit changer : la façon de procéder ou, une fois le brouillon prêt, ce qu’il faut modifier. **Marquer comme fait** indique que la tâche est traitée. L’option est visible sur une tâche prête sans brouillon ou sur une tâche qui vous pose une question ; sinon, elle se trouve en haut de **…**. La tâche quitte aussitôt la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou faites-le glisser hors de l’écran avec la souris pour le fermer plus tôt. La modification est conservée.

Pour procéder autrement, indiquez-le dans le **Chat** de la tâche. La réponse précise uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si une modification est impossible, comme celle d’une date d’échéance, elle vous le signale.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une révision](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour renommer la tâche, ou demandez-le dans son chat, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** réactive une tâche clôturée. Elle revient aussi automatiquement lorsqu’un nouvel élément survient, comme un nouveau message de la personne, mais pas après votre propre réponse. La tâche indique alors la date de son retour et est classée comme nouvelle. Le chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez régler vous-même, quel que soit le pays, crée une tâche avec le montant, la date d’échéance et les informations de paiement indiquées sur la facture. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne créent pas de tâche. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur confirmant la réception de votre paiement, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure donnée, comme une confirmation avant une réunion, se clôture automatiquement après cette heure. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche est déjà faite, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer votre brouillon tel quel.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête change de lieu ou si une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche toujours nécessaire suit le nouveau plan. Si rien ne reste à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire », son chat indique « Mis à jour : » et la raison, et **Annuler** permet de la rétablir pendant un jour.

Lors de vos premières tâches, une courte astuce présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. L’astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique les personnes concernées, l’organisation s’il y en a une (pas uniquement parce qu’une personne y travaille), le projet, Travail ou Perso, ainsi que la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Les noms de personnes et d’organisations affichent leur photo ou leur logo si le Graph en a un, et leurs initiales dans le cas contraire. Si un logo est illisible en petit, par exemple du blanc sur un fond transparent ou un nom très large, l’initiale s’affiche également.

Une ligne discrète précise parfois les informations manquantes, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis. » Elle apparaît lorsque le dernier échange avec la personne est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de deviner.

Lorsqu’un canal non connecté est indiqué, **Connecter** à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée garde son titre, avec une indication de la façon dont elle s’est achevée, par exemple « Fait : Sam l’a signée mardi ».

Au-dessus du brouillon, une ligne discrète indique le message dont il provient, avec le logo du service concerné. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, pour vous montrer immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de ce qu’une personne a indiqué ailleurs, comme la suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Touchez-la pour lire ce message. Elle disparaît lorsqu’une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, de la plus ancienne à la plus récente : les messages précédant celui auquel la tâche se rapporte, puis les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message associé à la tâche est marqué « Cette tâche » et s’ouvre dans le fil. **Afficher les messages précédents** ajoute les messages plus anciens. Les autres e-mails du fil sont repliés au-dessus et en dessous du message concerné.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification, avec la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, les adresses en Cci ou une adresse de réponse différente. Si rien n’est à ajouter, aucune information n’est affichée.

Une réponse dans un fil Slack affiche aussi les messages précédant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste concise ; le message dont elle provient se trouve sous **Détails**.

Une tâche **En attente de** renvoie vers votre dernier message à la personne et celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) crée une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée là où elle doit l’être, selon les personnes et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il date de longtemps.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue également. L’icône de calendrier propose des dates rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il provienne d’un e-mail, de Slack, Teams, WhatsApp, Telegram ou de tout autre service auquel The Machine a accès. Faites une recherche par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez joindre jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour retirer un fichier.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez joindre uniquement des fichiers : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour l’agrandir.
