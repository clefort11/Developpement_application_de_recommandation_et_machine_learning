import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as mpl
from soccerplots.radar_chart import Radar
import seaborn as sns

dataset = pd.read_excel("dataset_clustering_consolide_features_V2.xlsx")
post_names = dataset["Position Générale Jointure WS"].unique().tolist()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="FootMatcher le bon joueur pour un bon coach !"),
    html.Div(children=html.P(children="""
        Sélectionnez le poste de joueur que vous recherchez.
    """)),
dcc.Dropdown(
        id="select-posts-names",
        options=[{"label":p, "value":p} for p in post_names],
        value="",
    ),

html.Div(children=html.P(children="""
        Sélectionnez le nom du joueur pour lequel vous souhaitez trouver un profil similaire.
    """)),

html.Div(id="post-name-div"),

html.Div(children=html.P(children="""
        Sélectionnez un des joueurs proposés au profil similaire.
    """)),

html.Div(id="recommended-players-names-div"),

html.Div(children=html.P(children="""
        Comparaison des deux joueurs sélectionnés.
    """)),



])

@app.callback(
    dash.dependencies.Output("post-name-div", "children"),
    dash.dependencies.Input("select-posts-names","value"))
def filtre_post_name(post_name):
    players_names = dataset.loc[dataset["Position Générale Jointure WS"]==post_name,"Joueur"].tolist()
    dd_menu = dcc.Dropdown(
        id = "select-players-names",
        options=[{"label":p, "value":p} for p in players_names],
        value = "",
    )
    return dd_menu

@app.callback(
    dash.dependencies.Output("recommended-players-names-div", "children"),
    dash.dependencies.Input("select-players-names","value")) 
def recommended_players(reference_player):
    # on va chercher la ligne correspondant au joueur
    mask_joueur = (dataset["Joueur"]==reference_player)
    info_joueur = dataset.loc[mask_joueur,:].reset_index(drop = True)
    # on récupère le cluster d'appartenance du joueur
    position_id = info_joueur.loc[0,"position_id"]
    colonne_cluster_position = "cluster_"+position_id
    cluster_joueur = info_joueur.loc[:,colonne_cluster_position].values[0]
    # On créer le sous dataset correspondant au cluster du joueur
    mask_cluster = (dataset["position_id"]==position_id)&(dataset[colonne_cluster_position]==cluster_joueur)
    dataset_cluster = dataset[mask_cluster]
    # Rapatrier la distance entre le joueur de référence et les autres joueurs du cluster
    # charger le dataset 'distance matrix' pour le poste
    nom_fichier_distance_matrix = "distance_matrix_"+position_id+".xlsx"
    dataset_distance_matrix = pd.read_excel(nom_fichier_distance_matrix,index_col = 0)
    # selectionner la colonne correspondante au joueur de reference
    id_position_joueur = info_joueur.loc[:,"id_joueur"]
    dataset_distance_matrix_joueur = dataset_distance_matrix.loc[:,id_position_joueur]
    # Merger 'dataset_cluster' avec 'dataset_distance_matrix_joueur', ça rajoute juste normalement une colonne qui donne la distance
    sous_dataset_consolide = pd.merge(dataset_cluster,dataset_distance_matrix_joueur,left_on = "id_joueur", right_on = dataset_distance_matrix_joueur.index)
    # Extraire et trier la recommandation de joueurs en fonction de leur 'proximité'
    sous_dataset_consolide_trie = sous_dataset_consolide.sort_values(by = id_position_joueur.values[0])
    # Filtre pour écarter de la recommandation le joueur sélectionné
    recommended_players_names = sous_dataset_consolide_trie[sous_dataset_consolide_trie["Joueur"]!=reference_player]["Joueur"][:10]

    recommended_menu = dcc.Dropdown(
        id = "select-recommended-player-name",
        options=[{"label":p, "value":p} for p in recommended_players_names],
        value=""
    )
    return recommended_menu

@app.callback(
    dash.dependencies.Output("recommended-player-selected-div", "children"),
    dash.dependencies.Input("select-recommended-player-name", "value"))
def display_selected_recommended_player(display_selected_recommended_player):

    # Radar
    selected_player_team = dataset[dataset["Joueur"] == reference_player]["Équipe"].values[0]
    recommended_player_team = dataset[dataset["Joueur"]==display_selected_recommended_player]["Équipe"].values[0]

    dataset_radar = dataset[(dataset["Joueur"]==reference_player) | (dataset["Joueur"] == selected_recommended_player)].reset_index()

    for i in dataset.Joueur.index:
        if post_name == "Gardien":
            col_list = ["Joueur", "Équipe", "Efficacité Gardien", "But concédé par tirs contre par 90", "Buts évités par 90", "Sorties par 90", "Duels aériens gagnés, %", "Interceptions par 90", "Dribbles réussis, %", "Tacles glissés par 90"]
        
        elif post_name == "Défenseur central (axe droit)" or "Défenseur central (axe gauche)" or "Défenseur central":
            col_list = ["Joueur", "Équipe", "Actions défensives réussies par 90", "Duels défensifs gagnés, %", "Interceptions par 90", "Duels aériens gagnés, %", "Passes en avant précises, %", "Passes courtes / moyennes précises, %", "Longues passes précises, %", "Buts de la tête"]
        
        elif post_name == "Défenseur latéral droit" or "Piston droit" or "Défenseur latéral gauche" or "Piston gauche":
            col_list = ["Joueur", "Équipe","Actions défensives réussies par 90", "Duels défensifs gagnés, %", "Interceptions par 90", "Centres précises, %", "Passes en avant précises, %", "Accélérations par 90", "Courses progressives par 90", "Efficacité Passeur"]
        
        elif post_name == "Milieu central défensif axial" or "Milieu central défensif droit" or "Milieu central défensif gauche":
            col_list = ["Joueur", "Équipe", "Actions défensives réussies par 90", "Duels défensifs gagnés, %", "Interceptions par 90", "Tacles glissés par 90", "Courses progressives par 90", "Accélérations par 90", "Passes en avant précises, %", "Dribbles réussis, %"]
        
        elif post_name == "Milieu axial droit" or "Milieu axial gauche":
            col_list = ["Joueur", "Équipe", "Interceptions par 90", "Courses progressives par 90", "Accélérations par 90", "Passes en avant précises, %", "Dribbles réussis, %", "Passes courtes / moyennes précises, %", "Longues passes précises, %", "Efficacité Passeur"]
        
        elif post_name == "Milieu droit" or "Milieu gauche" or "Meneur de jeu" :
            col_list = ["Joueur", "Équipe", "Efficacité passeur", "Courses progressives par 90", "Implication Passe Décisive par 90", "Passes en avant précises, %", "Passes dans tiers adverse précises, %", "Passes vers la surface de réparation précises, %", "Dribbles réussis, %", "Efficacité Buteur"]
        
        elif post_name == "Ailier droit" or "Ailier gauche" or "Attaquant droit" or "Attaquant gauche":
            col_list = ["Joueur", "Équipe", "Courses progressives par 90", "Accélérations par 90", "Dribbles réussis, %", "Efficacité Passeur", "Efficacité Buteur", "Passes en avant précises, %", "Centres précises, %", "Centres dans la surface de but par 90"]
        
        else :
            post_name == "Avant-Centre"
            col_list = ["Joueur", "Équipe", "Efficacité Buteur", "Buts", "Buts par 90", "Buts hors penalty", "Buts de la tête", "Dribbles réussis, %", "Efficacité Passeur", "Implication Passe Décisive par 90"]

    dataset_radar = dataset_radar[col_list]

    params = list(dataset_radar.columns)
    params = params[2:]

    ranges = []
    a_values = []
    b_values = []

    for x in params:
        a = min(dataset_radar[params][x])
        a = a - (a*.25)
        b = max(dataset_radar[params][x])
        b = b + (b*.25)
        ranges.append((a,b))

    for x in range(len(dataset_radar["Joueur"])):
        if dataset_radar["Joueur"][x] == reference_player:
            a_values = dataset_radar.iloc[x].values.tolist()
        if dataset_radar["Joueur"][x] == selected_recommended_player:
            b_values = dataset.radar.iloc[x].values.tolist()

    a_values = a_values[2:]
    b_values = b_values[2:]

    values = [a_values, b_values]

    title = dict(
        title_name = reference_player,
        title_color = "red",
        subtitle_name = selected_player_team,
        subtitle_color = "red",
        title_name_2 = selected_recommended_player,
        title_color_2 = "green",
        subtitle_name_2 = recommended_player_team,
        subtitle_color_2 = "green",
        title_fontsize = 20,
        subtitle_fontsize = 15
    )

    endnote = "data from Wyscout and Football Manager"

    radar = Radar()
    fig, ax = radar.plot_radar(ranges=ranges, params=params, value=values,
                            radar_color = ["red", "green"],
                            alphas=[.75,.6], title=title, endnote=endnote,
                            compare = True)

    # Beeswarm

    dataset["id_poste"] = dataset["Position Générale"].apply(lambda x : poste in x)

    mask = (dataset["id_poste"] == True)
    dataset_beeswarm = dataset.loc[mask,]
    dataset_beeswarm = dataset_beeswarm.drop("id_poste", axis=1).reset_index()

    for i in dataset.Joueur.index:
        if post_name == "Gardien":
            metrics = ["Efficacité Gardien", "But concédé par tirs contre par 90", "Buts évités par 90", "Sorties par 90", "Duels aériens gagnés, %", "Interceptions par 90", "Dribbles réussis, %", "Tacles glissés par 90"]
        
        elif post_name == "Défenseur central (axe droit)" or "Défenseur central (axe gauche)" or "Défenseur central":
            metrics = ["Actions défensives réussies par 90", "Duels défensifs gagnés, %", "Interceptions par 90", "Duels aériens gagnés, %", "Passes en avant précises, %", "Passes courtes / moyennes précises, %", "Longues passes précises, %", "Buts de la tête"]
        
        elif post_name == "Défenseur latéral droit" or "Piston droit" or "Défenseur latéral gauche" or "Piston gauche":
            metrics = ["Actions défensives réussies par 90", "Duels défensifs gagnés, %", "Interceptions par 90", "Centres précises, %", "Passes en avant précises, %", "Accélérations par 90", "Courses progressives par 90", "Efficacité Passeur"]
        
        elif post_name == "Milieu central défensif axial" or "Milieu central défensif droit" or "Milieu central défensif gauche":
            metrics = ["Actions défensives réussies par 90", "Duels défensifs gagnés, %", "Interceptions par 90", "Tacles glissés par 90", "Courses progressives par 90", "Accélérations par 90", "Passes en avant précises, %", "Dribbles réussis, %"]
        
        elif post_name == "Milieu axial droit" or "Milieu axial gauche":
            metrics = ["Interceptions par 90", "Courses progressives par 90", "Accélérations par 90", "Passes en avant précises, %", "Dribbles réussis, %", "Passes courtes / moyennes précises, %", "Longues passes précises, %", "Efficacité Passeur"]
        
        elif post_name == "Milieu droit" or "Milieu gauche" or "Meneur de jeu" :
            metrics = ["Efficacité passeur", "Courses progressives par 90", "Implication Passe Décisive par 90", "Passes en avant précises, %", "Passes dans tiers adverse précises, %", "Passes vers la surface de réparation précises, %", "Dribbles réussis, %", "Efficacité Buteur"]
        
        elif post_name == "Ailier droit" or "Ailier gauche" or "Attaquant droit" or "Attaquant gauche":
            metrics = ["Courses progressives par 90", "Accélérations par 90", "Dribbles réussis, %", "Efficacité Passeur", "Efficacité Buteur", "Passes en avant précises, %", "Centres précises, %", "Centres dans la surface de but par 90"]
        
        else :
            post_name == "Avant-Centre"
            metrics = ["Joueur", "Équipe", "Efficacité Buteur", "Buts", "Buts par 90", "Buts hors penalty", "Buts de la tête", "Dribbles réussis, %", "Efficacité Passeur", "Implication Passe Décisive par 90"]

    background = "#313332"
    text_color = "white"

    fig, axes = plt.subplots(3,2, figsize=(14,10))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    mpl.rcParams["xtick.color"] = text_color
    mpl.rcParams["ytick.color"] = text_color

    counter1 = 0
    counter2 = 0
    metrics_counter = 0

    for i,ax in zip(dataset_beeswarm["Joueur"], axes.flatten()):
        ax.set_facecolor(background)

        spines = ["top", "bottom", "left", "right"]
        for x in spines :
            if x in spines:
                ax.spines[x].set_visible(False)

        sns.swarmplot(x=metrics[metrics_counter], data=dataset_beeswarm, ax=axes[counter1, counter2], zorder=1)
        ax.set_xlabel(f"{metrics[metrics_counter]}", c="white")

        for x in range(len(dataset_beeswarm["Joueur"])):
            if dataset_beeswarm["Joueur"][x] == reference_player:
                ax.scatter(x=dataset_beeswarm[metrics[metrics_counter]][x], y=0, s=200, c="red", zorder=2)
            if dataset_beeswarm["Joueur"][x] == selected_recommended_player:
                ax.scatter(x=dataset_beeswarm[metrics[metrics_counter]][x], y=0, s=200, c="green", zorder=2)
        
        metrics_counter+=1
        if counter2 == 0:
            counter2 = 1
            continue
        if counter2 == 1:
            counter2 = 0
            counter1+=1


if __name__ == "__main__":
    app.run_server(debug=True)