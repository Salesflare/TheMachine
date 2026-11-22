---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Découvrez ce que signifie chaque partie d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: fef065570d3fd972
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a été effectuée pendant votre absence. Elle reste là jusqu’à ce que vous appuyiez sur **Compris**, pendant une journée au maximum. Votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend votre réponse, par ordre d’urgence. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le concrétiser), **Vous attend** (une décision ou une réponse est nécessaire ; si le travail est bloqué par quelque chose que vous seul pouvez fournir, comme une information, une connexion ou un choix, une ligne sous le titre vous l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape revient à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec le moment où elles ont été terminées, par exemple « Terminé il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche conservée. » **Ouvrir** vous y amène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou à échéance demain au plus tard, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais affichées comme étant en retard. Si le statut apparaît dans un message, la tâche se clôture automatiquement au bout d’une journée, avec **Annuler**. Sinon, elle attend que vous la **Marquiez comme faite**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Si un message provient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le message affiche l’adresse de la personne, jamais le nom qu’elle a utilisé. Votre Machine vérifie le message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son auteur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une révision ou une réponse, indique l’étape **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question en retour : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci est plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors qui doit encore répondre.

Quand une tâche concerne un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche revient avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier la tâche.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les tâches récentes apparaissent en premier après quelques jours d’absence. Il n’y a rien de nouveau si aucun nouveau message n’a été reçu et si vous n’avez rien fait sur la tâche, comme envoyer un message dans le chat, la modifier ou la mettre en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, bientôt à échéance et dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque toutes les tâches de Plus anciennes comme non nécessaires après une seule confirmation, comme le fait **Pas nécessaire** pour chaque tâche, avec **Annuler**. Toute nouveauté sur une tâche la ramène dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine pose une seule fois la question **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve, et la question ne sera plus posée. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et elle n’est plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut recevoir une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et votre liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou a pris du retard, la ligne l’indique et affiche **Vérifier maintenant**.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou un seul type de tâche. Votre téléphone et votre ordinateur utilisent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, comme un composant qui ne cesse de redémarrer, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre option : sous **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le dernier récap du matin ou du soir et ce qu’il compte, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire le récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou appuyez sur son **×**, il reste sur tous vos appareils jusqu’au prochain récap.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso, ou seulement pour le filtre sélectionné.

Une tâche associée à un projet affiche son nom sous le titre. Appuyez dessus pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de le retirer. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les contenus qu’elle peut lire et les messages qu’elle peut envoyer sont déplacés avec elle. **Annuler** dans la note la remet à sa place.

Quand une tâche doit passer dans votre autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle s’y déplace automatiquement et continue. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous n’appuyez pas dessus. Une tâche que vous avez ajoutée sans choisir Travail ou Perso se déplace automatiquement dès qu’elle trouve sa place. En attendant, elle n’est classée ni dans Travail ni dans Perso, et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez classée comme Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est classée dans Perso dès le départ.

Le travail qui arrive sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte mail personnelle, est classé dans Travail dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche Perso de ce type répond tout de même depuis l’adresse professionnelle qui a reçu l’e-mail, et n’apparaît jamais dans une Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous vous les présente une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie le contenu affiché, `S` met en attente, `→` ignore et Échap arrête. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un récapitulatif indique le nombre d’éléments envoyés ou clôturés, ainsi que ceux dont la préparation est toujours en cours.

Une tâche qui vous pose une question n’est incluse dans aucun des deux cas : elle attend votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès que 40 messages sont en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30 pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, les vérifications affichent « Suspendues pour la nuit. Rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit toutes les sources immédiatement. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre les vérifications dans Connexions. Si des tâches sont ouvertes, l’option se trouve en haut de la liste sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou pris du retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Quand une nouvelle tâche attend un moment plus propice, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche reportée jusqu’à demain 08:30 ».

Appuyez sur la ligne pour afficher chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’auteur, l’objet ou les premiers mots, et la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Appuyez sur un élément pour le lire.

Les 10 premiers résultats s’affichent. Appuyez en dessous pour voir les autres. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification de téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour leur contexte et pour repérer les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou un avis de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** indique ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, les éléments à modifier. **Marquer comme fait** indique que la tâche est traitée : l’option est visible sur une tâche prête sans brouillon, sinon en haut de **…**, y compris pour une tâche qui nécessite votre décision. La tâche disparaît immédiatement de la liste, avec **Annuler** dans le message. Balayez le message ou faites-le glisser hors de l’écran avec la souris pour le clôturer plus tôt. La modification est conservée.

Pour que la tâche soit faite autrement, dites-le dans son **Chat**. La réponse indique uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si la modification n’a pas pu être effectuée, comme le changement d’une échéance, la réponse vous le signale.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une révision](ask-to-review.md).
- **Répéter…** : la tâche [revient selon un rythme défini](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat de la tâche, par exemple « Renomme-la en … ». Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle réapparaît aussi automatiquement quand quelque chose de nouveau se produit, comme un nouveau message de la personne, mais pas après votre propre réponse. La tâche indique alors quand elle est revenue et apparaît parmi les nouvelles tâches. Le chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche qui indique le montant, la date d’échéance et les modalités de paiement précisées sur la facture. Les factures réglées automatiquement, par exemple par prélèvement ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur confirmant la réception du règlement, la tâche se clôture automatiquement. **Annuler** la rétablit pendant une journée.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement après cette heure. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la rétablit pendant une journée.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos discussions récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a accepté, la tâche se clôture automatiquement. **Annuler** la rétablit pendant une journée.

Si quelqu’un d’autre a écrit dans la même conversation après la création du brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent modifie le plan, par exemple si une fête change de lieu ou si une réservation est annulée, The Machine met elle-même ses tâches à jour. Une tâche qui reste nécessaire suit le nouveau plan. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et la raison, et **Annuler** la rétablit pendant une journée.

Lors de vos premières tâches, une courte astuce présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. Elle disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue apparaît en haut de Tâches et indique depuis combien de temps quelqu’un attend votre réponse. Cette réponse est rédigée en priorité pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation s’il y en a une (et non simplement parce que la personne y travaille), le projet, Travail ou Perso, ainsi que la date de création. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Les noms de personnes et d’organisations s’affichent avec leur photo ou leur logo si le Graph en possède un, et avec leurs initiales sinon. Un logo illisible en petit, par exemple blanc sur fond transparent ou sous forme de long nom, est remplacé par l’initiale.

Parfois, une ligne discrète indique ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle apparaît si le dernier échange avec la personne est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine vous indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Quand la ligne mentionne un canal qui n’est pas connecté, appuyez sur **Connecter** à côté pour ouvrir la connexion.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Terminé : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service concerné. Appuyez dessus pour lire le fil. Le brouillon affiche le logo du service auquel il est destiné : vous voyez ainsi tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de ce que quelqu’un a indiqué ailleurs, par exemple une suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Appuyez dessus pour lire le message.

Une conversation (Slack, WhatsApp, Telegram, Intercom…) s’affiche dans l’ordre chronologique, de la plus ancienne à la plus récente : les messages qui précèdent celui auquel la tâche se rapporte, puis les réponses suivantes. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message lié à la tâche porte la mention « Cette tâche » et s’ouvre directement. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, l’e-mail s’ouvre dans l’application Gmail si vous l’avez installée.

Les **Détails** d’un e-mail affichent uniquement les éléments que son en-tête ne montre pas, comme les adresses complètes en copie, en copie cachée ou une adresse de réponse différente. Si aucun renseignement supplémentaire n’est disponible, rien ne s’affiche.

Une réponse dans un fil Slack affiche aussi les messages envoyés avant le début du fil. Le lien d’une tâche vers le message d’origine l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste concise ; le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » renvoie au dernier message que vous avez envoyé à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet d’ajouter une tâche pour n’importe quel sujet. La création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, la tâche est classée au bon endroit selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue aussi. L’icône du calendrier propose des raccourcis et **Choisir une date**.
- **Répéter** : la tâche revient selon un rythme défini. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message auquel The Machine a accès. Faites une recherche par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez joindre jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). × retire un fichier.

Les fichiers restent associés à la tâche, et The Machine les lit quand elle s’en occupe. Vous pouvez joindre uniquement des fichiers : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo apparaît sous forme de petite image. Appuyez dessus pour l’afficher en taille réelle.
