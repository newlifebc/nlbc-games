from PIL import Image, ImageDraw, ImageFont
import colorsys
import csv
import textwrap

filename_nouns = '04-Nouns.csv'
filename_adjectives = '04-Adjectives.csv'
filename_names = '04-Authors.csv'
filename_logo = 'nlbc_logo-1500.png'

nouns = []
adjectives = []
names = []
# with open('some.csv', newline='') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)
with open(filename_nouns, newline='',encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) #skip header
    for row in reader:
        nouns.append(row)

with open(filename_adjectives, newline='',encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) #skip header
    for row in reader:
        adjectives.append(row)

with open(filename_names, newline='',encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) #skip header
    for row in reader:
        names.append(row)


def IntelliDraw(drawer,text,font,containerWidth):
    #https://mail.python.org/pipermail/image-sig/2004-December/003064.html
    words = text.split()  
    lines = [] # prepare a return argument
    lines.append(words) 
    finished = False
    line = 0
    while not finished:
        thistext = lines[line]
        newline = []
        innerFinished = False
        while not innerFinished:
            #print 'thistext: '+str(thistext)
            if drawer.textsize(' '.join(thistext),font)[0] > containerWidth:
                # this is the heart of the algorithm: we pop words off the current
                # sentence until the width is ok, then in the next outer loop
                # we move on to the next sentence. 
                newline.insert(0,thistext.pop(-1))
            else:
                innerFinished = True
        if len(newline) > 0:
            lines.append(newline)
            line = line + 1
        else:
            finished = True
    tmp = []        
    for i in lines:
        tmp.append( ' '.join(i) )
    lines = tmp
    w = 0
    h = 0
    for line in lines:
        (width,height) = drawer.textsize(line,font)
        w = max(w,width)
        h += height
    return (lines,w,h)


def imgTextCentered(msg, font=ImageFont.load_default(), fill="black",wrapWidth=100):
    # lines = textwrap.wrap(msg, width=wrapWidth)
    #https://stackoverflow.com/questions/1970807/center-middle-align-text-with-pil
    
    im = Image.new('RGB', (200,200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    #w,h = draw.textsize(msg,font=font)

    lines,wmax,hmax = IntelliDraw(draw,msg,font,wrapWidth)
    print([wmax,hmax,len(lines),lines])
    #w = wrapWidth
    #h = 2*h*(len(lines))
    
    # current_h, pad = 50, 10
    # for line in lines:
    #     w, h = draw.textsize(line, font=font)
    #     # draw.text(((MAX_W - w) / 2, current_h), line, font=font)
    #     current_h += h + pad
    # h = current_h

    im = Image.new("RGBA", (wmax,hmax), (0,0,0,0))
    draw = ImageDraw.Draw(im)
    #draw.text((0,0), msg, fill=fill, font=font)
    # draw.multiline_text((0,0), lines[0], fill=fill, font=font)
    current_h, pad = 0, 0
    for line in lines:
        w, h = draw.textsize(line, font=font)
        draw.text(((wmax - w) / 2, current_h), line, fill=fill, font=font)
        current_h += h + pad

    return im

def rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius)
        ],
        fill=fill,
        outline=outline
    )
    self.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1])
        ],
        fill=fill,
        outline=outline
    )
    self.pieslice([upper_left_point, (upper_left_point[0] + corner_radius * 2, upper_left_point[1] + corner_radius * 2)],
        180,
        270,
        fill=fill,
        outline=outline
    )
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, bottom_right_point[1] - corner_radius * 2), bottom_right_point],
        0,
        90,
        fill=fill,
        outline=outline
    )
    self.pieslice([(upper_left_point[0], bottom_right_point[1] - corner_radius * 2), (upper_left_point[0] + corner_radius * 2, bottom_right_point[1])],
        90,
        180,
        fill=fill,
        outline=outline
    )
    self.pieslice([(bottom_right_point[0] - corner_radius * 2, upper_left_point[1]), (bottom_right_point[0], upper_left_point[1] + corner_radius * 2)],
        270,
        360,
        fill=fill,
        outline=outline
    )
ImageDraw.rounded_rectangle = rounded_rectangle


#noun color
purple = (199,220,180)
purple_light = (199,40,240)

#adjective color
green = (55,220,180)
green_light = (55,40,240)

#instruction color
red = (0,220,180)
red_light = (0,40,240)

light = (0,0,255)
lightRGB = (220,220,220)
dark = (0,0,0)

sf = 3

CARD_WIDTH_300DPI = 747
CARD_HEIGHT_300DPI = 1122
CARD_WIDTH_HIGH_DPI = 747*sf
CARD_HEIGHT_HIGH_DPI = 1122*sf

heights = [120*sf,120*sf,10*sf]
widths = [1200*sf,375*sf,375*sf]
fontSizes = [60*sf,24*sf,36*sf,18*sf]
fnts = []
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[0]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[1]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[2]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[3]))



edgeOffset = 80*sf
cornerRadius = 25*sf


# for noun in nouns:
# for i in range(len(nouns)):
for i in range(0):
    noun = nouns[i]
    img = Image.new('HSV', (CARD_WIDTH_HIGH_DPI, CARD_HEIGHT_HIGH_DPI), color = purple)
    
    d = ImageDraw.Draw(img)
    ImageDraw.rounded_rectangle(d,[(edgeOffset,edgeOffset),(CARD_WIDTH_HIGH_DPI-edgeOffset,CARD_HEIGHT_HIGH_DPI-edgeOffset)], cornerRadius, fill=light, outline=None)
    ImageDraw.rounded_rectangle(d,[(edgeOffset*2.1,edgeOffset*1.25),(CARD_WIDTH_HIGH_DPI-edgeOffset*2.1,CARD_HEIGHT_HIGH_DPI-edgeOffset*1.25)], cornerRadius, fill=purple_light, outline=None)
    
    # d.text((10*sf,10*sf), "Hello world", font=fnt, fill=dark)
    cardId = noun[0]+'-'+noun[1]+'-'+noun[2].zfill(2)
    versionId = 'v1.0'
    Title_EN = noun[3]
    BCV_EN = noun[4]
    Verse_EN = noun[5]
    Title_KR = noun[6]
    BCV_KR = noun[7]
    Verse_KR = noun[8]

    tim = imgTextCentered(Title_EN,fnts[0],dark,widths[0])
    tim = tim.rotate(90, expand=1)
    sx, sy = tim.size
    # px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), 400-int(sy/2)
    px, py = heights[0]-int(sx/2), int((CARD_HEIGHT_HIGH_DPI-sy)/2)
    img.paste(tim, (px, py, px + sx, py + sy), tim)

    tim = imgTextCentered(Verse_EN,fnts[1],dark,widths[1])
    tim = tim.rotate(0, expand=1)
    sx, sy = tim.size
    px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[1]
    # px, py = heights[0]-int(sx/2), int((CARD_HEIGHT_HIGH_DPI-sy)/2)
    img.paste(tim, (px, py, px + sx, py + sy), tim)
    lasty = py + sy

    tim = imgTextCentered(BCV_EN,fnts[2],dark,widths[2])
    tim = tim.rotate(0, expand=1)
    sx, sy = tim.size
    px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[2]+lasty
    # px, py = heights[0]-int(sx/2), int((CARD_HEIGHT_HIGH_DPI-sy)/2)
    img.paste(tim, (px, py, px + sx, py + sy), tim)



    tim = imgTextCentered(Title_KR,fnts[0],dark,widths[0])
    tim = tim.rotate(-90, expand=1)
    sx, sy = tim.size
    # px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), 400-int(sy/2)
    px, py = CARD_WIDTH_HIGH_DPI-heights[0]-int(sx/2), int((CARD_HEIGHT_HIGH_DPI-sy)/2)
    img.paste(tim, (px, py, px + sx, py + sy), tim)

    tim = imgTextCentered(Verse_KR,fnts[1],dark,widths[1])
    tim = tim.rotate(180, expand=1)
    sx, sy = tim.size
    px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), CARD_HEIGHT_HIGH_DPI-heights[1]-sy
    # px, py = heights[0]-int(sx/2), int((CARD_HEIGHT_HIGH_DPI-sy)/2)
    img.paste(tim, (px, py, px + sx, py + sy), tim)
    lasty = py

    tim = imgTextCentered(BCV_KR,fnts[2],dark,widths[2])
    tim = tim.rotate(180, expand=1)
    sx, sy = tim.size
    px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), lasty-heights[2]-sy
    # px, py = heights[0]-int(sx/2), int((CARD_HEIGHT_HIGH_DPI-sy)/2)
    img.paste(tim, (px, py, px + sx, py + sy), tim)



    tim = imgTextCentered(cardId+' '+versionId,fnts[3],lightRGB,500)
    tim = tim.rotate(0, expand=1)
    sx, sy = tim.size
    px, py = CARD_WIDTH_HIGH_DPI-sx-edgeOffset-10, CARD_HEIGHT_HIGH_DPI-sy-edgeOffset+18*sf+10
    img.paste(tim, (px, py, px + sx, py + sy), tim)





    img = img.convert('RGB')
    img_resized = img.resize((CARD_WIDTH_300DPI,CARD_HEIGHT_300DPI), Image.ANTIALIAS)
    img_resized.save(cardId+'.png')







heights = [150*sf,30*sf]
widths = [375*sf,375*sf]
fontSizes = [60*sf,30*sf,18*sf]
fnts = []
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[0]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[1]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[2]))


# for adjective in adjectives:
# for i in range(len(adjectives)):
for i in range(0):
    adjective = adjectives[i]
    img = Image.new('HSV', (CARD_WIDTH_HIGH_DPI, CARD_HEIGHT_HIGH_DPI), color = green)
    
    d = ImageDraw.Draw(img)
    ImageDraw.rounded_rectangle(d,[(edgeOffset,edgeOffset),(CARD_WIDTH_HIGH_DPI-edgeOffset,CARD_HEIGHT_HIGH_DPI-edgeOffset)], cornerRadius, fill=light, outline=None)
    ImageDraw.rounded_rectangle(d,[(edgeOffset*2.1,edgeOffset*1.25),(CARD_WIDTH_HIGH_DPI-edgeOffset*2.1,CARD_HEIGHT_HIGH_DPI-edgeOffset*1.25)], cornerRadius, fill=green_light, outline=None)
    
    # d.text((10*sf,10*sf), "Hello world", font=fnt, fill=dark)
    cardId = adjective[0]+'-'+adjective[1]+'-'+adjective[2].zfill(2)
    versionId = 'v1.0'
    Title_EN = adjective[3]
    Syn_EN = (adjective[4]).split(';')
    Title_KR = adjective[5]
    Syn_KR = (adjective[6]).split(';')


    tim = imgTextCentered(Title_EN,fnts[0],dark,widths[0])
    tim = tim.rotate(0, expand=1)
    sx, sy = tim.size
    px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[0]
    img.paste(tim, (px, py, px + sx, py + sy), tim)
    lasty = py + sy

    for j in range(len(Syn_EN)-1):
        syn = Syn_EN[j]
        tim = imgTextCentered(syn,fnts[1],dark,widths[1])
        tim = tim.rotate(0, expand=1)
        sx, sy = tim.size
        px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[1]+lasty
        img.paste(tim, (px, py, px + sx, py + sy), tim)
        lasty = lasty - heights[1]+sy+120




    tim = imgTextCentered(Title_KR,fnts[0],dark,widths[0])
    tim = tim.rotate(180, expand=1)
    sx, sy = tim.size
    px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), CARD_HEIGHT_HIGH_DPI-heights[0]-sy
    img.paste(tim, (px, py, px + sx, py + sy), tim)
    lasty = py

    for j in range(len(Syn_KR)-1):
        syn = Syn_KR[j]
        tim = imgTextCentered(syn,fnts[1],dark,widths[1])
        tim = tim.rotate(180, expand=1)
        sx, sy = tim.size
        px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), lasty-heights[1]-sy
        img.paste(tim, (px, py, px + sx, py + sy), tim)
        lasty = lasty + heights[1] - sy-120



    tim = imgTextCentered(cardId+' '+versionId,fnts[2],lightRGB,500)
    tim = tim.rotate(0, expand=1)
    sx, sy = tim.size
    px, py = CARD_WIDTH_HIGH_DPI-sx-edgeOffset-10, CARD_HEIGHT_HIGH_DPI-sy-edgeOffset+18*sf+10
    img.paste(tim, (px, py, px + sx, py + sy), tim)





    img = img.convert('RGB')
    img_resized = img.resize((CARD_WIDTH_300DPI,CARD_HEIGHT_300DPI), Image.ANTIALIAS)
    # img_resized.save('test.png')
    img_resized.save(cardId+'.png')








heights = [120*sf,10*sf,10*sf]
widths = [375*sf,375*sf,375*sf]
fontSizes = [40*sf,24*sf,24*sf,18*sf]
fnts = []
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[0]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[1]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[2]))
fnts.append(ImageFont.truetype('malgun.ttf', fontSizes[3]))


Title_EN = "How to Play"
Title_KR = "게임 방법"
instructions_EN = "Each player receives 5 purple noun cards. One player is chosen as judge. The judge chooses one green adjective card. The other players must choose a purple card that best matches the green card. The judge selects the best purple card. Another player becomes a judge in the next round."
instructions_KR = "각 플레이어는 5 개의 보라색 명사 카드를받습니다. 한 명의 선수가 판사로 선택됩니다. 판사는 녹색 형용사 카드 하나를 선택합니다. 다른 플레이어는 녹색 카드와 가장 잘 어울리는 보라색 카드를 선택해야합니다. 판사가 보라색 카드를 선택합니다. 다른 플레이어는 다음 라운드에서 판사가됩니다."

names_EN = 'Created by: '
names_KR = '만든 사람 : '
for i in range(len(names)):
    names_EN = names_EN + names[i][0] + ', '
    names_KR = names_KR + names[i][1] + ', '

names_EN = names_EN[:-2]
names_KR = names_KR[:-2]
cardId = "04-I-01"
versionId = 'v1.0'


img = Image.new('HSV', (CARD_WIDTH_HIGH_DPI, CARD_HEIGHT_HIGH_DPI), color = red)

d = ImageDraw.Draw(img)
ImageDraw.rounded_rectangle(d,[(edgeOffset,edgeOffset),(CARD_WIDTH_HIGH_DPI-edgeOffset,CARD_HEIGHT_HIGH_DPI-edgeOffset)], cornerRadius, fill=light, outline=None)
ImageDraw.rounded_rectangle(d,[(edgeOffset*2.1,edgeOffset*1.25),(CARD_WIDTH_HIGH_DPI-edgeOffset*2.1,CARD_HEIGHT_HIGH_DPI-edgeOffset*1.25)], cornerRadius, fill=red_light, outline=None)





tim = imgTextCentered(Title_EN,fnts[0],dark,widths[0])
tim = tim.rotate(0, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[0]
img.paste(tim, (px, py, px + sx, py + sy), tim)
lasty = py + sy

tim = imgTextCentered(instructions_EN,fnts[1],dark,widths[1])
tim = tim.rotate(0, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[1]+lasty
img.paste(tim, (px, py, px + sx, py + sy), tim)
lasty = py + sy

tim = imgTextCentered(names_EN,fnts[2],dark,widths[2])
tim = tim.rotate(0, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[2]+lasty
img.paste(tim, (px, py, px + sx, py + sy), tim)




tim = imgTextCentered(Title_KR,fnts[0],dark,widths[0])
tim = tim.rotate(180, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), CARD_HEIGHT_HIGH_DPI-heights[0]-sy
img.paste(tim, (px, py, px + sx, py + sy), tim)
lasty = py


tim = imgTextCentered(instructions_KR,fnts[1],dark,widths[1])
tim = tim.rotate(180, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), lasty-heights[1]-sy
img.paste(tim, (px, py, px + sx, py + sy), tim)
lasty = py

tim = imgTextCentered(names_KR,fnts[2],dark,widths[2])
tim = tim.rotate(180, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), lasty-heights[2]-sy
img.paste(tim, (px, py, px + sx, py + sy), tim)
lasty = py



tim = imgTextCentered(cardId+' '+versionId,fnts[3],lightRGB,500)
tim = tim.rotate(0, expand=1)
sx, sy = tim.size
px, py = CARD_WIDTH_HIGH_DPI-sx-edgeOffset-10, CARD_HEIGHT_HIGH_DPI-sy-edgeOffset+18*sf+10
img.paste(tim, (px, py, px + sx, py + sy), tim)



img = img.convert('RGB')
img_resized = img.resize((CARD_WIDTH_300DPI,CARD_HEIGHT_300DPI), Image.ANTIALIAS)
# img_resized.save('test.png')
img_resized.save(cardId+'.png')
















heights = [120*sf]
widths = [500*sf]
fontSizes = [60*sf]
fnts = []
fnts.append(ImageFont.truetype('malgunbd.ttf', fontSizes[0]))


Title_EN = "Grapes 2 Podo"
Title_KR = "그레이프스2포도"

logo = Image.open("nlbc_logo-1500.png")
img = Image.new('HSV', (CARD_WIDTH_HIGH_DPI, CARD_HEIGHT_HIGH_DPI), color = green)

d = ImageDraw.Draw(img)
ImageDraw.rounded_rectangle(d,[(edgeOffset,edgeOffset),(CARD_WIDTH_HIGH_DPI-edgeOffset,CARD_HEIGHT_HIGH_DPI-edgeOffset)], cornerRadius, fill=light, outline=None)

sx, sy = logo.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2),int((CARD_HEIGHT_HIGH_DPI-sy)/2)
print(logo.size)
img.paste(logo, ( px,py,px+sx,py+sy) )

tim = imgTextCentered(Title_EN,fnts[0],dark,widths[0])
tim = tim.rotate(0, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), heights[0]
img.paste(tim, (px, py, px + sx, py + sy), tim)




tim = imgTextCentered(Title_KR,fnts[0],dark,widths[0])
tim = tim.rotate(180, expand=1)
sx, sy = tim.size
px, py = int((CARD_WIDTH_HIGH_DPI-sx)/2), CARD_HEIGHT_HIGH_DPI-heights[0]-sy
img.paste(tim, (px, py, px + sx, py + sy), tim)
lasty = py




img = img.convert('RGB')
img_resized = img.resize((CARD_WIDTH_300DPI,CARD_HEIGHT_300DPI), Image.ANTIALIAS)
img_resized.save('04-A-Back.png')
# img_resized.save(cardId+'.png')