from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QMovie
from pygame import mixer
import cv2
import numpy as np
import random
import time

from interface_menu import Ui_MenuWindow
from interface_gameplay import Ui_GameplayWindow, CameraLabel, CircularProgress
from question_list import QuestionListLevelOne, QuestionListLevelTwo ,QuestionListLevelThree, QuestionListLevelFour
from interface_result import Ui_ResultWindow
from interface_gesture import Ui_GestureWindow
from interface_introduction import Ui_IntroductionWindow
from interface_level import Ui_LevelWindow
from interface_practice import Ui_PracticeWindow

# 手勢辨識相關檔案
from sign_detect.sign_detector import SignDetector # 負責做手部辨識的本體
from sign_detect.utils import draw_bounding_box, draw_landmarks # 未來可替換成自己的畫圖函式


# 定義 controller_MainWindow 類別
class controller_MainWindow(QtWidgets.QMainWindow):
    ### 用於整個控制邏輯的init函式

    def __init__(self):
        super().__init__()
        self.goto_menu() #  顯示主選單

    # 音效
    def sound(self, file):

        mixer.init()
        # 載入音效
        mixer.music.load(file)
        # 音量大小
        mixer.music.set_volume(0.8)
        # 播放
        mixer.music.play()

    ### 切換UI畫面到主選單Menu
    def goto_menu(self):
        # print("UI : goto_menu")
        self.global_degree = None
        self.global_gesture = None
        'global_score1 改名 global_p1_score'
        self.global_p1_score = None
        'global_score2 改名 global_p2_score'
        self.global_p2_score = None
        self.global_isGamePlay = False
        self.global_isPractice = False
        self.global_isResult = False

        self.init_ui_timer() # 初始化切換UI的計時器
        self.stop_camera_access()

        self.ui = Ui_MenuWindow() # 建立 Ui_MenuWindow 子物件
        self.ui.setupUi(self) # 設置 UI

        self.setup_menu() # 啟動 setup_menu 函式設置控制邏輯

    ### 定義切換UI時的延遲時間，以確保切換前的函式可以正確執行
    def init_ui_timer(self):
        self.goto_result_timer = QtCore.QTimer(self)
        self.goto_result_timer.setSingleShot(True)
        self.goto_result_timer.timeout.connect(self.goto_result)

        self.goto_gesture_timer = QtCore.QTimer(self)
        self.goto_gesture_timer.setSingleShot(True)
        self.goto_gesture_timer.timeout.connect(self.goto_gesture)

        self.stop_camera_timer = QtCore.QTimer(self)
        self.stop_camera_timer.setSingleShot(True)
        self.stop_camera_timer.timeout.connect(self.stop_camera_access)

    def stop_camera_access(self):
        if hasattr(self, 'cap') and self.cap is not None:  # 檢查self.cap是否存在且不為None
            self.cap.release()  # 釋放相機資源
            self.frame_timer.stop()  # 停止定時器

    ### 設定主選單Menu的按鈕邏輯
    def setup_menu(self):
        # setVisible() 用來顯示物件
        # clicked.connect() 用來連接按鈕點擊事件
        self.ui.button_menu_play.setVisible(True)
        self.ui.button_menu_play.clicked.connect(self.goto_level)
        self.ui.button_menu_play.clicked.connect(lambda: self.sound("click.mp3"))

        self.ui.button_menu_practice.setVisible(True)
        self.ui.button_menu_practice.clicked.connect(self.goto_gesture)
        self.ui.button_menu_practice.clicked.connect(lambda: self.sound("click.mp3"))

        self.ui.button_menu_intro.setVisible(True)
        self.ui.button_menu_intro.clicked.connect(self.goto_intro)
        self.ui.button_menu_intro.clicked.connect(lambda: self.sound("click.mp3"))

    ### 切換UI畫面到選擇關卡
    def goto_level(self):
        # print("UI : goto_level")
        self.ui = Ui_LevelWindow() # 建立 Ui_LevelWindow 子物件
        self.ui.setupUi(self) # 設置 UI
        self.setup_level()

    ### 設定選擇關卡level的按鈕邏輯
    def setup_level(self):
        # 定義一個字典將按鈕和對應的等級綁定在一起
        level_buttons = {
            self.ui.button_level_one: 1,
            self.ui.button_level_two: 2,
            self.ui.button_level_three: 3,
            self.ui.button_level_four: 4
        }
        # 對每一個按鈕設置
        # setVisible() 用來顯示物件
        # clicked.connect() 用來連接按鈕點擊事件
        # 在 PyQt 中按鈕的點擊事件會傳遞一個事件參數, 暫時將其命名為 _clicked_event, 但之後不需要用到它
        for button, level in level_buttons.items():
            button.setVisible(True)
            button.clicked.connect(lambda _clicked_event, lvl=level: self.choose_level(lvl))
            button.clicked.connect(lambda: self.sound("click.mp3"))

        # 設置從關卡回選單的按鈕
        self.ui.button_level_2_menu.setVisible(True)
        self.ui.button_level_2_menu.clicked.connect(self.goto_menu)
        self.ui.button_level_2_menu.clicked.connect(lambda: self.sound("click.mp3"))

    ### 設定選擇關卡之後的控制邏輯
    def choose_level(self, level):
        self.global_degree = level
        # print(f"Choose level: {level}")
        self.goto_gameplay() # 前往遊戲畫面

    ### 切換UI畫面到選擇練習手勢
    def goto_gesture(self):
        # print("UI : goto_gesture")
        self.ui = Ui_GestureWindow() # 建立 Ui_GameplayWindow 子物件
        self.ui.setupUi(self) # 設置 UI

        # 顯示所有按鈕
        for row in range(self.ui.buttons_layout.rowCount()):
            for col in range(self.ui.buttons_layout.columnCount()):
                item = self.ui.buttons_layout.itemAtPosition(row, col)
                if item is not None:
                    button = item.widget()
                    if button:
                        button.setVisible(True)
                        # 傳入參數 btn.property('gesture') 為該按鈕代表的手勢(一個字串)
                        button.clicked.connect(lambda _checked, btn=button: self.choose_gesture(btn.property('gesture')))
                        button.clicked.connect(lambda: self.sound("click.mp3"))

        # 設置從關卡回選單的按鈕
        self.ui.button_gesture_2_menu.setVisible(True)
        self.ui.button_gesture_2_menu.clicked.connect(self.goto_menu)
        self.ui.button_gesture_2_menu.clicked.connect(lambda: self.sound("click.mp3"))

    ### 設定選擇手勢之後的控制邏輯
    def choose_gesture(self, gesture):
        self.global_gesture = gesture
        # print(f"Choose gesture: {self.global_gesture}")
        self.goto_practice() # 前往練習模式

    ### 切換UI畫面到到介紹頁面
    def goto_intro(self):
        # print("UI : goto_intro")
        self.ui = Ui_IntroductionWindow() # 建立 Ui_GameplayWindow 子物件
        self.ui.setupUi(self) # 設置 UI

        self.ui.button_intro_2_menu.setVisible(True)
        self.ui.button_intro_2_menu.clicked.connect(self.goto_menu)
        self.ui.button_intro_2_menu.clicked.connect(lambda: self.sound("click.mp3"))

    ### 切換UI畫面到開始遊玩遊戲 gameplay
    def goto_gameplay(self):
        # print("UI : goto_gameplay")
        self.ui = Ui_GameplayWindow() # 建立 Ui_GameplayWindow 子物件
        self.ui.setupUi(self) # 設置 UI
        self.setup_gameplay() # 啟動 setup_gameplay 函式

    ### 設置遊玩遊戲 gameplay 運作邏輯
    def setup_gameplay(self):
        self.global_isGamePlay = True
        self.init_camera() # 初始化相機
        self.init_gesture()  # 初始化手勢
        time.sleep(0.03)  # 等待30毫秒(鏡頭畫面初始化)
        self.init_timer()
        self.init_question()

    ### 切換到開始練習模式 practice
    def goto_practice(self):
        # print("Start gesture practice")
        # print("UI : goto_practice")
        # print(f"Start gesture practice for button: {self.global_gesture}")

        self.ui = Ui_PracticeWindow() # 建立 Ui_PracticeWindow 子物件
        self.ui.setupUi(self) # 設置 UI
        self.setup_practice() # 啟動 setup_practice 函式

    ### 設置練習模式 practice 運作邏輯
    def setup_practice(self):
        self.global_isPractice = True
        self.init_camera() # 初始化相機
        self.init_gesture() # 初始化手勢
        time.sleep(0.03)  # 等待30毫秒(鏡頭畫面初始化)
        self.init_input()

    ### 鏡頭畫面初始化
    def init_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.frame_timer = QtCore.QTimer(self) # 刷新鏡頭的timer

        self.frame_timer.start(30) # timer間隔為30 ms, 代表每30秒呼叫一次連結的方法(FPS=33)
        self.frame_timer.timeout.connect(self.update_frame) # timer的timeout信號連接到update_frame方法

    ### 手勢辨識初始化
    def init_gesture(self):
        # 初始化手勢偵測器
        self.sign_detector = SignDetector(gesture_keep_time = 1, detect_count_threshold = 8)

        # 設定當兩個玩家比出字母時，要呼叫的函式
        self.sign_detector.listen_p1_input(self.on_p1_input)
        self.sign_detector.listen_p2_input(self.on_p2_input)

    ### 倒數計時和得分機制初始化
    def init_timer(self):
        self.global_countdown_time = 10000  # 初始倒數時間為10秒 (10000 毫秒)
        self.player1_time_remaining = self.global_countdown_time # 玩家1初始剩餘時間
        self.player2_time_remaining = self.global_countdown_time # 玩家2初始剩餘時間

        # 玩家1的計時器
        self.player1_countdown_timer = QtCore.QTimer(self) # 倒數計時的timer
        self.player1_countdown_timer.start(30)  # timer 間隔為 30 ms, 代表每 30 毫秒呼叫一次連結的方法
        # timer的timeout信號連接到 update_timer 方法
        # 由於直接連接信號和帶參數的函數並不直接支持使用帶有參數的函式
        # 因此可以使用 lambda 來創建一個無參數的匿名函式
        self.player1_countdown_timer.timeout.connect(lambda: self.update_timer(1))

        # 玩家2的計時器
        self.player2_countdown_timer = QtCore.QTimer(self) # 倒數計時的timer
        self.player2_countdown_timer.start(30)  # timer 間隔為 30 ms, 代表每 30 毫秒呼叫一次連結的方法
        # timer的timeout信號連接到 update_timer 方法
        self.player2_countdown_timer.timeout.connect(lambda: self.update_timer(2))

    ### 隨機出題功能初始化
    def init_question(self):
        # 初始化
        self.player1_current_score = 0 # 玩家1初始分數
        self.player2_current_score = 0 # 玩家2初始分數
        self.question_count = 0 # 計算當前出題數目

        # print("QuestionListLevel: ", self.global_degree)

        if self.global_degree == 1:
            self.word = random.choice(QuestionListLevelOne) # 儲存要顯示的問題單詞
        elif self.global_degree == 2:
            self.word = random.choice(QuestionListLevelTwo) # 儲存要顯示的問題單詞
        elif self.global_degree == 3:
            self.word = random.choice(QuestionListLevelThree) # 儲存要顯示的問題單詞
        elif self.global_degree == 4:
            self.word = random.choice(QuestionListLevelFour) # 儲存要顯示的問題單詞

        self.player1_current_index = 0 # 追蹤玩家1目前輸入到哪一個字母
        self.player2_current_index = 0 # 追蹤玩家2目前輸入到哪一個字母

        self.ui.setup_question(self.ui.label_player1_question, self.word, self.player1_current_index) # 初始化玩家1的輸入在畫面上
        self.ui.setup_question(self.ui.label_player2_question, self.word, self.player2_current_index) # 初始化玩家2的輸入在畫面上

    ### 練習模式的玩家輸入初始化
    def init_input(self):
        # print("Practice gesture is: ", self.global_gesture)
        if self.global_gesture is not None:
            self.word = self.global_gesture

        self.ui.setup_instruction(self.ui.label_player1_instruction, self.word) # 初始化玩家1的指示在畫面上
        self.ui.setup_instruction(self.ui.label_player2_instruction, self.word) # 初始化玩家1的指示在畫面上

        self.player1_current_index = 0 # 追蹤玩家1目前輸入到哪一個字母
        self.player2_current_index = 0 # 追蹤玩家2目前輸入到哪一個字母

        self.ui.setup_input(self.ui.label_player1_input, self.word, self.player1_current_index) # 初始化玩家1的題目在畫面上
        self.ui.setup_input(self.ui.label_player2_input, self.word, self.player2_current_index) # 初始化玩家1的題目在畫面上

    # 鏡頭更新, 使用QTimer來更新畫面
    def update_frame(self):
        if not self.cap.isOpened():
            print("Cannot open camera.")
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1) # 將影像左右翻轉
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # 先將BGR轉換成RGB以符合QImage格式

            # 結算畫面就不顯示手勢
            if self.global_isResult == False:
                # [Sign] 3. 將 frame 丟入手勢辨識
                self.sign_detector.recognize(frame)


            # 建立低亮度低對比的圖像
            # 公式: frame * (contrast/127 + 1) - contrast + brightness
            # np.clip() 會將一個array內的數值限制在一個區間, 這裡是限制在0~255
            # np.uint8() 會將數值全部取整數
            brightness = -100 # 亮度範圍: -127 ~ 127
            contrast = -50 # 對比範圍: -127 ~ 127
            dark_frame = np.uint8(np.clip(frame*(contrast/127+1)-contrast+brightness, 0, 255))


            # 結算畫面就不顯示手勢
            if self.global_isResult == False:
                # [Sign] 4. （畫圖相關）使用 get_bounding_boxes 取得資訊，畫出辨識到的手部區域 boundig box
                for box in self.sign_detector.get_bounding_boxes():
                    dark_frame = draw_bounding_box(dark_frame, box['min_x'], box['max_x'], box['min_y'], box['max_y'], box['gesture'])

                # [Sign] 5. （畫圖相關）使用 get_landmarks 取得資訊，畫出手部關鍵點
                for landmark in self.sign_detector.get_landmarks():
                    dark_frame = draw_landmarks(dark_frame, landmark)

            # 建立QImage物件以用於放入Qlabel中顯示出來
            # dark_frame.data代表圖像數據的記憶體位置, w, h 代表寬和高
            # QtGui.QImage.Format_RGB888 指定圖像的格式, 代表每個像素由3個byte組成(R,G,B),
            # 這是將 OpenCV 中的 BGR 格式轉換為 PyQt 中的 RGB 格式的常用方法
            # cvt2Qimage.scaled() 將 QImage 對象縮放到指定的大小, QtCore.Qt.KeepAspectRatio 確保在縮放過程中保持畫面的長寬比
            h, w, ch = dark_frame.shape # 取得高, 寬, 色彩通道
            bytesPerLine = ch * w # 計算每行畫面所佔的byte數, 用於建立QImage
            cvt2Qimage = QtGui.QImage(dark_frame.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            cvt2Qimage = cvt2Qimage.scaled(960, 720, QtCore.Qt.KeepAspectRatio)
            self.ui.label_camera.setPixmap(QtGui.QPixmap.fromImage(cvt2Qimage)) # 更新 QLabel

    ### 定義 player1 比出字母 (char) 時要做的事情
    # self.current_index < len(self.word) 代表還有字母未被輸入
    # event.text() 獲取由鍵盤事件（event）產生的文字。例如，如果玩家按下了 'A' 鍵，event.text() 就會是 'A'
    # lower() 方法將獲取的文字轉換為小寫。這是為了確保比較時不區分大小寫，因為 self.word 是小寫的
    # self.word[self.current_index] 2代表玩家目前需要回答的字母
    # event.text().lower() == self.word[self.current_index] 代表鍵盤接收的輸入後與答案批配
    def on_p1_input(self, char):
        # print("on_p1_input:", char)
        if self.global_isGamePlay: # 遊戲模式
            if self.player1_current_index < len(self.word) and char.lower() == self.word[self.player1_current_index]:
                self.player1_current_index += 1 # 繼續下一個字母
                self.ui.setup_question(self.ui.label_player1_question ,self.word, self.player1_current_index) # 更新畫面

                # 如果所有字母都輸入正確，則得分
                if self.player1_current_index == len(self.word):
                    # print("Player1, you're awesome!")
                    self.increase_score(1)  # 玩家1得分
                    # print("player1_current_score: ", self.player1_current_score)
                    self.player1_countdown_timer.stop()  # 停止計時器
                    self.check_continue() # 判斷是否可以切換題目或結束遊戲

        elif self.global_isPractice: # 練習模式
            if self.player1_current_index < len(self.word) and char.lower() == self.word[self.player1_current_index]:
                self.player1_current_index += 1 # 繼續下一個字母
                self.ui.setup_input(self.ui.label_player1_input ,self.word, self.player1_current_index) # 更新畫面

                # 如果所有字母都輸入正確，則修改偵測狀態
                if self.player1_current_index == len(self.word):
                    self.ui.label_player1_state.setText("GOOD JOB!")
                    # 播放音效
                    self.sound("point1.mp3")
                    self.check_continue() # 判斷是否可以切換題目或結束遊戲

    ### 定義 player2 比出字母 (char) 時要做的事情
    def on_p2_input(self, char):
        # print("on_p2_input:", char)
        if self.global_isGamePlay: # 遊戲模式
            if self.player2_current_index < len(self.word) and char.lower() == self.word[self.player2_current_index]:
                self.player2_current_index += 1 # 繼續下一個字母
                self.ui.setup_question(self.ui.label_player2_question ,self.word, self.player2_current_index) # 更新畫面

                # 如果所有字母都輸入正確，則得分
                if self.player2_current_index == len(self.word):
                    # print("Player2, you're awesome!")
                    self.increase_score(2)  # 玩家2得分
                    # print("player2_current_score: ", self.player2_current_score)
                    self.player2_countdown_timer.stop()  # 停止計時器
                    self.check_continue() # 判斷是否可以切換題目或結束遊戲

        elif self.global_isPractice: # 練習模式
            if self.player2_current_index < len(self.word) and char.lower() == self.word[self.player2_current_index]:
                self.player2_current_index += 1 # 繼續下一個字母
                self.ui.setup_input(self.ui.label_player2_input ,self.word, self.player2_current_index) # 更新畫面

                # 如果所有字母都輸入正確，則修改偵測狀態
                if self.player2_current_index == len(self.word):
                    self.ui.label_player2_state.setText("GOOD JOB!")
                    # 播放音效
                    self.sound("point2.mp3")
                    self.check_continue() # 判斷是否可以切換題目或結束遊戲

    # 更新倒數計時, 每次 timer 觸發，扣除時間並更新倒數計時的顯示
    # 接收 player 參數, 以便存取 player_data 內的數據
    def update_timer(self, player):
        if player == 1:
            self.player1_time_remaining -= 30  # 30 毫秒為 timer 的間隔
            seconds_remaining = int(self.player1_time_remaining / 1000)
            self.ui.label_player1_timer.setText(f"{max(seconds_remaining+1, 1)}") # 倒數計時顯示從10一直減到1

            # 更新 CircularProgress 的值，使其根據剩餘時間進行更新
            progress_value1 = (self.player1_time_remaining / self.global_countdown_time) * 100
            self.ui.circularProgress1.setValue(progress_value1)

            # 每次 timer 觸發，根據剩餘時間增加得分
            if self.player1_time_remaining <= 0:
                self.player1_countdown_timer.stop()
                # print("Player1 TIME OUT")
                self.check_continue() # 判斷是否可以切換題目或結束遊戲
        elif player == 2:
            self.player2_time_remaining -= 30  # 30 毫秒為 timer 的間隔
            seconds_remaining = int(self.player2_time_remaining / 1000)
            self.ui.label_player2_timer.setText(f"{max(seconds_remaining+1, 1)}") # 倒數計時顯示從10一直減到1

            # 更新 CircularProgress 的值，使其根據剩餘時間進行更新
            progress_value2 = (self.player2_time_remaining / self.global_countdown_time) * 100
            self.ui.circularProgress2.setValue(progress_value2)

            # 每次 timer 觸發，根據剩餘時間增加得分
            if self.player2_time_remaining <= 0:
                self.player2_countdown_timer.stop()
                # print("Player2 TIME OUT")
                self.check_continue() # 判斷是否可以切換題目或結束遊戲

    ### 切換UI畫面到結算分數畫面 result
    def goto_result(self):
        # print("UI: goto_result")

        self.ui = Ui_ResultWindow() # 建立 Ui_ResultWindow 子物件
        self.ui.setupUi(self) # 設置 UI
        self.setup_result() # 啟動 setup_end 函式

    ### 設置結束遊戲的 gameplay 運作邏輯
    def setup_result(self):
        self.global_isResult = True
        self.ui.label_player1_finalscore.setText("THE FINAL SCORE IS:\n{:06}".format(self.global_p1_score))
        self.ui.label_player2_finalscore.setText("THE FINAL SCORE IS:\n{:06}".format(self.global_p2_score))
        if self.global_p1_score > self.global_p2_score:
            self.ui.label_player1_result.setText("Player1 WIN!!!")
            # 彩帶動畫
            self.movie = QMovie("win.gif")
            self.ui.label_player1_gif.setMovie(self.movie)
            self.movie.start()
            self.ui.label_player2_result.setText("Player2 LOSE...")
        elif self.global_p1_score < self.global_p2_score:
            self.ui.label_player2_result.setText("Player2 WIN!!!")
            # 彩帶動畫
            self.movie = QMovie("win.gif")
            self.ui.label_player2_gif.setMovie(self.movie)
            self.movie.start()
            self.ui.label_player1_result.setText("Player1 LOSE...")
        elif self.global_p1_score == self.global_p2_score:
            self.ui.label_player1_result.setText("THE GAME IS TIED.")
            self.ui.label_player2_result.setText("THE GAME IS TIED.")
        # 播放勝利音效
        self.sound("cheer.mp3")
        # 連接按鈕點擊事件
        self.ui.button_return_menu.setVisible(True)
        self.ui.button_return_menu.clicked.connect(self.goto_menu)
        self.ui.button_return_menu.clicked.connect(lambda: self.sound("click.mp3"))

    ### 判斷題目更新或結束遊戲, 透過update_timer和keyPressEvent觸發
    def check_continue(self):
        # print("check_continue")
        if self.global_isGamePlay: # 遊玩模式
            # self.question_count += 1
            # print("question_count:", self.question_count)
            # print(f"player1_current_index: {self.player1_current_index}, player2_current_index: {self.player2_current_index}")
            # 如果玩家1和2都完成題目, 且尚未超過10題, 則刷新題目, 從題庫中選擇新字串
            if self.player1_current_index == len(self.word) and self.player2_current_index == len(self.word):
                self.question_count += 1
                if  self.question_count < 10:
                    self.continue_game()
                else: # 如果玩家1和2都完成題目, 且超過10題, 則結束遊戲, 進入結算畫面
                    self.end_game()

            # 如果玩家1或2時間到, 且尚未超過10題, 則刷新題目, 從題庫中選擇新字串
            elif self.player1_time_remaining <= 0 or self.player2_time_remaining <= 0:
                self.question_count += 1
                if  self.question_count < 10:
                    self.continue_game()
                else: # 如果玩家1和2時間到, 且超過10題, 則結束遊戲, 進入結算畫面
                    self.end_game()

        elif self.global_isPractice: # 練習模式
            # print(f"player1_current_index: {self.player1_current_index}, player2_current_index: {self.player2_current_index}")
            # 如果玩家1和2都完成練習
            if self.player1_current_index == len(self.word) and self.player2_current_index == len(self.word):
                self.global_isPractice = False
                self.stop_camera_timer.start(2000)
                self.goto_gesture_timer.start(2000+200) # 1000ms 後回到選擇手勢介面

    ### 題目更新
    def continue_game(self):
        # print("continue_game")
        self.player1_time_remaining = self.global_countdown_time
        self.player2_time_remaining = self.global_countdown_time
        self.player1_countdown_timer.start(30)  # 更新計時
        self.player2_countdown_timer.start(30)  # 更新計時

        if self.global_degree == 1:
            self.word = random.choice(QuestionListLevelOne) # 儲存要顯示的問題單詞
        elif self.global_degree == 2:
            self.word = random.choice(QuestionListLevelTwo) # 儲存要顯示的問題單詞
        elif self.global_degree == 3:
            self.word = random.choice(QuestionListLevelThree) # 儲存要顯示的問題單詞
        elif self.global_degree == 4:
            self.word = random.choice(QuestionListLevelFour) # 儲存要顯示的問題單詞

        self.player1_current_index = 0 # 重置玩家1的輸入
        self.player2_current_index = 0 # 重置玩家2的輸入

        self.ui.setup_question(self.ui.label_player1_question, self.word, self.player1_current_index) # 重置玩家1的題目在畫面上
        self.ui.setup_question(self.ui.label_player2_question, self.word, self.player2_current_index) # 重置玩家1的題目在畫面上

    ### 結束遊戲
    def end_game(self):
        # print("end_game")
        # self.close()
        self.player1_countdown_timer.stop()  # 停止計時器
        self.player2_countdown_timer.stop()  # 停止計時器

        self.global_p1_score = self.player1_current_score
        self.global_p2_score = self.player2_current_score

        self.global_isGamePlay = False
        self.goto_result_timer.start(1000)  # 1000ms 後切換到結算頁面

    # 增加得分
    def increase_score(self, player):
        if player == 1:
            # 取得當前顯示分數
            self.player1_current_score = int(self.ui.label_player1_score.text().split(":")[1])
            # 播放音效
            self.sound("point1.mp3")
            # 增加得分(剩餘幾毫秒就得幾分)
            self.player1_current_score += self.player1_time_remaining
            # 更新得分顯示
            self.ui.label_player1_score.setText("SOORE: {:06}".format(self.player1_current_score))
            # zoom_in_font_size 得分特效放大字體
            self.zoom_in_font_size(self.ui.label_player1_score, 3)
            QtCore.QTimer.singleShot(30, lambda: self.zoom_in_font_size(self.ui.label_player1_score, 2))
            # 在300毫秒後縮小字體大小
            QtCore.QTimer.singleShot(450, lambda: self.zoom_out_font_size(self.ui.label_player1_score, 3))
            QtCore.QTimer.singleShot(450+30, lambda: self.zoom_out_font_size(self.ui.label_player1_score, 2))

        elif player == 2:
            # 取得當前顯示分數
            self.player2_current_score = int(self.ui.label_player2_score.text().split(":")[1])
            # 播放音效
            self.sound("point2.mp3")
            # 增加得分(剩餘幾毫秒就得幾分)
            self.player2_current_score += self.player2_time_remaining
            # 更新得分顯示
            self.ui.label_player2_score.setText("SCORE: {:06}".format(self.player2_current_score))
            # zoom_in_font_size 得分特效放大字體
            self.zoom_in_font_size(self.ui.label_player2_score, 3)
            QtCore.QTimer.singleShot(30, lambda: self.zoom_in_font_size(self.ui.label_player2_score, 2))
            # 在200毫秒後縮小字體大小
            QtCore.QTimer.singleShot(450, lambda: self.zoom_out_font_size(self.ui.label_player2_score, 3))
            QtCore.QTimer.singleShot(450+30, lambda: self.zoom_out_font_size(self.ui.label_player2_score, 2))

    # 放大字體大小
    def zoom_in_font_size(self, label, size):
        font = label.font()
        font.setPointSize(font.pointSize() + size)  # 增加size字體大小
        label.setFont(font)

    # 縮小字體大小
    def zoom_out_font_size(self, label, size):
        font = label.font()
        font.setPointSize(font.pointSize() - size)  # 減少size字體大小
        label.setFont(font)

    ### 函式 keyPressEvent 用來處理鍵盤事件, 當玩家按下鍵盤時, 這個方法會被呼叫。
    ### 這邊覆寫 PyQt 的標準 keyPressEvent 方法, 藉此設定自定義的鍵盤事件
    def keyPressEvent(self, event):
        # 如果按下的是 Esc 則進入結束遊戲畫面
        if event.key() == QtCore.Qt.Key_Escape:
            # print("press esc")
            # self.close()
            self.player1_countdown_timer.stop()  # 停止計時器
            self.player2_countdown_timer.stop()  # 停止計時器

            self.global_p1_score = self.player1_current_score
            self.global_p2_score = self.player2_current_score

            self.global_isGamePlay = False
            self.goto_result()

# 也可以將以下整段放在 start.py 中
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv) # 創建一個 QApplication 物件，它是啟動所有 PyQt 應用程式的基礎
    window = controller_MainWindow() # 創建一個 controller_MainWindow 物件作為主視窗
    window.show()
    sys.exit(app.exec_())