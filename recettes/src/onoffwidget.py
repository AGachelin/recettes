from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QCheckBox,
    
)
from doubleSlider import InputQuantite
from PyQt5.QtSql import QSqlQuery

class CheckBox(QCheckBox):
    def __init__(self,parent=None):
        super().__init__(parent)
    def nextCheckState(self) -> None:
        if self.checkState()==1:
            self.setCheckState(0)
        elif self.checkState()==0:
            self.setCheckState(2)
        else:
            self.setCheckState(1)

class OnOffWidget(QWidget):
    def __init__(self, name, amount_range=None, tabConv=None):
        super(OnOffWidget, self).__init__()
        self.name = name
        query=QSqlQuery()
        self.is_on = False
        self.lbl = QLabel(self.name)
        self.btn_on = CheckBox()
        self.btn_on.setTristate(True)
        self.btn = QPushButton("Spécifier la quantité")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btn_on)
        self.hbox.addWidget(self.lbl)
        if amount_range is not None:
            self.tabConv={i:tabConv[i].copy() for i in tabConv}
            query.exec(f"""select * from ingredients where nom='{name}'""")
            query.first()
            allowed=[query.value(i) for i in range(1,5)]            
            self.amount_range = [""]
            if allowed[1]:
                self.amount_range+=amount_range['Masse'].copy()
            if allowed[2]:
                self.amount_range+=amount_range['Volume'].copy()
            if query.value(4)>0:
                for i in self.tabConv['Volume']:
                    self.tabConv['Volume'][i]*=query.value(4)
            self.tabConv=[self.tabConv[i] for i in self.tabConv]
            self.tabConv=self.tabConv[0] | self.tabConv[1]
            self.hbox.addWidget(self.btn)
            self.btn.setVisible(self.is_on)
            self.btn_on.stateChanged.connect(self.change)
            self.btn.clicked.connect(self.qte)
        self.setLayout(self.hbox)
        self.hbox.addStretch()


    def qte(self):
        self.f=InputQuantite(self,self.amount_range,self.tabConv)
        self.f.show()
        
    def change(self):
        self.is_on = self.btn_on.checkState()==2
        self.btn.setVisible(self.is_on)
        if not (self.is_on):
            self.btn.setText("Spécifier la quantité")

    def show(self):
        for w in [self, self.lbl, self.btn_on]:
            w.setVisible(True)
        self.btn.setVisible(self.is_on)

    def hide(self):
        for w in [self, self.lbl, self.btn_on]:
            w.setVisible(False)
        self.btn.setVisible(self.is_on)

    def checked(self):
        if self.btn_on.checkState()==2:
            try:
                return self.amount
            except :
                return (0,0)
        elif self.btn_on.checkState()==0:
            return True
        else:
            return False
