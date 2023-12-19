# streamlit-sanbox

## Set up environment (Create virtual environment)
```
$ pipenv install
```

Other pipenv commands for your references.
```
Enter the virtual environment.
$ pipenv sync

Exit the virtual environment.
$ exit

Install the package.
$ pipenv install [package name]

Uninstall the package.
$ pipenv uninstall [package name]

Uninstall all packages not specified in Pipfile.lock
$ pipenv clearn

Remove the virtual environment.
$ pipenv --rm

Show dependencies between packages
$ pipenv graph
```

## Run application
```
$ cd xxx (e.g. cd components_folium)
$ pipenv run streamlit run app.py
```
