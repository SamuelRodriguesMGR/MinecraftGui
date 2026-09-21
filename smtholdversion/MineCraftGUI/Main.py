
from TextRecognition.TextRecognition import TextRecognition


def main():
    recog_pos = TextRecognition((4, 108, 360, 18), "screenshot_position.png")
    recog_angle = TextRecognition((4, 162, 522, 18), "screenshot_position.png")
    print(recog_pos.get_text())
    print(recog_angle.get_text())

if __name__ == "__main__":
    main()