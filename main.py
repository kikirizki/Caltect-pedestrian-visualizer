# [class] [identity] [x_center] [y_center] [width] [height]
import cv2
import os
import os.path as path

IMAGES_DIR = "Caltech/images"
LABELS_DIR = "Caltech/labels_with_ids"


def remove_leading_zeros(img_name):
    result = ""
    leading = True
    for c in img_name:

        if int(c) != 0:
            leading = False
        if not leading:
            result += c

    return result
framenum_list = [remove_leading_zeros(img.replace(".jpg","").replace("img","")) for img in os.listdir(IMAGES_DIR)]
framenum_list = [int(n) for n in framenum_list]
framenum_list.sort()
framenum_list = [str(n).zfill(5) for n in framenum_list]
image_path_list = [path.join(IMAGES_DIR, "img{}.jpg".format(num)) for num in framenum_list ]




def draw(label_str, img_cv):
    img_width = img_cv.shape[1]
    img_height = img_cv.shape[0]
    assert (img_width > img_height)
    for l in label_str:
        l = l.replace("\n", "")
        cls, identitty, x_center, y_center, width, height = l.split(" ")
        cls, identitty, x_center, y_center, width, height = \
            int(cls), \
            int(identitty), \
            float(x_center), \
            float(y_center), \
            float(width), \
            float(height)
        top, left = y_center - (height / 2), x_center - (width / 2)
        bottom, right = top + height, left + width
        top = int(top * img_height)
        bottom = int(bottom * img_height)
        left = int(left * img_width)
        right = int(right * img_width)

        cv2.rectangle(img_cv, (left, top), (right, bottom), (255, 0, 0), 1)
    return img_cv


for img_path in image_path_list:
    img_cv = cv2.imread(img_path)
    lbl_path = img_path.replace(IMAGES_DIR, LABELS_DIR).replace("jpg", "txt")
    lbl = open(lbl_path, 'r')
    drawed = draw(lbl.readlines(), img_cv)
    cv2.imshow("track", drawed)
    lbl.close()
    if cv2.waitKey(1000) == 'q':
        break
