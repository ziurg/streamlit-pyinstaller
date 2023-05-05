### Préparer l'environnement de développement

Créer un environnement virtuel et installer les dépendances :

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements\dev.txt
```

### Manipulations spécifiques à la compilation Streamlit

Modifiez le fichier venv\Lib\site-packages\streamlit\web\cli.py, en ajoutant la fonction **\_main_run_clExplicit** appelée par **run_app.py** :

```py
def _main_run_clExplicit(file, command_line, args=[ ], flag_options={}):
    main._is_running_with_streamlit = True
    bootstrap.run(file, command_line, args, flag_options)
```

A ce stade, l'application doit pouvoir être lancée par la commande :

```sh
python run.py
```

Si ce n'est pas déjà fait,

- créez un dossier **.streamlit** contenant le fichier **config.toml** suivant :

```toml
[global]
developmentMode = false

[server]
port = 8501
```

- créez un dossier **hooks** contenant le fichier **hook-streamlit.py** suivant :

```py
from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('streamlit')

```

### Compilation

Lancer la compilation depuis le dossier de contenant l'application:

```sh
pyinstaller run.py --onefile --additional-hooks-dir=./hooks --paths=.\venv\Lib\site-packages --clean
```

Modifier le contenu de **datas** et **hiddenimports** dans le fichier **run.spec** comme suit :

```
    datas=[
        (
            "venv/Lib/site-packages/altair/vegalite/v4/schema/vega-lite-schema.json",
            "./altair/vegalite/v4/schema/"
        ),
        (
            "venv/Lib/site-packages/streamlit/static",
            "./streamlit/static"
        )
    ],
    hiddenimports=["streamlit.runtime.scriptrunner.magic_funcs"]
```

puis relancer la commande suivante :

```sh
pyinstaller run.spec --clean
```

Il ne reste plus qu'à récupérer le fichier **dist\run.exe** pour le mettre au même niveau que app.py (et que le dossier .streamlit normalement).
Les réperertoire **build** et **dist** peuvent être supprimés.

### Module import error

En cas d'erreur d'import, de type ModuleNotFoundError, il faut ajouter les modules correspondants dans hiddenimports du fichier spec.

## Distribution

La distribution de la version compilée se fait en copiant les fichiers et répertoires suivants :

- /.streamlit
- app.py
- run.exe
