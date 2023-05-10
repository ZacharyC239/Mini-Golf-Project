from math import sqrt
from PIL import ImageTk, Image
import pygame as py
import json
from tkinter import Canvas, Tk
import tkinter as tk
from random import randint

# variable list
currentScore = "0"
xcordone = 0
rect_object = ""
xcordtwo = 0
circlex = 0
circley = 0
holex = 0
holey = 0
colorIndex = 0
gamelevel = 1
list1 = []
list2 = []
colorList = []
poslist = []
text = ""
ballimage = ""
ballbool = True
running = True


# constant values
WIDTH = 980
HEIGHT = 500
MAX_VELOCITY = 250

# import pygame libraries, modify screen size and display title
py.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Mini Golf")

# load image files
imp = py.image.load("Golfcourse.png")
imgolfflag = py.image.load(r"C:\Users\zacou\OneDrive\School files\CS Files\Python files\CS1Py\Mini Golf Python\golf_flag.png")
coin = py.image.load("coin.png")
ball = ""

# organize all ball image files into list [colorlist]
with open("golf_balls.json","r") as golfBalls:
    balls = json.load(golfBalls)
    colorList = [balls[key] for key in balls]

# starting window for selecting ball color and instructions
def startUpWindow():
    global xcordone,xcordtwo,rect_object,colorIndex,ballimage,ball
    root = Tk()
    root.title("select color")
    canvas = Canvas(root)
    canvas.pack()
    xcordone = 5
    xcordtwo = 40
    rect_object = canvas.create_rectangle(xcordone,25,xcordtwo,60, outline= 'black', width=3)
    imgLock = ImageTk.PhotoImage(Image.open("lock.png"))
    imgBlue = ImageTk.PhotoImage(Image.open("blueball.png"))
    imgRed = ImageTk.PhotoImage(Image.open("redball.png"))
    imgGreen = ImageTk.PhotoImage(Image.open("greenball.png"))
    imgClock = ImageTk.PhotoImage(Image.open("clockball.png"))
    imgEarth = ImageTk.PhotoImage(Image.open("earthball.png"))
    imgPizza = ImageTk.PhotoImage(Image.open("pizzaball.png"))
    titleLabel = tk.Label(root,text="Use the arrow keys to select a ball and hit enter to start the game").place(relx=0,rely=0)
    blueLabel = tk.Label(root,image=imgBlue).place(relx=.02,rely=.1)
    redLabel = tk.Label(root,image=imgRed).place(relx=.12,rely=.1)
    greenLabel = tk.Label(root,image=imgGreen).place(relx=.22,rely=.1)
    clockLabel = tk.Label(root,image=imgClock).place(relx=.32,rely=.1)
    earthLabel = tk.Label(root,image=imgEarth).place(relx=.42,rely=.1)
    pizzaLabel = tk.Label(root,image=imgPizza).place(relx=.52,rely=.1)
    with open("stroke.json","r") as file:
        states = json.load(file)
        if not states["state"][0]["clockball.png"][0]:
            lockLabel1 = tk.Label(root,image=imgLock)
            lockLabel1.place(relx=.32,rely=.1)
        if not states["state"][0]["earthball.png"][0]:
            lockLabel2 = tk.Label(root,image=imgLock)
            lockLabel2.place(relx=.42,rely=.1)
        if not states["state"][0]["pizzaball.png"][0]:
            lockLabel3 = tk.Label(root,image=imgLock)
            lockLabel3.place(relx=.52,rely=.1)
    # move the selector left
    def move_left(event):
        global xcordone,xcordtwo,rect_object,colorIndex
        if colorIndex>0:
            xcordone -= 38
            xcordtwo -= 38
            colorIndex-=1
            canvas.delete(rect_object)
            rect_object = canvas.create_rectangle(xcordone,25,xcordtwo,60, outline= 'black', width=3)
    # move the selector right
    def move_right(event):
        global xcordone,xcordtwo,rect_object,colorIndex
        xcordone += 38
        xcordtwo += 38
        colorIndex+=1
        canvas.delete(rect_object)
        rect_object = canvas.create_rectangle(xcordone,25,xcordtwo,60, outline= 'black', width=3)
    # updates ball file and destroys tkinter window
    def startGame(event):
        global colorIndex,ballimage,ball
        ballimage = colorList[colorIndex]
        with open("stroke.json","r") as file:
            states = json.load(file)
            if states["state"][0][ballimage][0]:
                ball = py.image.load(ballimage)
                root.destroy()
            else:
                with open("stroke.json","r") as file:
                    coinfile = json.load(file)
                    coinamount = coinfile["coins"][0]["coin_number"]
                    coinlimit = coinfile["state"][0][ballimage][1]
                print(coinamount,coinlimit)
                if coinamount >= coinlimit:
                    newcoin = coinamount - coinlimit
                    coinfile["coins"][0]["coin_number"] = newcoin
                    coinfile["state"][0][ballimage][0] = True
                    with open("stroke.json","w") as writefile:
                        json.dump(coinfile,writefile)
                    if ballimage == "clockball.png":
                        lockLabel1.after(1,lockLabel1.destroy())
                    if ballimage == "earthball.png":
                        lockLabel2.after(1,lockLabel2.destroy())
                    if ballimage == "pizzaball.png":
                        lockLabel3.after(1,lockLabel3.destroy())
    root.bind("<Left>",move_left)
    root.bind("<Right>",move_right)
    root.bind("<Return>",startGame)
    root.mainloop()

# add stroke counter, coin counter to screen, lowest recorded score, and background
def displayInformation():
    py.draw.rect(screen,"white",(0,0,500,30))
    txtfont = py.font.SysFont("Arial",30)
    txt = txtfont.render("Strokes: "+currentScore,True,"black")
    screen.blit(txt, (0,0))
    with open("stroke.json","r") as file:
        low = json.load(file)
    lowest = low["scores"][0]["lowest"]
    highStroke = txtfont.render("Lowest Score: " + str(lowest),True,"black")
    screen.blit(highStroke, (300,0))
    with open("stroke.json","r") as file:
        info = json.load(file)
    coins = info["coins"][0]["coin_number"]
    coincount = txtfont.render(str(coins),True,"black")
    screen.blit(coincount, (160,0))
    screen.blit(coin,(130,6))
    levelcount = txtfont.render("Level: " + str(gamelevel),True,"black")
    screen.blit(levelcount,(190,0))
# ends the game after all levels are complete
def endGame():
    screen.blit(imp,(0,0))
    displayInformation()
    py.display.update()
    with open("stroke.json","r") as file:
        lowest = json.load(file)
    if lowest["scores"][0]["lowest"] > int(currentScore) or lowest["scores"][0]["lowest"] == 0:
        lowest["scores"][0]["lowest"] = int(currentScore)
        with open("stroke.json","w") as writeFile:
            json.dump(lowest,writeFile)
    displayInformation()
    txtfont = py.font.SysFont("Arial",30)
    txt = txtfont.render("GAME OVER close the window and reload the game",True,"black")
    screen.blit(txt, (200,200))
# finds data for next level and resets most variables
def restartGame():
    global circlex, circley, holex, holey, list1,list2, poslist
    with open("golflevels.json","r") as file:
        levels = json.load(file)
        for x in levels["golflevel"]:
            if x["level"] == gamelevel:
                circlex = x["ballpos"][0]
                circley = x["ballpos"][1]
                holex = x["holepos"][0]
                holey = x["holepos"][1]
                list1 = x["obstaclestart"]
                list2 = x["obstacleend"]
                screen.blit(imp, (0, 0))
                for a in range(len(list1)):
                    py.draw.rect(screen,"yellow",py.Rect(list1[a][0],list1[a][1],list2[a][0],list2[a][1]))
                break
        screen.blit(ball,(circlex,circley))
        py.draw.circle(screen,"black",(holex,holey),17.5)
        screen.blit(imgolfflag, (holex - 10,holey - 50))
        displayInformation()
        poslist.clear()
        coinamount = randint(0,5)
        for r in range(coinamount):
            randxpos = randint(25,955)
            randypos = randint(85,475)
            poslist.append([randxpos,randypos])
            screen.blit(coin,(randxpos,randypos))
        py.display.update()
# code segment for event handeling
def loadGame():
    global running, circlex, circley, velocity, ballbool, text, currentScore, ball, colorIndex, colorIndex, poslist, coin, holex, holey, gamelevel
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                py.quit()

            # check for mouse click
            if event.type == py.MOUSEBUTTONDOWN:
                py.mouse.set_pos(circlex+12,circley+12)
                initialXpos = py.mouse.get_pos()[0]
                initialYpos = py.mouse.get_pos()[1]
            
            # check for mouse release
            if event.type == py.MOUSEBUTTONUP:
                displayInformation()
                currentScore = int(currentScore)
                currentScore+=1
                currentScore = str(currentScore)
                displayInformation()
                mousex = py.mouse.get_pos()[0]
                mousey = py.mouse.get_pos()[1]
                distancex = initialXpos - mousex
                distancey = initialYpos - mousey
                velocity = sqrt(pow(distancex,2)+pow(distancey,2))
                if velocity > MAX_VELOCITY:
                    velocity = MAX_VELOCITY
                
                # check if ball is near hole
                # will clear the board and add the next level
                def check_hole(cx,cy,hx,hy,velocity):
                    global gamelevel
                    if abs(cx - hx) <= 20 and abs(cy - hy) <= 20 and velocity <= 10:
                        gamelevel+=1
                        if gamelevel != 10:
                            restartGame()
                            return True
                    if gamelevel == 10:
                        endGame()
                        return True
                    return False

                # check if ball is near perimeter
                # change the direction of the ball
                def check_walls(dist,circ,meas):
                    if circ+dist*.1 >= meas:
                        return dist*-1
                    if circ+dist*.1 <= 1:
                        return dist*-1
                    return dist

                # check if ball is in a sand pit
                # reduce the speed while in the bondaries
                def check_sand_pit(circx,circy):
                    for x in range(len(list1)):
                        # check if circle is in rectangle
                        if circx >= list1[x][0] and circx <= list1[x][0] + list2[x][0] and circy >= list1[x][1] and circy <= list1[x][1] + list2[x][1]:
                            return True
                    return False
                # check if the ball collides with coin
                # writes to json file
                def check_coin_collide(circx,circy,poslist):
                    for x in poslist:
                        if abs(x[0] - circx) <= 25 and abs(x[1] - circy) <= 25:
                            poslist.remove(x)
                            with open("stroke.json","r") as file:
                                getcoins = json.load(file)
                            coin = getcoins["coins"][0]['coin_number']
                            coin+=1
                            getcoins["coins"][0]["coin_number"] = coin
                            with open("stroke.json","w") as file:
                                json.dump(getcoins,file)
                breakTrue = False

                # ball movement
                while velocity >= 0.01:
                    # track smaller units without impacting performance
                    for x in range(25):
                        check_coin_collide(circlex,circley,poslist)
                        if check_hole(circlex,circley,holex,holey,velocity):
                            breakTrue = True
                            break
                        distancex = check_walls(distancex,circlex,WIDTH-12.5)
                        distancey = check_walls(distancey,circley,HEIGHT-12.5)
                        if check_sand_pit(circlex,circley):
                            velocity/=1.75
                        circlex+=distancex*0.04
                        circley+=distancey*0.04
                        screen.blit(ball,(circlex,circley))
                        py.display.update()
                    if breakTrue:
                        break
                    velocity/=2
                    distancex/=1.2
                    distancey/=1.2
                    # update screen to hide ball path
                    screen.blit(imp, (0, 0))
                    for a in range(len(list1)):
                        py.draw.rect(screen,"yellow",py.Rect(list1[a][0],list1[a][1],list2[a][0],list2[a][1]))
                    screen.blit(ball,(circlex,circley))
                    py.draw.circle(screen,"black",(holex,holey),17.5)
                    screen.blit(imgolfflag, (holex - 10,holey - 50))
                    for x in poslist:
                        screen.blit(coin,(x[0],x[1]))
                    displayInformation()
                if gamelevel == 9:
                    screen.blit(imp,(0,0))
                    displayInformation()
                    for a in range(2):
                        py.draw.rect(screen,"yellow",py.Rect(randint(100,500),randint(100,300),randint(20,200),randint(20,200)))
                    for x in poslist:
                            screen.blit(coin,(x[0],x[1]))
                    holex = randint(100,700)
                    holey = randint(100,400)
                    py.draw.circle(screen,"black",(holex,holey),17.5)
                    screen.blit(imgolfflag, (holex - 10,holey - 50))
                    py.display.update()
                screen.blit(ball,(circlex,circley))
                py.display.flip()

# start the game
if __name__ == "__main__":
    startUpWindow()
    restartGame()
    loadGame()