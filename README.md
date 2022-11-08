# Information system of the E-shop

[Zadanie](assets/zadanie.pdf)

## Downloading and intializing git

1. [Download git](https://git-scm.com/) and follow installation guide
2. In your local project folder open [command prompt](https://www.youtube.com/watch?v=bgSSJQolR0E)
3. Enter command `git config --global user.name "your github username"`
4. Next enter `git config --global user.email "your e-mail"`
5. Clone this repository `git clone https://github.com/tomas-magat/camels-eshop-infosystem.git`
 
## Working with git

*Follow these steps:*

#### Create new branch for new changes (in your terminal)
1. Take recent code from Github `git pull`
2. Create branch `git checkout -b name-of-the-new-branch`

#### Making changes (repeat these steps until you're finished with changing the code)
3. Make changes to the code
4. Stage changes `git add .`
5. Commit changes `git commit -am "Describe what has changed"`

#### Publishing changes on Github
6. Push your changes to the Github `git push --set-upstream origin name-of-the-branch-you-created`
> On the github website:
7. Click 'compare & pull request' button that appeared on the top of the github page
8. Click 'create pull request' button
9. Click 'merge pull request' button on the following page
10. Click 'confirm merge' and 'delete old branch' buttons
> In your terminal:
11. Switch to the main branch `git checkout main`
12. Sync your code with github `git pull`


## Installing PyQt5 and Qt Designer

1. Install PyQt5  `pip install -r requirements.txt`
2. [Download](https://build-system.fman.io/qt-designer-download) and install Qt designer (tool)  

- [PyQt5 tutorial](https://www.pythonguis.com/pyqt5-tutorial/)
- [Qt Designer tutorial](https://realpython.com/qt-designer-python/)


## Basic workflow

#### Changing the 'look' (GUI) of the app
1. In Qt Designer open file `source\code\main.ui`
2. Make changes and save
3. Open cmd in `..\source\code>` and type command `pyuic5 -x main.ui -o main_ui.py`

#### Changing the window behaviour (button press...)
1. Open `source\code\modules\[your_module].py`
2. Change the module class
3. Test the changes by running app.py


## Module and datafile structure 

![](assets/STRUCTURE_2.png)
