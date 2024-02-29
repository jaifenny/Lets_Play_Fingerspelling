from PyQt5 import QtCore, QtGui, QtWidgets

### 設定物件布局
class Ui_GestureWindow(object):
    def __init__(self):
        self.main_window_width = 960
        self.main_window_height = 720

    def setupUi(self, MainWindow):
        ### 設定主視窗
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(self.main_window_width, self.main_window_height)

        ### 設定字體
        self.font_file = QtGui.QFontDatabase.addApplicationFont("font/consola.ttf") # 載入字體檔案
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(self.font_file)[0] # 假設字體包含多個字體家族, 則取第一個使用
        # 如果要設定字體就使用下面這行
        # self.font = QtGui.QFont(self.font_family, 12)

        ### 設定尺寸策略(sizePolicy)
        # 第一個變數設定寬, 第二個變數設定高, 視窗的大小將不會根據內容或外部因素自動變化
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)

        ### 設定中央widget, 用於作為所有widget放置的容器
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        ### 用於顯示背景
        self.label_background = QtWidgets.QLabel(self.centralwidget)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.main_window_width, self.main_window_height)) # 設定x, y, width, height
        self.label_background.setStyleSheet('background: #0F2167;') # 設定背景風格, 使用 hex code, #0F2167: 深藍色. 如果需要設定多行則用三個'包起來
        self.label_background.setObjectName("label_background")

        ### 用於顯示關卡選擇的標題
        title_font = QtGui.QFont(self.font_family) # 設定字型
        title_font.setPointSize(15)
        title_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_gesture_title = QtWidgets.QLabel(self.centralwidget)
        self.label_gesture_title.setGeometry(QtCore.QRect(80, 40, 800, 40))
        self.label_gesture_title.setFont(title_font)
        self.label_gesture_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gesture_title.setStyleSheet("color: "+ title_text_color+ ";")
        self.label_gesture_title.setObjectName("label_menu_title")

        ### 手勢選擇的按鈕
        gesturebutton_font = QtGui.QFont(self.font_family)
        gesturebutton_font.setPointSize(12)
        buttons_style_sheet ="""
            QPushButton {
                color: #FFECD6;
                background-color: #0F2167;
                border: 2px solid #FFECD6;
                border-radius: 20px;
            }
            QPushButton:hover {
                color: #0F2167;
                background-color: #FFECD6;
            }
            QPushButton:pressed {
                background-color: #4CB9E7;
            }
            """
        # color: #FFECD6; 按鈕文字顏色
        # background-color: #0F2167; 按鈕背景顏色
        # border: 2px solid #FFECD6; 按鈕邊框線條
        # border-radius: 30px; 按鈕圓角
        # #FFECD6: 淺橘色, #0F2167: 深藍色, #4CB9E7: 淺藍色

        # 創建 QGridLayout
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 150, 800, 260))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.buttons_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.buttons_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(10)
        self.buttons_layout.setObjectName("buttons_layout")
        button_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                        'u', 'v', 'w', 'x', 'y', 'z']
        num_buttons = 26
        button_counter = 0
        # 將按鈕添加到布局中
        for row in range(3):
            for col in range(9):
                if button_counter < num_buttons:
                    # print(button_names[button_counter])
                    button = QtWidgets.QPushButton("button_level_" + button_names[button_counter])
                    button.setFixedSize(80, 80)
                    button.setFont(gesturebutton_font)
                    button.setStyleSheet(buttons_style_sheet)
                    button.setText(button_names[button_counter].upper())
                    button.setProperty('gesture', button_names[button_counter]) # 為每個按鈕添加一個屬性來標記它所代表的手勢
                    self.buttons_layout.addWidget(button, row, col)
                    button_counter += 1

        ### 設定畫面中央的裝飾水平線
        # 建立frame, 父容器為centralwidget
        self.menu_horizon_line = QtWidgets.QFrame(self.centralwidget)
        self.menu_horizon_line.setGeometry(QtCore.QRect(80, 450, 800, 16))
        self.menu_horizon_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.menu_horizon_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.menu_horizon_line.setObjectName("menu_horizon_line")

        ### 用於顯示主選單的提示
        gesturehint_font = QtGui.QFont(self.font_family)
        gesturehint_font.setPointSize(15)
        levelhint_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_gesture_hint = QtWidgets.QLabel(self.centralwidget)
        self.label_gesture_hint.setGeometry(QtCore.QRect(80, 480, 800, 80))
        self.label_gesture_hint.setFont(gesturehint_font)
        self.label_gesture_hint.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gesture_hint.setStyleSheet("color: "+ levelhint_text_color+ ";")
        self.label_gesture_hint.setObjectName("label_menu_hint")

        ### 回到主選單的按鈕
        returnbutton_font = QtGui.QFont(self.font_family) # 設定字型
        returnbutton_font.setPointSize(12)
        self.button_gesture_2_menu = QtWidgets.QPushButton(self.centralwidget)
        self.button_gesture_2_menu.setGeometry(QtCore.QRect(320, 600, 320, 60))
        self.button_gesture_2_menu.setFont(returnbutton_font)
        self.button_gesture_2_menu.setStyleSheet("""
            QPushButton {
                color: #FFECD6;
                background-color: #0F2167;
                border: 2px solid #FFECD6;
                border-radius: 30px;
            }
            QPushButton:hover {
                color: #0F2167;
                background-color: #FFECD6;
            }
            QPushButton:pressed {
                background-color: #4CB9E7;
            }
            """
        )
        self.button_gesture_2_menu.setObjectName("button_gesture_2_menu")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_gesture_title.setText(_translate("MainWindow", "Let\'s Play Fingerspelling"))
        # self.button_level_a.setText("A")

        self.level_hint = "Choose a gesture to practice."
        self.label_gesture_hint.setText(_translate("MainWindow", self.level_hint))
        self.button_gesture_2_menu.setText(_translate("MainWindow", "MENU"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_GestureWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
