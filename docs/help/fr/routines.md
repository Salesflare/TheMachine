---
title: Routines
area: cards
summary: Du travail que votre Machine fait seule, à un rythme, comme un résumé du lundi de vos deals ouverts. Elle ne fait que lire.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter
---
## En créer une

Ouvrez **Routines** dans la barre latérale et dites en une ligne ce qu’elle doit faire et quand : « chaque lundi à 9 h, résume mes deals ouverts » ou « chaque jour ouvré le matin, liste les e-mails auxquels je dois encore répondre ». Puis **Ajouter**.

Sans heure, elle tourne à 8:00. L’heure est celle de l’horloge de votre Machine.

## Ce que fait une routine

À son heure, votre Machine lit ce dont elle a besoin, comme vos messages, vos réunions et le Graph, et place le résultat sur la page Routines. Chaque résultat indique **Prête**, **Rien de nouveau** (avec pourquoi) ou **N’a pas marché** (avec pourquoi). Une exécution qui se termine sans résultat compte comme ratée, jamais comme faite.

Les routines ne font que lire : vos messages, des pages web, GitHub et des sites comme X dans le navigateur. Elles n’envoient, ne répondent, ne publient et ne modifient rien.

Quand la tâche d’une routine finit par une publication ou un message, elle fait tout jusqu’à cette étape et montre le brouillon, comme **Publierait sur X :**. Après une vraie exécution, vous le recevez comme tâche à approuver ; une exécution de test le montre seulement. Son nom dit de quoi il s’agit et où cela part, son bouton nomme l’étape, comme **Publier**, et **De votre routine** en dessous ouvre la routine.

La tâche commence dans l’espace du compte d’où elle part, comme Travail pour le compte X de votre entreprise, et ne demande donc jamais à être déplacée.

Chaque exécution connaît le dernier résultat, elle peut donc dire ce qui a changé depuis.

Après une bonne exécution, votre Machine peut s’écrire une recette pour la lecture qui est la même à chaque fois, comme les e-mails ou les changements GitHub à regarder. Les exécutions suivantes lisent cela d’abord, en code simple, et l’IA choisit seulement ce qui compte et l’écrit, avec moins de tokens. Une recette ne fait que lire ; si elle ne fonctionne plus, l’exécution lit d’elle-même et la répare. Elle apparaît sous **Avancé : étapes de script** dans le menu ⋯.

## Jours manqués

Si votre Machine était éteinte ou occupée, les exécutions manquées ne s’empilent pas : seule la plus récente tourne, une fois. Chaque date tourne une fois, même après un redémarrage.

Les routines tournent une à la fois et attendent quand l’usage de votre forfait IA est bas, comme tout le travail en arrière-plan. **Lancer maintenant** la lance tout de suite.

## La modifier ou l’arrêter

C’est dans le menu ⋯ de la routine. **Changer quand** prend un nouveau rythme dans vos propres mots, comme « chaque jour ouvré à 8 h ». **Mettre en pause** arrête les exécutions jusqu’à **Reprendre** ; ce qui a été manqué pendant la pause ne tourne pas ensuite. **Arrêter** met fin à une routine pour de bon.

Quand vous utilisez **Demander des modifications** sur une tâche d’une routine et que votre note vaut pour chaque exécution, comme « jamais d’emoji », la tâche propose **Modifier aussi la routine**. Elle montre ce qui change dans les mots de la routine, et la routine ne change que quand vous touchez **Modifier**. **Laisser ainsi** la laisse telle quelle. Une correction de ce seul brouillon ne propose rien.

## Avancé : étapes de script

Vous n’avez jamais besoin d’un script : dites avec vos propres mots ce qu’une routine doit faire.

Pour les utilisateurs avancés, une routine peut aussi lancer vos propres commandes sur votre Machine : dans le menu ⋯, choisissez **Avancé : étapes de script**. **Modifier** ne les montre que si une routine en a déjà. **Récupérer les données** lance d’abord une commande, dans son dossier (vide : votre dossier personnel) et pendant au plus ses secondes. Ce qu’elle affiche va à l’exécution pour travailler avec. Sans mots, ce qu’elle affiche est le résultat.

**Vérification** reçoit le résultat en entrée après l’exécution. Si elle se termine par une erreur, l’exécution affiche **N’a pas marché** avec ce que la vérification a dit. Une commande de Récupérer les données qui échoue s’affiche de la même façon.

Une commande tient sur une ligne et tourne sans shell : pas de pipes ni de variables. Les étapes de script sont à vous, réglées sur votre tableau de bord uniquement. Une exécution de test et **Essayer** lancent aussi Récupérer les données et le disent ; elles n’envoient et ne gardent toujours rien. Une routine n’envoie jamais, donc une étape de script devrait seulement lire.

## Depuis vos tâches OpenClaw

Si vous aviez créé des tâches planifiées dans OpenClaw, votre Machine les lit (elle ne les modifie jamais) et propose celles qui conviennent comme routines sous **Suggérée**. Chacune a tourné une fois, pour que vous voyiez un vrai résultat.

Elle garde vos corrections de la tâche et laisse de côté ce qu’elle envoyait ou publiait. Une tâche qui lançait un script, ou lisait ce qu’une tâche de script collectait, l’apporte comme Récupérer les données. **Ajouter** en fait une routine, **Non merci** ne redemande jamais pour cette tâche. Une tâche qui vous rappelait de faire quelque chose arrive plutôt comme offre de tâche récurrente dans Tâches.

Trois suggestions au plus attendent en même temps. Après une semaine de bonnes exécutions, la routine demande **Désactiver l’ancienne tâche OpenClaw ?** Elle n’est désactivée que si vous touchez **Désactiver**, et vous pouvez la réactiver dans OpenClaw.

## Depuis ce que vous faites

Votre Machine remarque aussi le travail que vous faites à un rythme et le propose comme routine sous **Suggérée**, même sans OpenClaw. Elle cherche :

- la même demande, trois fois ou plus de suite, comme « résume les tickets de support ouverts » chaque lundi ;
- un e-mail que vous envoyez à un rythme, comme un rapport hebdomadaire à votre équipe ;
- des newsletters et e-mails de mise à jour qui reviennent chaque semaine ;
- un canal Slack animé où d’autres écrivent chaque semaine ;
- des e-mails que vous transférez un par un à la même personne, comme ceux de l’école et du club à votre partenaire : un condensé hebdomadaire pour cette personne évite les transferts ;
- la même demande à laquelle vous répondez à un rythme, comme une validation mensuelle pour la même personne.

Chaque suggestion dit ce qu’elle a vu, comme « Demandé 4 fois de suite » ou « 6 e-mails transférés à Sam en 3 semaines », et a tourné une fois pour que vous voyiez un vrai résultat. Pensez à un récap d’équipe, un brief avant un appel hebdomadaire, un résumé du support ou du dev, le pouls de vos chiffres ou un condensé des newsletters que vous recevez.

Elle ne propose que ce qui vous est propre et clairement utile : un condensé d’actualités seulement sur vos propres newsletters, jamais un générique. Quand rien ne convient, il n’y a pas de suggestion.

Elle regarde au plus une fois par jour et apporte au plus une nouvelle suggestion par semaine, sans notification. **Non merci** ne la ramène jamais. Les transferts et les réponses restent avec le compte d’où ils sont partis, pour que Travail et Perso ne se mélangent pas. Tout reste sur votre Machine. Une tâche que vous terminez à un rythme arrive plutôt comme offre de tâche récurrente.

## Routines et tâches récurrentes

Une tâche récurrente (recurring.md) vous rappelle de faire quelque chose. Une routine est du travail que votre Machine fait seule et vous montre. Utilisez une tâche récurrente pour « payer le loyer le premier du mois », et une routine pour « chaque vendredi, dis-moi quels deals se sont tus ».
