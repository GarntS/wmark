import sys
from os import listdir
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageOps

def main():
    if len(sys.argv) < 4:
	print("Usage: python watermark.py <indir> <outdir> <watermark text>");
	return;

    for fname in listdir(sys.argv[1]):
        base = Image.open(sys.argv[1]+ fname).convert('RGB')

	fontSize = int(base.size[1] * .05 if base.size[0] > base.size[1] else base.size[0] * .05)
        fnt = ImageFont.truetype('./font.otf', int(fontSize))
        tCopy = base.copy()
        d = ImageDraw.Draw(tCopy)

        tSize = d.textsize(sys.argv[3], font=fnt)
        avgBox = (int(base.size[0] * .95 - tSize[0]), int(base.size[1] * .95 - tSize[1]), int(base.size[0] * .95), int(base.size[1] * .95))
        avgColor = int(sum(ImageStat.Stat(ImageOps.invert(base.crop(avgBox))).mean) / 3)
        drawColor = (avgColor, avgColor, avgColor, 90)
        d.text((int(base.size[0] * .95 - tSize[0]), int(base.size[1] * .95 - tSize[1])), sys.argv[3], font=fnt, fill=drawColor)

	tCopy.save(sys.argv[2]+ fname.split(".")[0]+ "-watermark.jpg")

if __name__ == '__main__':
    main()
