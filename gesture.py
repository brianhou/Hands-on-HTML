import cv2
import numpy as np
import time

PALM_CONCAVITY_DIST_THRESH = 7000


class GestureRecognition:
  def recognize(self):
    cap = cv2.VideoCapture(0)
    old_pos = []
    new_pos = []
    old_areas = []
    new_areas = []
    next_element_last = False
    locked = True
    print "Gesture recognition locked...press <space> to unlock"
    while cap.isOpened():
      ret, img = cap.read()
      imageYCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
      min_YCrCb = np.array([0, 133, 77], np.uint8)
      max_YCrCb = np.array([255, 173, 127], np.uint8)
      skinRegion = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
  
      contours, _ = cv2.findContours(skinRegion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      if not contours:
        continue
      cnt = max(contours, key=lambda contour: cv2.contourArea(contour))
      hull = cv2.convexHull(cnt)
      moments = cv2.moments(cnt)
      if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
      else:
        continue
      center = (cx, cy)
      cv2.circle(img, center, 5, [0, 0, 255], 2)
      ret_val = ""

      cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
      hull = cv2.convexHull(cnt, returnPoints=False)
      defects = cv2.convexityDefects(cnt, hull)
      if defects is None:
        continue
      concave_starts_ends = []
      concave_points = []
      rotate = False
      for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        if self._get_distance(far, (cx, cy)) < PALM_CONCAVITY_DIST_THRESH:
          cv2.line(img, start, end, [0, 255, 0], 2)
          if end[0] != start[0]:
            if abs((end[1] - start[1]) * 1.0 / (end[0] - start[0])) < 0.05:
              rotate = True
          cv2.circle(img, far, 5, [0, 0, 255], -1)
          concave_starts_ends.append((start, end))
          concave_points.append(far)
      if len(concave_points) == 0:
        continue
      area = cv2.contourArea(cnt)
      if len(old_areas) < 10:
        old_areas.append(area)
      if len(new_areas) < 10:
        new_areas.append(area)
      else:
        if np.percentile(np.array(new_areas), 10) > max(old_areas):
          ret_val = "zoom in\n"
        if np.percentile(np.array(new_areas), 90) < min(old_areas):
          ret_val = "zoom out\n"
        old_areas.pop(0)
        old_areas.append(new_areas.pop(0))
        new_areas.append(area)
      if rotate:
        if sum([p[0] for p in concave_points]) / len([p[0] for p in concave_points]) > cx:
          ret_val = "rotate left\n"
        else:
          ret_val = "rotate right\n"
      if len(concave_points) == 1:
        start, end = concave_starts_ends[0]
        if end[0] != start[0] and (end[1] - start[1]) * 1.0 / (end[0] - start[0]) > 0:
          # discard ret_val and make it solely "next element"
          ret_val = "next element"

      if len(old_pos) < 5:
        old_pos.append((cx, cy))
      elif len(new_pos) < 5:
        new_pos.append((cx, cy))
      else:
        diff_x = sum([x[0] for x in new_pos]) / len(new_pos) - sum([x[0] for x in old_pos]) / len(old_pos)
        diff_y = sum([x[1] for x in new_pos]) / len(new_pos) - sum([x[1] for x in old_pos]) / len(old_pos)
        if diff_x < -50:
          ret_val = "right\n"
        if diff_x > 50:
          ret_val = "left\n"
        if diff_y < -50:
          ret_val = "down\n"
        if diff_y > 50:
          ret_val = "up\n"
        old_pos.pop(0)
        old_pos.append(new_pos.pop(0))
        new_pos.append((cx, cy))

      cv2.imshow('input', img)
      k = cv2.waitKey(3)

      # spacebar unlocks gestures
      if k in (1048608, 32):
        if locked:
          print "Unlocked gestures"
          locked = False
        else:
          print "Locked gestures"
          # resetting state maintenance variables
          old_pos = []
          new_pos = []
          old_areas = []
          new_areas = []
          next_element_last = False
          with open("static/instructions.txt", "w+") as f:
            f.write("")
          locked = True
      if not locked:
        ret_val = ret_val.strip()
        if ret_val == "next element":
          if next_element_last:
            ret_val = ""
          else:
            next_element_last = True
        else:
          next_element_last = False
        print ret_val
        with open("static/instructions.txt", "w+") as f:
          f.write(ret_val)

  def _get_distance(self, pos1, pos2):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


if __name__ == "__main__":
  gr = GestureRecognition()
  gr.recognize()
