import cv2
import torch
import numpy as np
from network import Pip_sfnetv2
from PIL import Image, ImageDraw
import torchvision.models as models
import torchvision.transforms as transforms


# 此api仅支持单张人脸
class Get_Ldms():
    def __init__(self, weight_path = './weight.pth', device='cuda'):
        super(Get_Ldms, self).__init__()

        self.num_ldms = 68
        self.device = device
        self.reverse_index1 = [1, 2, 17, 18, 36, 1, 2, 17, 18, 36, 1, 2, 17, 18, 36, 1, 2, 17, 18, 36, 1, 2, 0, 2, 3, 17, 0, 2, 3, 17, 0, 2, 3, 17, 0, 2, 3, 17, 0, 2, 3, 17, 0, 2, 0, 1, 3, 4, 0, 1, 3, 4, 0, 1, 3, 4, 0, 1, 3, 4, 0, 1, 3, 4, 0, 1, 1, 2, 4, 5, 1, 2, 4, 5, 1, 2, 4, 5, 1, 2, 4, 5, 1, 2, 4, 5, 1, 2, 2, 3, 5, 6, 2, 3, 5, 6, 2, 3, 5, 6, 2, 3, 5, 6, 2, 3, 5, 6, 2, 3, 3, 4, 6, 7, 3, 4, 6, 7, 3, 4, 6, 7, 3, 4, 6, 7, 3, 4, 6, 7, 3, 4, 3, 4, 5, 7, 8, 3, 4, 5, 7, 8, 3, 4, 5, 7, 8, 3, 4, 5, 7, 8, 3, 4, 5, 6, 8, 9, 5, 6, 8, 9, 5, 6, 8, 9, 5, 6, 8, 9, 5, 6, 8, 9, 5, 6, 6, 7, 9, 10, 6, 7, 9, 10, 6, 7, 9, 10, 6, 7, 9, 10, 6, 7, 9, 10, 6, 7, 7, 8, 10, 11, 7, 8, 10, 11, 7, 8, 10, 11, 7, 8, 10, 11, 7, 8, 10, 11, 7, 8, 8, 9, 11, 12, 13, 8, 9, 11, 12, 13, 8, 9, 11, 12, 13, 8, 9, 11, 12, 13, 8, 9, 9, 10, 12, 13, 9, 10, 12, 13, 9, 10, 12, 13, 9, 10, 12, 13, 9, 10, 12, 13, 9, 10, 10, 11, 13, 14, 10, 11, 13, 14, 10, 11, 13, 14, 10, 11, 13, 14, 10, 11, 13, 14, 10, 11, 11, 12, 14, 15, 11, 12, 14, 15, 11, 12, 14, 15, 11, 12, 14, 15, 11, 12, 14, 15, 11, 12, 12, 13, 15, 16, 12, 13, 15, 16, 12, 13, 15, 16, 12, 13, 15, 16, 12, 13, 15, 16, 12, 13, 13, 14, 16, 26, 13, 14, 16, 26, 13, 14, 16, 26, 13, 14, 16, 26, 13, 14, 16, 26, 13, 14, 14, 15, 25, 26, 45, 14, 15, 25, 26, 45, 14, 15, 25, 26, 45, 14, 15, 25, 26, 45, 14, 15, 0, 1, 2, 18, 19, 36, 37, 41, 0, 1, 2, 18, 19, 36, 37, 41, 0, 1, 2, 18, 19, 36, 0, 1, 17, 19, 20, 36, 37, 38, 41, 0, 1, 17, 19, 20, 36, 37, 38, 41, 0, 1, 17, 19, 0, 17, 18, 20, 21, 36, 37, 38, 40, 41, 0, 17, 18, 20, 21, 36, 37, 38, 40, 41, 0, 17, 17, 18, 19, 21, 36, 37, 38, 39, 40, 41, 17, 18, 19, 21, 36, 37, 38, 39, 40, 41, 17, 18, 18, 19, 20, 22, 27, 28, 37, 38, 39, 40, 41, 18, 19, 20, 22, 27, 28, 37, 38, 39, 40, 41, 21, 23, 24, 25, 27, 28, 42, 43, 44, 46, 47, 21, 23, 24, 25, 27, 28, 42, 43, 44, 46, 47, 22, 24, 25, 26, 42, 43, 44, 45, 46, 47, 22, 24, 25, 26, 42, 43, 44, 45, 46, 47, 22, 24, 16, 22, 23, 25, 26, 43, 44, 45, 46, 47, 16, 22, 23, 25, 26, 43, 44, 45, 46, 47, 16, 22, 15, 16, 23, 24, 26, 43, 44, 45, 46, 15, 16, 23, 24, 26, 43, 44, 45, 46, 15, 16, 23, 24, 14, 15, 16, 24, 25, 44, 45, 46, 14, 15, 16, 24, 25, 44, 45, 46, 14, 15, 16, 24, 25, 44, 20, 21, 22, 23, 28, 29, 38, 39, 40, 42, 43, 47, 20, 21, 22, 23, 28, 29, 38, 39, 40, 42, 21, 22, 27, 29, 30, 39, 40, 42, 47, 21, 22, 27, 29, 30, 39, 40, 42, 47, 21, 22, 27, 29, 27, 28, 30, 31, 35, 39, 42, 27, 28, 30, 31, 35, 39, 42, 27, 28, 30, 31, 35, 39, 42, 27, 28, 29, 31, 32, 33, 34, 35, 28, 29, 31, 32, 33, 34, 35, 28, 29, 31, 32, 33, 34, 35, 28, 2, 3, 29, 30, 32, 33, 48, 49, 2, 3, 29, 30, 32, 33, 48, 49, 2, 3, 29, 30, 32, 33, 29, 30, 31, 33, 34, 35, 49, 50, 29, 30, 31, 33, 34, 35, 49, 50, 29, 30, 31, 33, 34, 35, 29, 30, 31, 32, 34, 35, 50, 51, 52, 29, 30, 31, 32, 34, 35, 50, 51, 52, 29, 30, 31, 32, 29, 30, 31, 32, 33, 35, 52, 53, 29, 30, 31, 32, 33, 35, 52, 53, 29, 30, 31, 32, 33, 35, 13, 14, 29, 30, 32, 33, 34, 53, 54, 13, 14, 29, 30, 32, 33, 34, 53, 54, 13, 14, 29, 30, 0, 1, 2, 17, 18, 19, 20, 37, 38, 39, 40, 41, 0, 1, 2, 17, 18, 19, 20, 37, 38, 39, 0, 1, 17, 18, 19, 20, 21, 36, 38, 39, 40, 41, 0, 1, 17, 18, 19, 20, 21, 36, 38, 39, 0, 1, 17, 18, 19, 20, 21, 27, 28, 36, 37, 39, 40, 41, 0, 1, 17, 18, 19, 20, 21, 27, 19, 20, 21, 27, 28, 29, 36, 37, 38, 40, 41, 19, 20, 21, 27, 28, 29, 36, 37, 38, 40, 41, 0, 1, 17, 18, 19, 20, 21, 27, 28, 36, 37, 38, 39, 41, 0, 1, 17, 18, 19, 20, 21, 27, 0, 1, 2, 17, 18, 19, 20, 21, 36, 37, 38, 39, 40, 0, 1, 2, 17, 18, 19, 20, 21, 36, 22, 23, 24, 27, 28, 29, 43, 44, 45, 46, 47, 22, 23, 24, 27, 28, 29, 43, 44, 45, 46, 47, 15, 16, 22, 23, 24, 25, 26, 27, 42, 44, 45, 46, 47, 15, 16, 22, 23, 24, 25, 26, 27, 42, 15, 16, 22, 23, 24, 25, 26, 42, 43, 45, 46, 47, 15, 16, 22, 23, 24, 25, 26, 42, 43, 45, 14, 15, 16, 23, 24, 25, 26, 42, 43, 44, 46, 47, 14, 15, 16, 23, 24, 25, 26, 42, 43, 44, 14, 15, 16, 22, 23, 24, 25, 26, 42, 43, 44, 45, 47, 14, 15, 16, 22, 23, 24, 25, 26, 42, 15, 16, 22, 23, 24, 25, 26, 27, 28, 42, 43, 44, 45, 46, 15, 16, 22, 23, 24, 25, 26, 27, 2, 3, 4, 5, 6, 49, 59, 60, 2, 3, 4, 5, 6, 49, 59, 60, 2, 3, 4, 5, 6, 49, 3, 4, 5, 31, 32, 48, 50, 51, 59, 60, 61, 67, 3, 4, 5, 31, 32, 48, 50, 51, 59, 60, 30, 31, 32, 33, 34, 48, 49, 51, 52, 58, 59, 60, 61, 62, 66, 67, 30, 31, 32, 33, 34, 48, 30, 31, 32, 33, 34, 35, 48, 49, 50, 52, 53, 54, 56, 58, 60, 61, 62, 63, 64, 65, 66, 67, 30, 32, 33, 34, 35, 50, 51, 53, 54, 55, 56, 62, 63, 64, 65, 30, 32, 33, 34, 35, 50, 51, 11, 12, 13, 34, 35, 52, 54, 55, 63, 64, 65, 11, 12, 13, 34, 35, 52, 54, 55, 63, 64, 65, 10, 11, 12, 13, 14, 53, 55, 64, 10, 11, 12, 13, 14, 53, 55, 64, 10, 11, 12, 13, 14, 53, 8, 9, 10, 11, 12, 13, 53, 54, 56, 57, 63, 64, 65, 8, 9, 10, 11, 12, 13, 53, 54, 56, 7, 8, 9, 10, 11, 12, 54, 55, 57, 58, 63, 64, 65, 66, 7, 8, 9, 10, 11, 12, 54, 55, 6, 7, 8, 9, 10, 55, 56, 58, 59, 62, 65, 66, 67, 6, 7, 8, 9, 10, 55, 56, 58, 59, 4, 5, 6, 7, 8, 9, 48, 56, 57, 59, 60, 61, 62, 66, 67, 4, 5, 6, 7, 8, 9, 48, 3, 4, 5, 6, 7, 8, 48, 49, 57, 58, 60, 61, 67, 3, 4, 5, 6, 7, 8, 48, 49, 57, 2, 3, 4, 5, 6, 31, 48, 49, 59, 2, 3, 4, 5, 6, 31, 48, 49, 59, 2, 3, 4, 5, 31, 32, 33, 48, 49, 50, 51, 52, 57, 58, 59, 60, 62, 63, 66, 67, 31, 32, 33, 48, 49, 50, 33, 34, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 33, 34, 35, 50, 51, 52, 53, 54, 55, 56, 57, 61, 62, 64, 65, 66, 34, 35, 50, 51, 52, 53, 54, 10, 11, 12, 13, 14, 35, 53, 54, 55, 10, 11, 12, 13, 14, 35, 53, 54, 55, 10, 11, 12, 13, 9, 10, 11, 12, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 66, 67, 9, 10, 11, 12, 7, 8, 9, 50, 51, 52, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 67, 7, 8, 9, 50, 4, 5, 6, 7, 48, 49, 50, 51, 56, 57, 58, 59, 60, 61, 62, 63, 65, 66, 4, 5, 6, 7]
        self.reverse_index2 = [0, 3, 1, 7, 8, 0, 3, 1, 7, 8, 0, 3, 1, 7, 8, 0, 3, 1, 7, 8, 0, 3, 1, 1, 4, 9, 1, 1, 4, 9, 1, 1, 4, 9, 1, 1, 4, 9, 1, 1, 4, 9, 1, 1, 6, 1, 1, 5, 6, 1, 1, 5, 6, 1, 1, 5, 6, 1, 1, 5, 6, 1, 1, 5, 6, 1, 5, 0, 0, 6, 5, 0, 0, 6, 5, 0, 0, 6, 5, 0, 0, 6, 5, 0, 0, 6, 5, 0, 2, 0, 1, 7, 2, 0, 1, 7, 2, 0, 1, 7, 2, 0, 1, 7, 2, 0, 1, 7, 2, 0, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 1, 6, 2, 1, 9, 4, 0, 1, 4, 9, 4, 0, 1, 4, 9, 4, 0, 1, 4, 9, 4, 0, 1, 4, 9, 4, 5, 0, 1, 3, 5, 0, 1, 3, 5, 0, 1, 3, 5, 0, 1, 3, 5, 0, 1, 3, 5, 0, 4, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 4, 4, 0, 0, 4, 4, 0, 3, 0, 0, 5, 3, 0, 0, 5, 3, 0, 0, 5, 3, 0, 0, 5, 3, 0, 0, 5, 3, 0, 3, 1, 0, 4, 9, 3, 1, 0, 4, 9, 3, 1, 0, 4, 9, 3, 1, 0, 4, 9, 3, 1, 6, 1, 0, 2, 6, 1, 0, 2, 6, 1, 0, 2, 6, 1, 0, 2, 6, 1, 0, 2, 6, 1, 7, 1, 0, 2, 7, 1, 0, 2, 7, 1, 0, 2, 7, 1, 0, 2, 7, 1, 0, 2, 7, 1, 6, 1, 1, 4, 6, 1, 1, 4, 6, 1, 1, 4, 6, 1, 1, 4, 6, 1, 1, 4, 6, 1, 5, 1, 0, 6, 5, 1, 0, 6, 5, 1, 0, 6, 5, 1, 0, 6, 5, 1, 0, 6, 5, 1, 3, 0, 0, 9, 3, 0, 0, 9, 3, 0, 0, 9, 3, 0, 0, 9, 3, 0, 0, 9, 3, 0, 3, 1, 7, 2, 8, 3, 1, 7, 2, 8, 3, 1, 7, 2, 8, 3, 1, 7, 2, 8, 3, 1, 0, 3, 9, 0, 4, 4, 8, 6, 0, 3, 9, 0, 4, 4, 8, 6, 0, 3, 9, 0, 4, 4, 3, 8, 0, 0, 6, 5, 7, 9, 7, 3, 8, 0, 0, 6, 5, 7, 9, 7, 3, 8, 0, 0, 7, 4, 1, 1, 6, 6, 5, 7, 9, 5, 7, 4, 1, 1, 6, 6, 5, 7, 9, 5, 7, 4, 8, 4, 1, 0, 9, 6, 4, 7, 6, 8, 8, 4, 1, 0, 9, 6, 4, 7, 6, 8, 8, 4, 9, 6, 0, 4, 2, 7, 9, 6, 5, 5, 9, 9, 6, 0, 4, 2, 7, 9, 6, 5, 5, 9, 4, 1, 6, 9, 3, 8, 5, 6, 9, 9, 6, 4, 1, 6, 9, 3, 8, 5, 6, 9, 9, 6, 0, 1, 4, 8, 7, 5, 7, 9, 8, 5, 0, 1, 4, 8, 7, 5, 7, 9, 8, 5, 0, 1, 7, 6, 0, 1, 4, 7, 5, 6, 6, 9, 7, 6, 0, 1, 4, 7, 5, 6, 6, 9, 7, 6, 8, 3, 5, 0, 0, 9, 6, 5, 7, 8, 3, 5, 0, 0, 9, 6, 5, 7, 8, 3, 5, 0, 8, 3, 1, 4, 0, 8, 4, 5, 8, 3, 1, 4, 0, 8, 4, 5, 8, 3, 1, 4, 0, 8, 9, 1, 1, 9, 1, 2, 8, 4, 7, 2, 8, 7, 9, 1, 1, 9, 1, 2, 8, 4, 7, 2, 8, 8, 0, 0, 6, 6, 8, 6, 8, 8, 8, 0, 0, 6, 6, 8, 6, 8, 8, 8, 0, 0, 5, 0, 0, 9, 9, 9, 9, 5, 0, 0, 9, 9, 9, 9, 5, 0, 0, 9, 9, 9, 9, 5, 4, 1, 2, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 2, 4, 8, 8, 6, 5, 0, 7, 7, 9, 8, 8, 6, 5, 0, 7, 7, 9, 8, 8, 6, 5, 0, 7, 4, 3, 0, 0, 4, 5, 8, 7, 4, 3, 0, 0, 4, 5, 8, 7, 4, 3, 0, 0, 4, 5, 7, 2, 1, 1, 1, 1, 5, 8, 5, 7, 2, 1, 1, 1, 1, 5, 8, 5, 7, 2, 1, 1, 3, 1, 5, 4, 1, 0, 6, 9, 3, 1, 5, 4, 1, 0, 6, 9, 3, 1, 5, 4, 1, 0, 8, 9, 5, 4, 9, 6, 0, 8, 7, 8, 9, 5, 4, 9, 6, 0, 8, 7, 8, 9, 5, 4, 2, 2, 4, 2, 3, 5, 8, 1, 5, 8, 4, 1, 2, 2, 4, 2, 3, 5, 8, 1, 5, 8, 5, 6, 3, 2, 2, 3, 7, 1, 1, 3, 3, 0, 5, 6, 3, 2, 2, 3, 7, 1, 1, 3, 9, 9, 6, 6, 3, 2, 2, 7, 9, 3, 2, 1, 0, 3, 9, 9, 6, 6, 3, 2, 2, 7, 9, 4, 3, 4, 3, 9, 7, 4, 2, 1, 4, 9, 4, 3, 4, 3, 9, 7, 4, 2, 1, 4, 8, 7, 7, 8, 8, 5, 5, 8, 5, 2, 3, 0, 0, 2, 8, 7, 7, 8, 8, 5, 5, 8, 4, 4, 5, 5, 5, 7, 7, 9, 0, 0, 3, 2, 2, 4, 4, 5, 5, 5, 7, 7, 9, 0, 3, 4, 9, 1, 2, 8, 2, 4, 7, 4, 2, 3, 4, 9, 1, 2, 8, 2, 4, 7, 4, 2, 9, 9, 2, 2, 3, 6, 6, 6, 1, 2, 3, 3, 0, 9, 9, 2, 2, 3, 6, 6, 6, 1, 6, 5, 7, 3, 2, 2, 3, 4, 1, 1, 1, 3, 6, 5, 7, 3, 2, 2, 3, 4, 1, 1, 4, 2, 2, 8, 5, 3, 1, 8, 4, 1, 0, 4, 4, 2, 2, 8, 5, 3, 1, 8, 4, 1, 5, 5, 4, 9, 7, 7, 5, 5, 3, 3, 0, 0, 1, 5, 5, 4, 9, 7, 7, 5, 5, 3, 7, 8, 5, 6, 8, 8, 7, 9, 6, 0, 0, 3, 2, 2, 7, 8, 5, 6, 8, 8, 7, 9, 6, 3, 2, 2, 5, 3, 3, 0, 6, 3, 2, 2, 5, 3, 3, 0, 6, 3, 2, 2, 5, 3, 6, 7, 8, 4, 6, 1, 3, 9, 4, 1, 5, 8, 6, 7, 8, 4, 6, 1, 3, 9, 4, 1, 7, 3, 3, 4, 8, 5, 1, 1, 7, 9, 8, 5, 1, 6, 9, 5, 7, 3, 3, 4, 8, 5, 9, 6, 5, 3, 5, 6, 9, 6, 1, 1, 6, 9, 8, 8, 8, 3, 0, 3, 8, 6, 6, 6, 8, 8, 5, 3, 3, 8, 2, 1, 5, 8, 9, 7, 1, 5, 4, 8, 8, 5, 3, 3, 8, 2, 8, 7, 6, 6, 4, 3, 1, 3, 5, 1, 8, 8, 7, 6, 6, 4, 3, 1, 3, 5, 1, 8, 5, 2, 2, 4, 6, 2, 4, 0, 5, 2, 2, 4, 6, 2, 4, 0, 5, 2, 2, 4, 6, 2, 7, 5, 2, 3, 6, 7, 5, 2, 2, 9, 8, 2, 5, 7, 5, 2, 3, 6, 7, 5, 2, 2, 7, 5, 2, 3, 7, 8, 6, 0, 1, 5, 7, 6, 3, 8, 7, 5, 2, 3, 7, 8, 6, 0, 8, 4, 2, 4, 8, 7, 0, 0, 7, 8, 7, 4, 7, 8, 4, 2, 4, 8, 7, 0, 0, 7, 9, 7, 3, 2, 6, 7, 6, 5, 0, 0, 6, 7, 9, 7, 3, 9, 7, 3, 2, 6, 7, 6, 7, 6, 3, 2, 5, 8, 2, 5, 8, 2, 2, 8, 4, 7, 6, 3, 2, 5, 8, 2, 5, 8, 7, 5, 3, 4, 6, 8, 0, 0, 1, 7, 5, 3, 4, 6, 8, 0, 0, 1, 7, 5, 3, 4, 7, 7, 9, 3, 2, 0, 3, 9, 6, 4, 5, 3, 2, 6, 3, 0, 7, 7, 9, 3, 2, 0, 8, 9, 8, 7, 2, 0, 2, 7, 8, 9, 6, 5, 6, 9, 7, 2, 2, 7, 2, 0, 2, 8, 7, 7, 9, 4, 0, 3, 3, 5, 4, 7, 6, 3, 3, 0, 5, 7, 7, 9, 4, 0, 3, 3, 6, 4, 3, 5, 7, 8, 0, 0, 1, 6, 4, 3, 5, 7, 8, 0, 0, 1, 6, 4, 3, 5, 8, 9, 9, 9, 7, 4, 4, 4, 2, 1, 4, 7, 9, 5, 0, 4, 2, 9, 8, 9, 9, 9, 9, 9, 9, 6, 5, 8, 6, 3, 2, 3, 6, 9, 4, 1, 4, 9, 1, 1, 9, 9, 9, 6, 8, 9, 9, 8, 4, 4, 4, 6, 7, 3, 1, 2, 4, 0, 4, 9, 9, 1, 8, 9, 9, 8]
        self.max_len = 22
        
        sfnet_v2 = models.shufflenet_v2_x0_5(pretrained=False)
        net = Pip_sfnetv2(sfnet_v2).to(self.device)
        state_dict = torch.load(weight_path, map_location=self.device)
        net.load_state_dict(state_dict)
        self.net = net
        
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        self.preprocess = transforms.Compose([transforms.ToTensor(), normalize])
        
    def get_ldms(self, ori_image, det_result, det_box_scale = 1.2):
        
        # Bbox 预处理
        det_xmin = det_result[0]
        det_ymin = det_result[1]
        det_width = det_result[2]
        det_height = det_result[3]
        det_xmax = det_xmin + det_width - 1
        det_ymax = det_ymin + det_height - 1

        det_xmin -= int(det_width * (det_box_scale-1)/2)
        det_ymin += int(det_height * (det_box_scale-1)/2)
        det_xmax += int(det_width * (det_box_scale-1)/2)
        det_ymax += int(det_height * (det_box_scale-1)/2)
        
        det_xmin = max(det_xmin, 0)
        det_ymin = max(det_ymin, 0)
        det_xmax = min(det_xmax, ori_image.width-1)
        det_ymax = min(det_ymax, ori_image.height-1)
        det_width = det_xmax - det_xmin + 1
        det_height = det_ymax - det_ymin + 1
        
        # 将框画在图上，画上去之后性能会提升，很玄学，实际使用建议采用copy的方式
        draw = ImageDraw.Draw(ori_image)
        draw.rectangle(((det_xmin, det_ymin), (det_xmax, det_ymax)),fill=None,outline=(255,0,0), width=2)
        
        # 图片裁剪及预处理
        det_crop = ori_image.crop((det_xmin, det_ymin, det_xmax, det_ymax))
        inputs = det_crop.resize((256, 256), resample = 1)
        inputs = self.preprocess(inputs).unsqueeze(0)
        
        inputs = inputs.to(self.device)
        
        # 人脸关键推理
        lms_pred_x, lms_pred_y, lms_pred_nb_x, lms_pred_nb_y, outputs_cls, max_cls = self.forward_pip(self.net, inputs)
        
        # 后处理
        lms_pred = torch.cat((lms_pred_x, lms_pred_y), dim=1).flatten()
        tmp_nb_x = lms_pred_nb_x[self.reverse_index1, self.reverse_index2].view(self.num_ldms, self.max_len)
        tmp_nb_y = lms_pred_nb_y[self.reverse_index1, self.reverse_index2].view(self.num_ldms, self.max_len)
        tmp_x = torch.mean(torch.cat((lms_pred_x, tmp_nb_x), dim=1), dim=1).view(-1,1)
        tmp_y = torch.mean(torch.cat((lms_pred_y, tmp_nb_y), dim=1), dim=1).view(-1,1)
        lms_pred_merge = torch.cat((tmp_x, tmp_y), dim=1).flatten()
        lms_pred = lms_pred.cpu().numpy()
        lms_pred_merge = lms_pred_merge.cpu().numpy()
        
        # 可视化
        image = cv2.cvtColor(np.asarray(ori_image),cv2.COLOR_RGB2BGR)
        for i in range(self.num_ldms):
            x_pred = lms_pred_merge[i*2] * det_width
            y_pred = lms_pred_merge[i*2+1] * det_height
            
            cv2.circle(image, (int(x_pred)+det_xmin, int(y_pred)+det_ymin), 1, (0, 0, 255), 2)
        cv2.imwrite('./test_image_out.jpg', image)
        
        return lms_pred_merge
    
    def forward_pip(self, net, inputs, input_size=256, net_stride=32, num_nb=10):
        net.eval()
        with torch.no_grad():
            
            outputs_cls, outputs_x, outputs_y, outputs_nb_x, outputs_nb_y = net(inputs)
            tmp_batch, tmp_channel, tmp_height, tmp_width = outputs_cls.size()
            assert tmp_batch == 1

            outputs_cls = outputs_cls.view(tmp_batch*tmp_channel, -1)
            max_ids = torch.argmax(outputs_cls, 1)
            max_cls = torch.max(outputs_cls, 1)[0]
            max_ids = max_ids.view(-1, 1)
            max_ids_nb = max_ids.repeat(1, num_nb).view(-1, 1)

            outputs_x = outputs_x.view(tmp_batch*tmp_channel, -1)
            outputs_x_select = torch.gather(outputs_x, 1, max_ids)
            outputs_x_select = outputs_x_select.squeeze(1)
            outputs_y = outputs_y.view(tmp_batch*tmp_channel, -1)
            outputs_y_select = torch.gather(outputs_y, 1, max_ids)
            outputs_y_select = outputs_y_select.squeeze(1)

            outputs_nb_x = outputs_nb_x.view(tmp_batch*num_nb*tmp_channel, -1)
            outputs_nb_x_select = torch.gather(outputs_nb_x, 1, max_ids_nb)
            outputs_nb_x_select = outputs_nb_x_select.squeeze(1).view(-1, num_nb)
            outputs_nb_y = outputs_nb_y.view(tmp_batch*num_nb*tmp_channel, -1)
            outputs_nb_y_select = torch.gather(outputs_nb_y, 1, max_ids_nb)
            outputs_nb_y_select = outputs_nb_y_select.squeeze(1).view(-1, num_nb)

            tmp_x = (max_ids%tmp_width).view(-1,1).float()+outputs_x_select.view(-1,1)
            tmp_y = (max_ids//tmp_width).view(-1,1).float()+outputs_y_select.view(-1,1)
            tmp_x /= 1.0 * input_size / net_stride
            tmp_y /= 1.0 * input_size / net_stride

            tmp_nb_x = (max_ids%tmp_width).view(-1,1).float()+outputs_nb_x_select
            tmp_nb_y = (max_ids//tmp_width).view(-1,1).float()+outputs_nb_y_select
            tmp_nb_x = tmp_nb_x.view(-1, num_nb)
            tmp_nb_y = tmp_nb_y.view(-1, num_nb)
            tmp_nb_x /= 1.0 * input_size / net_stride
            tmp_nb_y /= 1.0 * input_size / net_stride

        return tmp_x, tmp_y, tmp_nb_x, tmp_nb_y, outputs_cls, max_cls

if __name__ == '__main__':
    
    ori_image = Image.open('./test_image.jpg')
    
    
    det_result = [597, 160, 77, 108]
    # [702, 290, 87, 111]
    # [597, 160, 77, 108]
    # [258, 293, 81, 104]
    
    get_ldms = Get_Ldms()
    get_ldms.get_ldms(ori_image, det_result)
    
