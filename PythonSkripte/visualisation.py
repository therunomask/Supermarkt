import cv2
import numpy as np


def drawArea(frame, pts, ratio1, ratio2, color_nr, alpha):
    pts = np.array([[ratio1 * pts[1] + (1 - ratio1) * pts[0]], [ratio2 * pts[1] + (1 - ratio2) * pts[0]],
                    [ratio2 * pts[3] + (1 - ratio2) * pts[2]], [ratio1 * pts[3] + (1 - ratio1) * pts[2]]], np.int32)
    overlay = frame.copy()
    output = frame.copy()
    if color_nr == 1:
        color = (255, 0, 0)
    elif color_nr == 2:
        color = (0, 255, 0)
    elif color_nr == 3:
        color = (0, 0, 255)
    elif color_nr == 4:
        color = (123, 123, 0)
    else:
        color = (0, 123, 123)

    cv2.polylines(overlay, [pts], True, color)
    cv2.fillPoly(overlay, np.int_([pts]), color)
    # apply the overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    return output


def draw_number(frame, pts, ratio1, ratio2, color_nr, number):
    pts1 = np.array([[ratio1 * pts[1] + (1 - ratio1) * pts[0]], [ratio2 * pts[1] + (1 - ratio2) * pts[0]],
                     [ratio1 * pts[3] + (1 - ratio1) * pts[2]], [ratio2 * pts[3] + (1 - ratio2) * pts[2]]], np.int32)
    pts[0] = 2 * pts1[0] - pts1[2]
    pts[1] = 2 * pts1[1] - pts1[3]
    pts[2] = pts1[0]
    pts[3] = pts1[1]
    if color_nr == 1:
        color = (255, 0, 0)
    elif color_nr == 2:
        color = (0, 255, 0)
    elif color_nr == 3:
        color = (0, 0, 255)
    elif color_nr == 4:
        color = (123, 123, 0)
    else:
        color = (0, 123, 123)
    cv2.putText(frame, str(number), tuple((ratio1 * pts[1] + (1 - ratio1) * pts[0]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX,
                2, color, 2, cv2.LINE_AA)
    return frame

# cap = cv2.VideoCapture('/Users/Mingzi/Movies/video.mp4')
# while True:
#     ret, frame = cap.read()
#     pts = np.array([[100, 200], [200, 300], [600, 200], [500, 100]], np.int32)
#     output = drawArea(frame, pts, 0.2, 0.6, 3, 0.3)
#     cv2.polylines(output, [pts], True, (0, 0, 255))
#     cv2.putText(output, '3', (100, 500), cv2.FONT_HERSHEY_SIMPLEX,
#                 4, (0, 0, 255), 2, cv2.LINE_AA)
#     cv2.imshow("Image", output)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
