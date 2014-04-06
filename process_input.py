import json
import cv2
import numpy as np
import subprocess

IMAGE_AREA_THRESHOLD = 2000
TEXT_AREA_THRESHOLD = 200
EROSION_FACTOR = 15


class ProcessInput:
  def __init__(self):
    self.json_obj = {}

  def execute(self, img_name):
    img_rects = self._process_for_images(img_name)
    self._process_for_text(img_name, img_rects)

  def _process_for_images(self, img_name):
    img = cv2.imread(img_name)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_thresh = np.array([0, 0, 0], dtype=np.uint8)
    upper_thresh = np.array([180, 100, 100], dtype=np.uint8)
    black_mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    contours, _ = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
    rects = []
    image_info = {}

    for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      if w * h > IMAGE_AREA_THRESHOLD:
        rects.append((x, y, w, h))
    self._remove_unwanted_rectangles(rects)
    for i, (x, y, w, h) in enumerate(rects):
      # cv2.rectangle(img, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=3)
      p_index = img_name.find(".")
      out_img_name = img_name[:p_index] + "images" + repr(i) + img_name[p_index:]
      cv2.imwrite(out_img_name, img[y:y+h, x:x+w])
      image_info["i" + repr(len(image_info))] = {"top": y * 1.0 / img.shape[0],
                                     "left": x * 1.0 / img.shape[1],
                                     "width": w * 1.0 / img.shape[1],
                                     "aspect": w * 1.0 / h,
                                     "path": out_img_name}
    self.json_obj["num_images"] = len(image_info)
    self.json_obj["images"] = image_info

    # cv2.imshow("img", img)
    # cv2.imshow("black_mask", black_mask)
    # cv2.waitKey(0)

    return rects

  def _process_for_text(self, img_name, img_rects):
    img = cv2.imread(img_name)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    mask = np.ones((EROSION_FACTOR, EROSION_FACTOR), dtype=np.uint8)
    img_eroded = cv2.erode(img, mask)
    hsv = cv2.cvtColor(img_eroded, cv2.COLOR_BGR2HSV)
    lower_thresh = np.array([0, 0, 0], dtype=np.uint8)
    upper_thresh = np.array([180, 100, 100], dtype=np.uint8)
    black_mask = cv2.inRange(hsv, lower_thresh, upper_thresh)
    # finds contours of eroded image
    contours, _ = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    text_info = {}

    for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      if w * h > TEXT_AREA_THRESHOLD:
        rects.append((x, y, w, h))
    self._remove_unwanted_rectangles(rects)
    # remove detected rectangles that completely surround image rectangles
    i = 0
    while i < len(rects):
      x, y, w, h = rects[i]
      i += 1
      for x2, y2, w2, h2 in img_rects:
        if x < x2 and x + w > x2 + w2 and y < y2 and y + h > y2 + h2:
          rects.remove((x, y, w, h))
          i -= 1
          break
    for i, (x, y, w, h) in enumerate(rects):
      # cv2.rectangle(img, (x, y), (x+w, y+h), color=(0, 0, 255), thickness=3)
      p_index = img_name.find(".")
      out_img_name = img_name[:p_index] + "text" + repr(i) + img_name[p_index:]
      cv2.imwrite(out_img_name, img[y:y+h, x:x+w])
      subprocess.call("tesseract " + out_img_name + " images/out > /dev/null 2>&1", shell=True)
      with open("images/out.txt", "r+") as f:
        text = f.read().strip()
        if text:
          text_info["t" + repr(len(text_info))] = {"top": y * 1.0 / img.shape[0],
                                       "left": x * 1.0 / img.shape[1],
                                       "string": text,
                                       "height": h}

    self.json_obj["num_texts"] = len(text_info)
    self.json_obj["texts"] = text_info

    # cv2.imshow("img", img)
    # cv2.imshow("black_mask", black_mask)
    # cv2.waitKey(0)

  def _remove_unwanted_rectangles(self, rects):
    i = 0
    while i < len(rects):
      x, y, w, h = rects[i]
      i += 1
      for x2, y2, w2, h2 in rects:
        if x > x2 and x + w < x2 + w2 and y > y2 and y + h < y2 + h2:
          rects.remove((x, y, w, h))
          i -= 1
          break

def jsonify(img_name):
  pi = ProcessInput()
  pi.execute(img_name)
  return json.dumps(pi.json_obj)


if __name__ == "__main__":
  jsonify("images/big_test.jpg")
