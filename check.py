
import cv2, os, numpy as np
files = sorted(os.listdir('data/frames'))[:20]
for f in files:
    img = cv2.imread(f'data/frames/{f}')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f'{f}: {score:.1f}')