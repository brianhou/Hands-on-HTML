import json
import cv2
import numpy as np

AREA_THRESHOLD = 20000


class ProcessInput:
  def process(self, jpg_name):
    img = cv2.imread(jpg_name + ".jpg")
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_thresh = np.array([0, 0, 0], dtype=np.uint8)
    upper_thresh = np.array([180, 100, 100], dtype=np.uint8)
    black_mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    contours, _ = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
    largest_area = max([cv2.contourArea(contour) for contour in contours])
    rects = []
    image_info = {}

    for contour in contours:
      if cv2.contourArea(contour) > AREA_THRESHOLD:
      # if cv2.contourArea(contour) == largest_area:
        rects.append(cv2.boundingRect(contour))
    for x, y, w, h in rects:
      for x2, y2, w2, h2 in rects:
        if x > x2 and x + w < x2 + w2 and y > y2 and y + h < y2 + h2:
          print("Removing contained rectangle")
          rects.remove((x, y, w, h))
    for i, (x, y, w, h) in enumerate(rects):
      cv2.rectangle(img, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=3)
      out_img_name = jpg_name + "_out%d.jpg"%i
      cv2.imwrite(out_img_name, img[y:y+h, x:x+w])
      image_info[len(image_info)] = {"top": y, "left": x, "width": w * 1.0 / img.shape[1], "aspect-ratio": w * 1.0 / h, "path": out_img_name}

    json_obj = {"num_images": len(image_info), "images": image_info}
    out = json.dumps(json_obj)
    print out
    return out

    # cv2.imshow("img", img)
    # cv2.imshow("black_mask", black_mask)
    # cv2.waitKey(0)

def jsonify(fname):
  pi = ProcessInput()
  return pi.process(fname)

if __name__ == "__main__":
  jsonify('images/test')
