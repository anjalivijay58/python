


import cv2
import numpy as np

def onChange(x):
    pass

def colourPickerTool():
    cv2.namedWindow("colour-picker")
    win = np.ones((512, 512, 3), np.uint8)
    cv2.createTrackbar("Red", "colour-picker", 0, 255, onChange)
    cv2.createTrackbar("Green", "colour-picker", 0, 255, onChange)
    cv2.createTrackbar("Blue", "colour-picker", 0, 255, onChange)
    while True:
        r = cv2.getTrackbarPos("Red", "colour-picker")
        g = cv2.getTrackbarPos("Green", "colour-picker")
        b = cv2.getTrackbarPos("Blue", "colour-picker")
        win[:] = [b, g, r]
        cv2.imshow("colour-picker", win)
        if cv2.waitKey(1) &  0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def getPicInfo():
    def getinfo(event, x, y, flag, param):
           
        print('x: ', x)
        print('y: ', y)
        print('flag: ', flag)
        print('param: ', param)
        
        if event == cv2.EVENT_LBUTTONDOWN :
            
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            cord = '.' + str(x) + ',' + str(y)
            cv2.putText(img, cord, (x, y), font, 1, (75, 255, 42), 1)
            cv2.imshow("lena", img)
            
        if event == cv2.EVENT_RBUTTONDOWN :
            
            b = img[x,y,0]
            g = img[x,y,1]
            r = img[x,y,2]
            
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            text = '.' + str(b) + ',' + str(g) + ',' + str(r)
            print("colour is: ",text)
            cv2.putText(img, text, (x,y), font, 1, (75, 255, 42), 1)
            cv2.imshow("lena", img)

    inp = input(r"Enter file location: ")
    img = cv2.imread(inp)
    cv2.namedWindow("lena")
    cv2.setMouseCallback("lena", getinfo)

    while True:
        
        cv2.imshow("lena", img)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        
    cv2.destroyAllWindows()

def imageBlender():
    samp = np.ones([600,400,3], np.uint8)*255

    cat = input(r"Enter the location of the first image: ")
    pik = input(r"Enter the location of the second image: ")
    cat = cv2.imread(cat)
    pik = cv2.imread(pik)

    cat = cv2.resize(cat, (600,400))
    pik = cv2.resize(pik, (600,400))

    cv2.namedWindow("controller")
    cv2.namedWindow("blender")

    cv2.createTrackbar("switch", "controller", 0, 1, onChange)
    cv2.createTrackbar("blender", "controller", 0, 100, onChange)

    while True:

        s = cv2.getTrackbarPos("switch", "controller")
        blend_val = cv2.getTrackbarPos("blender", "controller")

        cv2.imshow("controller", samp)

        if s == 0:
            res = samp[:] * 0
        else:
            res = cv2.addWeighted(cat, blend_val/100, pik, 1 - blend_val/100, 0)
            print(blend_val/100)
        cv2.imshow("blender", res)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def subtract_image():
    array = np.ones([512, 512], np.uint8) * 255
    img = cv2.imread(r"C:\Users\navee\projects\learn cv2\resources\lena.png", cv2.IMREAD_GRAYSCALE)

    res = 255 - img

    cv2.imshow("Result", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def split_and_merge():
    img = cv2.imread(r"C:\Users\navee\projects\learn cv2\resources\pikachu.jpg")
    img = cv2.resize(img, (300, 250))

    print('shape = ', np.shape(img))
    print('size = ', np.size(img))

    px = img[125, 150, 0]
    print('pixel value:', px)

    b, g, r = cv2.split(img)
    redone1 = cv2.merge((b, r, g))
    redone2 = cv2.merge((r, b, g))
    redone3 = cv2.merge((r, r, g))
    redone4 = cv2.merge((g, r, b))
    redone5 = cv2.merge((b, b, b))

    cv2.imshow("pikachu", img)
    cv2.imshow("brg", redone1)
    cv2.imshow("rbg", redone2)
    cv2.imshow("rrg", redone3)
    cv2.imshow("grb", redone4)
    cv2.imshow("bbb", redone5)

    cv2.imshow("blue", b)
    cv2.imshow("green", g)
    cv2.imshow("red", r)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def maskCreator():
    def nothing(x):
        pass

    cap = cv2.VideoCapture(0)

    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

    while cap.isOpened():
        
        ret, frame = cap.read()
        if ret == True:
            
            frame = cv2.resize(frame, (600,400))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            l_h = cv2.getTrackbarPos("L - H", "Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "Trackbars")
            u_h = cv2.getTrackbarPos("U - H", "Trackbars")
            u_s = cv2.getTrackbarPos("U - S", "Trackbars")
            u_v = cv2.getTrackbarPos("U - V", "Trackbars")

            lower_bound = np.array([l_h, l_s, l_v])
            upper_bound = np.array([u_h, u_s, u_v])

            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            result = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow("Mask", mask)
            cv2.imshow("Result", result)
            key = cv2.waitKey(1)
            if key == 27:
                break
# Add split_and_merge() to the main menu
def main():
    menu = np.zeros((500, 400, 3), dtype=np.uint8)

    while True:
        cv2.putText(menu, "Select an option:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(menu, "1. Colour Picker Tool", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(menu, "2. Picture Info Tool", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(menu, "3. Mask Creator", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(menu, "4. Image Blender", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(menu, "5. Subtract Image", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(menu, "6. Split and Merge", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(menu, "7. Quit", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Menu", menu)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('1'):
            colourPickerTool()
        elif key == ord('2'):
            getPicInfo()
        elif key == ord('3'):
            maskCreator()
        elif key == ord('4'):
            imageBlender()
        elif key == ord('5'):
            subtract_image()
        elif key == ord('6'):
            split_and_merge()
        elif key == ord('7'):
            cv2.destroyAllWindows()
            break

        menu[:] = 0

if __name__ == "__main__":
    main()

