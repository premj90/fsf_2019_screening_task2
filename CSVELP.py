import csv
import os
import re
from tkinter import filedialog, Tk
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QAction
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport


class PopUpPlotWindow(QtWidgets.QWidget):
    def __init__(self, plotType, MyWindowObject):
        super().__init__()

        
        self.setGeometry(50, 50, 650, 550)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.saveButton = QtWidgets.QPushButton("Save Image")
        self.saveButton.clicked.connect(self.saveImageAsPng)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.saveButton)

        
        self.rev = True

        self.reverseButton = QtWidgets.QPushButton("Reverse")
        if plotType == 1:
            self.reverseButton.clicked.connect(self.SaveRevDVal1)
        if plotType == 2:
            self.reverseButton.clicked.connect(self.SaveRevDVal2)
        if plotType == 3:
            self.reverseButton.clicked.connect(self.SaveRevDVal3)

        self.layout.addWidget(self.reverseButton)
        self.setLayout(self.layout)

        self.fileInstance = MyWindowObject

        if plotType == 1:
            self.plotScatterPoints(self.fileInstance, self.rev)
        if plotType == 2:
            self.plotScatterPointsWithLines(self.fileInstance, self.rev)
        if plotType == 3:
            self.plotLines(self.fileInstance, self.rev)

    def SaveRevDVal1(self):

        self.rev = self.reversePlot(self.rev)
        self.plotScatterPoints(self.fileInstance, self.rev)

    def SaveRevDVal2(self):

        self.rev = self.reversePlot(self.rev)
        self.plotScatterPointsWithLines(self.fileInstance, self.rev)

    def SaveRevDVal3(self):

        self.rev = self.reversePlot(self.rev)
        self.plotLines(self.fileInstance, self.rev)

    def saveImageAsPng(self):
        im = Image.open('plot.png')
        window = Tk()
        window.withdraw()
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
        if file:
            im.save(file)

    def plotScatterPoints(self, fileInstance, reverse):

        if len(fileInstance.selectedColumns()) != 2:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid No. Of Arguments")
            return -999

        self.figure.clf()
        f = open(fileInstance.fileName, 'r', errors='ignore')

        reader = csv.reader(f)
        style.use('ggplot')

        
        header = next(reader)
        year = []
        value = []
        for row in reader:

            if bool(re.match('^[0-9\.\- ]*$', row[fileInstance.selectedColumns()[0]])) and bool(
                    re.match('^[0-9\.\- ]*$', row[fileInstance.selectedColumns()[1]])):
                year.append(float(row[fileInstance.selectedColumns()[0]]))
                value.append(float(row[fileInstance.selectedColumns()[1]]))
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "Invalid Data")
                return -999

        ax = self.figure.add_subplot(111)

        
        colors = [0, 0, 0]
        if (reverse):

            ax.scatter(year, value, s=np.pi * 3 * 2, c=colors, alpha=0.5, marker='*')
            ax.set_xlabel(header[fileInstance.selectedColumns()[0]])
            ax.set_ylabel(header[fileInstance.selectedColumns()[1]])
        else:
            ax.scatter(value, year, s=np.pi * 3 * 2, c=colors, alpha=0.5, marker='*')
            ax.set_ylabel(header[fileInstance.selectedColumns()[0]])
            ax.set_xlabel(header[fileInstance.selectedColumns()[1]])

        ax.set_title("Subplot 1:Scatter Point Diagram")

        self.figure.savefig("plot.png")


        self.canvas.draw()

        return +999

    def plotScatterPointsWithLines(self, fileInstance, reverse):

        if len(fileInstance.selectedColumns()) != 2:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid No. Of Arguments")
            return -999

        self.figure.clf()

        f = open(fileInstance.fileName, 'r', errors='ignore')
        reader = csv.reader(f)

        header = next(reader)
        style.use('ggplot')

        year = []
        value = []
        for row in reader:

            if bool(re.match('^[0-9\.\- ]*$', row[fileInstance.selectedColumns()[0]])) and bool(
                    re.match('^[0-9\.\- ]*$', row[fileInstance.selectedColumns()[1]])):
                year.append(float(row[fileInstance.selectedColumns()[0]]))
                value.append(float(row[fileInstance.selectedColumns()[1]]))
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "Invalid Data")
                return -999

        ax = self.figure.add_subplot(111)


        if (reverse):

            ax.plot(year, value, '*-')

            ax.set_xlabel(header[fileInstance.selectedColumns()[0]])
            ax.set_ylabel(header[fileInstance.selectedColumns()[1]])
        else:
            ax.plot(value, year, '*-')

            ax.set_ylabel(header[fileInstance.selectedColumns()[0]])
            ax.set_xlabel(header[fileInstance.selectedColumns()[1]])

        ax.set_title("Subplot 2:Scatter Point Diagram With Smooth Lines")

        self.canvas.draw()
        self.figure.savefig("plot.png")
        return +999

    def plotLines(self, fileInstance, reverse):

        if len(fileInstance.selectedColumns()) != 2:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid No. Of Arguments")
            return -999

        self.figure.clf()

        f = open(fileInstance.fileName, 'r', errors='ignore')
        reader = csv.reader(f)
        style.use('ggplot')

        header = next(reader)

        year = []
        value = []

        for row in reader:

            if bool(re.match('^[0-9\.\- ]*$', row[fileInstance.selectedColumns()[0]])) and bool(
                    re.match('^[0-9\.\- ]*$', row[fileInstance.selectedColumns()[1]])):
                year.append(float(row[fileInstance.selectedColumns()[0]]))
                value.append(float(row[fileInstance.selectedColumns()[1]]))
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "Invalid Data")
                return -999

        ax = self.figure.add_subplot(111)

        if (reverse):
            ax.plot(year, value)
            ax.set_ylabel(header[fileInstance.selectedColumns()[0]])
            ax.set_xlabel(header[fileInstance.selectedColumns()[1]])
        else:
            ax.plot(value, year)
            ax.set_xlabel(header[fileInstance.selectedColumns()[0]])
            ax.set_ylabel(header[fileInstance.selectedColumns()[1]])
        ax.set_title("Subplot 3:Line Plot Diagram")
        self.figure.savefig("plot.png")


        self.canvas.draw()

        return +999

    def reversePlot(self, type):
        if (type):
            return False
        else:
            return True


class MyWindow(QtWidgets.QWidget):
    def __init__(self, fileName, parent=None):

        super(MyWindow, self).__init__(parent)
        self.fileName = ""
        self.fname = ""
        self.model = QtGui.QStandardItemModel(self)

        self.figure2 = plt.figure()
        self.figure3 = plt.figure()
        self.figure4 = plt.figure()

        self.label2 = QtWidgets.QLabel("Select Columns to Plot")

        self.tableView = QtWidgets.QTableView(self)

        
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.label = QtWidgets.QLabel("Plot")
        myfont = QtGui.QFont()
        myfont.setBold(True)

        self.label.setFont(myfont)

        self.label2.setFont(myfont)

        self.pushButton2 = QtWidgets.QPushButton("ScatterPlot")

        self.pushButton3 = QtWidgets.QPushButton("SmoothLines")

        self.pushButton4 = QtWidgets.QPushButton("Lines")

        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 1000, 645)
        self.model.dataChanged.connect(self.FinishEdit)

        self.pushDeleteRow = QtWidgets.QPushButton(self)
        self.pushDeleteRow.setText("DeleteRow")
        self.pushDeleteRow.clicked.connect(self.removeRow)
        self.pushDeleteRow.setFixedWidth(80)

        self.pushDeleteColumn = QtWidgets.QPushButton(self)
        self.pushDeleteColumn.setText("DeleteColumn")
        self.pushDeleteColumn.clicked.connect(self.removeColumn)
        self.pushDeleteColumn.setFixedWidth(86)

        self.pushClear = QtWidgets.QPushButton(self)
        self.pushClear.setText("Clear")
        self.pushClear.clicked.connect(self.clearList)
        self.pushClear.setFixedWidth(60)

        self.pushButton2.clicked.connect(self.openPlot1Window)
        self.pushButton3.clicked.connect(self.openPlot2Window)
        self.pushButton4.clicked.connect(self.openPlot3Window)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(9)

        grid.addWidget(self.label2)
        grid.addWidget(self.tableView, 1, 0, 1, 9)
        ground = 10
        grid.addWidget(self.pushDeleteRow, ground, 1)
        grid.addWidget(self.pushDeleteColumn, ground, 2)
        grid.addWidget(self.pushClear, ground, 0)
        grid.addWidget(self.label, ground, 5)
        grid.addWidget(self.pushButton2, ground, 6)
        grid.addWidget(self.pushButton3, ground, 7)
        grid.addWidget(self.pushButton4, ground, 8)

        self.setLayout(grid)

        item = QtGui.QStandardItem()
        self.model.appendRow(item)
        self.model.setData(self.model.index(0, 0), "", 0)
        self.tableView.resizeColumnsToContents()

    
        self.selectionModel = self.tableView.selectionModel()

    def saveImageAsPng(self):
        im = Image.open('plot.png')
        window = Tk()
        window.withdraw()
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
        if file:
            im.save(file)

    def plotScatterPointsSave(self, fileName):

        if len(self.selectedColumns()) != 2:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid No. Of Arguments")
            return -999
        self.figure2.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$', row[self.selectedColumns()[0]])) and bool(
                    re.match('^[0-9\.\- ]*$', row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "Invalid Data")
                return -999
        ax = self.figure2.add_subplot(111)

        # plot data
        colors = [0, 0, 0]
        ax.scatter(year, value, s=np.pi * 3 * 2, c=colors, alpha=0.5, marker='*')
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("scatter points")

        self.figure2.savefig("plot.png")
        self.saveImageAsPng()

    def plotScatterPointsWithLinesSave(self, fileName):
        self.label.setVisible(False)
        if len(self.selectedColumns()) != 2:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid No. Of Arguments")
            return -999

        self.figure3.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$', row[self.selectedColumns()[0]])) and bool(
                    re.match('^[0-9\.\- ]*$', row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "Invalid Data")
                return -999

        ax = self.figure3.add_subplot(111)

        
        ax.plot(year, value, '*-')
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("scatter points with lines")

        self.figure3.savefig("plot.png")
        self.saveImageAsPng()

    def plotLinesSave(self, fileName):
        self.label.setVisible(False)
        if len(self.selectedColumns()) != 2:
            QtWidgets.QMessageBox.about(self, "ERROR", "Invalid No. Of Arguments")
            return -999

        self.figure4.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$', row[self.selectedColumns()[0]])) and bool(
                    re.match('^[0-9\.\- ]*$', row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                QtWidgets.QMessageBox.about(self, "ERROR", "Invalid Data")
                return -999

        ax = self.figure4.add_subplot(111)

    
        ax.plot(year, value)
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("plot lines")
        self.figure4.savefig("plot.png")

        self.saveImageAsPng()

    def openPlot1Window(self):
        self.plot1 = PopUpPlotWindow(1, self)
        if (self.plot1.plotScatterPoints(self, self.plot1.rev) > 0):
            self.plot1.show()

    def openPlot2Window(self):
        self.plot2 = PopUpPlotWindow(2, self)
        if (self.plot2.plotScatterPointsWithLines(self, self.plot2.rev) > 0):
            self.plot2.show()

    def openPlot3Window(self):
        self.plot3 = PopUpPlotWindow(3, self)
        if (self.plot3.plotLines(self, self.plot3.rev) > 0):
            self.plot3.show()

        

    def selectedColumns(self):
        indexes = self.selectionModel.selectedIndexes()
        index_columns = []
        for index in indexes:
            index_columns.append(index.column())
        index_columns = list(set(index_columns))
        return index_columns

    def loadCsv(self, fileName):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
                                                            (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
        self.fileName = fileName
        if fileName:
            print(fileName)
            ff = open(fileName, 'r', newline='', errors='ignore')
            lines = [line for line in ff]
            print(lines[0].strip().split(','))
            mytext = ff.read()
            
            ff.close()
            f = open(fileName, 'r', errors='ignore')
            with f:
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)
                if mytext.count(';') <= mytext.count('\t'):
                    reader = csv.reader(f)
                    self.model.clear()
                    for row in reader:
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)

                    self.tableView.resizeColumnsToContents()
                else:
                    reader = csv.reader(f, delimiter=';')
                    self.model.clear()
                    for row in reader:
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                    self.tableView.resizeColumnsToContents()

    def writeCsv(self, fileName):
        
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row, column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",
                                                            (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),
                                                            "CSV Files (*.csv)")
        if fileName:
            print(fileName)
            f = open(fileName, 'w', newline='')
            with f:
                writer = csv.writer(f, delimiter=',')
                for rowNumber in range(self.model.rowCount()):
                    fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                              QtCore.Qt.DisplayRole)
                              for columnNumber in range(self.model.columnCount())]
                    writer.writerow(fields)
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)

    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.setFixedSize(1000, 700)
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
    
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row, column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)
        printer.setDocName(self.fname)
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        model = self.tableView.model()
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)

    def removeRow(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedRows()
        for index in sorted(indices):
            model.removeRow(index.row())

    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
        self.tableView.scrollToBottom()

    def clearList(self):
        self.model.clear()

    def removeColumn(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedColumns()
        for index in sorted(indices):
            model.removeColumn(index.column())

    def addColumn(self):
        count = self.model.columnCount()
        print(count)
        self.model.setColumnCount(count + 1)
        self.model.setData(self.model.index(0, count), "", 0)
        self.tableView.resizeColumnsToContents()

    def FinishEdit(self):
        self.tableView.resizeColumnsToContents()

    def DelRowByCon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            self.model.removeRow(row)
            print("Row " + str(row) + " deleted")
            self.tableView.selectRow(row)

    def AddRowByCon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row() + 1
            self.model.insertRow(row)
            print("Row at " + str(row) + " inserted")
            self.tableView.selectRow(row)

    def AddRowByCon2(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            self.model.insertRow(row)
            print("Row at " + str(row) + " inserted")
            self.tableView.selectRow(row)

    def AddColBcon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column()
            self.model.insertColumn(col)
            print("Column at " + str(col) + " inserted")

    def AddColAcon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column() + 1
            self.model.insertColumn(col)
            print("Column at " + str(col) + " inserted")

    def DelColByCon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column()
            self.model.removeColumn(col)
            print("Column at " + str(col) + " removed")

    def CopyByCon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row, col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())

    def PasteByCon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row, col)
            clip = QtWidgets.QApplication.clipboard()
            myitem.setText(clip.text())

    def CutByCon(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row, col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())
                myitem.setText("")

    def Edit(self):
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)


class Writer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.form_widget = MyWindow('')
        self.setCentralWidget(self.form_widget)

        self.init_ui()

    def init_ui(self):

        # MenuBar

        bar = self.menuBar()
        file = bar.addMenu('File')
        edit = bar.addMenu('Edit')
        data = file.addMenu('Add')
        save = file.addMenu('Save Plots')

        new_action = QAction('Clear', self)
        open_action = QAction('&Load', self)
        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        open_action.setShortcut('Ctrl+L')
        quit_action = QAction('&Quit', self)

        save_1 = QAction('&Save_Scatter_Point', self)
        save_2 = QAction('&Save_Scatter_Point_Lines', self)
        save_3 = QAction('&Save_Lines', self)

        edit_action = QAction('&Edit by double click', self)
        addrow_action = QAction('&Add row', self)
        addcoloumn_action = QAction('&Add column', self)

        file.addAction(open_action)
        file.addAction(save_action)
        data.addAction(addrow_action)
        data.addAction(addcoloumn_action)

        file.addMenu(data)
        save.addAction(save_1)
        save.addAction(save_2)
        save.addAction(save_3)
        file.addMenu(save)
        file.addAction(new_action)
        file.addAction(quit_action)

        edit.addAction(edit_action)

        quit_action.triggered.connect(self.QuitTrigg)

        file.triggered.connect(self.Resp1)
        edit.triggered.connect(self.Resp2)

        self.show()

    def QuitTrigg(self):
        sys.exit(app.exec_())

    def Resp1(self, q):
        signal = q.text()

        if signal == 'Clear':
            self.form_widget.clearList()
        elif signal == '&Load':
            self.form_widget.loadCsv(1)
        elif signal == '&Save':
            self.form_widget.writeCsv(1)
        elif signal == '&Add row':
            self.form_widget.addRow()
        elif signal == '&Add column':
            self.form_widget.addColumn()
        elif signal == '&Save_Scatter_Point':
            self.form_widget.plotScatterPointsSave('')
        elif signal == '&Save_Scatter_Point_Lines':
            self.form_widget.plotScatterPointsWithLinesSave('')
        elif signal == '&Save_Lines':
            self.form_widget.plotLinesSave('')

    def Resp2(self, q):
        signal = q.text()
        if signal == '&Edit by double click':
            self.form_widget.Edit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('CSV Edit And Plot')
    main = Writer()
    main.setMinimumSize(700, 300)
    main.setGeometry(20, 20, 800, 700)
    main.setWindowTitle("CSV LEP")
    main.show()

    sys.exit(app.exec_())














