from PIL import Image, ImageDraw

# text file with seismic data grabbed from:
# https://service.iris.edu/irisws/timeseries/1/query?net=CC&sta=SEP&loc=--&cha=BHE&start=2023-09-29T00:00:00&end=2023-09-30T00:00:00&demean=true&format=ascii1
DATA_FILE = "seis.dat"

# Colors
BLACK = 0
GRAY1 = 85
GRAY2 = 170
WHITE = 255

# MagTag is 296x128 pixels
WIDTH = 128   # 296
HEIGHT = 296  # 128
NN = 8        # pick a factor of HEIGHT
HH = HEIGHT // NN

# Add banded background
BANDED_BG = False

# Create image draw
img = Image.new("L", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
draw.rectangle([(0,0), (WIDTH, HEIGHT)], fill=WHITE)

# Draw background color bars
if BANDED_BG:
    GRAYS = (GRAY1, WHITE, GRAY2)
    for i, y in enumerate(range(0, HEIGHT, HH)):
        draw.rectangle([(0, y), (WIDTH, y+HH)], fill=GRAYS[i%3])

# Read data
data = []
with open(DATA_FILE, "r") as file:
    for line in file:
        try:
            val = float(line)
            data.append(float(val))
        except:
            pass

# Compute misc stuff
SKIP = len(data) // (NN * WIDTH)
data2 = data[::SKIP]
MAX = max(data2)
MIN = min(data2)
SCALE = HH / ( MAX - MIN )

# "Plot" data
for row in range(NN):
    y_offset = int(HH * (row + 0.5))
    xo = 0
    yo = y_offset
    for x in range(WIDTH):
        y = int(y_offset + (SCALE * data2[x + row*WIDTH]))
        draw.line([(xo, yo), (x, y)], fill=BLACK)
        xo = x
        yo = y

# Save to BMP file
img.rotate(90, expand=True).save("out.bmp")


