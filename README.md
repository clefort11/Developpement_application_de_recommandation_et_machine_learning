# Developpement_application_de_recommandation_et_machine_learning

L'objet de ce repository est de présenter les compétences acquises dans la réalisation du projet final au cours de la formation Jedha Bootcamp. Mené en collaboration avec 3 personnes : Hugo B., Nicolas G., Olivier G., l’objectif de ce projet était de développer une application de recommandation de joueur de foot pour faciliter le travail des recruteurs.

Cette application repose sur une approche par similarité et le développement d’un algorithme de machine learning non supervisé de clustering et d’une réduction de dimension.

Les différents documents ci-dessous présentent le code et les différentes étapes dans le développement de l’application.

Le premier notebook ‘’01_Data_Preprocessing’’ présente quelques éléments du code de preprocessing.

On s’intéresse dans un premier temps (partie A), à l’imputation de valeurs manquantes concernant le poids des joueurs. Celle-ci a été effectuée via la mise en place d’un modèle de régression linéaire permettant de prédire le poids à partir de la taille du joueur. Dans un deuxième temps (partie B et C), on s’intéresse aux traitements qui ont été effectués sur le variable ‘Name’’ et ‘’Age’’ pour ‘’créer’’ des ‘’clés de jointure’’ et permettre la jointure de deux fichiers.

Le deuxième notebook ‘’02_Dimensionality_Reduction_&_Clustering’’ présente le code développé pour procéder à une réduction de dimension des composantes joueurs et à l’algorithme de machine learning non supervisé (KMeans) mis en place pour identifier les clusters.

Le document ‘’03_Script_Dash’’ présente le script de création de l’interface graphique de notre application de recommandation via l’outil Dash. La principale difficulté dans la rédaction de ce script a été l’utilisation des dropdown imbriqués et callbacks nécessaires pour permettre la sélection/affichage d’informations spécifiques en fonction de la sélection utilisateur.

Le document ‘’ 04_Screenshot_demo’’ permet d’avoir un visuel présentant le rendu final de l’application.
