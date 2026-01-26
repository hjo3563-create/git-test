import sys
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLabel, QPushButton, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.history_data = []
        self.initUI()
        self.new_calculation = False

    def initUI(self):
        self.setWindowTitle('Scientific Calculator')
        self.setFixedSize(750, 650) 
        self.setStyleSheet("background-color: #F2F2F2;")
        main_h_layout = QHBoxLayout()
        calc_layout = QVBoxLayout()
        self.history_label = QLabel("")
        self.history_label.setFixedHeight(40)
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.history_label.setStyleSheet("font-size: 20px; color: #707070; padding-right: 15px; border: none;")
        calc_layout.addWidget(self.history_label)
        self.display = QLabel("")
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("font-size: 50px; color: #000000; padding-right: 15px; font-weight: bold; border: none;")
        calc_layout.addWidget(self.display)
        grid = QGridLayout()
        grid.setSpacing(2)
        buttons = [
            ['2nd', 'π', 'e', 'C', '⌫'],
            ['x²', '1/x', '|x|', 'exp', 'mod'],
            ['²√x', '(', ')', 'n!', '÷'],
            ['xʸ', '7', '8', '9', '×'],
            ['10ˣ', '4', '5', '6', '−'],
            ['log', '1', '2', '3', '+'],
            ['ln', '+/-', '0', '.', '=']
        ]
        self.c_button = None 
        for r, row in enumerate(buttons):
            for c, btn_text in enumerate(row):
                button = QPushButton(btn_text)
                button.setFixedSize(85, 55)
                if btn_text.isdigit() or btn_text == '.':
                    style = "QPushButton { background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 4px; font-size: 18px; font-weight: bold; color: #000000; }"
                elif btn_text == '=':
                    style = "QPushButton { background-color: #0067B8; color: white; font-size: 24px; border: none; border-radius: 4px; }"
                else:
                    style = "QPushButton { background-color: #F9F9F9; border: 1px solid #E0E0E0; border-radius: 4px; font-size: 15px; color: #1A1A1A; }"
                button.setStyleSheet(style)
                button.clicked.connect(self.on_click)
                grid.addWidget(button, r, c)
                if btn_text == 'C': self.c_button = button
        calc_layout.addLayout(grid)
        main_h_layout.addLayout(calc_layout, stretch=3)
        history_layout = QVBoxLayout()
        history_title = QLabel("기록")
        history_title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 5px; color: #333;")
        history_layout.addWidget(history_title)
        self.history_list_widget = QListWidget()
        self.history_list_widget.setStyleSheet("QListWidget { background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 4px; padding: 5px; } QListWidget::item { border-bottom: 1px solid #F0F0F0; padding: 10px; font-size: 14px; }")
        history_layout.addWidget(self.history_list_widget)
        clear_btn = QPushButton("기록 모두 지우기")
        clear_btn.clicked.connect(self.history_list_widget.clear)
        history_layout.addWidget(clear_btn)
        main_h_layout.addLayout(history_layout, stretch=2)
        self.setLayout(main_h_layout)
        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if event.modifiers() & Qt.ControlModifier and key == Qt.Key_V:
            clipboard = QApplication.clipboard()
            pasted_text = clipboard.text()
            clean_text = pasted_text.replace('*', ' × ').replace('/', ' ÷ ').replace('-', ' − ')
            if self.new_calculation:
                self.display.setText("")
                self.history_label.setText("")
                self.new_calculation = False
            self.display.setText(self.display.text() + clean_text)
            self.adjust_font_size()
            self.update_c_button()
            return
        if Qt.Key_0 <= key <= Qt.Key_9: self.process_input(text)
        elif key in [Qt.Key_Plus, Qt.Key_Asterisk, Qt.Key_Slash]:
            mapping = {Qt.Key_Plus: '+', Qt.Key_Asterisk: '×', Qt.Key_Slash: '÷'}
            self.process_input(mapping[key])
        elif key == Qt.Key_Minus: self.process_input('−')
        elif key in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal]: self.process_input('=')
        elif key == Qt.Key_Backspace: self.process_input('⌫')
        elif key == Qt.Key_Escape: self.process_input('C')
        elif text in ['(', ')', '.']: self.process_input(text)

    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    def divide(self, a, b): return a / b if b != 0 else "Error"
    def modulo(self, a, b): return a % b
    def power(self, a, b): return math.pow(a, b)
    def get_factorial(self, n):
        if n < 0: return "Error"
        if n == 0 or n == 1: return 1
        res = 1
        for i in range(2, int(n) + 1): res *= i
        return res
    def get_square(self, n): return n * n
    def get_inverse(self, n): return 1 / n if n != 0 else "Error"
    def get_absolute(self, n): return abs(n)
    def get_sqrt(self, n): return math.sqrt(n) if n >= 0 else "Error"
    def get_pi(self): return math.pi
    def get_e(self): return math.e
    def get_log(self, n): return math.log10(n) if n > 0 else "Error"
    def get_ln(self, n): return math.log(n) if n > 0 else "Error"
    def get_negation(self, n): return n * -1
    def get_exp(self, n): return math.exp(n)

    def format_result(self, res):
        try:
            if abs(res) >= 1e15 or (0 < abs(res) < 1e-10): return "{:.20e}".format(res)
            return str(int(res)) if float(res).is_integer() else str(round(res, 15))
        except: return "Error"

    def adjust_font_size(self):
        text_length = len(self.display.text())
        if text_length <= 12: fs = 50
        elif text_length <= 18: fs = 35
        elif text_length <= 28: fs = 22
        elif text_length <= 40: fs = 14
        else: fs = 11
        self.display.setStyleSheet(f"font-size: {fs}px; color: #000000; padding-right: 15px; font-weight: bold; border: none;")

    def update_c_button(self):
        if self.display.text(): self.c_button.setText("CE")
        else: self.c_button.setText("C")

    def on_click(self):
        btn_text = self.sender().text()
        self.process_input(btn_text)
        self.update_c_button()
        self.adjust_font_size()

    def process_input(self, btn_text):
        current = self.display.text()
        if btn_text == 'C': self.display.setText(""); self.history_label.setText(""); return
        if btn_text == 'CE':
            parts = current.rstrip().split(' ')
            if parts:
                parts.pop()
                new_text = ' '.join(parts)
                if new_text and current.endswith(' '): new_text += ' '
                self.display.setText(new_text)
            return
        if btn_text == '⌫': self.display.setText(current[:-1]); return
        if self.new_calculation and (btn_text.isdigit() or btn_text in ['π', 'e', '(', '.']):
            self.display.setText(""); self.history_label.setText(""); self.new_calculation = False; current = ""
        if btn_text == '=':
            if not current or current.count('(') != current.count(')'): self.display.setText("잘못된 입력입니다")
            else:
                result = self.calculate(current)
                if result != "Error":
                    item = QListWidgetItem(f"{current} = {result}")
                    item.setTextAlignment(Qt.AlignRight); self.history_list_widget.insertItem(0, item)
                self.history_label.setText(current + " ="); self.display.setText(result); self.new_calculation = True
            return
        if btn_text in ['+', '−', '×', '÷', 'mod', 'xʸ']:
            self.new_calculation = False; op_map = {'xʸ': '^'}; self.display.setText(current + f" {op_map.get(btn_text, btn_text)} ")
        elif btn_text == '(': self.display.setText(current + btn_text + " ")
        elif btn_text == ')':
            if current.count('(') > current.count(')'): self.display.setText(current + " " + btn_text)
        elif btn_text in ['π', 'e']:
            val = str(self.get_pi())
            if not current or current.endswith(' ') or current.endswith('('): self.display.setText(current + val)
        elif btn_text in ['1/x', 'x²', 'n!', '|x|', '²√x', '10ˣ', 'log', 'ln', '+/-', 'exp']:
            if not current or current.endswith(' ') or current.endswith('('): return
            parts = current.split()
            try:
                num = float(parts[-1].replace(')', ''))
                if btn_text == '1/x': res = self.get_inverse(num)
                elif btn_text == 'x²': res = self.get_square(num)
                elif btn_text == 'n!': res = self.get_factorial(int(num))
                elif btn_text == '|x|': res = self.get_absolute(num)
                elif btn_text == '²√x': res = self.get_sqrt(num)
                elif btn_text == '10ˣ': res = math.pow(10, num)
                elif btn_text == 'log': res = self.get_log(num)
                elif btn_text == 'ln': res = self.get_ln(num)
                elif btn_text == '+/-': res = self.get_negation(num)
                elif btn_text == 'exp': res = self.get_exp(num)
                if res == "Error": self.display.setText("Error")
                else: self.display.setText(" ".join(parts[:-1] + [self.format_result(res)]))
            except: self.display.setText("Error")
        else: self.display.setText(current + btn_text)

    def calculate(self, expr):
        try:
            safe_expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-').replace('^', '**').replace('mod', '%')
            res = eval(safe_expr)
            return self.format_result(res)
        except: return "Error"

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = ScientificCalculator(); sys.exit(app.exec_())