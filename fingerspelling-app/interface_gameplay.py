# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np

class Ui_GameplayWindow(object):
    def __init__(self):
        self.main_window_width = 960
        self.main_window_height = 720

    ### 設定物件布局
    def setupUi(self, MainWindow):
        ### 設定主視窗
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True) # 當 setEnabled 設為 True 時，視窗將可以與使用者互動。
        MainWindow.resize(self.main_window_width, self.main_window_height)

        ### 設定字體
        self.font_file = QtGui.QFontDatabase.addApplicationFont("font/consola.ttf") # 載入字體檔案
        self.font_family = QtGui.QFontDatabase.applicationFontFamilies(self.font_file)[0] # 假設字體包含多個字體家族, 則取第一個使用
        # 如果要設定字體就使用下面這行
        # self.font = QtGui.QFont(self.font_family, 12)

        ### 設定尺寸策略(sizePolicy)
        # 第一個變數設定寬, 第二個變數設定高, 視窗的大小將不會根據內容或外部因素自動變化
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0) # 設定了水平和垂直拉伸因子為 0，確保視窗大小不會根據其內容自動調整
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy) # 對主視窗套用尺寸策略

        ### 設定中央widget, 用於作為所widget來
        self.centralwidget = QtWidgets.QWidget(MainWindow) # 建立widget, 父容器為MainWindow
        self.centralwidget.setObjectName("centralwidget")

        ### 設定Cameralabel widget, 用於顯示鏡頭畫面
        self.label_camera = CameraLabel(self.centralwidget)
        self.label_camera.setGeometry(QtCore.QRect(0, 0, self.main_window_width, self.main_window_height)) # 設定x, y, width, height
        self.label_camera.setStyleSheet('border: 10px solid #61D6FF;') # 設定邊框風格, 使用 hex code, #61D6FF: 淺藍色. 如果需要設定多行則用三個'包起來
        self.label_camera.setObjectName("label_camera")

        ### 用於顯示玩家1和玩家2的分數
        score_font = QtGui.QFont(self.font_family) # 設定字型
        score_font.setPointSize(15)
        score_text_color = "#61D6FF" # #61D6FF: 淺藍色
        self.label_player1_score = QtWidgets.QLabel(self.centralwidget) # 建立label, 父容器為centralwidget
        self.label_player1_score.setGeometry(QtCore.QRect(90, 640, 310, 40)) # 設定x, y, width, height
        self.label_player1_score.setFont(score_font)
        self.label_player1_score.setAlignment(QtCore.Qt.AlignCenter) # 設定文字置中
        self.label_player1_score.setStyleSheet("color: "+score_text_color+ ";") # 設定文字顏色
        self.label_player1_score.setObjectName("label_player1_score")

        self.label_player2_score = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_score.setGeometry(QtCore.QRect(560, 640, 310, 40)) # 設定x, y, width, height
        self.label_player2_score.setFont(score_font)
        self.label_player2_score.setAlignment(QtCore.Qt.AlignCenter) # 設定文字置中
        self.label_player2_score.setStyleSheet("color: "+score_text_color+ ";") # 設定文字顏色
        self.label_player2_score.setObjectName("label_player2_score")

        ### 用於顯示玩家1和玩家2的倒數計時
        timer_font = QtGui.QFont(self.font_family) # 設定字型
        timer_font.setPointSize(20)
        timer_text_color = "#61D6FF" # #61D6FF: 淺藍色
        self.label_player1_timer = QtWidgets.QLabel(self.centralwidget)
        self.label_player1_timer.setGeometry(QtCore.QRect(210, 100, 60, 40))
        self.label_player1_timer.setFont(timer_font)
        self.label_player1_timer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player1_timer.setStyleSheet("color: "+ timer_text_color+ ";")
        self.label_player1_timer.setObjectName("label_player1_timer")
        # 添加圓形進度條  # add
        self.circularProgress1 = CircularProgress(self.centralwidget)
        self.circularProgress1.setGeometry(QtCore.QRect(190, 70, 110, 110))  # 設定位置和大小
        self.circularProgress1.setObjectName("circularProgress1")

        self.label_player2_timer = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_timer.setGeometry(QtCore.QRect(680, 100, 60, 40))
        self.label_player2_timer.setFont(timer_font)
        self.label_player2_timer.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player2_timer.setStyleSheet("color: "+ timer_text_color+ ";")
        self.label_player2_timer.setObjectName("label_player2_timer")
        # 添加圓形進度條  # add
        self.circularProgress2 = CircularProgress(self.centralwidget)
        self.circularProgress2.setGeometry(QtCore.QRect(660, 70, 110, 110))  # 設定位置和大小
        self.circularProgress2.setObjectName("circularProgress2")

        ### 用於顯示玩家1和玩家2的提示輸入文字
        hint_font = QtGui.QFont(self.font_family)
        hint_font.setPointSize(10)
        hint_text_color = "#61D6FF" # #61D6FF: 淺藍色

        self.label_player1_hint = QtWidgets.QLabel(self.centralwidget)
        self.label_player1_hint.setGeometry(QtCore.QRect(80, 470, 320, 20))
        self.label_player1_hint.setFont(hint_font)
        self.label_player1_hint.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player1_hint.setStyleSheet("color: "+ hint_text_color+ ";")
        self.label_player1_hint.setObjectName("label_player1_hint")

        self.label_player2_hint = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_hint.setGeometry(QtCore.QRect(550, 470, 320, 20))
        self.label_player2_hint.setFont(hint_font)
        self.label_player2_hint.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player2_hint.setStyleSheet("color: "+ hint_text_color+ ";")
        self.label_player2_hint.setObjectName("label_player2_hint")

        ### 用於顯示玩家1和玩家2的題目
        font_question = QtGui.QFont(self.font_family)
        font_question.setPointSize(20)

        self.label_player1_question = QtWidgets.QLabel(self.centralwidget)
        self.label_player1_question.setGeometry(QtCore.QRect(40, 380, 400, 60))
        self.label_player1_question.setFont(font_question)
        self.label_player1_question.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player1_question.setObjectName("label_player1_question")

        self.label_player2_question = QtWidgets.QLabel(self.centralwidget)
        self.label_player2_question.setGeometry(QtCore.QRect(510, 380, 400, 60))
        self.label_player2_question.setFont(font_question)
        self.label_player2_question.setAlignment(QtCore.Qt.AlignCenter)
        self.label_player2_question.setObjectName("label_player2_question")

        ### 設定畫面中央的水平線
        # 建立frame, 父容器為centralwidget
        self.player1_horizon_line = QtWidgets.QFrame(self.centralwidget)
        self.player1_horizon_line.setGeometry(QtCore.QRect(40, 450, 400, 16))
        self.player1_horizon_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.player1_horizon_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.player1_horizon_line.setObjectName("player1_horizon_line")

        self.player2_horizon_line = QtWidgets.QFrame(self.centralwidget)
        self.player2_horizon_line.setGeometry(QtCore.QRect(510, 450, 400, 16))
        self.player2_horizon_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.player2_horizon_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.player2_horizon_line.setObjectName("player2_horizon_line")

        MainWindow.setCentralWidget(self.centralwidget) # 正式指定central widget為MainWindow的central widget, 也就是和MainWindow建立關聯性

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow) # 自動將信號和槽（slots）連接起來

    ### 這個函式設定widget的文字內容, 也用來初始化介面資訊, 以及處理語言轉換
    def retranslateUi(self, MainWindow):
        # PyQt5 中的標準翻譯函數，用於處理文本的國際化和本地化。函式接收兩個參數,
        # 第一個參數是context, 一般用於指定包含該文字內容的類別或父容器
        # 這裡context都設定為為 "MainWindow"，這意味著所有需要翻譯的文本都屬於 MainWindow 這個類的一部分
        # 第二個參數是Default Text, 用於設定為預設顯示的文字
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_camera.setText(_translate("MainWindow", "TextLabel"))
        self.label_player1_score.setText(_translate("MainWindow", "SCORE: 000000"))
        self.label_player2_score.setText(_translate("MainWindow", "SCORE: 000000"))
        self.label_player1_timer.setText(_translate("MainWindow", "10"))
        self.label_player2_timer.setText(_translate("MainWindow", "10"))
        self.label_player1_hint.setText(_translate("MainWindow", "Please input your answer."))
        self.label_player2_hint.setText(_translate("MainWindow", "Please input your answer."))
        self.label_player1_question.setText(_translate("MainWindow", "player1 question"))
        self.label_player2_question.setText(_translate("MainWindow", "player2 question"))

    # 用來更新question的顯示畫面, label 為要更新的標籤,
    # word 為更新的內容, current_index 為玩家目前輸入到的位置
    def setup_question(self ,label ,word, current_index):
        img = np.zeros((label.height(), label.width(), 4), np.uint8) # 創建一個空白BGRA黑畫面

        # 計算文字的大小
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1
        thickness = 2
        (character_width, character_height), baseline = cv2.getTextSize("A", font, font_scale, thickness)
        # 計算字串開始座標, 以便置中顯示
        start_x = label.width()//2 - len(word)*character_width//2
        start_y = label.height()//2 + character_height//2
        # 在圖像上遍歷單詞中的每個字母
        for i, char in enumerate(word):
            # BGRA, 已正確輸入的字母顏色設為淺藍色(255, 255, 100)，其餘為淺灰色(230, 230, 230), 最後的數字代表透明度 0~255
            color = (255, 255, 100, 255) if i < current_index else (230, 230, 230, 255)
            # 將顏色設定套用在字母上
            cv2.putText(img, char.upper(), (start_x + i*character_width, start_y), font, font_scale, color, thickness)


        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA) # 將圖像從 BGRA 轉換成 RGBA 以符合QImage格式
        # 轉換成 QImage 以用於放入Qlabel中顯示出來
        # dark_frame.data代表圖像數據的記憶體位置, img.shape[1] 代表寬, img.shape[0] 代表高,
        # QtGui.QImage.Format_RGBA8888 指定圖像的格式, 代表每個像素由4個byte組成(R,G,B,A),
        # 這是將 OpenCV 中的 BGR 格式轉換為 PyQt 中的 RGB 格式的常用方法

        q_img = QtGui.QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 4, QtGui.QImage.Format_RGBA8888)

        # 顯示在 QLabel 上
        label.setPixmap(QtGui.QPixmap.fromImage(q_img))


# 創建自定義 QLabel 子類, 它繼承自 QtWidgets.QLabel
class CameraLabel(QtWidgets.QLabel):
    # 初始化方法, parent 參數指定了這個標籤的父元素（如果有）
    def __init__(self, parent=None):
        # 呼叫了父類 QLabel 的初始化方法，確保 CameraLabel 類繼承了 QLabel 的所有基本功能。
        super(CameraLabel, self).__init__(parent)

    # 覆寫了 paintEvent 方法, 以便自定義繪畫樣式
    def paintEvent(self, event):
        # 呼叫了父類 QLabel 原本的paintEvent方法，確保執行了 QLabel 的原始繪製邏輯，以便正常顯示標籤的文本或圖像
        super().paintEvent(event)
        qp = QtGui.QPainter(self) # 創建了一個 QPainter 物件，用於在標籤上進行繪畫
        qp.setPen(QtGui.QPen(QtGui.QColor('#61D6FF'), 10))  # 設置筆的顏色和寬度, #61D6FF: 淺藍色
        qp.drawLine(480, 5, 480, 715)  # 畫一條垂直分隔線

class CircularProgress(QtWidgets.QWidget):  # add
    def __init__(self, parent=None):
        super(CircularProgress, self).__init__(parent)
        self._value = 100
        self.setMinimumSize(100, 100)

    def setValue(self, value):
        self._value = value
        self.update()

    def paintEvent(self, event):
        timer_text_color = "#61D6FF" #61D6FF: 淺藍色
        timer_text_color2 = QtGui.QColor.fromRgb(100, 255, 255, 50)  # RGBA, 淺藍色(100, 255, 255), 透明度為 50
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # 設定圓形的矩形區域
        rect = QtCore.QRect(10, 10, 80, 80)
        start_angle = 90 * 16  # 起始角度
        full_angle = 360 * 16   # 完整圓的角度

        # 先繪製一個完整圓形
        painter.setPen(QtGui.QPen(QtGui.QColor(timer_text_color2), 6))
        painter.drawArc(rect, start_angle, full_angle)

        span_angle = int(self._value * 3.6 * 16)  # 計算角度

        # 設定筆和顏色
        painter.setPen(QtGui.QPen(QtGui.QColor(timer_text_color), 6))
        painter.drawArc(rect, start_angle, span_angle)

    def sizeHint(self):
        return QtCore.QSize(120, 120)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_GameplayWindow()
    ui.setupUi(MainWindow)

    ### 建立一個黑色背景底色
    bg = np.zeros((MainWindow.height(), MainWindow.width(), 3), np.uint8) # 創建一個空白BGR黑畫面
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB) # 將圖像從 BGRA 轉換成 RGBA 以符合QImage格式
    q_img = QtGui.QImage(bg.data, bg.shape[1], bg.shape[0], bg.shape[1] * 3, QtGui.QImage.Format_RGB888) # 轉換成 QImage 以用於放入Qlabel中顯示出來
    ui.label_camera.setPixmap(QtGui.QPixmap.fromImage(q_img))# 顯示在label_camera上

    MainWindow.show()
    sys.exit(app.exec_())
