## eink-flashcards

A small offline flashcard device. It's a Raspberry Pi Zero with a 2.7" e-ink display running a spaced-repetition study app.

I built it as a dedicated study gadget inspired by Anki. It uses session-based scheduling instead of calendar dates (the Pi Zero has no real-time clock), so it works fully offline.

Not affiliated with Anki / Ankitects. It's just a hobby project inspired by spaced repetition.

## Demo

There are two screens. The start screen shows how many cards are due and waits for you to begin. The study screen shows a word, you press show to reveal the translation, then know or again.

## Hardware
Part	Notes
Raspberry Pi Zero WH	The WH version has pre-soldered GPIO headers, so no soldering needed. A Pi Zero 2 W(H) works too.
Waveshare 2.7" e-Paper HAT	264x176 pixels, black/white. Has 4 built-in buttons.
Power bank	Any USB power bank. The device runs off USB power, no internal battery.
Case (optional)	A 3D-printed enclosure. See notes below.

The HAT plugs directly onto the Pi's 40-pin GPIO header, so there's no wiring.

## Buttons

The four buttons on the Waveshare HAT map to these GPIO pins:

Button	GPIO	Action
KEY1	5	show / start
KEY2	6	know
KEY3	13	again
KEY4	19	exit
Software setup

## On the Pi (Raspberry Pi OS Lite is fine):

bash
# enable SPI for the display
sudo raspi-config   # Interface Options -> SPI -> Enable

# system packages
sudo apt update
sudo apt install -y python3-pip git

# Waveshare e-Paper driver
git clone https://github.com/waveshare/e-Paper.git
cd e-Paper/RaspberryPi_JetsonNano/python
pip3 install . --break-system-packages

# this project
cd ~
git clone https://github.com/deleter81/eink-flashcards.git
cd eink-flashcards
pip3 install -r requirements.txt --break-system-packages

Run it:

bash
python3 main.py

Note on the display driver: this project uses the epd2in7_V2 driver. If your HAT is an older revision you might need epd2in7 instead. Just change the import in display.py.

## Run on boot (autostart)

If you want the device to launch automatically when it gets power, create a systemd service:

bash
sudo nano /etc/systemd/system/flashcards.service
ini
[Unit]
Description=E-ink Flashcards
After=multi-user.target

[Service]
Type=simple
User=deleter
WorkingDirectory=/home/deleter/eink-flashcards
ExecStart=/usr/bin/python3 /home/deleter/eink-flashcards/main.py
Restart=always

[Install]
WantedBy=multi-user.target
bash
sudo systemctl daemon-reload
sudo systemctl enable flashcards.service
sudo systemctl start flashcards.service

Now the device boots straight into study mode.

Testing on your computer

You don't need the Pi to work on the screens. When it runs on a normal computer (no Pi hardware detected), the app saves each screen as a PNG (start_screen.png, main_screen.png, done_screen.png) instead of drawing to the display, and it reads button actions from the keyboard. This makes it easy to tweak the layout before pushing to the device.

## Cards

Cards live in cards.json:

json
{
  "word": "hello",
  "translation": "привіт",
  "language": "en",
  "due": 0,
  "interval": 1,
  "ease": 2.5
}

Here word and translation are the front and back. language is just a tag like en or de. due is how many sessions until it shows again (0 means show now). interval is the current interval in sessions, and ease controls how fast that interval grows (it starts at 2.5).

To add your own words, just edit cards.json.

How the scheduling works

Instead of real dates the app counts study sessions. Each time you finish a session, the due counters tick down.

On know, the interval grows: interval = min(round(interval * ease), 8). On again, it resets: interval = 1 and ease drops by 0.2 (down to a minimum of 1.3), so cards you struggle with come back faster and grow slower after that.

It's the same core idea as SM-2, just decoupled from the calendar so it runs with no clock and no internet.

## Case

The enclosure is a 3D-printed Tamagotchi-style case for the Pi Zero and the Waveshare 2.7" HAT, sourced from Thingiverse. You can print it yourself or order it from a service like PCBWay. I held the components in with double-sided tape (M2.5 screws also work if you have them).
Models used:
- Top shell: https://www.thingiverse.com/thing:4893647
- Bottom: https://www.thingiverse.com/thing:4756381

  
## License

The case models belong to their original authors on Thingiverse under their own licenses. The MIT license here covers only the software in this repo.
