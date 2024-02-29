import time
import numpy as np
import mediapipe as mp
import sys

from sign_detect.utils import load_model
from sign_detect.utils import calc_landmark_list

class SignDetector():

    def __init__(self, gesture_keep_time = 1, detect_count_threshold = 8, model_path = "./classifier"):
        """ 創建手勢辨識器

        在 gesture_keep_time 秒內，有被辨識到超過 detect_count_threshold 次的字母才算輸入

        因為辨識的速度很快 (辨識的 FPS 在 15 以上) 會很容易誤觸發，
        gesture_keep_time 可以理解成每個手勢要維持幾秒才算輸入，
        當 gesture_keep_time 越小，手勢越容易被辨識到

        Args:
            gesture_keep_time (int): 在 gesture_keep_time 秒內，有被辨識到超過 detect_count_threshold 次的字母才算輸入，預設 1 秒。
            detect_count_threshold (int): 在 gesture_keep_time 秒內，有被辨識到超過 detect_count_threshold 次的字母才算輸入，
                參考目前辨識的 FPS 大概在 15~ 24 ，預設為 8。
            model_path (str): 手勢辨識模型的路徑，預設為 "./classifier"。
        """
        # 設定視訊鏡頭的 index
        self.camera_index = 1 # 通常是 0 或 1

        self.p1_char = '' # player 1 上一次成功比出的字母
        self.p2_char  = '' # player 2 上一次成功比出的字母

        self.current_hand = 0 # 目前被辨識到的手數量
        self.unknown_letter = '?' # 辨識不出來的回傳值

        # Mediapipe 手部辨識的參數
        self.max_hands = 2
        self.min_detection_confidence = 0.6  #@param {type:"slider", min:0, max:1, step:0.01}
        self.min_tracking_confidence  = 0.5  #@param {type:"slider", min:0, max:1, step:0.01}

        # Load model
        model_letter_path = f"{model_path}/classify_letter_model.p"
        # Load Classification Model
        self.letter_model = load_model(model_letter_path)

        # 切分兩個玩家的中心線
        self.mid_x = None # 辨識時初始化

        # 在 gesture_keep_time 秒內，有被辨識到超過 detect_count_threshold 次的字母才算輸入
        # 不然因為辨識的速度很快（辨識的 FPS 可以到 15/sec），會很容易誤觸發
        # 可以理解成每個手勢要維持幾秒才算輸入
        # - gesture_keep_time 越小，手勢越容易被辨識到
        self.gesture_keep_time = gesture_keep_time
        self.detect_count_threshold = detect_count_threshold

        # 設置每隔 gesture_keep_time 秒執行一次清空短時間內辨識的字母次數
        self.previous_time = time.time() # 上次清空的時間

        # 紀錄每個手勢的辨識次數
        self.p1_detect_count_dict = {chr(i+ord('a')): 0 for i in range(0, 26)}
        self.p2_detect_count_dict = {chr(i+ord('a')): 0 for i in range(0, 26)}

        # 當玩家比出手勢時，會呼叫對應的 callback
        self.p1_input_callback = lambda char : print(f"p1 input: {char}")
        self.p2_input_callback = lambda char : print(f"p2 input: {char}")

        # 給外部畫圖用的資訊
        self.bounding_boxes = [] # 儲存手部範圍的 bounding box
        self.landmarks = []

        self.init()

    def _set_player_current_char(self, char, player):
        if player == 1:
            self.p1_char = char
            self.p1_input_callback(char)
        else:
            self.p2_char = char
            self.p2_input_callback(char)

    def get_bounding_boxes(self):
        """
        取得 bounding box 資訊的 list[dict]

        Returns:
            list: 包含多個 dict 的 list，每個 dict 表示一個 bounding box，包含以下 key value:
                - 'min_x' (int): bounding box 的最小 x 值
                - 'max_x' (int): bounding box 的最大 x 值
                - 'min_y' (int): bounding box 的最小 y 值
                - 'max_y' (int): bounding box 的最大 y 值
                - 'gesture' (str): 預測的字母
                - 'current_player' (int): 玩家的編號
        """
        return self.bounding_boxes

    def get_landmarks(self):
        return self.landmarks

    def listen_p1_input(self, callback):
        """ 當 player1 比出手勢時，會使用 char (比出的字母) 參數呼叫 callback

        Args:
            callback (function): 一個以 char (比出的字母) 為參數的 function
        """
        self.p1_input_callback = callback

    def listen_p2_input(self, callback):
        """ 當 player2 比出手勢時，會使用 char (比出的字母) 參數呼叫 callback

        Args:
            callback (function): 一個以 char (比出的字母) 為參數的 function
        """
        self.p2_input_callback = callback

    def get_p1_char(self):
        return self.p1_char

    def get_p2_char(self):
        return self.p2_char

    def clear_detect_count_if_need(self):
        time_elapsed = time.time() - self.previous_time
        if time_elapsed >= self.gesture_keep_time:
            self._clear_both_player_detect_count()
            self.previous_time = time.time()

    def _clear_both_player_detect_count(self):
        self._reset_detect_count_dict(1)
        self._reset_detect_count_dict(2)

    def _handle_raw_detect(self, char, player):
        # 如果是無法判斷的字母就不處理
        if(char == self.unknown_letter):
            return

        char = char.lower()

        # 根據玩家，取得對應的 dict
        detect_count_dict = self.p1_detect_count_dict if player == 1 else self.p2_detect_count_dict
        # 該字母的辨識次數 + 1
        detect_count_dict[char] += 1

        # 短期間內，被辨識到的次數超過門檻，才算輸入
        if detect_count_dict[char] >= self.detect_count_threshold:
            # 超過辨識次數門檻，更新玩家的當前字母
            self._set_player_current_char(char, player)
            # 辨識成功，重置該玩家的辨識次數紀錄
            self._reset_detect_count_dict(player)

    def _reset_detect_count_dict(self, player):
        if player == 1:
            self.p1_detect_count_dict ={key : 0 for key in self.p1_detect_count_dict}
        else:
            self.p2_detect_count_dict ={key : 0 for key in self.p2_detect_count_dict}

    def init(self):
        # 初始化 mediapipe 手部偵測
        self.hands : mp.solutions.hands.Hands =  mp.solutions.hands.Hands (
            max_num_hands= self.max_hands,
            min_detection_confidence = self.min_detection_confidence,
            min_tracking_confidence = self.min_tracking_confidence,
        )
        print("Sign Detector Initialized")


    def recognize(self, image):
        # ps. input image 得色彩格式需要是 RGB

        if(self.mid_x == None):
            h, w, _ = image.shape
            self.mid_x = int(w/2)

        # To improve performance, optionally mark the image as not writeable to pass by reference
        image.flags.writeable = False
        results = self.hands.process(image)

        # Draw the hand annotations on the image
        image.flags.writeable = True

        # 清空手部範圍的 bounding box 與 landmarks
        self.bounding_boxes = []
        self.landmarks = []

        # 每隔 gesture_keep_time 秒執行一次清空短時間內辨識的字母次數
        self.clear_detect_count_if_need()

        try:
            image = self.recognize_gesture(image, results)

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(f"{error}, line {exc_tb.tb_lineno}")

        return image

    def _process_and_detect_gesture(self, current_select_hand, x_values, y_values, player):
        """ 處理並且辨識手勢，回傳辨識到的字母

        Returns:
            gesture(string): 辨識到的字母，若無法辨識會是"?"
        """
        # Create Data Augmentation for Corrected Hand
        data_aux = []
        for i in range(len(current_select_hand.landmark)):
            data_aux.append(x_values[i] - min(x_values))
            data_aux.append(y_values[i] - min(y_values))

        # Alphabets Prediction
        prediction = self.letter_model.predict([np.asarray(data_aux)])
        gesture = str(prediction[0]).title()
        gesture = gesture if gesture != 'Unknown_Letter' else '?'

        self._handle_raw_detect(gesture, player)

        return gesture

    def _determine_player(self, min_x, max_x):
        """ 依據手勢的 x 座標，判斷是哪個玩家 """
        if (min_x + max_x) /2 <= self.mid_x:
            # print("player 1")
            return 1  # 玩家 1
        else:
            # print("player 2")
            return 2


    def recognize_gesture(self, image, results):
        multi_hand_landmarks = results.multi_hand_landmarks
        multi_handedness = results.multi_handedness

        if results.multi_hand_landmarks:
            h, w, _ = image.shape
            for idx in reversed(range(len(multi_hand_landmarks))):
                current_select_hand = multi_hand_landmarks[idx]
                handness = multi_handedness[idx].classification[0].label
                landmark_list = calc_landmark_list(image, current_select_hand)

                # Get (x, y) coordinates of hand landmarks
                x_values = [lm.x for lm in current_select_hand.landmark]
                y_values = [lm.y for lm in current_select_hand.landmark]

                # Get Minimum and Maximum Values
                min_x = int(min(x_values) * w)
                max_x = int(max(x_values) * w)
                min_y = int(min(y_values) * h)
                max_y = int(max(y_values) * h)

                # Flip Left Hand to Right Hand
                if handness == 'Left':
                    x_values = list(map(lambda x: 1 - x, x_values))
                    min_x -= 10

                # 根據手勢的 x 座標，判斷是哪個玩家
                current_player = self._determine_player(min_x, max_x)

                # 偵測手勢
                gesture = self._process_and_detect_gesture(current_select_hand, x_values, y_values, current_player)

                # 儲存手部的 bounding box 與 landmarks
                self.bounding_boxes.append({"min_x": min_x, "max_x": max_x, \
                    "min_y": min_y, "max_y": max_y, "gesture": gesture, "current_player": current_player})
                self.landmarks.append(landmark_list)

        # Track hand numbers
        if results.multi_hand_landmarks:
            self.current_hand = len(multi_hand_landmarks)
        else:
            self.current_hand = 0
        # print(f"[Sign] 目前辨識到 {self.current_hand} 隻手")
        return image
