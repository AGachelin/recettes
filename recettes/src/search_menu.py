from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from onoffwidget import OnOffWidget


class search_menu(QWidget):
    def __init__(self, widget_names, amount_Range,tabConv):
        super(search_menu, self).__init__()
        self.global_lay = QVBoxLayout()
        self.widget_names = widget_names
        self.amount_Range = amount_Range
        self.scroll = QScrollArea()
        self.global_lay.addWidget(self.scroll)
        self.inner = QWidget(self.scroll)
        self.lay = QVBoxLayout(self.inner)
        self.widgets = []
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)
        # Autocomplete
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)
        self.lay.addWidget(self.searchbar)
        for i in range(len(widget_names)):
            item = OnOffWidget(self.widget_names[i], self.amount_Range, tabConv)
            self.lay.addWidget(item)
            self.widgets.append(item)
        self.scroll.setFixedWidth(250)
        self.inner.setLayout(self.lay)
        # Scroll Area Properties.

        self.scroll.setWidget(self.inner)
        self.scroll.setWidgetResizable(True)

        self.setLayout(self.global_lay)

    def update_display(self, text):
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def getWidgetNames(self):
        return self.widget_names
    
    def getAmountRanges(self):
        return self.amount_Range
    
    def getWidgets(self):
        return self.widgets

class search_menu_bis(QWidget):
    def __init__(self, widget_names):
        super(search_menu_bis, self).__init__()
        self.global_lay = QVBoxLayout()
        self.widget_names = widget_names
        self.scroll = QScrollArea()
        self.global_lay.addWidget(self.scroll)
        self.inner = QWidget(self.scroll)
        self.lay = QVBoxLayout(self.inner)
        self.widgets = []
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)
        self.lay.addWidget(self.searchbar)
        for i in range(len(widget_names)):
            item = OnOffWidget(self.widget_names[i])
            self.lay.addWidget(item)
            self.widgets.append(item)
        self.scroll.setFixedWidth(250)
        self.inner.setLayout(self.lay)
        self.scroll.setWidget(self.inner)
        self.scroll.setWidgetResizable(True)

        self.setLayout(self.global_lay)

    def update_display(self, text):
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def getWidgetNames(self):
        return self.widget_names
        
    def getWidgets(self):
        return self.widgets