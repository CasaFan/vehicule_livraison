# Projet Energy

## Requirements
1. [Python](https://www.python.org/downloads/) (3.7 ou 3.*)

1. [Tkinter](https://docs.python.org/fr/3.7/library/tk.html): l'outil stantard python pour créer interface graphique.
    > Normalement tkinter est installé par défaut en python (3.7) Si ce n'est pas le cas: *apt-get install python-tk*.

1. [folium](https://python-visualization.github.io/folium/): un outil pour la génération de map
    ````bash
    pip install folium
    ````
1. [cefpython](https://github.com/cztomczak/cefpython): un outil pour integrer un web browser dans Tkinter
    ````bash
    pip install cefpython3
    ````
1. [numpy](https://www.numpy.org/): une librairie pour les calculs scientifique.
    ````bash
    pip install numpy
    ````
## Structure du projet
- **data**: un dossier qui contient les raw data
- **exceptions**: un dossier qui contient les exceptions en cas d'erreur
- **src**: dossier code source.
    - **modele**: les classes modèles.
        - `BowserFrame.py`: la classe qui gère le web browser intégré dans notre interface
        - `Heuristique.py`: Le coeur de notre heuristique
        - `VehiculeConfiguration.py`: le data-modele de la configuration de véhicule
    - `GUI.py`: la classe GUI qui gère interface et interractions d'utilisateur.
- **tmp**: le dossier où on met le fichier .html (le map) généré par la librairie [*folium*](https://python-visualization.github.io/folium/)
- **util**:
    - `FileHandler.py`: le controller qui gère l'import et initialisation de fichier de config & fichier de donnée. 
    - `FocusHandler.py`: le controller qui gère la frame de map sur notre interface.
    - `LoadHandler.py`: le controller qui initialise le fichier html dans notre interface.
- `setup.py`: le ficher "main" pour lancer notre interface.

## Execution du programme
1. Executer le fichier *setup.py*
    ```bash
    py setup.py
    ```
2. Sur interface, dans le menu **File** cliquer sur **Load config file** en choisissant le fichier `.ini` pour initialiser les configurations de véhicule.
3. En suite, cliquer sur **Load config file** en choissant le dossier de donnée pour qu'il charge les données dans le programme.
4. L'heuristique calculé avec les chemins de véhicule devrait être affichées sur le map
    > Les chemins sont distinguées par les differentes couleurs et les points de livraison sont sous forme de marker sur map. Si on clique sur un marker, les coordonnées sont affichées dans un popup. 
5. **[Différent calcul d'heuristique]**: changer le mode de calcule d'heuristique en cliquant sur le menu **Heuristique Mode** > [Mode], le programme va re-calculer l'heuristique par rapport au critère demandée et recharger le map sur interface.
    
    >le mode de calcul par défaut est une heuristique déterministe exhaustive 
    
#### BUG potentiel:
Si le programme crash il suffit de relancer, il s'agit d'un bug de `numpy` ou `gtk` sous windows, on a pas pu trouver la solution.
>ref: Fatal Python error: PyEval_RestoreThread: NULL tstate

### Amélioration:
1. afficher plus d'info sur le popup du marker, aussi la list de client(dans l'ordre) qu'on livre dans la zone text sur notre interface.
2. optimiser le processus de traitement de donnée en entrée.
3. bien structurer le resultat obtenu par le calcul d'heuristique.

## Licence
MIT License

Copyright (c) [2019] [casafan.yang@gmail.com] & [Lermite.vivian@gmail.com] & [Hadjarab.anis94@gmail.com]
