import sys
from PyQt5 import QtWidgets


def get_text_values(initial_texts, parent=None, title="", label=""):
    dialog = QtWidgets.QInputDialog()
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.show()
    # hide default QLineEdit
    # dialog.findChild(QtWidgets.QLineEdit).hide()
    print(dialog.children())
    editors = []
    for i, text in enumerate(initial_texts, start=1):
        editor = QtWidgets.QSpinBox(text=text)
        dialog.layout().insertWidget(i, editor)
        editors.append(editor)
    editors.append(dialog.findChild(QtWidgets.QLineEdit))
    ret = dialog.exec_() == QtWidgets.QDialog.Accepted
    return ret, [editor.text() for editor in editors]


def main():
    app = QtWidgets.QApplication(sys.argv)
    ok, texts = get_text_values(
        ["hello", "world", "a"], title="Input Dialog", label="Enter your name:"
    )
    print(ok, texts)


if __name__ == "__main__":
    main()


import sys
from PyQt5.QtWidgets import (
    QInputDialog,
    QApplication,
    QWidget,
    QGridLayout,
    QListWidget,
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
    def __init__(self, liste, texte):
        super().__init__()
        self.liste = liste
        layout = QGridLayout(self)
        self.setLayout(layout)

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

        # show the window
        self.show()

    def add(self):
        text, ok = QInputDialog.getItem(
            self, "Add a New Wish", "New Wish:", self.liste, editable=True
        )
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
            QMessageBox.about(self, "Erreur", "Aucun item n'est sélectionné")

    def remove(self):
        try:
            current_row = self.list_widget.currentRow()
            if current_row >= 0:
                current_item = self.list_widget.takeItem(current_row)
                del current_item
        except:
            QMessageBox.about(self, "Erreur", "Aucun item n'est sélectionné")

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

        # show the window
        self.show()

    def add(self):
        text, ok = QInputDialog.getItem(
            self, "Ajout d'un ingrédient", "Ingrédient:", self.liste
        )
        if (
            ok
            and text
            and not self.list_widget1.findItems(text, Qt.MatchFlag.MatchExactly)
        ):
            text1, ok1 = QInputDialog.getText(
                self, "Ajout d'un ingrédient", "Quantité:"
            )
            if ok1 and text1:
                self.list_widget1.addItem(text)
                self.list_widget2.addItem(text1)
            self.add()
        elif ok and self.list_widget1.findItems(text, Qt.MatchFlag.MatchExactly):
            QMessageBox.about(self, "error", "l'ingrédient a déjà été ajouté")
            self.add()

    def insert(self):
        try:
            for item in self.list_widget1.selectedItems():
                text, ok = QInputDialog.getText(
                    self, "Insert a New Wish", "New Wish:", text=item.text()
                )
                if ok and text:
                    item.setText(text)
            for item in self.list_widget2.selectedItems():
                text, ok = QInputDialog.getText(
                    self, "Insert a New Wish", "New Wish:", text=item.text()
                )
                if ok and text:
                    item.setText(text)
        except:
            QMessageBox.about(self, "Erreur", "Aucun item n'est sélectionné")

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
            QMessageBox.about(self, "Erreur", "Aucun item n'est sélectionné")

    def clear(self):
        self.list_widget1.clear()
        self.list_widget2.clear()

    def getIngredients(self):
        ingredients = [
            (self.list_widget1.item(x).text(), self.list_widget2.item(x).text())
            for x in range(self.list_widget1.count())
        ]
        return ingredients
