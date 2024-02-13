from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QPlainTextEdit,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
    QInputDialog,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
)
from listes import liste_bouttons, liste_ingredients, TableWidget
from PyQt5.QtSql import QSqlQuery
import os
from fenetre_affichage import fenetre_affichage


class fenetre_edition(QWidget):
    def __init__(self, widget_names, all_tags, unites, liste, win):
        super().__init__()
        self.liste = liste.copy()
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
        self.btn.pressed.connect(lambda state: self.save(win))
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
                self, "Durée de préparation", "Nombre d'heures :", int(self.val_duree), min=0
            )[0],
            QInputDialog.getInt(
                self,
                "Durée de préparation",
                "Nombre de minutes :",
                int((self.val_duree - int(self.val_duree)) * 60), min=0
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
                self, "Durée de la cuisson", "Nombre d'heures :", int(self.val_duree1), min=0
            )[0],
            QInputDialog.getInt(
                self,
                "Durée de la cuisson",
                "Nombre de minutes :",
                int((self.val_duree1 - int(self.val_duree1)) * 60), min=0
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
                self, "Durée du repos", "Nombre d'heures :", int(self.val_duree2), min=0
            )[0],
            QInputDialog.getInt(
                self,
                "Durée du repos",
                "Nombre de minutes :",
                int((self.val_duree2 - int(self.val_duree2)) * 60), min=0
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
        print(1, epices, tags)
        query = QSqlQuery()
        query.exec("""select name from pragma_table_info('recettes')""")
        liste_ing = []
        name = "'" + name + "'"
        while query.next():
            liste_ing.append(query.value(0))
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
                # [syst, unite, text1, rho, rapport]
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
                insertion_query = insertion_query + "=" + str(l[2])
        for i in epices:
            if i not in self.all_tags:
                query.exec(f"""alter table recettes add column {i} Text default("")""")
            insertion_query = insertion_query + "," + i
            insertion_query = insertion_query + "=" + "épice"
        for i in tags:
            if i not in self.all_tags:
                query.exec(f"""alter table recettes add column {i} Text default("")""")
            insertion_query = insertion_query + "," + i
            insertion_query = insertion_query + "=" + "tag"
        insertion_query = insertion_query + f"where id={self.liste['val'][0]}"
        query.exec(f"""{insertion_query}""")
        query2 = query2[:-1] + f"where id={self.liste['val'][0]}"
        query.exec(f"""{query2}""")
        id = self.liste["val"][0]
        with open(f"..\\data\\{id}\\{id}.txt", "w", encoding="utf8") as f:
            f.write(recette)
        for i in range(self.tableWidget.rowCount()):
            if "..\data" not in i:
                path = (
                    "copy "
                    + self.tableWidget.item(i, 0).text().replace("/", "\\")
                    + f" ..\\data\\{id}"
                )
                os.system(path)
        win.close()
        w = fenetre_affichage(id, self.ingredients, self.all_tags, self.unites)
        w.show()
        self.close()
