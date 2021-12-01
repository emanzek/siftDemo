import cv2
import numpy as np


class CompareImage(object):

    def __init__(self, image_1_path, image_2_path):
        self.minimum_commutative_image_diff = 1
        self.image_1_path = image_1_path
        self.image_2_path = image_2_path

    def compare_image(self):
        image_1 = cv2.imread(self.image_1_path, 0)
        image_2 = cv2.imread(self.image_2_path, 0)

        size1 = image_1.shape[1] * image_1.shape[0]
        size2 = image_2.shape[1] * image_2.shape[0]
        if size1 > size2:
            # print('Image1 bigger')
            resized1 = image_1
            resized2 = cv2.resize(image_2, (image_1.shape[1], image_1.shape[0]), interpolation=cv2.INTER_CUBIC)
        elif size2 > size1:
            # print('Image2 bigger')
            resized1 = cv2.resize(image_1, (image_2.shape[1], image_2.shape[0]), interpolation=cv2.INTER_CUBIC)
            resized2 = image_2
        else:
            # print('Image equal')
            resized1 = image_1
            resized2 = image_2

        commutative_image_diff = self.get_image_difference(resized1, resized2)

        # if commutative_image_diff < self.minimum_commutative_image_diff:
        #     return commutative_image_diff
        return commutative_image_diff

    @staticmethod
    def get_image_difference(resized1, resized2):
        sift = cv2.SIFT_create()
        kp1, desc1 = sift.detectAndCompute(resized1, None)
        kp2, desc2 = sift.detectAndCompute(resized2, None)
        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        try:
            matches = flann.knnMatch(np.asarray(desc1, np.float32), np.asarray(desc2, np.float32), k=2)
            cv2.waitKey(0)
            good_points = []
            for m, n in matches:
                if m.distance < 0.5 * n.distance:
                    good_points.append(m)
            img3 = cv2.drawMatches(resized1, kp1, resized2, kp2, good_points[:20], None, flags=2)
            #img4 = cv2.drawMatches(resized2, kp1, target, kp2, good_points[:20], None, flags=2)
            cv2.imshow('test',img3)
            cv2.waitKey(0)
            commutative_image_diff = len(good_points) / len(matches) * 100
        except:
            commutative_image_diff = 100
        cv2.destroyAllWindows()

        return commutative_image_diff
