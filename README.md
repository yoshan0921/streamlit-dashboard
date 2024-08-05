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

If VSCode cannot find the path to the libraries installed in your virtual environment, try the following VSCode setting:
* Go to "Python › Analysis: Extra Paths"
* Add the path of libraries to the Extra Paths
* How to find the libraries path installed in your virtual machine is as follow.
```
$ pipenv shell
$ python 
Type "help", "copyright", "credits" or "license" for more information.
>>> import streamlit
>>> print(streamlit.__file__)
[Library path installed in your virtual environment]
>>> 
```



## Run application
```
$ cd xxx (e.g. cd components_folium)
$ pipenv run streamlit run app.py
```
