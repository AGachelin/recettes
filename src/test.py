from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QApplication,
    QMainWindow,
    QAction,
    QPlainTextEdit,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QInputDialog,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
    QCheckBox,
    QDoubleSpinBox,
)
import sys

from search_menu import search_menu, search_menu_bis
from spoiler import CollapsibleBox
from main_search import main_search
from listes import liste_bouttons, liste_ingredients, TableWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import os

app = QApplication(sys.argv)

app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

app.setApplicationName("Recettes")


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.menu = self.menuBar().addMenu("Ajouter une recette")
        self.ajout1 = QAction("&Manuellement")
        self.ajout1.triggered.connect(self.ajout_manuel)
        self.menu.addAction(self.ajout1)
        self.menu2 = self.menuBar().addMenu("Modifier...")
        self.ajout2 = QAction("&Ingrédient")
        self.ajout2.triggered.connect(self.modif_ing)
        self.ajout3 = QAction("&Unité")
        self.ajout3.triggered.connect(self.modif_unit)
        self.menu2.addAction(self.ajout2)
        self.menu2.addAction(self.ajout3)
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("../data/recettes.db")
        # Open the connection
        if not self.con.open():
            print("Database Error: %s" % self.con.lastError().databaseText())
            sys.exit(1)
        query = QSqlQuery()
        query.exec("""select name from pragma_table_info('recettes')""")
        query.first()
        self.all_tags = []
        while query.next():
            self.all_tags.append(query.value(0))
        self.all_tags = self.all_tags[7:]
        query.exec(""" select * from ingredients""")
        self.ingredients = {}
        s = ["Masse", "Volume"]
        while query.next():
            self.ingredients[query.value(0)] = {}
            self.ingredients[query.value(0)]["autorises"] = []
            for i in range(2, 4):
                if query.value(i):
                    self.ingredients[query.value(0)]["autorises"].append(s[i - 2])
            self.ingredients[query.value(0)]["Arbitraire"] = query.value(1)
            self.ingredients[query.value(0)]["rho"] = query.value(4)
        self.unites = {"Masse": ["g"], "Volume": ["mL"]}
        self.tabConv = {"Masse": {"g": 1}, "Volume": {"mL": 1}}
        query.exec("""select name from pragma_table_info('unite')""")
        l = []
        query.first()
        while query.next():
            l.append(query.value(0))
        query.exec("""select * from unite""")
        n = "Masse"
        while query.next():
            for i in range(2, len(l) + 1):
                if query.value(i) > 0:
                    self.tabConv[n][l[i - 1]] = query.value(i)
                    self.unites[query.value(0)[0].upper() + query.value(0)[1:]].append(
                        l[i - 1]
                    )
            n = "Volume"
        for i in self.ingredients:
            self.all_tags.pop(self.all_tags.index(i))
        central_widget = QWidget()
        widget_gauche = QWidget()
        self.lay1 = QVBoxLayout(widget_gauche)
        self.col1 = CollapsibleBox("Ingrédients", widget_gauche)
        self.col2 = CollapsibleBox("Autres tags et épices", widget_gauche)
        self.l1 = search_menu(
            sorted(list(self.ingredients.keys())), self.unites, self.tabConv
        )
        self.l2 = search_menu_bis(sorted(self.all_tags))
        self.col1.setContentLayout(self.l1.layout())
        self.col2.setContentLayout(self.l2.layout())
        self.lay1.addWidget(self.col1)
        self.lay1.addWidget(self.col2)
        self.lay1.addStretch()
        self.main_search = main_search(
            [self.l1, self.l2],
            self.con,
            self.ingredients,
            self.all_tags,
            self.unites,
            self.tabConv,
        )
        self.lay = QHBoxLayout(central_widget)
        widget_gauche.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.main_search.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Minimum
        )
        self.lay.addWidget(widget_gauche)
        self.lay.addWidget(self.main_search)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.lay)
        self.setWindowTitle("Recettes")

    def ajout_manuel(self, w1):
        self.w1 = fenetre_d_ajout(
            self.ingredients, self.all_tags, self.unites, self.tabConv, self
        )
        self.w1.show()

    def modif_ing(self):
        class QBox(QCheckBox):
            def __init__(self, text, parent=None):
                super().__init__(text, parent)

            def nextCheckState(self):
                pass

        def g(rho):
            if rho.value() > 0:
                rho.setSuffix("")
            else:
                rho.setSuffix("(Non spécifiée)")

        def save(self):
            query = QSqlQuery()
            query.exec(f"""delete from ingredients where nom='{text}'""")
            query.exec(
                f"""insert into ingredients (nom, arbitraire,masse,volume,rho) values ('{nom.text()}',{box3.isChecked()},{box1.isChecked()},{box2.isChecked()},{rho.value()})"""
            )
            query.exec(f"""alter table recettes rename column {text} to {nom.text()}""")
            query.exec(f"""alter table ing_bis rename column {text} to {nom.text()}""")
            self.cont.close()
            self.close(ok=True)

        text, ok = QInputDialog.getItem(
            self,
            "Modification d'un ingrédient",
            "Ingrédient :",
            sorted(list(self.ingredients.keys())),
            editable=False,
        )
        if ok:
            self.cont = QWidget()
            lay = QGridLayout()
            l = self.ingredients[text]
            n = 1
            lay.addWidget(QLabel("Nom"), 0, 0)
            nom = QLineEdit(text=text)
            lay.addWidget(nom, 1, 0)
            lay.addWidget(QLabel("Systèmes de mesure autorisés :"), 0, n, 1, 3)
            box1 = QCheckBox(text="Masse")
            if "Masse" in l["autorises"]:
                box1 = QBox(text="Masse")
                box1.setChecked(True)
            lay.addWidget(box1, 1, n)
            n = n + 1
            box2 = QCheckBox(text="Volume")
            if "Volume" in l["autorises"]:
                box2 = QBox(text="Volume")
                box2.setChecked(True)
            lay.addWidget(box2, 1, n)
            n = n + 1
            box3 = QCheckBox(text="Arbitraire")
            if l["Arbitraire"]:
                box3 = QBox(text="Arbitraire")
                box3.setChecked(True)
            lay.addWidget(box3, 1, n)
            n = n + 1
            lay.addWidget(QLabel("Masse volumique"), 0, n)
            rho = QDoubleSpinBox(value=l["rho"])
            lay.addWidget(rho, 1, n)
            if l["rho"] == 0:
                rho.setSuffix(" (Non spécifiée)")
            rho.valueChanged.connect(lambda: g(rho))
            self.btn1 = QPushButton("Enregistrer")
            self.btn2 = QPushButton("Annuler")
            self.btn1.clicked.connect(lambda: save(self))
            self.btn2.clicked.connect(lambda: self.cont.close())
            lay.addWidget(self.btn1, 2, 0)
            lay.addWidget(self.btn2, 2, n)
            self.cont.setLayout(lay)
            self.cont.show()

    def modif_unit(self):
        def save(self):
            query = QSqlQuery()
            if box1.isChecked():
                query.exec(
                    f"""update unite set {text}={coeff.value()} where nom='masse'"""
                )
                query.exec(f"""update unite set {text}=0 where nom='volume'""")
            else:
                query.exec(f"""update unite set {text}=0 where nom='masse'""")
                query.exec(
                    f"""update unite set {text}={coeff.value()} where nom='volume'"""
                )
            for i in self.ingredients:
                query.exec(
                    f"""update ing_bis set \"{i}\"='{nom.text()}' where \"{i}\"='{text}'"""
                )
            query.exec(f"""alter table unite rename column {text} to {nom.text()}""")
            self.cont.close()
            self.close(ok=True)

        text, ok = QInputDialog.getItem(
            self,
            "Modification d'une unité",
            "Unité :",
            sorted(self.unites["Masse"] + self.unites["Volume"]),
            editable=False,
        )
        if ok:
            query = QSqlQuery()
            query.exec(f"""select {text} from unite""")
            self.cont = QWidget()
            lay = QGridLayout()
            n = 0
            lay.addWidget(QLabel(text="Nom :"), 0, n)
            nom = QLineEdit(text=text)
            lay.addWidget(nom, 1, n)
            n = n + 1
            box1 = QCheckBox(text="Masse")
            box2 = QCheckBox(text="Volume")
            lay.addWidget(QLabel("Système de mesure :"), 0, n, 1, 2)
            lay.addWidget(box1, 1, n)
            n = n + 1
            lay.addWidget(box2, 1, n)
            n = n + 1
            lay.addWidget(QLabel("Coefficient avec l'unité de base du système :"), 0, n)
            try:
                coeff = QDoubleSpinBox(value=self.tabConv["Masse"][text], suffix=" g")
                box1.setChecked(True)
            except:
                coeff = QDoubleSpinBox(value=self.tabConv["Volume"][text], suffix=" mL")
                box2.setChecked(True)
            coeff.setPrefix(f"1 {text} = ")
            lay.addWidget(coeff, 1, n)
            l = ["mL", "", "g"]
            nom.textChanged.connect(lambda: coeff.setPrefix(f"1 {nom.text()} = "))
            box1.stateChanged.connect(
                lambda: [
                    box2.setCheckState((box1.checkState() + 2) % 4),
                    coeff.setSuffix(f" {l[box1.checkState()]}"),
                ]
            )
            box2.stateChanged.connect(
                lambda: [
                    box1.setCheckState((box2.checkState() + 2) % 4),
                    coeff.setSuffix(f" {l[box1.checkState()]}"),
                ]
            )
            n = n + 1
            self.btn1 = QPushButton("Enregistrer")
            self.btn2 = QPushButton("Annuler")
            self.btn1.clicked.connect(lambda: save(self))
            self.btn2.clicked.connect(lambda: self.cont.close())
            lay.addWidget(self.btn1, 2, 0)
            lay.addWidget(self.btn2, 2, n)
            self.cont.setLayout(lay)
            self.cont.show()

    def close(self, ok=False):
        super().close()
        if ok:
            self.__init__()
            self.showMaximized()


class fenetre_d_ajout(QWidget):
    def __init__(self, widget_names, all_tags, unites, tabConv, par):
        super().__init__()
        self.ok=True
        self.widget_names = widget_names
        self.tabConv = tabConv
        self.label = QLabel("Another Window")
        self.all_tags = all_tags
        self.unites = unites
        self.setGeometry(600, 100, 800, 600)
        self.recette = QPlainTextEdit()
        self.recette.textChanged.connect(self.i)
        self.recette.setPlaceholderText("Etapes de la recette")
        self.ingredients = liste_ingredients(widget_names, self.unites, self, {})
        self.epices = liste_bouttons(self.all_tags, "épices", self)
        self.other_tags = liste_bouttons(self.all_tags, "autres tags", self)
        self.lay = QGridLayout()
        self.btn = QPushButton()
        self.btn.setText("Enregistrer")
        self.btn.pressed.connect(lambda: self.save(par))
        self.btn1 = QPushButton()
        self.btn2 = QPushButton()
        self.btn3 = QPushButton()
        self.btn5 = QPushButton()
        self.btn4 = QPushButton()
        self.btn6 = QPushButton()
        self.btn7 = QPushButton()
        self.btn3.setText("Note")
        self.btn4.setText("Nb de personnes")
        self.btn5.setText("T° du four ?")
        self.btn5.clicked.connect(self.four)
        self.btn3.clicked.connect(self.note)
        self.btn4.clicked.connect(self.nb)
        self.btn2.setText("Durée de préparation ?")
        self.btn2.clicked.connect(self.duree)
        self.btn6.setText("Durée de la cuisson ?")
        self.btn6.clicked.connect(self.duree1)
        self.btn7.setText("Durée de repos ?")
        self.btn7.clicked.connect(self.duree2)
        self.nom_recette = QLineEdit()
        self.nom_recette.textChanged.connect(self.i)
        self.nom_recette.setPlaceholderText("Nom de la recette")
        self.source = QLineEdit()
        self.source.textChanged.connect(self.i)
        self.source.setPlaceholderText("Source")
        self.btn1.setText("Annuler")
        self.btn1.pressed.connect(self.f)
        self.btn8 = QPushButton()
        self.btn8.setText("Ajouter \n une \n photo...")
        self.btn8.clicked.connect(self.ajout_photo)
        self.lay.addWidget(self.nom_recette, 0, 0, 1, 4)
        self.lay.addWidget(self.recette, 5, 0, 1, 4)
        self.lay.addWidget(self.ingredients, 6, 0, 1, 4)
        self.lay.addWidget(self.epices, 7, 0, 1, 2)
        self.lay.addWidget(self.other_tags, 7, 2, 1, 2)
        self.lay.addWidget(self.btn1, 8, 0, 1, 2)
        self.lay.addWidget(self.btn, 8, 2, 1, 2)
        self.lay.addWidget(self.btn2, 1, 0)
        self.lay.addWidget(self.btn6, 2, 0)
        self.lay.addWidget(self.btn7, 3, 0)
        self.lay.addWidget(self.btn5, 3, 1)
        self.lay.addWidget(self.btn3, 1, 1)
        self.lay.addWidget(self.btn4, 2, 1)
        self.lay.addWidget(self.source, 4, 0, 1, 2)
        self.tableWidget = TableWidget()
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.viewport().installEventFilter(self)
        self.tableWidget.placeholder_text = "Glisser une photo"
        types = ["text/uri-list"]
        types.extend(self.tableWidget.mimeTypes())
        self.tableWidget.mimeTypes = lambda: types
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.cellClicked.connect(lambda state: self.open_jpg())
        self.row = 0
        self.column = 0
        self.lay.addWidget(self.tableWidget, 1, 2, 4, 1)
        self.btn8.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.lay.addWidget(self.btn8, 1, 3, 4, 1)
        self.setLayout(self.lay)

    def i(self):
        self.ok=False

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Drop and event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.addFile(url.toLocalFile())
            return True
        return super().eventFilter(source, event)

    def addFile(self, filepath):
        self.i()
        l = filepath.split("\\")
        l1 = l[-1].split(".")
        if len(l1) > 2 or l1[-1] not in ["jpg", "png", "jpeg"]:
            QMessageBox.about(
                self, "Format invalide", "Le format de l'image est invalide"
            )
        elif " " in filepath:
            QMessageBox.about(
                self, "Format invalide", "Il y a des espaces dans le chemin du fichier"
            )
        else:
            self.tableWidget.insertRow(self.row)
            item = QTableWidgetItem(filepath)
            item.setText(filepath)
            self.tableWidget.setItem(self.row, self.column, item)
            self.tableWidget.resizeColumnToContents(self.column)
            self.row += 1

    def ajout_photo(self):
        path, ok = QFileDialog.getOpenFileName(
            self, "Choix d'image", filter="Images (*.png *.jpg *.jpeg)"
        )
        if ok:
            self.addFile(path)

    def open_jpg(self):
        def g():
            texte = self.tableWidget.currentItem().text()
            os.system("start " + texte)
            self.wid.close()

        def h():
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            self.tableWidget.resizeColumnToContents(self.column)
            self.row -= 1
            self.wid.close()

        self.wid = QWidget()
        lay = QHBoxLayout()
        btn1 = QPushButton()
        btn2 = QPushButton()
        btn1.setText("Ouvrir")
        btn2.setText("Supprimer")
        lay.addWidget(btn1)
        lay.addWidget(btn2)
        self.wid.setLayout(lay)
        btn1.clicked.connect(g)
        btn2.clicked.connect(h)
        self.wid.show()

    def f(self):
        self.close()

    def duree(self):
        self.i()
        self.val_duree = (
            QInputDialog.getInt(self, "Durée de préparation", "Nombre d'heures :",min=0)[0],
            QInputDialog.getInt(self, "Durée de préparation", "Nombre de minutes :",min=0)[0],
        )
        self.btn2.setText(
            "Préparation : "
            + str(self.val_duree[0])
            + "h"
            + str(self.val_duree[1])
            + "min"
        )
        self.val_duree = self.val_duree[0] + self.val_duree[1] / 60

    def duree1(self):
        self.i()
        self.val_duree1 = (
            QInputDialog.getInt(self, "Durée de la cuisson", "Nombre d'heures :",min=0)[0],
            QInputDialog.getInt(self, "Durée de la cuisson", "Nombre de minutes :",min=0)[0],
        )
        self.btn6.setText(
            "Cuisson : "
            + str(self.val_duree1[0])
            + "h"
            + str(self.val_duree1[1])
            + "min"
        )
        self.val_duree1 = self.val_duree1[0] + self.val_duree1[1] / 60

    def duree2(self):
        self.i()
        self.val_duree2 = (
            QInputDialog.getInt(self, "Durée du repos", "Nombre d'heures :", min=0)[0],
            QInputDialog.getInt(self, "Durée du repos", "Nombre de minutes :", min=0)[0],
        )
        self.btn7.setText(
            "Repos : " + str(self.val_duree2[0]) + "h" + str(self.val_duree2[1]) + "min"
        )
        self.val_duree2 = self.val_duree2[0] + self.val_duree2[1] / 60

    def note(self):
        self.i()
        self.val_note = QInputDialog.getInt(self, "Note", "Note :", min=0, max=10)[0]
        self.btn3.setText(str(self.val_note) + "/10")

    def four(self):
        self.i()
        self.t_four = QInputDialog.getInt(self, "Four", "Température du four :", min=0)[0]
        self.btn5.setText("Four : " + str(self.t_four) + "°C")

    def nb(self):
        self.i()
        self.val_nb = QInputDialog.getInt(
            self, "Nombre de personnes", "Nombre de personnes :", min=0
        )[0]
        self.btn4.setText(str(self.val_nb) + " personnes")

    def closeEvent(par,x):
        if not(par.ok):
            par.ok=QMessageBox.question(par,"Fermeture de recette","Fermer la fenêtre ?")
            par.ok = par.ok!=65536
        if par.ok:
            super().close()
        else:
            x.ignore()

    def save(self, par):
        try:
            name = self.nom_recette.text()
            recette = self.recette.toPlainText()
            if self.source.text() != "":
                recette = recette + "\n" + "Source : " + self.source.text()
            ing = self.ingredients.getIngredients()
            epices = self.epices.getTags()
            tags = self.other_tags.getTags()
            query3 = QSqlQuery()
            query3.exec("""select id from recettes""")
            query3.last()
            if query3.value(0) != None:
                id = query3.value(0) + 1
            else:
                id = 1
            query = QSqlQuery()
            query.exec("""select name from pragma_table_info('recettes')""")
            liste_ing = []
            name = "'" + name + "'"
            while query.next():
                liste_ing.append(query.value(0))
            insertion_query = (
                "INSERT INTO recettes (id, nom, note, duree, duree1, duree2,nb,t"
            )
            name = (
                str(id)
                + ","
                + name
                + ","
                + str(self.val_note)
                + ","
                + str(self.val_duree)
                + ","
                + str(self.val_duree1)
                + ","
                + str(self.val_duree2)
                + ","
                + str(self.val_nb)
                + ","
                + str(self.t_four)
            )
            query2 = "INSERT INTO ing_bis (id,"
            query2_bis = f") values ({id},"
            for i in ing:
                l = ing[i]
                query2 = query2 + "'" + i + "',"
                query2_bis = query2_bis + "'" + l[1] + "',"
                if i not in liste_ing:
                    query.exec(
                        f"""ALTER TABLE recettes ADD COLUMN '{i}' DOUBLE default(0)"""
                    )
                    query.exec(f"""ALTER TABLE ing_bis ADD COLUMN '{i}' TEXT""")
                    if l[1] == "":
                        query.exec(
                            f"""insert into ingredients (nom, arbitraire) values ('{i}',True)"""
                        )
                    else:
                        query.exec(
                            f"""insert into ingredients (nom, {l[0].lower()}) values ('{i}', True)"""
                        )
                elif l[3] > 0:
                    query.exec(
                        f"""update ingredients set {l[0].lower()}=True, rho={l[3]} where nom='{i}'"""
                    )
                    if l[0] == "Masse":
                        query.exec(f"""update recettes set {i}=recettes.{i}/{l[3]}""")
                query.exec(
                    f"""update ingredients set {l[0].lower()}=True where nom='{i}'"""
                )
                if l[4] > 0:
                    query.exec(
                        f"""alter table unite add column '{l[1]}' double default(0)"""
                    )
                    query.exec(
                        f"""update unite set {l[1]}={l[4]} where nom='{l[0].lower()}'"""
                    )
                insertion_query = insertion_query + ",'" + i + "'"
                if l[0] == "Arbitraire":
                    name = name + "," + str(-1 * l[2])
                else:
                    try:
                        a = self.widget_names[i]["rho"]
                    except:
                        a = 0
                    if max(l[3], a) > 0 and l[1] in self.unites["Volume"]:
                        name = name + "," + str(l[2] * self.tabConv[l[0]][l[1]] * l[3])
                    else:
                        if l[1] in self.unites["Volume"]:
                            name = name + "," + str(l[2] * self.tabConv["Volume"][l[1]])
                        else:
                            name = name + "," + str(l[2] * self.tabConv["Masse"][l[1]])

            for i in epices:
                if i not in self.all_tags:
                    query.exec(
                        f"""alter table recettes add column '{i}' Text default('')"""
                    )
                insertion_query = insertion_query + "," + f"'{i}'"
                name = name + "," + "'épice'"
            for i in tags:
                if i not in self.all_tags:
                    query.exec(
                        f"""alter table recettes add column '{i}' Text default('')"""
                    )
                insertion_query = insertion_query + "," + f"'{i}'"
                name = name + "," + "'tag'"
            insertion_query = insertion_query + ") VALUES (" + name + ")"
            query.exec(f"""{insertion_query}""")
            query2 = query2[:-1] + query2_bis[:-1] + ")"
            query.exec(f"""{query2}""")
            path = "mkdir ..\\data\\" + str(id)
            os.system(path)
            with open(
                f"..\\data\\{id}\\{id}.txt",
                "w",
                encoding="utf8",
            ) as f:
                f.write(recette)
            for i in range(self.tableWidget.rowCount()):
                path = (
                    "copy "
                    + self.tableWidget.item(i, 0).text().replace("/", "\\")
                    + " ..\\data\\"
                    + str(id)
                )
                os.system(path)

            par.close(ok=True)
            self.ok=True
            self.close()
        except:
            QMessageBox.warning(
                self,
                "Enregistrement d'une recette",
                "Tous les champs obligatoires n'ont pas été remplis",
            )


w = MainWindow()
w.showMaximized()
sys.exit(app.exec_())
