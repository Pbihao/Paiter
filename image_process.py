import cv2

a = 32

img = cv2.imread("images/src.jpeg")
#cv2.imshow("input", img)
#cv2.waitKey(0)
dst = cv2.resize(img, (64, 64))
cv2.imwrite("images/cut.png", dst)