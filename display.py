from PIL import Image, ImageDraw, ImageFont
import sys
import os

ON_PI = os.path.exists('/sys/firmware/devicetree/base/model')

if ON_PI:
    libdir = os.path.join(os.path.expanduser('~'), 'e-Paper', 'RaspberryPi_JetsonNano', 'python', 'lib')
    sys.path.append(libdir)
    from waveshare_epd import epd2in7_V2

font = ImageFont.truetype("DejaVuSans.ttf", 16)
font_small = ImageFont.truetype("DejaVuSans.ttf", 10)
font_large = ImageFont.truetype("DejaVuSans.ttf", 22)

WIDTH = 264
HEIGHT = 176


def draw_start_screen(cards_today=67):
    image = Image.new('1', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=0)
    draw.line([48, 0, 48, HEIGHT], fill=0)
    draw.text((80, 50), "Today's goal:", font=font, fill=0)
    draw.rectangle([100, 90, 164, 120], outline=0)
    draw.text((112, 97), str(cards_today), font=font, fill=0)
    draw.rectangle([0, 0, 48, 44], outline=0, fill=0)
    draw.text((8, 12), "start", font=font_small, fill=255)
    if ON_PI:
        epd = epd2in7_V2.EPD()
        epd.init()
        epd.display(epd.getbuffer(image))
        epd.sleep()
    else:
        image.save("start_screen.png")
        print("Saved start_screen.png")


def draw_main_screen(word="hello", translation="привіт", card_num=11, total=27, show_translation=False):
    image = Image.new('1', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=0)
    draw.line([48, 0, 48, HEIGHT], fill=0)

    draw.rectangle([0, 0, 48, 44], outline=0, fill=0)
    draw.text((8, 12), "show", font=font_small, fill=255)
    draw.rectangle([0, 44, 48, 88], outline=0, fill=0)
    draw.text((8, 58), "know", font=font_small, fill=255)
    draw.rectangle([0, 88, 48, 132], outline=0, fill=0)
    draw.text((5, 102), "again", font=font_small, fill=255)
    draw.rectangle([0, 132, 48, HEIGHT-1], outline=0, fill=0)
    draw.text((8, 148), "exit", font=font_small, fill=255)

    draw.line([0, 44, 48, 44], fill=255, width=2)
    draw.line([0, 88, 48, 88], fill=255, width=2)
    draw.line([0, 132, 48, 132], fill=255, width=2)

    draw.text((60, 20), word, font=font_large, fill=0)

    if show_translation:
        draw.line([55, 70, WIDTH-5, 70], fill=0)
        draw.text((60, 80), translation, font=font, fill=0)

    draw.text((60, 150), f"{card_num}/{total}", font=font_small, fill=0)

    if ON_PI:
        epd = epd2in7_V2.EPD()
        epd.init()
        epd.display(epd.getbuffer(image))
        epd.sleep()
    else:
        image.save("main_screen.png")
        print("Saved main_screen.png")

def draw_done_screen():
    image = Image.new('1', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=0)
    draw.line([48, 0, 48, HEIGHT], fill=0)

    draw.rectangle([0, 132, 48, HEIGHT - 1], outline=0, fill=0)
    draw.text((8, 148), "exit", font=font_small, fill=255)

    draw.text((80, 70), "Done!", font=font_large, fill=0)
    draw.text((60, 110), "Cards saved.", font=font, fill=0)
    if ON_PI:
        epd = epd2in7_V2.EPD()
        epd.init()
        epd.display(epd.getbuffer(image))
        epd.sleep()
    else:
        image.save("done_screen.png")
        print("Saved done_screen.png")