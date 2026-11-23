---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Découvrez ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 88ccf5426e5a538f
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant une journée maximum, et votre téléphone en est aussi informé.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part ; quand le travail est bloqué par une information que vous seul pouvez fournir, comme un fait, une connexion ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un brief, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir plus bas).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir plus bas).
- **Revient plus tard** : les tâches mises en attente et celles auxquelles vous n’avez pas répondu à **Toujours utile ?** (voir plus bas).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec leur heure de clôture, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après votre envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui se contente de promettre de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche conservée. » **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord ce qui est en retard ou à échéance d’ici demain, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque groupe, l’ordre va du plus récent au plus ancien. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain apparaissent d’abord, puis les autres de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais signalées comme en retard. Quand un message indique qu’elle est terminée, elle se clôt automatiquement au bout d’une journée, avec **Annuler**. Sinon, elle attend que vous choisissiez **Marquer comme fait**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôt aussi automatiquement.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le message affiche l’adresse de la personne, jamais le nom qu’elle a utilisé. Votre Machine vérifie ces messages auprès de la personne dont vous avez déjà l’adresse, jamais auprès de leur expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une révision ou une réponse, indique **En attente de :** suivi de l’étape en question. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. Il en va de même après une question que vous avez posée : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si elle est passée. Elle précise alors qui doit encore répondre.

Quand une tâche porte sur un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôt automatiquement, avec **Annuler**. Si vous ne recevez rien au moment de relancer la personne, la tâche revient avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, pour faire remonter les nouvelles tâches après quelques jours d’absence. Par nouveauté, on entend un nouveau message sur la tâche ou une action de votre part, comme un message dans le chat, une modification ou une mise en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, celles dont l’échéance approche et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque toutes les tâches de Plus anciennes comme non nécessaires après une confirmation, comme le fait **Pas nécessaire** une par une, avec **Annuler**. Toute nouveauté sur une tâche la remet dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôt, avec **Annuler**. **Garder** la conserve et la question ne sera plus posée. Sans réponse pendant une autre semaine, elle est repliée dans Revient plus tard, et elle n’est plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet silencieux sans tâche ouverte peut donner lieu à une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et affiche une liste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification échoue ou prend du retard, sa ligne l’indique et affiche **Vérifier maintenant** en dessous.

**Tout**, **Travail** et **Perso** en haut de la barre latérale permettent d’afficher toutes les tâches ou uniquement celles d’un type. Votre téléphone et votre ordinateur conservent le même choix. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à toutes les tâches. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire ce récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou touchez son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : les tâches terminées aujourd’hui et celles qui sont encore ouvertes, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche liée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de le retirer. Consultez [les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche dans votre autre domaine. Les éléments auxquels elle peut accéder pour lire et envoyer des messages sont également transférés. **Annuler** dans la note permet de la déplacer à nouveau.

Quand une tâche a besoin de votre autre domaine pour avancer et que tous les messages dont elle dépend s’y trouvent, elle y est déplacée automatiquement et se poursuit. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que son domaine est identifié. D’ici là, elle n’est associée ni à Travail ni à Perso, et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Quand elle a besoin d’autres messages dans votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez indiquée comme Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise, et une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Un élément professionnel reçu sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte mail personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche s’affiche et avec qui elle est partagée, mais jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une telle tâche personnelle répond quand même depuis l’adresse professionnelle qui a reçu l’e-mail, et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

Quand au moins deux tâches sont en attente, **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie le contenu affiché, `S` le met en attente, `→` passe à la tâche suivante et Échap arrête le parcours. L’en-tête indique la durée estimée à votre rythme, par exemple « environ 2 min ».

À la fin, un récapitulatif indique ce qui a été envoyé ou clôturé et ce qui est encore en préparation.

Une tâche qui vous pose une question n’est pas incluse : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis traités ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, l’état des vérifications indique « Suspendues pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre les vérifications sous Connexions. Si des tâches sont ouvertes, cette option se trouve en haut sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou pris du retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare conservent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Cette ligne ne concerne que cette vérification : les tâches déjà dans votre liste restent inchangées. Quand une nouvelle tâche est conservée pour un meilleur moment, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche retenue jusqu’à demain 08:30 ».

Touchez la ligne pour afficher chaque fil d’e-mail, chat et notification avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la tâche créée ou la raison pour laquelle le message n’a rien nécessité, par exemple « En copie uniquement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison quand la vérification n’en a fourni qu’une vague. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont destinés sont comptés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou un avis de réparation, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : cette option est visible directement sur une tâche prête sans brouillon, sinon en haut du menu **…**, y compris sur une tâche qui nécessite votre décision. La tâche quitte aussitôt la liste, avec **Annuler** dans le message. Faites glisser le message pour le masquer, ou faites-le glisser hors de la liste avec la souris, pour le clôturer plus rapidement. La modification est conservée.

Pour que la tâche soit traitée autrement, indiquez-le dans son **Chat**. La réponse mentionne uniquement ce qui a changé, comme la mise en attente et sa durée. Si un élément ne peut pas être modifié, comme une échéance, la réponse vous le précise.

Dans **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la vérifier](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une fréquence définie](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez choisir une raison : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** sous **Détails** pour le renommer, ou demandez-le dans son chat, par exemple « Renomme-la en… ». Le titre choisi est conservé.

**Rouvrir** réaffiche une tâche clôturée. Elle réapparaît aussi automatiquement en cas de nouveauté, comme un nouveau message de la personne, mais pas après votre propre réponse. La tâche indique alors quand elle est revenue et est classée parmi les nouvelles. Le chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore régler vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les informations de paiement fournies sur la facture. Ce n’est pas le cas des factures réglées automatiquement, comme un prélèvement automatique ou une carte enregistrée. Quand un e-mail ultérieur confirme le paiement, par exemple l’expéditeur qui confirme l’avoir reçu, la tâche se clôt automatiquement. **Annuler** la rétablit pendant une journée.

Une tâche qui n’était utile que jusqu’à une heure précise, comme une confirmation avant une réunion, se clôt automatiquement après cette heure. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la rétablit pendant une journée.

Avant qu’un message ou un transfert destiné à quelqu’un soit marqué comme prêt, votre Machine consulte vos conversations récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a accepté, la tâche se clôt automatiquement. **Annuler** la rétablit pendant une journée.

Si quelqu’un a écrit dans la même conversation après la création de votre brouillon, **Envoyer** est suspendu : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent change les plans, par exemple si une fête est déplacée ou une réservation annulée, The Machine met elle-même ses tâches à jour. Une tâche toujours utile suit les nouveaux plans. S’il ne reste plus rien à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire », son chat indique « Mise à jour : » suivi de la raison, et **Annuler** la rétablit pendant une journée.

Lors de vos premières tâches, une courte astuce présente les actions essentielles : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. L’astuce disparaît définitivement lorsque vous utilisez le bouton correspondant ou appuyez sur ×.

Le premier jour, un message en haut de Tâches vous souhaite la bienvenue et indique qui attend depuis le plus longtemps votre réponse. Le brouillon de cette réponse est préparé en premier, pour qu’il soit prêt à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, son organisation s’il y en a une (pas simplement parce que cette personne y travaille), le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en contient un, et leurs initiales dans le cas contraire. Si un logo est difficile à lire en petit, par exemple un logo blanc sur fond transparent ou un long nom stylisé, l’initiale s’affiche aussi.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle apparaît quand le dernier échange avec cette personne remonte à longtemps ou n’a pas reçu de réponse, et mentionne les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Quand un canal non connecté est mentionné, l’option Connecter à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si cela change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Terminé : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique le message d’origine, avec le logo du service. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, pour voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Quand le brouillon tient compte de l’avis de quelqu’un ailleurs, comme une suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Touchez-la pour lire ce message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous la forme d’une seule conversation, de la plus ancienne à la plus récente : les messages qui précèdent celui concerné par la tâche et les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message concerné porte la mention « Cette tâche » et s’ouvre directement dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous du message concerné.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, l’e-mail s’ouvre dans l’application Gmail si vous l’avez installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, en Cci ou une adresse de réponse différente. Si rien n’est à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages qui précèdent le début du fil. Le lien d’une tâche vers le message concerné l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet, le domaine (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de codage. Son titre ouvre le chat. Une tâche terminée reste concise ; le message d’origine se trouve sous **Détails**.

Une tâche « En attente de » renvoie au dernier message que vous avez envoyé à la personne et dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet d’ajouter une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, elle est classée au bon endroit selon la personne et le sujet. Elle trouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue également. L’icône du calendrier propose des choix rapides et l’option **Choisir une date**.
- **Répéter** : la tâche revient selon une fréquence définie. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou d’un autre message auquel The Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit quand elle s’en occupe. Les fichiers suffisent à eux seuls : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour l’agrandir.
