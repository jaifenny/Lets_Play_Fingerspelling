from PyQt5 import QtCore, QtGui, QtWidgets

### 設定物件布局
class Ui_ResultWindow(object):
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
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")

        # ### 用於顯示結算畫面的背景
        # self.label_result_background = QtWidgets.QLabel(self.centralwidget)
        # self.label_result_background.setGeometry(QtCore.QRect(0, 0, self.main_window_width, self.main_window_height))
        # self.label_result_background.setStyleSheet("background: #DD64FF;")
        # self.label_result_background.setObjectName("label_result_background")

        ### 設定Cameralabel widget, 用於顯示鏡頭畫面
        self.label_camera = QtWidgets.QLabel(self.centralwidget)
        self.label_camera.setGeometry(QtCore.QRect(0, 0, self.main_window_width, self.main_window_height)) # 設定x, y, width, height
        self.label_camera.setStyleSheet("border: 10px solid #61D6FF;")
        self.label_camera.setObjectName("label_result_camera")

        ### 用於顯示玩家1和玩家2的競賽結果
        result_font = QtGui.QFont(self.font_family) # 設定字型
        result_font.setPointSize(20)
        result_text_color = "#61D6FF" # #61D6FF: 淺藍色
        self.label_player1_result = QtWidgets.QLabel(self.centralwidget)
        self.label_player1_result.setGeometry(QtCore.QRect(0, 100, 480, 100))
        self.label_player1_result.setFont(result_font)
        self.label_player1_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player1_result.setStyleSheet("color: "+result_text_color+ ";") # 設定文字顏色
        self.label_player1_result.setObjectName("label_player1_result")

        self.label_player2_result = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_result.setGeometry(QtCore.QRect(480, 100, 480, 100))
        self.label_player2_result.setFont(result_font)
        self.label_player2_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player2_result.setStyleSheet("color: "+result_text_color+ ";") # 設定文字顏色
        self.label_player2_result.setObjectName("label_player2_result")

        ### 用於顯示玩家1和玩家2的最終分數
        finalscore_font = QtGui.QFont(self.font_family) # 設定字型
        finalscore_font.setPointSize(15)
        finalscore_text_color = "#61D6FF" # #61D6FF: 淺藍色
        self.label_player1_finalscore = QtWidgets.QLabel(self.centralwidget)
        self.label_player1_finalscore.setGeometry(QtCore.QRect(0, 420, 480, 140))
        self.label_player1_finalscore.setFont(finalscore_font)
        self.label_player1_finalscore.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player1_finalscore.setStyleSheet("color: "+finalscore_text_color+ ";") # 設定文字顏色
        self.label_player1_finalscore.setObjectName("label_player1_finalscore")

        self.label_player2_finalscore = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_finalscore.setGeometry(QtCore.QRect(480, 420, 480, 140))
        self.label_player2_finalscore.setFont(finalscore_font)
        self.label_player2_finalscore.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player2_finalscore.setStyleSheet("color: "+finalscore_text_color+ ";") # 設定文字顏色
        self.label_player2_finalscore.setObjectName("label_player2_finalscore")


         ### 用於顯示玩家1和玩家2的動畫效果
        self.label_player1_gif = QtWidgets.QLabel(self.centralwidget)
        self.label_player1_gif.setGeometry(QtCore.QRect(0, 0, 420, 400))
        self.label_player1_gif.setObjectName("label_player1_gif")

        self.label_player2_gif = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_gif.setGeometry(QtCore.QRect(500, 0, 420, 400))
        self.label_player2_gif.setObjectName("label_player2_gif")

        ### 回到主選單的按鈕
        returnbutton_font = QtGui.QFont(self.font_family) # 設定字型
        returnbutton_font.setPointSize(12)
        buttons_style_sheet ="""
            QPushButton {
                color: #61D6FF;
                background-color: #0F2167;
                border: 2px solid #61D6FF;
                border-radius: 30px;
            }
            QPushButton:hover {
                color: #0F2167;
                background-color: #61D6FF;
            }
            QPushButton:pressed {
                background-color: #3559E0;
            }
            """
        # color: #FFECD6; 按鈕文字顏色
        # background-color: #0F2167; 按鈕背景顏色
        # border: 2px solid #FFECD6; 按鈕邊框線條
        # border-radius: 30px; 按鈕圓角
        # #FFECD6: 淺橘色, #0F2167: 深藍色, #4CB9E7: 淺藍色

        self.button_return_menu = QtWidgets.QPushButton(self.centralwidget)
        self.button_return_menu.setGeometry(QtCore.QRect(320, 600, 320, 60))
        self.button_return_menu.setFont(returnbutton_font)
        self.button_return_menu.setStyleSheet(buttons_style_sheet)
        self.button_return_menu.setObjectName("button_return_menu")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_player1_result.setText(_translate("MainWindow", "Player1 WINS!!!"))
        self.label_player1_finalscore.setText(_translate("MainWindow", "THE FINAL SOCRE IS\n000000"))
        self.label_player2_result.setText(_translate("MainWindow", "Player2 LOSES..."))
        self.label_player2_finalscore.setText(_translate("MainWindow", "THE FINAL SOCRE IS\n000000"))
        self.button_return_menu.setText(_translate("MainWindow", "MENU"))


if __name__ == "__main__":
    import sys
    import cv2
    import numpy as np
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ResultWindow()
    ui.setupUi(MainWindow)

    ### 建立一個黑色背景底色
    bg = np.zeros((MainWindow.height(), MainWindow.width(), 3), np.uint8) # 創建一個空白BGR黑畫面
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB) # 將圖像從 BGRA 轉換成 RGBA 以符合QImage格式
    q_img = QtGui.QImage(bg.data, bg.shape[1], bg.shape[0], bg.shape[1] * 3, QtGui.QImage.Format_RGB888) # 轉換成 QImage 以用於放入Qlabel中顯示出來
    ui.label_camera.setPixmap(QtGui.QPixmap.fromImage(q_img))# 顯示在label_camera上

    MainWindow.show()
    sys.exit(app.exec_())
