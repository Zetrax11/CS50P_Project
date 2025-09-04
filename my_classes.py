from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, 
                             QLineEdit, QTabWidget, QFormLayout, QComboBox, QDialogButtonBox, 
                             QMessageBox, QTableWidget, QTableWidgetItem, QSizePolicy)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

MONTHS = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(figsize=(5,4))
        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
class MainWindow(QMainWindow):
    def __init__(self, init_expenses):
        super().__init__()
        # Główne okno
        self.setWindowTitle("Expense tracker")
        self.resize(1000,700)
        self.setWindowIcon(QIcon("icon.png"))
        self.expenses = list(init_expenses)
        # Elementy form
        self.btn_add = QPushButton("Dodaj wydatek")
        self.btn_clear = QPushButton("Wyczyść listę")
        self.btn_clear_line = QPushButton("Usuń wiersz")
        self.amount = QLineEdit()
        self.category = QComboBox()
        self.month = QComboBox()
        # Dolny widget
        self.tabs = QTabWidget()
        # Wnętrze GUI
        self.initUI()
        self.load_table_data()
        self.update_charts()
        self.month.currentTextChanged.connect(self.update_charts)
        self.month.currentTextChanged.connect(self.update_sum)

    def initUI(self):
        # Górny widok
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        form = QFormLayout()
        # Przyciski
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_clear.clicked.connect(self.delete_data)
        self.btn_clear.setStyleSheet("color: red")
        self.btn_clear_line.clicked.connect(self.delete_line)
        self.btn_box = QDialogButtonBox()
        self.btn_box.addButton(self.btn_add, QDialogButtonBox.ActionRole)
        self.btn_box.addButton(self.btn_clear_line, QDialogButtonBox.ActionRole)

        self.btn_box.addButton(self.btn_clear, QDialogButtonBox.ActionRole)
        # pola do wpisu
        self.amount.setPlaceholderText("Podaj kwotę w PLN")
        self.category.addItems(["Jedzenie","Zachcianki","Ubrania","Oszczędności","Podróże", "Inne"])
        self.month.addItems(MONTHS)
        form.addRow("Kwota: ", self.amount)
        form.addRow("Kategoria: ", self.category)
        form.addRow("Miesiąc: ", self.month)
        # Napis z sumą 
        self.total = self.count_sum(self.month.currentText())
        self.sum = QLabel(f"Suma wszystkich wydatków w {self.month.currentText()}: {self.total:.2f} zł")
        self.sum.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        self.sum.setFont(font)
        # Dodawanie widgetów
        top_layout.addLayout(form)
        top_layout.addWidget(self.btn_box)
        top_layout.addWidget(self.sum)
        # Zakładki
        self.page1 = self.expense_list_page()
        self.page2 = self.pie_chart_page()
        self.page3 = self.bar_chart_page()
        self.tabs.addTab(self.page1, "Lista wydatków")
        self.tabs.addTab(self.page2, "Wykresy kołowe")
        self.tabs.addTab(self.page3, "Porównanie m->m")
        # Główne okno
        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.addWidget(top_widget)
        central_layout.addWidget(self.tabs)
        self.setCentralWidget(central)
    # Ustawienia strony z tabelą
    def expense_list_page(self):
        first_page = QWidget()
        first_page_vbox = QVBoxLayout(first_page)
        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(["Kwota", "Miesiąc", "Kategoria"])
        self.table.horizontalHeader().setStretchLastSection(True)
        style_sheet = "::section{Background-color:rgb(191,191,191)}"
        self.table.horizontalHeader().setStyleSheet(style_sheet)
        first_page_vbox.addWidget(self.table)
        return first_page
    # Ładowanie danych do tabeli
    def load_table_data(self):
        self.table.setRowCount(len(self.expenses))
        for a, b in enumerate(self.expenses):
            self.table.setItem(a, 0, QTableWidgetItem(f"{b["Kwota"]:.2f}"))
            self.table.setItem(a, 1, QTableWidgetItem(b["Miesiąc"]))
            self.table.setItem(a, 2, QTableWidgetItem(b["Kategoria"]))
    # Strona z wykresem kołowym
    def pie_chart_page(self):
        second_page = QWidget()
        second_page_vbox = QVBoxLayout(second_page)
        self.pie_chart = MplCanvas()
        self.pie_label = QLabel("Brak danych do wyświetlenia")
        self.pie_label.setAlignment(Qt.AlignCenter)
        second_page_vbox.addWidget(self.pie_label)
        second_page_vbox.addWidget(self.pie_chart)
        return second_page
    # Logika do wykresu kołowego
    def pie_logic(self, month):
        by_category = {}
        for entry in self.expenses:
            if entry["Miesiąc"] == month:
                by_category[entry["Kategoria"]] = by_category.get(entry["Kategoria"], 0.0) + entry["Kwota"]
        y = by_category.values()
        labels = by_category.keys()
        self.pie_chart.axes.clear()
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        self.pie_label.setText(f"Wydatki - {month}")
        self.pie_chart.axes.pie(y, labels=labels, autopct='%1.1f%%', colors=colors)
        self.pie_chart.draw()
    # Strona z wykresami kolumnowymi
    def bar_chart_page(self):
        third_page = QWidget()
        third_page_vbox = QVBoxLayout(third_page)
        self.bar_chart = MplCanvas()
        third_page_vbox.addWidget(self.bar_chart)
        return third_page
    # Logika do wykresów kolumnowych
    def bar_logic(self):
        months = [m for m in MONTHS if any(e["Miesiąc"] == m for e in self.expenses)]
        categories = sorted({e["Kategoria"] for e in self.expenses})
        value_by_cat = {m: {c: 0.0 for c in categories} for m in months}
        for entry in self.expenses:
            value_by_cat[entry["Miesiąc"]][entry["Kategoria"]] += float(entry["Kwota"])
        x = np.arange((len(months)))
        width = 0.8 / max(1, len(categories))
        self.bar_chart.axes.clear()
        for i, c in enumerate(categories):
            y = [value_by_cat[m][c] for m in months]
            self.bar_chart.axes.bar(x + i*width, y, width, label=c)
        self.bar_chart.axes.set_xticks(x + width*(len(categories)-1)/2)
        self.bar_chart.axes.set_xticklabels(months)
        self.bar_chart.axes.set_ylabel("[Zł]")
        self.bar_chart.axes.legend()
        self.bar_chart.draw()
    # Ponowne wywołanie logiki wykresów
    def update_charts(self):
        self.pie_logic(self.month.currentText())
        self.bar_logic()
    # Dodawanie wydatku
    def add_expense(self):
        formated_input = self.amount.text().strip().replace(",", ".")
        try:
            amount = float(formated_input)
        except ValueError:
            QMessageBox.warning(self,"Błąd", "Nieprawidłowy format danych, podaj liczbę")
            self.amount.clear()
            return
        if amount < 0:
            QMessageBox.warning(self, "Błąd", "Wartość nie może być niższa od 0")
            self.amount.clear()
            return
        month = self.month.currentText()
        category = self.category.currentText()
        self.expenses.append({"Kwota": amount, "Miesiąc": month, "Kategoria": category})
        self.update_sum(self.month.currentText())
        self.amount.clear()
        self.load_table_data()
        self.update_charts()
    # Usuwanie wszystkich wydatków
    def delete_data(self):
        self.expenses.clear()
        self.table.setRowCount(0)
        self.update_sum(self.month.currentText())
        self.update_charts()
    # Usuwanie wybranych wierszy
    def delete_line(self):
        rows = set()
        for index in self.table.selectedIndexes():
            rows.add(index.row())
        for row in sorted(rows, reverse=True):
            self.table.removeRow(row)
            self.expenses.pop(row)
        self.update_sum(self.month.currentText())
        self.update_charts()
    # Obliczanie sumy wydatków
    def count_sum(self, month):
        sum = 0
        for expense in self.expenses:
            if expense["Miesiąc"] == month:
                sum += expense["Kwota"]
        return sum
    # Aktualizacja info o sumie wydatków
    def update_sum(self,month):
        total = self.count_sum(month)
        self.sum.setText(f"Suma wszystkich wydatków w {month}: {total:.2f} zł")
    # Pobranie listy wydatków
    def get_expenses(self):
        return list(self.expenses)