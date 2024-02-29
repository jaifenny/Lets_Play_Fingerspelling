import cv2
import pickle


# Colors RGB Format
BLACK  = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (238, 194, 48)
NAVY = (15, 33, 103)
BLUE = (97, 214, 255)

### 顏色設定
BOX_TEXT_COLOR = NAVY
BOX_COLOR = BLUE
FINGER_LINE_COLOR = BLUE
FINGER_LINE_STROKE_COLOR = BLUE
FINGER_POINT_COLOR = BLUE
FINGER_POINT_STROKE_COLOR = BLUE

LABEL_TEXT_SIZE_SCALE = 0.6

### 手部圖示尺寸大小！
FINGER_POINT_SIZE_LARGE = 5 # 手指末端點的圓圈大小
FINGER_POINT_SIZE_SMALL = 5 # 其餘非末端點的圓圈大小

## 線條粗細大小！
LINE_WIDTH = 2
LINE_STROKE_WIDTH = 1 # 因目前設計沒有邊框線，所以設定與線條寬度相同，視同無邊框線


# 根據設計圖，不用畫出的點
# 編號對應的位置：https://www.researchgate.net/publication/362871842/figure/fig1/AS:11431281084350163@1663153181104/MediaPipe-Hands-21-landmarks-13.ppm
IGNORE_POINT_INDEX = [1, 6, 7, 10, 11, 14, 15, 18, 19]


def draw_bounding_box(image, min_x, max_x, min_y, max_y, gesture):
    cv2.rectangle(image, (min_x - 20, min_y - 10), (max_x + 20, max_y + 10), BLUE, 2)
    image = draw_info_text(image, [min_x - 20, min_y - 10, max_x + 20, max_y + 10], gesture)
    return image

def draw_info_text(image, pos, hand_sign_text):
    cv2.rectangle(
        image, (pos[0] - 2, pos[1]), (pos[2] + 2, pos[1] - 30),
        BOX_COLOR, -1
    )

    info_text = ""
    if hand_sign_text != "":
        info_text = hand_sign_text
    cv2.putText(
        image, info_text, (pos[0] + 8, pos[1] - 4),
        cv2.FONT_HERSHEY_SIMPLEX, LABEL_TEXT_SIZE_SCALE, BOX_TEXT_COLOR, 1, cv2.LINE_AA
    )
    return image


def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # Thumb
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]), FINGER_LINE_COLOR, LINE_WIDTH)

        # Index finger
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]), FINGER_LINE_COLOR, LINE_WIDTH)

        # Middle finger
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]), FINGER_LINE_COLOR, LINE_WIDTH)

        # Ring finger
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]), FINGER_LINE_COLOR, LINE_WIDTH)

        # Little finger
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]), FINGER_LINE_COLOR, LINE_WIDTH)

        # Palm
        cv2.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]), FINGER_LINE_COLOR, LINE_WIDTH)
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), FINGER_LINE_STROKE_COLOR, LINE_STROKE_WIDTH)
        cv2.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]), FINGER_LINE_COLOR, LINE_WIDTH)

    # Key Points

    landmark_point = list(filter(lambda x: landmark_point.index(x) not in IGNORE_POINT_INDEX, landmark_point))

    for index, landmark in enumerate(landmark_point):
        if index == 0:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 1:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 2:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 3:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 4:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_STROKE_COLOR,  1)
        if index == 5:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 6:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 7:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 8:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_STROKE_COLOR,  1)
        if index == 9:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 10:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 11:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 12:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_STROKE_COLOR,  1)
        if index == 13:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 14:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 15:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 16:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_STROKE_COLOR,  1)
        if index == 17:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 18:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 19:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_SMALL, FINGER_POINT_STROKE_COLOR,  1)
        if index == 20:
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_COLOR, -1)
            cv2.circle(image, (landmark[0], landmark[1]), FINGER_POINT_SIZE_LARGE, FINGER_POINT_STROKE_COLOR,  1)

    return image


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    # Keypoint
    landmark_point = []
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width ), image_width  - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point.append([landmark_x, landmark_y])
    return landmark_point


def classify_landmark(landmark):
    wrist         = landmark[0]
    thump         = landmark[1:5]
    index_finger  = landmark[5:9]
    middle_finger = landmark[9:13]
    ring_finger   = landmark[13:17]
    pinky         = landmark[17:21]
    return [[wrist], thump, index_finger, middle_finger, ring_finger, pinky]


def is_finger_on(idx, finger, landmark_label):
    if idx == 0:
        if landmark_label == "Right":
            return finger[-1].x < finger[-2].x
        else:
            return finger[-1].x > finger[-2].x
    return finger[-1].y < finger[0].y


# model_dict = pickle.load(open(model_path, 'rb'))
def load_model(model_path):
    with open(model_path, 'rb') as model_file:
        model_dict = pickle.load(model_file)
        model = model_dict['model']
    return model