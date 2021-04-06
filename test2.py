import cv2
import pytesseract
import csv
from pytesseract import Output


image = cv2.imread('test_img_2.jpg')

cv2.imshow("Orginal Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_blur = cv2.GaussianBlur(image,(3,3),0)
cv2.imshow("Imgae after smoothing", img_blur)
cv2.waitKey(0)
cv2.destroyAllWindows()
#chuyển hình ảnh thành hình ảnh thang độ xám

gray_image = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image after convert to gray", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# chuyển đổi nó sang hình ảnh nhị phân bằng Thresholding
# nếu là hình màu thì tesseract sẽ không thể phát hiện văn bản chính xác và điều này sẽ
# cho kết quả không chính xác
threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# hiển thị ảnh đã chuyển sáng nhị phân
cv2.imshow("threshold image", threshold_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# cấu hình các thông số cho tesseract
custom_config = r'--oem 3 --psm 6'

# Truy cập đến thư mục cài đặt trsseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# cung cấp hình ảnh vào cho tersseract
details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')
print(details.keys())
total_boxes = len(details['text'])

for sequence_number in range(total_boxes):
	if int(details['conf'][sequence_number]) >30:
		(x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
		threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# hiển thị ảnh đã được xử lý tesseract
cv2.imshow('captured text', threshold_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

parse_text = []

word_list = []

last_word = ''

for word in details['text']:

    if word!='':
        word_list.append(word)
        last_word = word
    if (last_word!='' and word == '') or (word==details['text'][-1]):
        parse_text.append(word_list)
        word_list = []

with open('result.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)