from PIL import Image

picture = Image.open("test.png")

# Get the size of the image
width, height = picture.size
new_color = (0, 0, 0)
# Process every pixel
for x in width:
    for y in height:
        current_color = picture.getpixel((x, y))
        ####################################################################
        # Do your logic here and create a new (R,G,B) tuple called new_color
        ####################################################################
        picture.putpixel((x, y), new_color)

# import cv2
# from PIL import Image, ImageDraw
# import numpy as np
# import math
#
# img_rgb = cv2.imread('emulator-5554-screenshot.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# cv2.imwrite('gray-screenshot.png', img_gray)
# template1 = cv2.imread('icons/train3.png')
# template = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
# w, h = template.shape[::-1]
#
# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) # TM_CCORR_NORMED TM_CCOEFF_NORMED
# min_val, max_val, min_loc, max_loc= cv2.minMaxLoc(res)
# threshold = 0.8
# loc = np.where( res >= threshold)
# x = 0
# y = 0
# if len(loc[0]):
#     y = loc[0][0]
#     x = loc[1][0]
# print(x, y)
#
# pt = max_loc
# print(pt)
# # for pt in zip(*loc[::-1]):
# #     print(pt[0], pt[1])
# cv2.rectangle(img_rgb, pt, (pt[0] + 100, pt[1] + 100), (0,0,255), 2)
# # cv2.rectangle(img_rgb, min_loc, (min_loc[0] + 100, min_loc[1] + 100), (0,0,255), 2)
# # for pt in zip(*loc[::-1]):
# #     cv2.rectangle(img_rgb, pt, (w,  h), (0,255,255), 2)
# #
# cv2.imshow('Detected', img_rgb)
# cv2.waitKey()
# input("Press Enter to continue...")






















#
# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv.imread('icons/train.png',0)
# img2 = img.copy()
# template = cv.imread('emulator-5554-screenshot.png',0)
# w, h = template.shape[::-1]
# # All the 6 methods for comparison in a list
# methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
#             'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
# for meth in methods:
#     img = img2.copy()
#     method = eval(meth)
#     # Apply template Matching
#     res = cv.matchTemplate(img,template,method)
#     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#     cv.rectangle(img,top_left, bottom_right, 255, 2)
#     plt.subplot(121),plt.imshow(res,cmap = 'gray')
#     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img,cmap = 'gray')
#     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)
#     plt.show()