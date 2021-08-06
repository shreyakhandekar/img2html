# importing modules
from ensurepip import bootstrap
import cv2
import pytesseract
import csv
import numpy as np
# reading image using opencv
from pytesseract import Output
from imutils import grab_contours as grb_cns
from imutils import resize as rsz
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model

img_height = 180
img_width = 180
AUTOTUNE = tf.data.AUTOTUNE
from keras.models import load_model

class_names = ['button', 'checkbox', 'dropdown', 'input', 'text']
model = load_model('trModel.h5')
num = 0
of = open("sample.html", "w")
# importing modules
from ensurepip import bootstrap

#html = "<html><head><link rel = 'stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css' integrity='sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB' crossorigin='anonymous'><style>.box{border:1px solid black;} </style></head><body>"

html = "<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6' crossorigin='anonymous'><style>.box{border:1px solid black;} </style></head>" \
       "<body><style>button{background-color:green; color: black;padding: 14px 50px;}input[type=text]{padding: 2px 5px;text-align: center;}" \
       "select{display:block;padding:10px;cursor:pointer;}</style>"

image = cv2.imread("sample.png", cv2.IMREAD_GRAYSCALE)
(_, threshold) = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY_INV)
# Copy the thresholded image.
im_floodfill = threshold.copy()
# Mask used to flood filling.
# Notice the size needs to be 2 pixels than the image.
h, w = threshold.shape[:2]
mask = np.zeros((h + 2, w + 2), np.uint8)
# Floodfill from point (0, 0)
cv2.floodFill(im_floodfill, mask, (0, 0), 255)
# Invert floodfilled image
im_floodfill_inv = cv2.bitwise_not(im_floodfill)
# Combine the two images to get the foreground
thresh = threshold | im_floodfill_inv
# Display images.

#cv2.imshow("Thresholded Image", threshold)
#cv2.waitKey(0)
#cv2.imshow("Floodfilled Image", im_floodfill)
#cv2.waitKey(0)
#cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
#cv2.waitKey(0)
#cv2.imshow("Foreground", thresh)
#cv2.waitKey(0)

threshold_img = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# display image
#cv2.imshow('threshold image', threshold_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
(contours, _) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    #p = cv2.arcLength(cnt,True)

    #if area > 400:
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt,
                                                             True), True)
    #if len(approx) == 4:
    img = cv2.drawContours(image, [approx], 0, (0, 0, 0xFF), 5)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.imwrite('object.png', img[y:y + h+2 , x:x + w+2 ])

    print("approx ", x, y, w, h)
    # load and resize image

    testing = keras.preprocessing.image.load_img('object.png', target_size=(img_height, img_width))
        # convert image to array
    test = keras.preprocessing.image.img_to_array(testing)
            # create a batch/dimension
    test = tf.expand_dims(test, 0)
            # predict label
    predictions = model.predict(test)
            # label with maximum chances
    score = tf.nn.softmax(predictions[0])
            # output label
    label = class_names[np.argmax(score)]
    print(label)
    #   if label==input
    if label=='input':
        div = "<div class='input' style='"
        div = div + "position: absolute;"
        div = div + "left: " + str(x) + ";"
        div = div + "top: " + str(y) + ";"
        #div = div + "width: " + str(w) + "px;"
        #div = div + "height: " + str(h) + "px;"
        div = div + "'><input type='text' placeholder='Input' /></div>"
        html = html + "\n" + div
    #   if label==checkbox
    elif label=='checkbox':
        div = "<div class='input' style='"
        div = div + "position: absolute;"
        div = div + "left: " + str(x) + ";"
        div = div + "top: " + str(y) + ";"
        #div = div + "width: " + str(w) + ";"
        #div = div + "height: " + str(h) + ";"
        div = div + "'><input type='checkbox' /></div>"
        html = html + "\n" + div
    #   if label==button
    elif label=='button':
        div = "<div class='button' style='"
        div = div + "position: absolute;"
        div = div + "left: " + str(x) + ";"
        div = div + "top: " + str(y) + ";"
        #div = div + "width: " + str(w) + ";"
        #div = div + "height: " + str(h) + ";"
        div = div + "'><button type = 'submit' value='Button'>Button</button></div>"
        html = html + "\n" + div
    #   if label==dropdown
    elif label=='dropdown':
        div = "<div class='select' style='"
        div = div + "position: absolute;"
        div = div + "left: " + str(x) + ";"
        div = div + "top: " + str(y) + ";"
        #div = div + "width: " + str(w) + ";"
        #div = div + "height: " + str(h) + ";"
        div = div + "'><select><option value='1'>--Select--</option><option value='2'>--Select--</option></select></div>"
        html = html + "\n" + div
    #if label==text
    elif label=='text':
        div = "<div class='text' style='"
        div = div + "position: absolute;"
        div = div + "left: " + str(x) + ";"
        div = div + "top: " + str(y) + ";"
        #div = div + "width: " + str(w) + ";"
        #div = div + "height: " + str(h) + ";"
        div = div + "'>Text</div>"
        html = html + "\n" + div
    num += 1

html = html + '</center></body></html>'

of.write(html)
of.close()

#if cv2.waitKey(0) & 0xFF == ord('q'):
#    cv2.destroyAllWindows()