from PyQt5.QtWidgets import (
    QInputDialog,
    QWidget,
    QGridLayout,
    QPushButton,
    QAbstractItemView,
    QMessageBox,
)
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
    def __init__(self, liste, texte, l=[]):
        super().__init__()
        self.liste = liste
        layout = QGridLayout(self)
        self.setLayout(layout)
        if texte == "épices":
            self.texte = "épice"
        else:
            self.texte = "tag"
        self.liste_tag = []
        self.list_widget = ListWidget()
        self.list_widget.placeholder_text = texte
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
        for i in l:
            self.add(text1=i, ok=True)
        # show the window
        self.show()

    def add(self, text1="", ok=False):
        if not (ok):
            text, ok = QInputDialog.getItem(
                self,
                f"Ajout d'un {self.texte}",
                f"{self.texte[0].upper()+self.texte[1:]} :",
                self.liste,
                editable=True,
            )
        else:
            text = text1
        if ok and text and text not in self.liste_tag:
            self.list_widget.addItem(text)
            self.liste_tag.append(text)
            if text1 == "":
                self.add()
        elif ok and text:
            self.add()

    def insert(self):
        try:
            text, ok = QInputDialog.getText(
                self,
                "Modification",
                f"{self.texte} :",
                text=self.list_widget.currentItem().text(),
            )
            if ok and text and text not in self.liste_tag:
                current_row = self.list_widget.currentRow()
                self.list_widget.insertItem(current_row + 1, text)
                self.remove()
                self.liste_tag = (
                    self.liste_tag[:current_row] + [text] + self.liste_tag[current_row:]
                )
            elif ok and text:
                QMessageBox.about(self, "Erreur", "L'item a déjà été ajouté")
                self.insert()
        except:
            QMessageBox.about(self, "Erreur", "Aucun item n'est sélectionné")

    def remove(self):
        try:
            current_row = self.list_widget.currentRow()
            if current_row >= 0:
                self.liste_tag.pop(current_row)
                current_item = self.list_widget.takeItem(current_row)
                del current_item
        except:
            QMessageBox.about(self, "Erreur", "Aucun item n'est sélectionné")

    def clear(self):
        self.liste_tag = []
        self.list_widget.clear()

    def getTags(self):
        return self.liste_tag


class liste_ingredients(QWidget):
    def __init__(self, liste, unites, liste_ing={}):
        super().__init__()
        self.liste = liste
        self.unites = unites
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

        self.liste_ing = liste_ing
        for i in self.liste_ing:
            for j in self.unites:
                if self.liste_ing[i][1] in self.unites[j]:
                    liste_ing[i][0] = j
            if liste_ing[i][0] == "":
                liste_ing[i][0] = "Arbitraire"
            self.add(ing=i, lIng=liste_ing[i], ok1=False)
        self.show()

    def add(self, ing="", lIng=[], ok1=True):
        if ok1:
            text, ok = QInputDialog.getItem(
                self,
                "Ajout d'un ingrédient",
                "Ingrédient :",
                sorted(list(self.liste.keys())),
            )
            s = ["Masse", "Volume", "Arbitraire"]
            base = ["g", "mL"]
            rho = -1
            rapport = -1
            if ok and text and not text in self.liste_ing:
                if text not in self.liste:
                    ok = False
                    while not (ok):
                        syst, ok = QInputDialog.getItem(
                            self,
                            "Nouvel ingrédient",
                            "Système de mesure de l'ingrédient :",
                            s,
                        )
                        if not ok:
                            QMessageBox.about(
                                self,
                                "Nouvel ingrédient",
                                "Indiquer le système de mesure",
                            )
                    if syst == "Arbitraire":
                        unite, ok = QInputDialog.getText(
                            self,
                            "Ajout d'un ingrédient",
                            "Nom de l'unité arbitraire (laisser vide si c'est le nombre) :",
                        )
                    else:
                        ok = False
                        while not (ok):
                            unite, ok = QInputDialog.getItem(
                                self,
                                "Ajout d'un ingrédient",
                                "Unité :",
                                self.unites[syst],
                            )
                            if unite == "":
                                QMessageBox.about(
                                    self,
                                    "Nouvel ingrédient",
                                    "Indiquer une unité \n S'il n'y en a pas, annuler l'opération et spécifier le système de mesure comme étant 'Arbitraire'",
                                )
                                ok = False
                            elif unite not in self.unites[syst]:
                                i = (s.index(syst) + 1) % 2
                                if unite in self.unites[s[i]]:
                                    syst = s[i]
                                else:
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et {base[((i+1)%2)]} :",
                                        min=0.0000000001,
                                    )
                else:
                    syst = self.liste[text]["autorises"]
                    u = []
                    for i in self.liste[text]["autorises"]:
                        u = u + self.unites[i]
                    if self.liste[text]["Arbitraire"]:
                        u.append("Arbitraire")
                    unite, ok = QInputDialog.getItem(
                        self, "Ajout d'un ingrédient", "Unité :", u
                    )
                    if unite == "Arbitraire":
                        syst = "Arbitraire"
                        unite, ok = QInputDialog.getText(
                            self, "Ajout d'un ingrédient", "Nom de l'unité arbitraire :"
                        )
                    elif unite not in u:
                        if len(syst) > 0:
                            i = (s.index(syst[0]) + 1) % 2
                            if len(syst) == 1 and unite in self.unites[s[i]]:
                                syst = s[i]
                                rho, ok = QInputDialog.getDouble(
                                    self,
                                    "Ajout d'une unité",
                                    f"Masse volumique de l'ingrédient {text} :",
                                    min=0.0000000001,
                                )
                            else:
                                ok = QMessageBox.question(
                                    self,
                                    "Nouvelle unité",
                                    f"L'unité {unite} est-elle une unité de {s[((i+1)%2)]} ?",
                                )
                                if ok == 16384:
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et {base[((i+1)%2)]} :",
                                        min=0.0000000001,
                                    )
                                    syst = s[(i + 1) % 2]
                                else:
                                    if len(syst) == 1:
                                        rho, ok = QInputDialog.getDouble(
                                            self,
                                            "Ajout d'une unité",
                                            f"Masse volumique de l'ingrédient {text} :",
                                            min=0.0000000001,
                                        )
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et {base[i]} :",
                                        min=0.0000000001,
                                    )
                                    syst = s[i]
                        else:
                            if unite in self.unites["Masse"]:
                                syst = "Masse"
                            elif unite in self.unites["Volume"]:
                                syst = "Volume"
                            else:
                                ok = QMessageBox.question(
                                    self,
                                    "Nouvelle unité",
                                    f"L'unité {unite} est-elle une unité de masse ?",
                                )
                                if ok == 16384:
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et g :",
                                        min=0.0000000001,
                                    )
                                    syst = "Masse"
                                else:
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et mL :",
                                        min=0.0000000001,
                                    )
                                    syst = "Volume"

                    else:
                        for i in ["Masse", "Volume"]:
                            if unite in self.unites[i]:
                                syst = i
                if unite == "":
                    text1, ok1 = QInputDialog.getDouble(
                        self, "Ajout d'un ingrédient", "Quantité:", min=0.0000000001
                    )
                else:
                    text1, ok1 = QInputDialog.getDouble(
                        self,
                        "Ajout d'un ingrédient",
                        "Quantité (en " + unite + ")",
                        min=0.0000000001,
                    )
                if ok1 and text1:
                    self.liste_ing[text] = [syst, unite, text1, rho, rapport]
                    self.list_widget1.addItem(text)
                    self.list_widget2.addItem(str(text1) + " " + unite)
                self.add()
            elif ok and text:
                QMessageBox.warning(
                    self, "Ajout d'un ingrédient", "L'ingrédient a déjà été ajouté"
                )
                self.add()
        else:
            self.list_widget1.addItem(ing)
            unite = lIng[1]
            self.list_widget2.addItem(str(lIng[2]) + " " + unite)

    def insert(self):
        rows = []
        for item in self.list_widget1.selectedItems():
            item.setSelected(False)
            text, ok = QInputDialog.getText(
                self,
                "Modification de l'ingrédient",
                "Nouvel ingrédient:",
                text=item.text(),
            )
            s = ["Masse", "Volume", "Arbitraire"]
            base = ["g", "mL"]
            rho = -1
            rapport = -1
            if ok and text and text not in self.liste_ing:
                if text not in self.liste:
                    ok = False
                    while not (ok):
                        syst, ok = QInputDialog.getItem(
                            self,
                            "Nouvel ingrédient",
                            "Système de mesure de l'ingrédient :",
                            s,
                        )
                        if not ok:
                            QMessageBox.about(
                                self,
                                "Nouvel ingrédient",
                                "Indiquer le système de mesure",
                            )
                    if syst == "Arbitraire":
                        unite, ok = QInputDialog.getText(
                            self,
                            "Ajout d'un ingrédient",
                            "Nom de l'unité arbitraire (laisser vide si c'est le nombre) :",
                        )
                    else:
                        ok = False
                        while not (ok):
                            unite, ok = QInputDialog.getItem(
                                self,
                                "Ajout d'un ingrédient",
                                "Unité :",
                                self.unites[syst],
                            )
                            if unite == "":
                                QMessageBox.about(
                                    self,
                                    "Nouvel ingrédient",
                                    "Indiquer une unité \n S'il n'y en a pas, annuler l'opération et spécifier le système de mesure comme étant 'Arbitraire'",
                                )
                                ok = False
                            elif unite not in self.unites[syst]:
                                i = (s.index(syst) + 1) % 2
                                if unite in self.unites[s[i]]:
                                    syst = s[i]
                                else:
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et {base[((i+1)%2)]} :",
                                        min=0.0000000001,
                                    )
                else:
                    syst = self.liste[text]["autorises"]
                    u = []
                    for i in self.liste[text]["autorises"]:
                        u = u + self.unites[i]
                    if self.liste[text]["Arbitraire"]:
                        u.append("Arbitraire")
                    unite, ok = QInputDialog.getItem(
                        self, "Ajout d'un ingrédient", "Unité :", u
                    )
                    if unite == "Arbitraire":
                        syst = "Arbitraire"
                        unite, ok = QInputDialog.getText(
                            self, "Ajout d'un ingrédient", "Nom de l'unité arbitraire :"
                        )
                    elif unite not in u:
                        i = (s.index(self.liste[text]["base"]) + 1) % 2
                        if len(syst) == 1 and unite in self.unites[s[i]]:
                            syst = syst[0]
                            rho, ok = QInputDialog.getDouble(self, "Ajout d'une unité",f"{s[(i+1)%2]} {s[i][:-1].lower() + "ique"} de l'ingrédient {text} :",min=0.0000000001)
                        else:
                            ok = QMessageBox.question(self, "Nouvelle unité", f"L'unité {unite} est-elle une unité de {self.liste[text]["base"]} ?")
                            if ok == 16384:
                                rapport, ok = QInputDialog.getDouble(
                                    self,
                                    "Ajout d'une unité",
                                    f"Coefficient entre {unite} et {base[((i+1)%2)]} :",
                                    min=0.0000000001,
                                )
                                syst = s[(i + 1) % 2]
                            else:
                                if len(syst) == 1:
                                    rho, ok = QInputDialog.getDouble(self, "Ajout d'une unité",f"{s[(i+1)%2]} {s[i][:-1].lower() + "ique"} de l'ingrédient {text} :",min=0.0000000001)
                                rapport, ok = QInputDialog.getDouble(self, "Ajout d'une unité",f"Coefficient entre {unite} et {base[i]} :",min=0.0000000001)
                                syst = s[i]
                    else:
                        for i in ["Masse", "Volume"]:
                            if unite in self.unites[i]:
                                syst = i
                if unite == "":
                    text1, ok1 = QInputDialog.getDouble(
                        self, "Ajout d'un ingrédient", "Quantité:", min=0.0000000001
                    )
                else:
                    text1, ok1 = QInputDialog.getDouble(
                        self,
                        "Ajout d'un ingrédient",
                        "Quantité (en " + unite + ")",
                        min=0.0000000001,
                    )
                if ok1 and text1:
                    del self.liste_ing[item.text()]
                    item.setText(text)
                    row = self.list_widget1.row(item)
                    rows.append(row)
                    item2 = self.list_widget2.item(row)
                    item2.setText(str(text1) + " " + unite)
                    self.liste_ing[text] = [syst, unite, text1, rho, rapport]
            elif ok and self.list_widget1.findItems(text, Qt.MatchFlag.MatchExactly):
                QMessageBox.about(self, "error", "l'ingrédient a déjà été ajouté")
                self.insert()
        for item in self.list_widget2.selectedItems():
            item.setSelected(False)
            if self.list_widget2.row(item) not in rows:
                s = ["Masse", "Volume", "Arbitraire"]
                base = ["g", "mL"]
                rho = -1
                rapport = -1
                text = self.list_widget1.item(self.list_widget2.row(item)).text()
                if text not in self.liste:
                    syst, ok = QInputDialog.getItem(
                        self,
                        "Nouvel ingrédient",
                        "Système de mesure de l'ingrédient :",
                        s,
                    )
                    if syst == "Arbitraire":
                        unite, ok = QInputDialog.getText(
                            self,
                            "Ajout d'un ingrédient",
                            "Nom de l'unité arbitraire (laisser vide si c'est le nombre) :",
                        )
                    else:
                        ok = False
                        while not (ok):
                            unite, ok = QInputDialog.getItem(
                                self,
                                "Ajout d'un ingrédient",
                                "Unité :",
                                self.unites[syst],
                            )
                            if unite == "":
                                QMessageBox.about(
                                    self,
                                    "Nouvel ingrédient",
                                    "Indiquer une unité \n S'il n'y en a pas, annuler l'opération et spécifier le système de mesure comme étant 'Arbitraire'",
                                )
                                ok = False
                            elif unite not in self.unites[syst]:
                                i = (s.index(syst) + 1) % 2
                                if unite in self.unites[s[i]]:
                                    syst = s[i]
                                else:
                                    rapport, ok = QInputDialog.getDouble(
                                        self,
                                        "Ajout d'une unité",
                                        f"Coefficient entre {unite} et {base[((i+1)%2)]} :",
                                        min=0.0000000001,
                                    )
                else:
                    syst = self.liste[text]["autorises"]
                    u = []
                    for i in self.liste[text]["autorises"]:
                        u = u + self.unites[i]
                    if self.liste[text]["Arbitraire"]:
                        u.append("Arbitraire")
                    unite, ok = QInputDialog.getItem(
                        self, "Ajout d'un ingrédient", "Unité :", u
                    )
                    if unite == "Arbitraire":
                        syst = "Arbitraire"
                        unite, ok = QInputDialog.getText(
                            self, "Ajout d'un ingrédient", "Nom de l'unité arbitraire :"
                        )
                    elif unite not in u:
                        i = (s.index(self.liste[text]["base"]) + 1) % 2
                        if len(syst) == 1 and unite in self.unites[s[i]]:
                            syst = syst[0]
                            rho, ok = QInputDialog.getDouble(self, "Ajout d'une unité",f"{s[(i+1)%2]} {s[i][:-1].lower() + "ique"} de l'ingrédient {text} :",min=0.0000000001)
                        else:
                            ok = QMessageBox.question(self, "Nouvelle unité", f"L'unité {unite} est-elle une unité de {self.liste[text]["base"]} ?")
                            if ok == 16384:
                                rapport, ok = QInputDialog.getDouble(self, "Ajout d'une unité",f"Coefficient entre {unite} et {base[((i+1)%2)]} :",min=0.0000000001)
                                syst = s[(i + 1) % 2]
                            else:
                                if len(syst) == 1:
                                    rho, ok = QInputDialog.getDouble(self, "Ajout d'une unité",f"{s[(i+1)%2]} {s[i][:-1].lower() + "ique"} de l'ingrédient {text} :",min=0.0000000001)
                                rapport, ok = QInputDialog.getDouble(
                                    self,
                                    "Ajout d'une unité",
                                    f"Coefficient entre {unite} et {base[i]} :",
                                    min=0.0000000001,
                                )
                                syst = s[i]
                    else:
                        for i in ["Masse", "Volume"]:
                            if unite in self.unites[i]:
                                syst = i
                if unite == "":
                    text1, ok1 = QInputDialog.getDouble(
                        self, "Ajout d'un ingrédient", "Quantité:", min=0.0000000001
                    )
                else:
                    text1, ok1 = QInputDialog.getDouble(
                        self,
                        "Ajout d'un ingrédient",
                        "Quantité (en " + unite + ")",
                        min=0.0000000001,
                    )
                if ok1 and text1:
                    item.setText(str(text1) + " " + unite)
                    self.liste_ing[text] = [syst, unite, text1, rho, rapport]

    def remove(self):
        current_row = max(
            self.list_widget1.currentRow(), self.list_widget2.currentRow()
        )
        if current_row >= 0:
            current_item = self.list_widget1.takeItem(current_row)
            del self.liste_ing[current_item.text()]
            del current_item
            current_item = self.list_widget2.takeItem(current_row)
            del current_item

    def clear(self):
        self.liste_ing = {}
        self.list_widget1.clear()
        self.list_widget2.clear()

    def getIngredients(self):
        return self.liste_ing
