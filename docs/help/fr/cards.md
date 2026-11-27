---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Découvrez ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: dfbc7ccc7313ecfe
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, la dernière étape que vous avez confirmée, comme l’envoi d’un formulaire ou la résolution d’un problème, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum. Votre téléphone en est informé aussi.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par ce qui arrive à échéance demain ou avant. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le réaliser), **Vous attend** (une décision ou une réponse de votre part est nécessaire ; si le travail ne peut pas continuer ou être utilisé sans une information que vous seule pouvez fournir, comme un prix, un fait ou un choix, une ligne sous le titre le précise), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches sans nouveauté depuis une semaine sont repliées (voir ci-dessous).
- **En attente des autres** : les tâches dont la prochaine étape revient à quelqu’un d’autre sont repliées (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, les messages qui [seront envoyés plus tard](send-later.md) et celles sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche conservée. » **Ouvrir** vous y mène. La recherche permet de trouver une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain ou avant s’affichent d’abord, puis les questions de votre Fleet, les suivis d’un tableau, et enfin les autres tâches. Au sein de chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et lorsqu’elle est terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain ou avant apparaissent d’abord, puis les autres, de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais considérées comme en retard. Quand un message l’indique, la tâche se clôture automatiquement après un jour, avec **Annuler**. Sinon, elle attend que vous la **Marquiez comme fait**.

Une tâche que vous avez déjà réglée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture elle aussi automatiquement. Une réponse qui indique qu’un fichier est joint alors qu’il ne l’est pas ne clôture pas la tâche.

Quand un message vient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example pour sam@acmecorp.example, la tâche le précise clairement : « Ce n’est pas Sam Lee. » La personne est affichée sous sa propre adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne associée à l’adresse que vous avez déjà, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, comme une relecture ou une réponse, indique l’étape concernée avec **En attente de**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci est plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors qui doit encore répondre.

Quand une tâche concerne un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement avec le résultat et **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Pour changer ce qui compte comme terminé, dites-le dans le chat.

Quand le résultat doit apparaître sur une page Web publique mentionnée dans ses messages, comme un article qui doit parler de vous, votre Machine consulte cette page au moment de relancer la personne. Si le résultat y figure, alors qu’il n’y figurait pas au début de l’attente, la tâche se clôture automatiquement et indique le résultat, avec **Annuler**. Votre Machine se contente de consulter la page comme le ferait n’importe quel visiteur. Elle n’envoie jamais rien.

Si le résultat n’apparaît pas sur la page et que l’échéance n’est pas encore passée, votre Machine la consulte une nouvelle fois le lendemain matin de l’échéance. Sinon, la tâche revient comme avant, avec « Vérifié » ou « Impossible à ouvrir » et la page dans son chat.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les nouvelles soient prioritaires après quelques jours d’absence. Une nouveauté désigne un nouveau message concernant la tâche ou une action de votre part, comme un message dans le chat, une modification ou une mise en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires toutes les tâches de Plus anciennes, après une confirmation, comme le fait **Pas nécessaire** pour une tâche à la fois, avec **Annuler**. Toute nouveauté sur une tâche la ramène dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve, et la question ne sera plus posée. Sans réponse pendant une semaine de plus, elle est repliée dans Revient plus tard, et elle n’est plus comptabilisée sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet qui n’a plus bougé et ne contient aucune tâche ouverte peut recevoir une tâche proposant une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique, avec **Vérifier maintenant** en dessous.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou une seule catégorie. Votre téléphone et votre ordinateur utilisent le même filtre. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, comme une partie qui redémarre sans cesse, n’est ni Travail ni Perso et n’apparaît que dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre catégorie : dans **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptabilisait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire ce récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou touchez son **×**, il reste affiché sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est toujours en cours, pour Travail et Perso, ou seulement pour la catégorie sélectionnée.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de le retirer. Voir [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche dans l’autre domaine. Les messages qu’elle peut lire et auxquels elle peut répondre la suivent. **Annuler** sur la note permet de la remettre à sa place.

Quand une tâche a besoin de l’autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et le travail continue. Sinon, **Déplacer vers Travail** s’affiche, et rien ne bouge tant que vous ne le touchez pas. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que votre Machine trouve où elle doit aller. En attendant, elle n’appartient ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de l’autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez indiquée comme personnelle compte comme Perso. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche liée à votre vie personnelle, comme un message de votre famille reçu à votre adresse professionnelle, est Perso dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte mail personnelle ou une [promesse](promises.md) concernant le travail, est associé à Travail dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche Perso de ce type répond toujours depuis l’adresse professionnelle qui a reçu l’e-mail, et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

Quand au moins deux tâches vous attendent, **Passer en revue** dans l’en-tête de Pour vous permet de les parcourir une par une, dans l’ordre de la liste, avec chaque brouillon affiché en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. L’en-tête indique combien de temps le parcours prendra à votre rythme, par exemple « environ 2 min ».

À la fin, le récap indique ce qui a été envoyé ou clôturé et ce qui est toujours en préparation.

Une tâche qui vous pose une question n’est incluse dans aucun des deux groupes : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont quand même lus et conservés, puis vérifiés ensemble à 06:30, afin que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la ligne des vérifications indique « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous absentiez pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre les vérifications dans Connexions. Si des tâches sont ouvertes, cette option se trouve en haut de la liste sur ordinateur. Une courte ligne ne s’affiche que pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle concerne uniquement cette vérification : les tâches déjà présentes dans votre liste restent telles quelles. Quand une nouvelle tâche attend un meilleur moment, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a nécessité aucune action, comme « En copie seulement, un collègue répond » ou « Réunion déjà fixée pour jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Touchez un élément pour le lire avec les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Le nombre après un nom, comme (3), indique le nombre de nouveaux messages de ce chat. Sur Android, une notification concernant un message déjà listé ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour leur contexte et les promesses qu’elles contiennent, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que votre Machine vous envoie, comme le récap du matin ou un avis de correction, ne sont jamais lus ni listés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche indique la prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, les éléments à modifier. Si vous commencez à écrire sans terminer, votre texte vous attendra à votre retour. **Annuler** l’efface.

**Marquer comme fait** indique que la tâche est réglée. Sur ordinateur, cette option est placée avec les autres boutons lorsqu’ils tiennent sur une ligne. Sur téléphone, elle est visible pour une tâche prête sans brouillon ou qui vous pose une question. Sinon, elle se trouve en haut de **…**. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer ou faites-le glisser hors de l’écran avec la souris pour le fermer plus tôt. La modification est conservée.

Pour faire avancer la tâche autrement, dites-le dans son **Chat**. La réponse indique uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si quelque chose n’a pas pu être modifié, comme une échéance, la réponse vous le dit.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la relire](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une fréquence définie](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez choisir une raison : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat de la tâche, par exemple « Renomme-la … ». Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle revient aussi automatiquement quand quelque chose de nouveau se produit, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La tâche indique alors la date de son retour et apparaît parmi les nouvelles. Le chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les informations de paiement fournies. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple si l’expéditeur confirme avoir reçu votre paiement, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement une fois cette heure passée. Elle passe dans **Fait / écarté** avec la mention « Plus nécessaire ». **Annuler** la fait réapparaître pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un s’affiche comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche a déjà été réalisée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création de votre brouillon, **Envoyer** est suspendu : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent modifie les plans, par exemple si une fête est déplacée ou qu’une réservation est annulée, The Machine met elle-même ses tâches à jour. Une tâche toujours utile suit le nouveau plan. Si elle n’a plus rien à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et la raison. **Annuler** la fait réapparaître pendant un jour.

Lors de vos premières tâches, un court conseil présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**. Un conseil disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est rédigée en premier, pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, son organisation si le sujet s’y rapporte, mais pas simplement parce que cette personne y travaille, le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom et une organisation affichent leur photo ou leur logo si le Graph en possède un, et leurs initiales dans le cas contraire. Si un logo est illisible en petit, par exemple s’il est blanc sur un fond transparent ou s’il s’agit d’un long nom stylisé, les initiales s’affichent aussi.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle s’affiche quand le dernier échange est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine précise ce qu’elle ne sait pas au lieu de faire des suppositions.

Quand la ligne indique un canal qui n’est pas connecté, l’option Connecter à côté permet d’ouvrir cette connexion.

Le titre indique ce qu’il faut faire et ne change que si la tâche elle-même change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Fait : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique le message d’origine et affiche le logo du service correspondant. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, pour vous permettre de voir d’un coup d’œil s’il s’agit d’une réponse Slack ou d’un e-mail.

Quand le brouillon s’appuie sur une contribution reçue ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « D’après Sam dans #ops ». Touchez-la pour lire ce message. Elle disparaît quand une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous forme d’une conversation, du plus ancien au plus récent : les messages qui précèdent celui auquel la tâche se rapporte, puis les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message lié à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification, avec la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si vous l’avez installée.

Les **Détails** d’un e-mail affichent uniquement ce qui ne figure pas dans son en-tête, comme les adresses Cc complètes, Bcc ou une autre adresse de réponse. Si rien n’est à ajouter, cette section est absente.

Une réponse dans un fil Slack affiche aussi les messages qui précèdent le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche son nom, son projet, son domaine, que vous pouvez toucher pour les modifier, votre dernière note et le résultat d’un agent de codage. Touchez le titre pour ouvrir le chat. Une tâche terminée reste succincte : le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » renvoie au dernier message que vous lui avez envoyé, celui auquel vous attendez une réponse : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet d’ajouter une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, la tâche est classée là où elle doit être, selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il date.

Si vous fermez la tâche avant de l’ajouter, votre texte et vos choix seront conservés pour la prochaine fois. Les fichiers ne le sont pas. **Supprimer** dans le message les efface.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue. L’icône du calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient selon une fréquence définie. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message auquel votre Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × permet d’en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit pour travailler dessus. Les fichiers seuls suffisent : votre Machine complète la tâche à partir d’un PDF ou d’un fichier texte. Une photo apparaît sous forme de petite image. Touchez-la pour l’afficher en taille réelle.
