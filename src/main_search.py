from PyQt5.QtWidgets import QWidget, QLineEdit, QToolButton, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QCompleter
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlQuery
from fenetre_affichage import fenetre_affichage
from PyQt5.QtCore import Qt


class main_search(QWidget):
    def __init__(self, search_menus, con, widget_names, all_tags, unites, tabConv):
        self.widget_names = widget_names
        self.all_tags = all_tags
        self.tabConv = tabConv
        self.unites = unites
        super(main_search, self).__init__()
        self.search_menus = search_menus
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Rechercher une recette...")
        query = QSqlQuery()
        query.exec("""select nom from recettes""")
        lr = []
        while query.next():
            lr.append(query.value(0))
        self.completer = QCompleter(lr)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchBar.setCompleter(self.completer)
        self.search_button = QToolButton()
        self.icon = QIcon("../data/icon.png")
        self.search_button.setIcon(self.icon)
        self.vBox = QVBoxLayout()
        self.hcontainer = QWidget()
        self.vBox.addWidget(self.hcontainer)
        self.hBox = QHBoxLayout(self.hcontainer)
        self.hBox.addWidget(self.searchBar)
        self.hBox.addWidget(self.search_button)
        self.hcontainer.setLayout(self.hBox)
        self.scroll = QScrollArea()
        self.vBox.addWidget(self.scroll)
        self.setLayout(self.vBox)
        self.search_button.clicked.connect(self.search)
        self.searchBar.returnPressed.connect(self.search)
        self.con = con

    def search(self):
        self.boutons = []
        try:
            del self.inner
            self.inner = QWidget(self.scroll)
            self.lay = QVBoxLayout(self.inner)
            self.inner.setLayout(self.lay)
            self.scroll.setWidget(self.inner)
            self.scroll.setWidgetResizable(True)
        except:
            self.inner = QWidget(self.scroll)
            self.lay = QVBoxLayout(self.inner)
            self.inner.setLayout(self.lay)
            self.scroll.setWidget(self.inner)
            self.scroll.setWidgetResizable(True)
        t = self.searchBar.text()
        t = "'%" + t + "%'"
        for i in reversed(range(self.lay.count())):
            self.lay.itemAt(i).widget().setParent(None)
        self.ids = []
        query = QSqlQuery()
        chechstates = [i.checked() for i in self.search_menus[0].getWidgets()]
        names = self.search_menus[0].getWidgetNames()
        request = "SELECT id,nom from recettes where "
        for i in range(0, len(chechstates)):
            if type(chechstates[i]) is not bool:
                if chechstates[i][0] > 0:
                    request = (
                        request
                        + "("
                        + f'"{names[i]}" between {chechstates[i][0]} and {chechstates[i][1]} or "{names[i]}"<0) and '
                    )
                elif chechstates[i][0] < 0:
                    request = (
                        request
                        + "("
                        + f'"{names[i]}" between {chechstates[i][1]} and {chechstates[i][0]} or "{names[i]}">0) and '
                    )
                else:
                    request = request + f'"{names[i]}"<> 0.0 and '
            elif not (chechstates[i]):
                request = request + f'"{names[i]}"' + "=0 and "
        checkstates_bis = [i.checked() for i in self.search_menus[1].getWidgets()]
        names = self.search_menus[1].getWidgetNames()
        for i in range(0, len(checkstates_bis)):
            if checkstates_bis[i] == 2:
                request = request + f'"{names[i]}" <> 0 and '
            elif checkstates_bis[i] == 0:
                request = request + f'"{names[i]}" = 0 and '
        request = request[:-5]
        if len(request) < len("SELECT id,nom from recettes where "):
            request = f"SELECT id,nom from recettes where nom like {t}"
        else:
            request = request + " and nom like " + t
        query.exec(f"""{request}""")
        while query.next():
            btn = QPushButton(self.inner)
            btn.setText(query.value(1))
            self.boutons.append(btn)
            self.ids.append(query.value(0))
            self.lay.addWidget(btn)
            self.boutons[-1].clicked.connect(
                lambda state, x=self.boutons[-1]: self.ouverture_recette(x)
            )

    def ouverture_recette(self, btn):
        id = self.ids[self.boutons.index(btn)]
        self.w = fenetre_affichage(
            id, self.widget_names, self.all_tags, self.unites, self
        )
        self.w.show()
