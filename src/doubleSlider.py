from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QDoubleSpinBox,
    QComboBox,
)


class InputQuantite(QWidget):
    def __init__(self, wind, l=["", "a", "b"], tabConv=None):
        self.tabConv = tabConv
        super(InputQuantite, self).__init__()
        self.unite = QComboBox(editable=False)
        self.unite.addItems(l)
        self.u = l[0]
        self.mini = QDoubleSpinBox(prefix="Minimum : ", suffix=" " + self.u)
        self.maxi = QDoubleSpinBox(
            maximum=float("inf"), prefix="Maximum : ", suffix=" " + self.u
        )
        self.mini.valueChanged.connect(self.changeMin)
        self.maxi.valueChanged.connect(self.changeMax)
        self.unite.currentIndexChanged.connect(self.change)
        cont = QWidget()
        hbox = QHBoxLayout()
        self.btn_save = QPushButton("Ok")
        self.btn_cancel = QPushButton("Annuler")
        hbox.addWidget(self.btn_cancel)
        self.btn_cancel.pressed.connect(self.cancel)
        hbox.addWidget(self.btn_save)
        self.btn_save.pressed.connect(lambda: self.save(wind))
        cont.setLayout(hbox)
        vbox = QVBoxLayout()
        vbox.addWidget(self.unite)
        vbox.addWidget(self.mini)
        vbox.addWidget(self.maxi)
        vbox.addWidget(cont)
        self.setLayout(vbox)

    def change(self):
        self.u = self.unite.currentText()
        self.mini.setSuffix(" " + self.u)
        self.maxi.setSuffix(" " + self.u)

    def changeMin(self):
        self.maxi.setMinimum(self.mini.value())

    def changeMax(self):
        self.mini.setMaximum(self.maxi.value())

    def cancel(self):
        self.close()

    def save(self, wind):
        if self.u != "":
            amount = f"entre {self.mini.value()} et {self.maxi.value()} {self.u}"
            wind.amount = (
                self.convert(self.mini.value()),
                self.convert(self.maxi.value()),
            )
        else:
            amount = f"entre {self.mini.value()} et {self.maxi.value()}"
            wind.amount = (-self.mini.value(), -self.maxi.value())
        wind.btn.setText(amount)
        self.close()

    def convert(self, x):
        return x * self.tabConv[self.u]
