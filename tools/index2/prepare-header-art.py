from pathlib import Path
import cv2,numpy as np
root=Path(__file__).resolve().parents[2]
im=cv2.imread(str(root/'assets/faithful/media/fcfdbbb19fa8a366fc216a4b.png'),cv2.IMREAD_UNCHANGED)
bgr=im[:,:,:3];mask=np.zeros(bgr.shape[:2],np.uint8)
boxes=[(88,75,354,93),(790,39,992,54),(58,132,542,214),(58,216,510,273),(61,278,642,310),(77,387,234,421),(276,387,430,421),(475,387,622,421),(330,474,467,499)]
for x1,y1,x2,y2 in boxes:
 region=bgr[y1:y2,x1:x2];bright=np.ones(region.shape[:2],bool)
 mask[y1:y2,x1:x2]=bright.astype(np.uint8)*255
mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
for x1,y1,x2,y2 in [(78,339,123,382),(275,340,319,378),(483,337,508,379),(944,607,1016,632)]:mask[y1:y2,x1:x2]=255
clean=cv2.inpaint(bgr,mask,9,cv2.INPAINT_NS)
smooth=cv2.GaussianBlur(clean,(0,0),12)
feather=cv2.GaussianBlur(mask,(0,0),9).astype(np.float32)/255
clean=(smooth*feather[:,:,None]+clean*(1-feather[:,:,None])).astype(np.uint8)
if im.shape[2]==4:clean=np.dstack([clean,im[:,:,3]])
cv2.imwrite(str(root/'assets/index2/hero-clean.webp'),clean,[cv2.IMWRITE_WEBP_QUALITY,101])

cv2.imwrite(str(root/'assets/index2/hero-clean-mobile.webp'),cv2.resize(clean,(1031,671)),[cv2.IMWRITE_WEBP_QUALITY,101])
