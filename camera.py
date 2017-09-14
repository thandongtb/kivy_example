import cv2
import dlib
import imutils
from kivy.app import App
from imutils import face_utils

class SimpleKivy(App):
    def build(self):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        (mountStart, mountEnd) = (48, 68)
        video_capture = cv2.VideoCapture(0)
        print video_capture.isOpened()

        while (video_capture.isOpened()):
            ret, frame = video_capture.read()
            if ret == True:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = imutils.resize(gray, width=150)
                ratio = frame.shape[0] / float(gray.shape[0])
                rects = detector(gray, 1)

                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    mount = shape[mountStart:mountEnd]
                    mount[:] = [x * ratio for x in mount]
                    mountHull = cv2.convexHull(mount)
                    cv2.drawContours(frame, [mountHull], -1, (0, 0, 255), 5)

                cv2.imshow('Video', frame)
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    SimpleKivy().run()