from PyQt5 import QtCore, QtGui, QtWidgets

### 設定物件布局
class Ui_IntroductionWindow(object):
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

        ### 用於顯示介紹頁面的標題
        title_font = QtGui.QFont(self.font_family) # 設定字型
        title_font.setPointSize(15)
        title_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_intro_title = QtWidgets.QLabel(self.centralwidget)
        self.label_intro_title.setGeometry(QtCore.QRect(80, 40, 800, 40))
        self.label_intro_title.setFont(title_font)
        self.label_intro_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_intro_title.setStyleSheet("color: "+ title_text_color+ ";")
        self.label_intro_title.setObjectName("label_intro_title")

        ### 用於顯示主選單的提示
        introhint_font = QtGui.QFont(self.font_family)
        introhint_font.setPointSize(12)
        introhint_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_intro_hint = QtWidgets.QLabel(self.centralwidget)
        self.label_intro_hint.setGeometry(QtCore.QRect(60, 100, 840, 350))
        self.label_intro_hint.setFont(introhint_font)
        self.label_intro_hint.setAlignment(QtCore.Qt.AlignCenter)
        self.label_intro_hint.setStyleSheet("color: "+ introhint_text_color + ";")
        self.label_intro_hint.setObjectName("label_menu_hint")


        ### 設定畫面中央的裝飾水平線
        # 建立frame, 父容器為centralwidget
        self.menu_horizon_line = QtWidgets.QFrame(self.centralwidget)
        self.menu_horizon_line.setGeometry(QtCore.QRect(80, 480, 800, 16))
        self.menu_horizon_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.menu_horizon_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.menu_horizon_line.setObjectName("menu_horizon_line")

        ### 回到主選單的按鈕
        returnbutton_font = QtGui.QFont(self.font_family) # 設定字型
        returnbutton_font.setPointSize(12)
        buttons_style_sheet ="""
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
        # color: #FFECD6; 按鈕文字顏色
        # background-color: #0F2167; 按鈕背景顏色
        # border: 2px solid #FFECD6; 按鈕邊框線條
        # border-radius: 30px; 按鈕圓角
        # #FFECD6: 淺橘色, #0F2167: 深藍色, #4CB9E7: 淺藍色

        self.button_intro_2_menu = QtWidgets.QPushButton(self.centralwidget)
        self.button_intro_2_menu.setGeometry(QtCore.QRect(320, 600, 320, 60))
        self.button_intro_2_menu.setFont(returnbutton_font)
        self.button_intro_2_menu.setStyleSheet(buttons_style_sheet)
        self.button_intro_2_menu.setObjectName("button_intro_2_menu")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_intro_title.setText(_translate("MainWindow", "Let\'s Play Fingerspelling"))

        self.intro_text = """Welcome to our interactive ASL fingerspelling game.
This game is powered by machine learning technology.\n
Fingerspelling is a part of American Sign Language
which is making an alphabet with your hands to sign a word.
You can invite your friends learning, playing,
while mastering the art of American Sign Language.\n
Get ready for a journey of fun with ASL fingerspelling!"""
        self.label_intro_hint.setText(_translate("MainWindow", self.intro_text))
        self.button_intro_2_menu.setText(_translate("MainWindow", "MENU"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_IntroductionWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
