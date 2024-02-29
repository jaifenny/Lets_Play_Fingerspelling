from PyQt5 import QtCore, QtGui, QtWidgets

### 設定物件布局
class Ui_MenuWindow(object):
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

        ### 用於顯示主選單的標題
        title_font = QtGui.QFont(self.font_family) # 設定字型
        title_font.setPointSize(28)
        title_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_menu_title = QtWidgets.QLabel(self.centralwidget)
        self.label_menu_title.setGeometry(QtCore.QRect(80, 160, 800, 130))
        self.label_menu_title.setFont(title_font)
        self.label_menu_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_menu_title.setStyleSheet("color: "+ title_text_color+ ";")
        self.label_menu_title.setObjectName("label_menu_title")

        ### 設定畫面中央的裝飾水平線
        # 建立frame, 父容器為centralwidget
        self.menu_horizon_line = QtWidgets.QFrame(self.centralwidget)
        self.menu_horizon_line.setGeometry(QtCore.QRect(80, 290, 800, 16))
        self.menu_horizon_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.menu_horizon_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.menu_horizon_line.setObjectName("menu_horizon_line")

        ### 用於顯示主選單的提示
        menuhint_font = QtGui.QFont(self.font_family)
        menuhint_font.setPointSize(12)
        menuhint_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_menu_hint = QtWidgets.QLabel(self.centralwidget)
        self.label_menu_hint.setGeometry(QtCore.QRect(80, 320, 800, 120))
        self.label_menu_hint.setFont(menuhint_font)
        self.label_menu_hint.setAlignment(QtCore.Qt.AlignCenter)
        self.label_menu_hint.setStyleSheet("color: "+ menuhint_text_color+ ";")
        self.label_menu_hint.setObjectName("label_menu_hint")

        ### 開始遊戲的按鈕
        playbutton_font = QtGui.QFont(self.font_family)
        playbutton_font.setPointSize(12)
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
        self.button_menu_play = QtWidgets.QPushButton(self.centralwidget)
        self.button_menu_play.setGeometry(QtCore.QRect(320, 460, 320, 60))
        self.button_menu_play.setFont(playbutton_font)
        self.button_menu_play.setStyleSheet(buttons_style_sheet)

        self.button_menu_play.setObjectName("button_menu_play")

        ### 開始練習的按鈕
        practicebutton_font = QtGui.QFont(self.font_family)
        practicebutton_font.setPointSize(12)
        self.button_menu_practice = QtWidgets.QPushButton(self.centralwidget)
        self.button_menu_practice.setGeometry(QtCore.QRect(320, 530, 320, 60))
        self.button_menu_practice.setFont(practicebutton_font)
        self.button_menu_practice.setStyleSheet(buttons_style_sheet)
        self.button_menu_practice.setObjectName("button_menu_practice")

        ### 前往介紹的按鈕
        introbutton_font = QtGui.QFont(self.font_family)
        introbutton_font.setPointSize(12)
        self.button_menu_intro = QtWidgets.QPushButton(self.centralwidget)
        self.button_menu_intro.setGeometry(QtCore.QRect(320, 600, 320, 60))
        self.button_menu_intro.setFont(introbutton_font)
        self.button_menu_intro.setStyleSheet(buttons_style_sheet)
        self.button_menu_intro.setObjectName("button_menu_intro")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_menu_title.setText(_translate("MainWindow", "Let\'s Play Fingerspelling"))
        self.label_menu_hint.setText(_translate("MainWindow", "Explore ASL Fingerspelling in a fun way!\nEngage in friendly competition and enjoy learning together."))
        self.button_menu_play.setText(_translate("MainWindow", "START"))
        self.button_menu_practice.setText(_translate("MainWindow", "PRACTICE"))
        self.button_menu_intro.setText(_translate("MainWindow", "ABOUT"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MenuWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
