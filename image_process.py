import cv2

a = 32

img = cv2.imread("images/smaller.jpeg")
#cv2.imshow("input", img)
#cv2.waitKey(0)
dst = cv2.resize(img, (32, 32))
cv2.imwrite("images/smaller.png", dst)