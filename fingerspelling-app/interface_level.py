from PyQt5 import QtCore, QtGui, QtWidgets

### 設定物件布局
class Ui_LevelWindow(object):
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
        self.label_background.setStyleSheet('background: #0F2167;') # 設定背景風格, 使用 hex code, ##0F2167表示深藍色. 如果需要設定多行則用三個'包起來
        self.label_background.setObjectName("label_background")

        ### 用於顯示關卡選擇的標題
        title_font = QtGui.QFont(self.font_family) # 設定字型
        title_font.setPointSize(15)
        title_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_level_title = QtWidgets.QLabel(self.centralwidget)
        self.label_level_title.setGeometry(QtCore.QRect(80, 40, 800, 40))
        self.label_level_title.setFont(title_font)
        self.label_level_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_level_title.setStyleSheet("color: "+ title_text_color+ ";")
        self.label_level_title.setObjectName("label_menu_title")


        ### 關卡選擇的按鈕, 使用定義的 HoverButton widget, 用於定義鼠標懸停在按鈕時可以發送訊號
        levelbutton_font = QtGui.QFont(self.font_family)
        levelbutton_font.setPointSize(12)
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

        # Level1的按鈕
        self.button_level_one = HoverButton(self.centralwidget)
        self.button_level_one.setGeometry(QtCore.QRect(320, 150, 320, 60))
        self.button_level_one.setFont(levelbutton_font)
        self.button_level_one.setStyleSheet(buttons_style_sheet)
        self.button_level_one.setObjectName("button_level_one")
        self.button_level_one.hover.connect(
            lambda:  self.label_level_hint.setText(
                "Test your skills with letters:\nA, B, C, D, E, F, I, L, O, S, U, V, W, X."
                )
            )
        self.button_level_one.leave.connect(
            lambda:  self.label_level_hint.setText(self.level_hint)
            )

        # Level2的按鈕
        self.button_level_two = HoverButton(self.centralwidget)
        self.button_level_two.setGeometry(QtCore.QRect(320, 220, 320, 60))
        self.button_level_two.setFont(levelbutton_font)
        self.button_level_two.setStyleSheet(buttons_style_sheet)
        self.button_level_two.setObjectName("button_level_two")
        self.button_level_two.hover.connect(
            lambda:  self.label_level_hint.setText(
                "Test your skills with letters:\nG, H, J, K, M, N, P, Q, R, T, Y, Z."
                )
            )
        self.button_level_two.leave.connect(
            lambda:  self.label_level_hint.setText(self.level_hint)
            )

        # Level3的按鈕
        self.button_level_three = HoverButton(self.centralwidget)
        self.button_level_three.setGeometry(QtCore.QRect(320, 290, 320, 60))
        self.button_level_three.setFont(levelbutton_font)
        self.button_level_three.setStyleSheet(buttons_style_sheet)
        self.button_level_three.setObjectName("button_level_three")
        self.button_level_three.hover.connect(
            lambda:  self.label_level_hint.setText(
                "Challenge yourself with simple words like:\nAPP, HCI, GPT, OS"
                )
            )
        self.button_level_three.leave.connect(
            lambda:  self.label_level_hint.setText(self.level_hint)
            )

        # Level4的按鈕
        self.button_level_four = HoverButton(self.centralwidget)
        self.button_level_four.setGeometry(QtCore.QRect(320, 360, 320, 60))
        self.button_level_four.setFont(levelbutton_font)
        self.button_level_four.setStyleSheet(buttons_style_sheet)
        self.button_level_four.setObjectName("button_level_four")
        self.button_level_four.hover.connect(
            lambda:  self.label_level_hint.setText(
                "Challenge yourself with complex words like:\nAPPLICATION, COMPUTER, INTERFACE"
                )
            )
        self.button_level_four.leave.connect(
            lambda:  self.label_level_hint.setText(self.level_hint)
            )

        ### 設定畫面中央的裝飾水平線
        # 建立frame, 父容器為centralwidget
        self.menu_horizon_line = QtWidgets.QFrame(self.centralwidget)
        self.menu_horizon_line.setGeometry(QtCore.QRect(80, 450, 800, 16))
        self.menu_horizon_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.menu_horizon_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.menu_horizon_line.setObjectName("menu_horizon_line")

        ### 用於顯示主選單的提示
        levelhint_font = QtGui.QFont(self.font_family)
        levelhint_font.setPointSize(15)
        levelhint_text_color = "#FFECD6" # #FFECD6: 淺橘色
        self.label_level_hint = QtWidgets.QLabel(self.centralwidget)
        self.label_level_hint.setGeometry(QtCore.QRect(80, 480, 800, 80))
        self.label_level_hint.setFont(levelhint_font)
        self.label_level_hint.setAlignment(QtCore.Qt.AlignCenter)
        self.label_level_hint.setStyleSheet("color: "+ levelhint_text_color+ ";")
        self.label_level_hint.setObjectName("label_menu_hint")

        ### 回到主選單的按鈕
        level2menuebutton_font = QtGui.QFont(self.font_family) # 設定字型
        level2menuebutton_font.setPointSize(12)
        self.button_level_2_menu = QtWidgets.QPushButton(self.centralwidget)
        self.button_level_2_menu.setGeometry(QtCore.QRect(320, 600, 320, 60))
        self.button_level_2_menu.setFont(level2menuebutton_font)
        self.button_level_2_menu.setStyleSheet(buttons_style_sheet)
        self.button_level_2_menu.setObjectName("button_return_menu")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_level_title.setText(_translate("MainWindow", "Let\'s Play Fingerspelling"))
        self.button_level_one.setText(_translate("MainWindow", "LEVEL ONE"))
        self.button_level_two.setText(_translate("MainWindow", "LEVEL TWO"))
        self.button_level_three.setText(_translate("MainWindow", "LEVEL THREE"))
        self.button_level_four.setText(_translate("MainWindow", "LEVEL FOUR"))
        self.level_hint = "Pick your challenge level."
        self.label_level_hint.setText(_translate("MainWindow", self.level_hint))
        self.button_level_2_menu.setText(_translate("MainWindow", "MENU"))

# 創建自定義 QPushButton 子類, 它繼承自 QtWidgets.QPushButton
class HoverButton(QtWidgets.QPushButton):
    # 定義一個自定義的信號
    hover = QtCore.pyqtSignal()
    leave = QtCore.pyqtSignal()

    # 初始化方法, parent 參數指定了這個標籤的父元素（如果有）
    def __init__(self, parent=None):
        # 呼叫了父類 QPushButton 的初始化方法，確保 HoverButton 類繼承了 QPushButton 的所有基本功能。
        super(HoverButton, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        # 當鼠標進入按鈕範圍時，發射 hover 信號
        self.hover.emit()
        # 呼叫了父類 QPushButton 原本的enterEvent，確保執行了 QPushButton 的懸停邏輯
        super(HoverButton, self).enterEvent(event)

    def leaveEvent(self, event):
        # 當鼠標離開按鈕範圍時，發射 hover 信號
        self.leave.emit()
        # 呼叫了父類 QPushButton 原本的leaveEvent，確保執行了 QPushButton 的離開邏輯
        super(HoverButton, self).leaveEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LevelWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
