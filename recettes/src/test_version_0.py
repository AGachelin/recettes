#test

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
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog
)
import sys
from search_menu import search_menu
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
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("../data/recettes.db")
        # Open the connection
        if not self.con.open():
            print("Database Error: %s" % self.con.lastError().databaseText())
            sys.exit(1)
        query = QSqlQuery()
        query.exec("""select name from pragma_table_info('recettes')""")
        query.first()
        self.widget_names = []
        while query.next():
            self.widget_names.append(query.value(0))
        self.widget_names = self.widget_names[2:]
        amount_Range = [
            "Heater",
            "Stove",
            "Living Room Light",
            "Balcony Light",
            "Fan",
            "Room Light",
            "Oven",
            "Desk Light",
            "Bedroom Heater",
            "Wall Switch",
            "Heater",
            "Stove",
            "Living Room Light",
            "Balcony Light",
            "Fan",
            "Room Light",
            "Oven",
            "Desk Light",
            "Bedroom Heater",
            "Wall Switch",
        ]
        central_widget = QWidget()
        widget_gauche = QWidget()
        self.lay1 = QVBoxLayout(widget_gauche)
        self.col1 = CollapsibleBox("Ingrédients", widget_gauche)
        self.col2 = CollapsibleBox("Autres tags", widget_gauche)
        self.l1 = search_menu(self.widget_names, amount_Range)
        self.l2 = search_menu(self.widget_names, amount_Range)
        self.col1.setContentLayout(self.l1.layout())
        self.col2.setContentLayout(self.l2.layout())
        self.lay1.addWidget(self.col1)
        self.lay1.addWidget(self.col2)
        self.lay1.addStretch()
        self.main_search = main_search([self.l1, self.l2], self.con)
        self.lay = QHBoxLayout(central_widget)
        """
        for w, (r, c) in zip(
            (self.col1, self.col2),
            ((0, 0), (1, 0)),
        ):
            self.lay.addWidget(w, r, c)
        """
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
        self.w1 = fenetre_d_ajout(self.widget_names)
        self.w1.show()


class fenetre_d_ajout(QWidget):
    def __init__(self, widget_names):
        super().__init__()
        self.label = QLabel("Another Window")
        self.setGeometry(600, 100, 800, 600)
        self.recette = QPlainTextEdit()
        self.recette.setPlaceholderText("Etapes de la recette")
        self.ingredients = liste_ingredients(widget_names)
        self.epices = liste_bouttons(widget_names, "épices")
        self.other_tags = liste_bouttons(widget_names, "autres tags")
        self.lay = QGridLayout()
        self.btn = QPushButton()
        self.btn.setText("Enregistrer")
        self.btn.pressed.connect(self.save)
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
        self.nom_recette.setPlaceholderText("Nom de la recette")
        self.source = QLineEdit()
        self.source.setPlaceholderText("Source")
        self.btn1.setText("Annuler")
        self.btn1.pressed.connect(self.f)
        self.btn8=QPushButton()
        self.btn8.setText("Ajouter \n une \n photo...")
        self.btn8.clicked.connect(self.ajout_photo)
        self.lay.addWidget(self.nom_recette, 0, 0, 1, 4)
        self.lay.addWidget(self.recette, 5, 0, 1, 4)
        self.lay.addWidget(self.ingredients, 6, 0, 1, 4)
        self.lay.addWidget(self.epices, 7, 0,1,2)
        self.lay.addWidget(self.other_tags, 7, 2,1,2)
        self.lay.addWidget(self.btn1, 8, 0,1,2)
        self.lay.addWidget(self.btn, 8, 2,1,2)
        self.lay.addWidget(self.btn2, 1, 0)
        self.lay.addWidget(self.btn6, 2, 0)
        self.lay.addWidget(self.btn7, 3, 0)
        self.lay.addWidget(self.btn5, 3,1)
        self.lay.addWidget(self.btn3,1,1)
        self.lay.addWidget(self.btn4,2,1)
        self.lay.addWidget(self.source,4,0,1,2)
        self.tableWidget = TableWidget()
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.viewport().installEventFilter(self)
        self.tableWidget.placeholder_text="Glisser une photo"
        types = ['text/uri-list']
        types.extend(self.tableWidget.mimeTypes())
        self.tableWidget.mimeTypes = lambda: types
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.cellClicked.connect(lambda state : self.open_jpg())
        self.row=0
        self.column=0
        self.lay.addWidget(self.tableWidget,1,2,4,1)
        self.btn8.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Expanding)
        self.lay.addWidget(self.btn8,1,3,4,1)
        self.setLayout(self.lay)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Drop and
            event.mimeData().hasUrls()):
            for url in event.mimeData().urls():
                self.addFile(url.toLocalFile())
            return True
        return super().eventFilter(source, event)

    def addFile(self, filepath):
        l=filepath.split("\\")
        l1=l[-1].split(".")
        if len(l1)>2 or l1[-1] not in ["jpg","png","jpeg"]:
            QMessageBox.about(self,"Format invalide","Le format de l'image est invalide")
        elif " " in filepath:
            QMessageBox.about(self,"Format invalide","Il y a des espaces dans le chemin du fichier")
        else:
            self.tableWidget.insertRow(self.row)
            item = QTableWidgetItem(filepath)
            item.setText(filepath)
            self.tableWidget.setItem(self.row, self.column, item)
            self.tableWidget.resizeColumnToContents(self.column)
            self.row +=1

    def ajout_photo(self):
        path,ok=QFileDialog.getOpenFileName(self,"Choix d'image", filter="Images (*.png *.jpg *.jpeg)")
        if ok:
            self.addFile(path)

    def open_jpg(self):
        def g():
            texte=self.tableWidget.currentItem().text()
            os.system("start "+ texte)
            self.wid.close()
        def h():
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            self.tableWidget.resizeColumnToContents(self.column)
            self.row-=1
            self.wid.close()
        self.wid=QWidget()
        lay=QHBoxLayout()
        btn1=QPushButton()
        btn2=QPushButton()
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
            QInputDialog.getInt(self, "Durée de préparation", "Nombre d'heures :")[0],
            QInputDialog.getInt(self, "Durée de préparation", "Nombre de minutes :")[0],
        )
        self.btn2.setText("Préparation : " + str(self.val_duree[0]) +"h"+ str(self.val_duree[1])+"min")

    def duree1(self):
        self.val_duree1 = (
            QInputDialog.getInt(self, "Durée de la cuisson", "Nombre d'heures :")[0],
            QInputDialog.getInt(self, "Durée de la cuisson", "Nombre de minutes :")[0],
        )
        self.btn6.setText("Cuisson : " + str(self.val_duree1[0]) +"h"+ str(self.val_duree1[1])+"min")

    def duree2(self):
        self.val_duree2 = (
            QInputDialog.getInt(self, "Durée du repos", "Nombre d'heures :")[0],
            QInputDialog.getInt(self, "Durée du repos", "Nombre de minutes :")[0],
        )
        self.btn7.setText("Repos : " + str(self.val_duree2[0]) +"h"+ str(self.val_duree2[1])+"min")

    def note(self):
        self.val_note = QInputDialog.getInt(self, "Note", "Note :", min=0, max=10)[0]
        self.btn3.setText(str(self.val_note)+"/10")

    def four(self):
        self.t_four = QInputDialog.getInt(self, "Four", "Température du four :")[0]
        self.btn5.setText("Four : " + str(self.t_four)+"°C")


    def nb(self):
        self.val_nb = QInputDialog.getInt(self, "Nombre de personnes", "Nombre de personnes :", min=0)[0]
        self.btn4.setText(str(self.val_nb)+" personnes")

    def save(self):
        name = self.nom_recette.text()
        recette = self.recette.toPlainText()
        ing = self.ingredients.getIngredients()
        epices = self.epices.getTags()
        tags = self.other_tags.getTags()
        query = QSqlQuery()
        query.exec("""select name from pragma_table_info('recettes')""")
        liste_ing = []
        name = "'" + name + "'"
        while query.next():
            liste_ing.append(query.value(0))
        insertion_query = "INSERT INTO recettes (nom"
        for i in ing:
            if i[0] not in liste_ing:
                query.exec(f"""ALTER TABLE recettes ADD COLUMN {i[0]} TEXT""")
            insertion_query = insertion_query + "," + i[0]
            name = name + "," + "'" + i[1] + "'"
        insertion_query = insertion_query + ") VALUES (" + name + ")"
        query.exec(f"""{insertion_query}""")
        query.exec("""select id from recettes""")
        query.last()
        path = "mkdir ..\\data\\" + str(query.value(0))
        os.system(path)
        with open(f"..\\data\\{query.value(0)}\\{query.value(0)}.txt", "w") as f:
            f.write(recette)
        self.close()


w = MainWindow()
w.showMaximized()
sys.exit(app.exec_())


#listes
import sys
from PyQt5.QtWidgets import (
    QInputDialog,
    QApplication,
    QWidget,
    QGridLayout,
    QListWidget,
    QPushButton,
    QAbstractItemView,
    QMessageBox)
from PyQt5.QtCore import Qt

from PyQt5 import QtCore, QtGui, QtWidgets

class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._placeholder_text = ""

    @property
    def placeholder_text(self):
        return self._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, text):
        self._placeholder_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.rowCount() == 0:
            painter = QtGui.QPainter(self.viewport())
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                self.placeholder_text, QtCore.Qt.ElideRight, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), QtCore.Qt.AlignCenter, elided_text)
            painter.restore()

class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._placeholder_text = ""

    @property
    def placeholder_text(self):
        return self._placeholder_text

    @placeholder_text.setter
    def placeholder_text(self, text):
        self._placeholder_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QtGui.QPainter(self.viewport())
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                self.placeholder_text, QtCore.Qt.ElideRight, self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), QtCore.Qt.AlignCenter, elided_text)
            painter.restore()

class liste_bouttons(QWidget):
    def __init__(self,liste,texte):
        super().__init__()
        self.liste=liste
        layout = QGridLayout(self)
        self.setLayout(layout)

        self.list_widget = ListWidget()
        self.list_widget.placeholder_text= texte
        layout.addWidget(self.list_widget, 0, 0, 4, 1)

        # create buttons
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add)

        insert_button = QPushButton("Modifier")
        insert_button.clicked.connect(self.insert)

        remove_button = QPushButton("Supprimer")
        remove_button.clicked.connect(self.remove)

        clear_button = QPushButton("Vider la liste")
        clear_button.clicked.connect(self.clear)

        layout.addWidget(add_button, 0, 1)
        layout.addWidget(insert_button, 1, 1)
        layout.addWidget(remove_button, 2, 1)
        layout.addWidget(clear_button, 3, 1)

        # show the window
        self.show()

    def add(self):
        text, ok = QInputDialog.getItem(self, "Add a New Wish", "New Wish:", self.liste, editable=True)
        if ok and text:
            self.list_widget.addItem(text)
            self.add()

    def insert(self):
        try:
            text, ok = QInputDialog.getText(
                self,
                "Insert a New Wish",
                "New Wish:",
                text=self.list_widget.currentItem().text(),
            )
            if ok and text:
                current_row = self.list_widget.currentRow()
                self.list_widget.insertItem(current_row + 1, text)
                self.remove()
        except:
            QMessageBox.about(self,"Erreur","Aucun item n'est sélectionné")

    def remove(self):
        try:
            current_row = self.list_widget.currentRow()
            if current_row >= 0:
                current_item = self.list_widget.takeItem(current_row)
                del current_item
        except:
            QMessageBox.about(self,"Erreur","Aucun item n'est sélectionné")
    def clear(self):
        self.list_widget.clear()

    def getTags(self):
        return [
            self.list_widget.item(x).text() for x in range(self.list_widget.count())
        ]


class liste_ingredients(QWidget):
    def __init__(self, liste):
        super().__init__()
        self.liste = liste
        layout = QGridLayout(self)
        self.setLayout(layout)
        self.list_widget1 = ListWidget()
        self.list_widget1.placeholder_text = "Ingrédients"
        self.list_widget1.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_widget2 = ListWidget()
        self.list_widget2.placeholder_text = "Quantités"
        self.list_widget2.setSelectionMode(QAbstractItemView.MultiSelection)

        layout.addWidget(self.list_widget1, 0, 0, 4, 1)
        layout.addWidget(self.list_widget2, 0, 1, 4, 1)
        # create buttons
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add)

        insert_button = QPushButton("Modifier")
        insert_button.clicked.connect(self.insert)

        remove_button = QPushButton("Supprimer")
        remove_button.clicked.connect(self.remove)

        clear_button = QPushButton("Vider la liste")
        clear_button.clicked.connect(self.clear)

        layout.addWidget(add_button, 0, 2)
        layout.addWidget(insert_button, 1, 2)
        layout.addWidget(remove_button, 2, 2)
        layout.addWidget(clear_button, 3, 2)
        self.liste_ing=[]
        # show the window
        self.show()

    def add(self):
        text, ok = QInputDialog.getItem(self, "Ajout d'un ingrédient", "Ingrédient:",self.liste)
        if ok and text and not text in self.liste_ing:
            l=self.liste.copy()
            l=[i.split(" (") for i in l]
            if text not in self.liste:
                try:
                    unite=text.split("(")[1][:-1]
                    text=text.split("(")[0][:-1]
                except:
                    ok = False
                    u=""
                    if text in [i[0] for i in l]:
                        u=l[[i[0] for i in l].index(text)][1][:-1]
                    while not(ok):
                        unite, ok = QInputDialog.getText(self, "Nouvel ingrédient","Unité :",text=u)
                        if not ok:
                            QMessageBox.about(self,"Nouvel ingrédient","Indiquer une unité")
            else:
                i=self.liste.index(text)
                try:
                    unite=l[i][1][:-1]
                except:
                    unite=""
            if unite=="":
                text1, ok1 = QInputDialog.getText(self, "Ajout d'un ingrédient", "Quantité:")
            else:
                text1, ok1 = QInputDialog.getDouble(self, "Ajout d'un ingrédient", "Quantité (en " + unite + ")")
            if ok1 and text1:
                if unite != "":
                    text=text+" ("+unite+")"
                self.liste_ing.append(text)
                self.liste.append(text)
                self.list_widget1.addItem(text)
                self.list_widget2.addItem(str(text1) + " " + unite)
            self.add()
        elif ok and self.list_widget1.findItems(text,Qt.MatchFlag.MatchExactly):
            QMessageBox.about(self,"error","l'ingrédient a déjà été ajouté")
            self.add()

    def insert(self):
        rows=[]
        for item in self.list_widget1.selectedItems():
            text, ok = QInputDialog.getText(
                self, "Modification de l'ingrédient", "Nouvel ingrédient:", text=item.text()
            )
            if ok and text and not self.list_widget1.findItems(text,Qt.MatchFlag.MatchExactly):
                l=self.liste.copy()
                l=[i.split("(") for i in l]
                if text not in [i[0] for i in l]:
                    try:
                        unite=text.split("(")[1][:-1]
                    except:
                        ok = False
                        while not(ok):
                            unite, ok = QInputDialog.getText(self, "Nouvel ingrédient","Unité :")
                            if not ok:
                                QMessageBox.about(self,"Nouvel ingrédient","Indiquer une unité")
                else:
                    i=self.liste.index(text)
                    try:
                        unite=l[i][1][:-1]
                    except:
                        unite=""
                if unite=="":
                    text1, ok1 = QInputDialog.getText(self, "Ajout d'un ingrédient", "Quantité:")
                else:
                    text1, ok1 = QInputDialog.getDouble(self, "Ajout d'un ingrédient", "Quantité (en " + unite + ")")
                if ok1 and text1:
                    item.setText(text)
                    row=self.list_widget1.row(item)
                    rows.append(row)
                    item2=self.list_widget2.item(row)
                    item2.setText(str(text1) + " " + unite)
            elif ok and self.list_widget1.findItems(text,Qt.MatchFlag.MatchExactly):
                QMessageBox.about(self,"error","l'ingrédient a déjà été ajouté")
                self.insert()
        for item in self.list_widget2.selectedItems():
            if self.list_widget2.row(item) not in rows:
                val=self.list_widget1.item(self.list_widget2.row(item)).text()
                val=val.split("(")
                try:
                    unite=val[1][:-1]
                except:
                    unite=""
                if unite=="":
                    text1, ok1 = QInputDialog.getText(self, "Ajout d'un ingrédient", "Quantité:")
                else:
                    text1, ok1 = QInputDialog.getDouble(self, "Ajout d'un ingrédient", "Quantité (en " + unite + ")")
                if ok1 and text1:
                    item.setText(str(text1))

    def remove(self):
        try:
            current_row = max(
                self.list_widget1.currentRow(), self.list_widget2.currentRow()
            )
            print(current_row)
            if current_row >= 0:
                current_item = self.list_widget1.takeItem(current_row)
                del current_item
                current_item = self.list_widget2.takeItem(current_row)
                del current_item
        except:
            QMessageBox.about(self,"Erreur","Aucun item n'est sélectionné")

    def clear(self):
        self.list_widget1.clear()
        self.list_widget2.clear()

    def getIngredients(self):
        ingredients = [
            (self.list_widget1.item(x).text(), self.list_widget2.item(x).text())
            for x in range(self.list_widget1.count())
        ]
        return ingredients


import PyQt5
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit, QGridLayout
import os
from img_viewer import Slides

#createTableQuery.exec("""CREATE TABLE recettes(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,nom TEXT,note DOUBLE, duree DOUBLE, duree1 DOUBLE, duree2 DOUBLE,nb INT,t INT)""")

class fenetre_affichage(QWidget):
    def __init__(self, id, con):
        self.con = con
        super().__init__()
        self.setGeometry(600, 100, 800, 600)
        self.layout = QVBoxLayout()
        query = QSqlQuery()
        query2 = QSqlQuery()
        query3 = QSqlQuery()
        query4 = QSqlQuery()
        liste_img=os.listdir(f"..\\data\\{id}")
        i=0
        n=len(liste_img)
        while i<n:
            if liste_img[i].split(".")[1]=='txt':
                liste_img.pop(i)
            else:
                liste_img[i]=f"..\\data\\{id}\\"+liste_img[i]
                i+=1
            n=len(liste_img)
        self.slide=Slides(liste_img)
        self.slide.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Ignored,PyQt5.QtWidgets.QSizePolicy.Preferred)
        query.exec(f"""select * from recettes where id={id}""")
        query2.exec("""select name from pragma_table_info('recettes')""")
        query3.exec(f"""select * from ing_bis where id={id}""")
        query4.exec("""select name from pragma_table_info('ing_bis')""")
        query.first()
        query4.first()
        query2.first()
        query3.first()
        for i in range(7):
            query2.next()
        name = query.value(1)
        with open(f"../data/{id}/{id}.txt", "r", encoding='utf8') as file:
            data = file.read()
        self.titre = QLabel()
        self.titre.setText(name)
        self.titre.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        font1=self.titre.font()
        font1.setPointSize(20)
        self.titre.setFont(font1)
        self.layout.addWidget(self.titre)
        self.container1=QWidget()
        self.lay_container1=QHBoxLayout()
        self.containerIngredients=QWidget()
        self.container3=QWidget()
        self.lay_container3=QHBoxLayout()
        self.layout.addWidget(self.container3)
        self.lay_containerIngredients=QVBoxLayout()
        self.lay_container1.addWidget(self.containerIngredients)
        self.label2 = QPlainTextEdit(self.container1,plainText=data, readOnly=True)
        self.label2.setStyleSheet("background-color: rgb(53,53,53)")
        self.label2.setFrameStyle(0)
        self.lay_container1.addWidget(self.label2)
        self.container4=QWidget()
        self.lay_container4=QGridLayout()
        self.lbl1=QLabel()
        a=str(int((query.value(3)-int(query.value(3)))*60))
        if len(a)==1:
            a='0'+a
        self.lbl1.setText("Durée de préparation : "+str(int(query.value(3)))+"h"+a)
        self.lbl2=QLabel()
        a=str(int((query.value(4)-int(query.value(4)))*60))
        if len(a)==1:
            a='0'+a
        self.lbl2.setText("Durée de cuisson : "+str(int(query.value(4)))+"h"+a)
        self.lbl3=QLabel()
        a=str(int((query.value(5)-int(query.value(5)))*60))
        if len(a)==1:
            a='0'+a
        self.lbl3.setText("Durée de repos : "+str(int(query.value(5)))+"h"+a)
        self.lbl4 = QLabel()
        self.lbl4.setText(f"{query.value(2)}/10")
        self.lbl5 = QLabel()
        self.lbl5.setText(f"{query.value(6)} personnes")
        self.lbl6 =QLabel()
        if query.value(7)>0:
            self.lbl6.setText(f"Température du four : {query.value(7)}°C")
        else:
            self.lbl6.setText("Pas de four")
        self.l_lbl=[[self.lbl1,self.lbl2,self.lbl3],[self.lbl4,self.lbl5,self.lbl6]]
        self.lay_container4.addWidget(self.slide,0,0,3,1)
        for i in range(3):
            for j in range(2):
                self.lay_container4.addWidget(self.l_lbl[j][i],i,j+1)
        self.lay_container3.addWidget(self.container4)
        self.container4.setLayout(self.lay_container4)
        self.container3.setLayout(self.lay_container3)
        self.layout.addWidget(self.container1)
        n = 7
        i=1
        while query4.next() :
            label = QLabel()
            while query2.value(0)!=query4.value(0):
                query2.next()
                n=n+1
            if query3.value(i)!="":
                label.setText(query4.value(0) + " : " + str(abs(query.value(n)))+" " + query3.value(i))
            else:
                label.setText(str(abs(query.value(n)))+" " + query4.value(0))
            self.lay_containerIngredients.addWidget(label)
            n += 1
            i=i+1
            query2.next()
        self.lay_containerIngredients.addStretch()
        self.containerIngredients.setLayout(self.lay_containerIngredients)
        self.container1.setLayout(self.lay_container1)
        self.setLayout(self.layout)
