import numpy as np
import cv2 as cv
import sys
import time
import curses


# ascii_chars = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'."""
# ascii_chars = """`                                              .-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""
# ascii_chars = ascii_chars[::-1]
ascii_chars='  █'
# ascii_chars=' .:░▒▓█'
# ascii_chars = '🌝🌕🌔🌓🌒🌑🌚'
# ascii_chars = ascii_chars[::-1]

# ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|"

# contrast = 10
# density = ('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|'
#            '()1{}[]?-_+~<>i!lI;:,"^`\'.            ')
# ascii_chars = density[:-11+contrast]
def pxl_to_char(pxl_value,i):
    global ascii_chars
    brightness = pxl_value/255
    white = ' '*0
    a=white+ascii_chars
    index = int(brightness*len(a))-1
    return a[index]




def run():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    SCALE_FACTOR = 20
    convert_char = np.vectorize(pxl_to_char)
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    i=0
    add=True
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        frame = cv.resize(frame, (int((1920//SCALE_FACTOR)*2),1080//SCALE_FACTOR))
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if add==True:
            i+=1
        else:
            i-=1
        
        output_frame = ""
        for i,row in enumerate(gray):
            ascii_row = convert_char(row,i)[::-1]
            output_frame=output_frame+''.join(map(str, ascii_row))+'\n'
        
        try:
            # stdscr.addstr(0,0,str(i))

            stdscr.addstr(0,0,output_frame)
        except curses.error:
            pass
        # sys.stdout.write(output_frame)
        # stdscr.addstr(output_frame)
        stdscr.refresh()

        # cv.imshow('frame', gray)
        # sys.stdout.flush()
        # time.sleep(1)
        if (i%10)==0:
            add=not add
        if cv.waitKey(1) == ord('q'):
            break
        
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
run()
#cd Documents/personal/ascii_camera/
