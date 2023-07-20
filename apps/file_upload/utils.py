import cv2

def get_filtered_image(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (100, 100)
        elif width > 200 and width < 500:
            k = (25, 25)
        else:
            k = (25, 25)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'BINARY':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'INVERT':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)
    return filtered
