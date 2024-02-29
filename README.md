# Let's Play Fingerspelling
 使用機器學習訓練的手語辨識模型來偵測玩家手勢，支援兩位玩家一同遊玩。
## :book: Introduction

美國拼寫手語（ASL Fingerspelling）是利用特定手勢來表達特定的英文字母，可以補足一般手語
系統中無法表示的概念，常用於表達人名、專有名詞。

現有的手語學習工具大多使用影片教學，對於學習手語拼寫的初學者而言缺少互動性和趣味性。
少數採用遊戲化的方式，卻採用「猜測圖片代表的手勢」， 缺少實際演練讓人很難提起學習興趣 。

本遊戲使用機器學習訓練的手語辨識模型 來偵測玩家手勢，支援 兩位玩家一同遊玩。兩位玩家根
據畫面出現的英文單字，使用 拼寫手語答題，透過遊玩與練習模式熟悉英文字母的手語手勢。

### :small_blue_diamond: 手語辨識模型:
* MediaPipe
* Scikit-learn
* Google ASL Fingerspelling (Dataset)
### :small_blue_diamond: 程式介面:
* OpenCV
* PyQt5
* Pygame
### :small_blue_diamond: Python Library Requirement:
* opencv-python
* mediapipe
* scikit-learn==1.2.0
* tensorflow # Tensorflow Lite for Kaggle Model
* PyQt5
* pygame

##  Results
![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/1.png)

![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/2.png)

![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/3.png)

![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/4.png)

![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/5.png)

![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/6.png)

![](https://github.com/jaifenny/Lets_Play_Fingerspelling/blob/main/picture/7.png)


## Conclusion

### :small_orange_diamond: 學習成效

- 雙人競賽的遊玩機制讓學習手語的過程變得更有趣。
- 經過多次的遊玩有助於記憶拼寫手語的手勢。

### :small_orange_diamond: 未來改進方向

- 更現代化的介面設計與互動設計。
- 改成跨平台或網頁應用程式，更容易推廣。
- 吸引玩家願意重複遊玩的機制。

## Reference
1. Fingerspelling - Wikipedia:
 https://en.wikipedia.org/wiki/Fingerspelling
2. Learn ASL: The Fingerspelling Alphabet for Beginners - Youtube:
 https://youtu.be/fXf4d23WqiA?si=Iszfn8bNgwMOdU3B
3. ASL fingerspelling keyboard - GitHub:
 https://github.com/Bhuribhat/ASL-Finger-Spelling-To-Text
4. ] Fingerspelling - American Society for Deaf Children:
 https://fingerspelling.xyz/
5. Gesture Recognition - MediaPipe Studio:
 https://mediapipe-studio.webapps.google.com/studio/demo/gesture_recognizer
6. Google - ASL Fingerspelling Recognition - Kaggle:
 https://www.kaggle.com/competitions/asl-fingerspelling/overview

