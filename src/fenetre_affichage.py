import PyQt5
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPlainTextEdit,
    QGridLayout,
    QAction,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QSizePolicy,
    QInputDialog,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
)
import os
from img_viewer import Slides

from PyQt5 import QtCore
from listes import liste_bouttons, liste_ingredients, TableWidget

# from fenetre_edition import fenetre_edition


# createTableQuery.exec("""CREATE TABLE recettes(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,nom TEXT,note DOUBLE, duree DOUBLE, duree1 DOUBLE, duree2 DOUBLE,nb INT,t INT)""")


class fenetre_affichage(QMainWindow):
    def __init__(self, id, widget_names, all_tags, unites, par):
        self.liste = {}
        self.id = id
        self.tabConv = {i: par.tabConv[i].copy() for i in par.tabConv}
        self.widget_names = widget_names
        self.all_tags = all_tags
        self.unites = unites
        super().__init__()
        self.menu = self.menuBar().addMenu("Recette...")
        self.ajout1 = QAction("&Modifier la recette")
        self.ajout2 = QAction("&Supprimer la recette")
        self.ajout1.triggered.connect(lambda: self.modification(par))
        self.ajout2.triggered.connect(self.suppression)
        self.menu.addAction(self.ajout1)
        self.menu.addAction(self.ajout2)
        self.setGeometry(600, 100, 800, 600)
        self.layout = QGridLayout()
        self.bigContainer = QWidget()
        query = QSqlQuery()
        query2 = QSqlQuery()
        query3 = QSqlQuery()
        query4 = QSqlQuery()
        liste_img = os.listdir(f"..\\data\\{id}")
        i = 0
        n = len(liste_img)
        while i < n:
            if liste_img[i].split(".")[1] == "txt":
                liste_img.pop(i)
            else:
                liste_img[i] = f"..\\data\\{id}\\" + liste_img[i]
                i += 1
            n = len(liste_img)
        self.liste["images"] = liste_img.copy()
        if len(liste_img) > 0:
            self.slide = Slides(liste_img)
        else:
            self.slide = Slides(["..\\data\\default.png"])
        self.slide.setMinimumHeight(0)
        self.slide.setSizePolicy(
            PyQt5.QtWidgets.QSizePolicy.Ignored,
            PyQt5.QtWidgets.QSizePolicy.MinimumExpanding,
        )
        query.exec(f"""select * from recettes where id={id}""")
        query2.exec("""select name from pragma_table_info('recettes')""")
        query3.exec(f"""select * from ing_bis where id={id}""")
        query4.exec(
            """select name,rho from pragma_table_info('ing_bis') join ingredients on name=nom"""
        )
        query.first()
        query2.first()
        query3.first()
        for i in range(7):
            query2.next()
        name = query.value(1)
        with open(f"../data/{id}/{id}.txt", "r", encoding="utf8") as file:
            data = file.read()
        self.titre = QLabel()
        self.titre.setText(name)
        self.liste["nom"] = name
        self.titre.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        font1 = self.titre.font()
        font1.setPointSize(20)
        self.titre.setFont(font1)
        self.layout.addWidget(self.titre, 0, 0, 1, 3)
        self.containerIngredients = QWidget()
        self.container1 = QWidget()
        self.lay_container1 = QHBoxLayout()
        self.lay_containerIngredients = QVBoxLayout()
        self.lay_container1.addWidget(self.containerIngredients)
        self.liste["data"] = data
        self.label2 = QPlainTextEdit(self.container1, plainText=data, readOnly=True)
        self.label2.setStyleSheet("background-color: rgb(53,53,53)")
        self.label2.setFrameStyle(0)
        self.lay_container1.addWidget(self.label2)
        self.lbl1 = QLabel()
        self.liste["val"] = [query.value(i) for i in range(8)]
        a = str(int((query.value(3) - int(query.value(3))) * 60))
        if len(a) == 1:
            a = "0" + a
        self.lbl1.setText(
            "Durée de préparation : " + str(int(query.value(3))) + "h" + a
        )
        self.lbl2 = QLabel()
        a = str(int((query.value(4) - int(query.value(4))) * 60))
        if len(a) == 1:
            a = "0" + a
        self.lbl2.setText("Durée de cuisson : " + str(int(query.value(4))) + "h" + a)
        self.lbl3 = QLabel()
        a = str(int((query.value(5) - int(query.value(5))) * 60))
        if len(a) == 1:
            a = "0" + a
        self.lbl3.setText("Durée de repos : " + str(int(query.value(5))) + "h" + a)
        self.lbl4 = QLabel()
        self.lbl4.setText(f"{query.value(2)}/10")
        self.lbl5 = QLabel()
        self.lbl5.setText(f"{query.value(6)} personnes")
        self.lbl6 = QLabel()
        if query.value(7) > 0:
            self.lbl6.setText(f"Température du four : {query.value(7)}°C")
        else:
            self.lbl6.setText("Pas de four")
        self.l_lbl = [
            [self.lbl1, self.lbl2, self.lbl3],
            [self.lbl4, self.lbl5, self.lbl6],
        ]
        self.liste["Bouttons"] = self.l_lbl
        self.layout.addWidget(self.slide, 1, 0, 3, 1)
        for i in range(3):
            for j in range(2):
                self.l_lbl[j][i].setAlignment(PyQt5.QtCore.Qt.AlignCenter)
                self.layout.addWidget(self.l_lbl[j][i], i + 1, j + 1)
        self.layout.addWidget(self.container1, 4, 0, 1, 3)
        n = 7
        i = 1
        self.l_tags = []
        self.l_epices = []
        self.liste_ing = {}
        while query4.next():
            label = QLabel()
            while query2.value(0) != query4.value(0):
                if query.value(n) == "épice":
                    self.l_epices.append(query2.value(0))
                elif query.value(n) == "tag":
                    self.l_tags.append(query2.value(0))
                query2.next()
                n = n + 1
            if query.value(n) != 0:
                if query3.value(i) != "" and query3.value(i) in unites["Masse"]:
                    self.liste_ing[query4.value(0)] = [
                        "Masse",
                        query3.value(i),
                        query.value(n) / self.tabConv["Masse"][query3.value(i)],
                        -1,
                        -1,
                    ]
                    label.setText(
                        query4.value(0)
                        + " : "
                        + str(query.value(n) / self.tabConv["Masse"][query3.value(i)])
                        + " "
                        + query3.value(i)
                    )
                elif query3.value(i) != "" and query3.value(i) in unites["Volume"]:
                    if query4.value(1) == 0:
                        rho = 1
                    else:
                        rho = query4.value(1)
                    self.liste_ing[query4.value(0)] = [
                        "Volume",
                        query3.value(i),
                        query.value(n)
                        / (rho * self.tabConv["Volume"][query3.value(i)]),
                        -1,
                        -1,
                    ]
                    label.setText(
                        query4.value(0)
                        + " : "
                        + str(
                            query.value(n)
                            / (rho * self.tabConv["Volume"][query3.value(i)])
                        )
                        + " "
                        + query3.value(i)
                    )
                elif query3.value(i) != "":
                    self.liste_ing[query4.value(0)] = [
                        "Arbitraire",
                        query3.value(i),
                        abs(query.value(n)),
                        -1,
                        -1,
                    ]
                    label.setText(
                        query4.value(0)
                        + " : "
                        + str(abs(query.value(n)))
                        + " "
                        + query3.value(i)
                    )
                else:
                    self.liste_ing[query4.value(0)] = [
                        "Arbitraire",
                        query3.value(i),
                        abs(query.value(n)),
                        -1,
                        -1,
                    ]
                    label.setText(str(abs(query.value(n))) + " " + query4.value(0))
                self.lay_containerIngredients.addWidget(label)
            n += 1
            i = i + 1
            query2.next()
        self.liste["l_ing"] = self.liste_ing.copy()
        query2.previous()
        while query2.next():
            if query.value(n) == "épice":
                self.l_epices.append(query2.value(0))
            elif query.value(n) == "tag":
                self.l_tags.append(query2.value(0))
            n = n + 1
        self.liste["tags"] = self.l_tags.copy()
        self.liste["epices"] = self.l_epices.copy()
        for i in self.l_epices:
            self.lay_containerIngredients.addWidget(QLabel(text=i))
        t1 = "\n\nTags : "
        t2 = ""
        for j in self.l_tags:
            t2 = t2 + j + ", "
        if t2 != "":
            t2 = t2[:-2]
            data = data + t1 + t2
            self.label2.setPlainText(data)
        self.lay_containerIngredients.addStretch()
        self.containerIngredients.setLayout(self.lay_containerIngredients)
        self.container1.setLayout(self.lay_container1)
        self.layout.setRowStretch(4, 4)
        self.bigContainer.setLayout(self.layout)
        self.setCentralWidget(self.bigContainer)

    def modification(self, win):
        w = fenetre_edition(
            self.widget_names, self.all_tags, self.unites, self.liste, win
        )
        w.show()

    def suppression(self):
        ok = QMessageBox.question(
            self,
            "Suppression de recette",
            "La suppression d'une recette est définitive. Poursuivre ?",
        )
        if ok:
            query = QSqlQuery()
            query.exec(f"""delete from recettes where id={self.id}""")
            query.exec(f"""delete from ing_bis where id={self.id}""")
            query.exec(f"""update recettes set id=id-1 where id>{self.id}""")
            query.exec(f"""update ing_bis set id=id-1 where id>{self.id}""")
            n = self.id
            os.system(f"rd /s /q ..\\data\\{n}")
            n = n + 1
            while os.system(f"rename ..\\data\\{n} {n-1}") == 0:
                os.system(f"rename ..\\data\\{n-1}\\{n}.txt {n-1}.txt")
                n = n + 1
            self.close()


class fenetre_edition(QWidget):
    def __init__(self, widget_names, all_tags, unites, liste, win):
        super().__init__()
        self.liste = liste
        self.widget_names = widget_names
        self.val_duree = liste["val"][3]
        self.val_duree1 = liste["val"][4]
        self.val_duree2 = liste["val"][5]
        self.val_note = liste["val"][2]
        self.val_nb = liste["val"][6]
        self.t_four = liste["val"][7]
        self.label = QLabel("Another Window")
        self.all_tags = all_tags
        self.unites = unites
        self.setGeometry(600, 100, 800, 600)
        self.recette = QPlainTextEdit(liste["data"])
        self.recette.setPlaceholderText("Etapes de la recette")
        self.ingredients = liste_ingredients(widget_names, self.unites, liste["l_ing"])
        self.epices = liste_bouttons(self.all_tags, "épices", l=liste["epices"])
        self.other_tags = liste_bouttons(self.all_tags, "autres tags", l=liste["tags"])
        self.lay = QGridLayout()
        self.btn = QPushButton()
        self.btn.setText("Enregistrer")
        self.btn.pressed.connect(lambda: self.save(win))
        self.btn1 = QPushButton()
        self.btn2 = QPushButton()
        self.btn3 = QPushButton()
        self.btn5 = QPushButton()
        self.btn4 = QPushButton()
        self.btn6 = QPushButton()
        self.btn7 = QPushButton()
        self.btn3.setText(liste["Bouttons"][1][0].text())
        self.btn4.setText(liste["Bouttons"][1][1].text())
        self.btn5.setText(liste["Bouttons"][1][2].text())
        self.btn5.clicked.connect(self.four)
        self.btn3.clicked.connect(self.note)
        self.btn4.clicked.connect(self.nb)
        self.btn2.setText(liste["Bouttons"][0][0].text())
        self.btn2.clicked.connect(self.duree)
        self.btn6.setText(liste["Bouttons"][0][1].text())
        self.btn6.clicked.connect(self.duree1)
        self.btn7.setText(liste["Bouttons"][0][2].text())
        self.btn7.clicked.connect(self.duree2)
        self.nom_recette = QLineEdit(liste["nom"])
        self.nom_recette.setPlaceholderText("Nom de la recette")
        self.source = QLineEdit()
        self.source.setPlaceholderText(
            "Source (ne pas spécifier si la source est déjà dans la recette)"
        )
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
        for i in liste["images"]:
            self.addFile(i)
        self.setLayout(self.lay)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.Drop and event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.addFile(url.toLocalFile())
            return True
        return super().eventFilter(source, event)

    def addFile(self, filepath):
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
        self.val_duree = (
            QInputDialog.getInt(
                self, "Durée de préparation", "Nombre d'heures :", int(self.val_duree)
            )[0],
            QInputDialog.getInt(
                self,
                "Durée de préparation",
                "Nombre de minutes :",
                int((self.val_duree - int(self.val_duree)) * 60),
            )[0],
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
        self.val_duree1 = (
            QInputDialog.getInt(
                self, "Durée de la cuisson", "Nombre d'heures :", int(self.val_duree1)
            )[0],
            QInputDialog.getInt(
                self,
                "Durée de la cuisson",
                "Nombre de minutes :",
                int((self.val_duree1 - int(self.val_duree1)) * 60),
            )[0],
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
        self.val_duree2 = (
            QInputDialog.getInt(
                self, "Durée du repos", "Nombre d'heures :", int(self.val_duree2)
            )[0],
            QInputDialog.getInt(
                self,
                "Durée du repos",
                "Nombre de minutes :",
                int((self.val_duree2 - int(self.val_duree2)) * 60),
            )[0],
        )
        self.btn7.setText(
            "Repos : " + str(self.val_duree2[0]) + "h" + str(self.val_duree2[1]) + "min"
        )
        self.val_duree2 = self.val_duree2[0] + self.val_duree2[1] / 60

    def note(self):
        self.val_note = QInputDialog.getInt(
            self, "Note", "Note :", int(self.val_note), min=0, max=10
        )[0]
        self.btn3.setText(str(self.val_note) + "/10")

    def four(self):
        self.t_four = QInputDialog.getInt(
            self, "Four", "Température du four :", int(self.t_four)
        )[0]
        self.btn5.setText("Four : " + str(self.t_four) + "°C")

    def nb(self):
        self.val_nb = QInputDialog.getInt(
            self,
            "Nombre de personnes",
            "Nombre de personnes :",
            int(self.val_nb),
            min=0,
        )[0]
        self.btn4.setText(str(self.val_nb) + " personnes")

    def save(self, win):
        name = self.nom_recette.text()
        recette = self.recette.toPlainText()
        if self.source.text() != "":
            recette = recette + "\n" + "Source : " + self.source.text()
        ing = self.ingredients.getIngredients()
        epices = self.epices.getTags()
        tags = self.other_tags.getTags()
        query = QSqlQuery()
        query3 = QSqlQuery()
        query.exec("""select name from pragma_table_info('recettes')""")
        liste_ing = []
        name = "'" + name + "'"
        while query.next():
            liste_ing.append(query.value(0))
        id = self.liste["val"][0]
        liste_ing = liste_ing[1:]
        for i in liste_ing:
            query3.exec(f"""update recettes set {i}=0 where id={id}""")
        insertion_query = f"update recettes set nom={name}, note={self.val_note}, duree={self.val_duree}, duree1={self.val_duree1}, duree2={self.val_duree2},nb={self.val_nb},t={self.t_four}"
        query2 = "update ing_bis set "
        for i in ing:
            l = ing[i]
            query2 = query2 + "'" + i + "'=" + "'" + l[1] + "',"
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
                insertion_query = insertion_query + "=" + str(-1 * l[2])
            else:
                try:
                    a = self.widget_names[i]["rho"]
                except:
                    a = 0
                if max(l[3], a) > 0 and l[1] in self.unites["Volume"]:
                    insertion_query = (
                        insertion_query
                        + "="
                        + str(l[2] * win.tabConv[l[0]][l[1]] * max(l[3], a))
                    )
                else:
                    if l[1] in self.unites["Volume"]:
                        insertion_query = (
                            insertion_query
                            + "="
                            + str(l[2] * win.tabConv["Volume"][l[1]])
                        )
                    else:
                        insertion_query = (
                            insertion_query
                            + "="
                            + str(l[2] * win.tabConv["Masse"][l[1]])
                        )
        for i in self.all_tags:
            query.exec(f"""update recettes set {i}='' where id={id}""")
        for i in epices:
            if i not in self.all_tags:
                query.exec(
                    f"""alter table recettes add column '{i}' Text default('')"""
                )
            insertion_query = insertion_query + "," + i
            insertion_query = insertion_query + "=" + "'épice'"
        for i in tags:
            if i not in self.all_tags:
                query.exec(
                    f"""alter table recettes add column '{i}' Text default('')"""
                )
            insertion_query = insertion_query + "," + i
            insertion_query = insertion_query + "=" + "'tag'"
        insertion_query = insertion_query + f" where id={self.liste['val'][0]}"
        query.exec(f"""{insertion_query}""")
        query2 = query2[:-1] + f" where id={self.liste['val'][0]}"
        query.exec(f"""{query2}""")
        with open(f"..\\data\\{id}\\{id}.txt", "w", encoding="utf8") as f:
            f.write(recette)
        for i in range(self.tableWidget.rowCount()):
            if "..\data" not in self.tableWidget.item(i, 0).text():
                path = (
                    "copy "
                    + self.tableWidget.item(i, 0).text().replace("/", "\\")
                    + f" ..\\data\\{id}"
                )
                os.system(path)
        win.w.close()
        win.w = fenetre_affichage(
            id, self.widget_names, self.all_tags, self.unites, win
        )
        win.w.show()
        self.close()
