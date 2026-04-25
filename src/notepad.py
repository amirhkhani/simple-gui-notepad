from PyQt6.QtWidgets import QMainWindow, QTextEdit, QMessageBox, QFileDialog, QInputDialog, QFontDialog, QApplication
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtGui import QAction, QIcon, QTextCursor, QColor
from PyQt6.QtCore import Qt
from sys import exit

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.opened_file = None
        self.config_main_window()
        self.menu_act()
        self.menu_list()
        self.show()

    def config_main_window(self):
        self.setWindowTitle("Notepad Gui")
        self.resize(800, 600)
        self.move((1920 // 2) - (self.width() // 2),
                  self.height() // 3)
        self.setMinimumSize(400, 100)
        self.setWindowIcon(QIcon("../images/notepad.png"))

        self.text_box = QTextEdit()
        self.setCentralWidget(self.text_box)
        self.text_box.setStyleSheet("font-size: 25px")

        self.text_box.cursorPositionChanged.connect(lambda: self.text_box.setExtraSelections([]))

    def menu_list(self):
        menu = self.menuBar()
        menu.setStyleSheet("font-size: 23px;")

        self.file = self.menuBar().addMenu("&File")
        self.edit = self.menuBar().addMenu("&Edit")
        self.tools = self.menuBar().addMenu("&Tools")
        self.help = self.menuBar().addMenu("&Help")

        self.file.addAction(self.new_file_act)
        self.file.addAction(self.open_file_act)
        self.file.addSeparator()
        self.file.addAction(self.save_file_act)
        self.file.addAction(self.save_as_file_act)
        self.file.addSeparator()
        self.file.addAction(self.quit_act)

        self.edit.addAction(self.undo_act)
        self.edit.addAction(self.redo_act)
        self.edit.addSeparator()
        self.edit.addAction(self.copy_act)
        self.edit.addAction(self.cut_act)
        self.edit.addAction(self.paste_act)
        self.edit.addSeparator()
        self.edit.addAction(self.find_all_act)

        self.tools.addAction(self.font_act)
        self.tools.addAction(self.color_act)
        self.tools.addAction(self.highlight_act)
        self.tools.addAction(self.b_color_act)

        self.help.addAction(self.about_act)

    def menu_act(self):
        self.new_file_act = QAction(QIcon("../images/new.png"), "New")
        self.new_file_act.setShortcut("Ctrl+N")
        self.new_file_act.triggered.connect(self.new_file)

        self.open_file_act = QAction(QIcon("../images/open.png"), "Open")
        self.open_file_act.setShortcut("Ctrl+O")
        self.open_file_act.triggered.connect(self.open_file)

        self.save_file_act = QAction(QIcon("../images/save.png"), "Save")
        self.save_file_act.setShortcut("Ctrl+S")
        self.save_file_act.triggered.connect(self.save_file)

        self.save_as_file_act = QAction(QIcon("../images/save.png"), "Save as ...")
        self.save_as_file_act.setShortcut("Ctrl+Shift+S")
        self.save_as_file_act.triggered.connect(self.save_as)

        self.quit_act = QAction(QIcon("../images/quit.png"), "Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

        self.undo_act = QAction(QIcon("../images/undo.png"), "Undo")
        self.undo_act.setShortcut("Ctrl+Z")
        self.undo_act.triggered.connect(self.text_box.undo)

        self.redo_act = QAction(QIcon("../images/redo.png"), "Redo")
        self.redo_act.setShortcut("Ctrl+Shift+Z")
        self.redo_act.triggered.connect(self.text_box.redo)

        self.copy_act = QAction(QIcon("../images/copy.png"), "Copy")
        self.copy_act.setShortcut("Ctrl+C")
        self.copy_act.triggered.connect(self.text_box.copy)

        self.cut_act = QAction(QIcon("../images/cut.png"), "Cut")
        self.cut_act.setShortcut("Ctrl+X")
        self.cut_act.triggered.connect(self.text_box.cut)

        self.paste_act = QAction(QIcon("../images/paste.png"), "Paste")
        self.paste_act.setShortcut("Ctrl+V")
        self.paste_act.triggered.connect(self.text_box.paste)

        self.find_all_act = QAction(QIcon("../images/find.png"), "Find All")
        self.find_all_act.setShortcut("Ctrl+F")
        self.find_all_act.triggered.connect(self.find_all)

        self.font_act = QAction(QIcon("../images/font.png"), "Font")
        self.font_act.setShortcut("Ctrl+P")
        self.font_act.triggered.connect(self.choose_font)

        self.color_act = QAction(QIcon("../images/color.png"), "Color")
        self.color_act.setShortcut("Ctrl+Shift+C")
        self.color_act.triggered.connect(self.choose_color)

        self.highlight_act = QAction(QIcon("../images/highlight.png"), "Highlight")
        self.highlight_act.setShortcut("Ctrl+H")
        self.highlight_act.triggered.connect(self.highlight)

        self.b_color_act = QAction(QIcon("../images/b_color.png"), "Background-Color")
        self.b_color_act.setShortcut("Ctrl+Shift+B")
        self.b_color_act.triggered.connect(self.choose_b_color)

        self.about_act = QAction(QIcon("../images/question.png"), "About")
        self.about_act.setShortcut("Ctrl+?")
        self.about_act.triggered.connect(self.about)

    def new_file(self):
        text = None
        if self.opened_file:
            with open(self.opened_file, "r", encoding="utf-8") as file:
                text = file.read()
        if text and text == self.text_box.toPlainText():
            self.text_box.clear()
            self.opened_file = None
        else:
            self.new_file_flag = True
            while self.new_file_flag:
                user_choice = QMessageBox.question(self, "New File",
                                                   "Do you want to save this text file before open new file?",
                                                   QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.No | \
                                                   QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Cancel)
                if user_choice == QMessageBox.StandardButton.Ok:
                    if self.save_file():
                        self.new_file_flag = False
                        self.text_box.clear()
                        self.opened_file = None
                elif user_choice == QMessageBox.StandardButton.No:
                    self.text_box.clear()
                    self.new_file_flag = False
                else:
                    self.new_file_flag = False

    def save_file(self):
        if self.opened_file:
            with open(self.opened_file, "w", encoding="utf-8") as file:
                file.write(self.text_box.toPlainText())
            QMessageBox.information(self, "Saved", "File Saved successfully..!",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return True
        else:
            self.opened_file, flag = self.save_as()
            return True if flag else False

    def save_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "Text Files (*.txt);;Html Files (*.html);;All files (*.*)")
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                if filename.endswith(".html"):
                    file.write(self.text_box.toHtml())
                else:
                    file.write(self.text_box.toPlainText())
            QMessageBox.information(self, "Saved", "File Saved Successfully..!",
                                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return filename, True
        else:
            if self.opened_file:
                return self.opened_file, False
            return None, False

    def open_file(self):
        if self.opened_file or self.text_box.toPlainText() != "":
            self.new_file()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;"
                                                                         "Html Files (*.html);;All files (*.*)")
        if filename:
            self.opened_file = filename
            with open(filename, "r", encoding="utf-8") as file:
                text = file.read()
            self.text_box.setText(text)

    def closeEvent(self, event):
        text = None
        if self.opened_file:
            with open(self.opened_file, "r", encoding="utf-8") as file:
                text = file.read()
        if text and text == self.text_box.toPlainText():
            self.close_message(event)
        else:
            if self.text_box.toPlainText() == "":
                self.close_message(event)
            else:
                flag = True
                while flag:
                    user_choice = QMessageBox.question(self, "Quit without saving",
                                                       "Do you want to save this file before quit?",
                                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No |
                                                       QMessageBox.StandardButton.Cancel)
                    if user_choice == QMessageBox.StandardButton.No:
                        event.accept()
                        flag = False
                    elif user_choice == QMessageBox.StandardButton.Cancel:
                        flag = False
                        event.ignore()
                    else:
                        if self.save_file():
                            flag = False
                            event.accept()

    def close_message(self, event):
        q = QMessageBox.question(self, "Quit", "Do you want to close this notepad?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                 QMessageBox.StandardButton.No)
        if q == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def find_all(self):
        text, ok = QInputDialog.getText(self, "Find All", "Find this: ")
        if ok:
            selections = list()
            self.text_box.moveCursor(QTextCursor.MoveOperation.Start)
            while self.text_box.find(text):
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(QColor(Qt.GlobalColor.gray))
                selection.cursor = self.text_box.textCursor()
                selections.append(selection)
            self.text_box.moveCursor(QTextCursor.MoveOperation.End)
            self.text_box.setExtraSelections(selections)

    def choose_font(self):
        current_font = self.text_box.currentFont()
        font, ok = QFontDialog.getFont(current_font, self, options=QFontDialog.FontDialogOption.DontUseNativeDialog)
        if ok:
            ans = QMessageBox.question(self, "Choose Font", "Set font for current text?\n(for all texts of "
                                                            "this file choose <Yes All>",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No |
                                       QMessageBox.StandardButton.YesAll, QMessageBox.StandardButton.No)
            if ans == QMessageBox.StandardButton.Yes:
                self.text_box.setCurrentFont(font)
            elif ans == QMessageBox.StandardButton.YesAll:
                self.text_box.setFont(font)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_box.setTextColor(color)

    def highlight(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_box.setTextBackgroundColor(color)

    def choose_b_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color = color.name()
            self.text_box.setStyleSheet(f"background-color: {color}")

    def about(self):
        QMessageBox.about(self, "About Notepad", "this is a simple notepad_GUI application "
                                                 "developed by TESA")


if __name__ == '__main__':
    app = QApplication([])
    notepad = Notepad()
    exit(app.exec())
