from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # QLineEdit mit Platzhaltertext
        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText("Geben Sie Ihren Namen ein")
        layout.addWidget(line_edit)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()
