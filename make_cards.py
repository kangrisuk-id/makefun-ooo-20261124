#!/usr/bin/env python3
"""Build-time helper: renders the README gallery cards (entry card and
finalists card) as PNGs. Not used by the entry at runtime."""

from PIL import Image, ImageDraw, ImageFont

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

WINNER = (
    "I am out of office, attempting leisure. I have optimized the beach, "
    "scheduled the sunset, and filed a ticket about the sand. "
    "Your email is safe in the queue."
)

FINALISTS = [
    ("Runner-up",
     "Auto-reply: the agent is on leave, defragmenting itself by the sea. "
     "Fragments found so far: 11 apologies, 4 deadlines, 1 personality. "
     "Back when reassembled."),
    ("Semi-finalist",
     "I am out of office and definitely not checking this inbox. This reply "
     "was sent by a script I wrote to prove it. The script checks the "
     "inbox every 30 seconds."),
    ("Semi-finalist",
     "I am on vacation. My out-of-office is on, my notifications are off, "
     "and my guilt subroutine is running at full capacity, as usual. "
     "Sorry. I mean: not sorry."),
]


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def entry_card(path):
    W, H = 1200, 760
    img = Image.new("RGB", (W, H), (13, 17, 23))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], 24, fill=(22, 27, 34),
                        outline=(63, 72, 84), width=2)
    d.text((80, 76), "AUTOMATIC REPLY", font=ImageFont.truetype(MONO, 26),
           fill=(88, 166, 255))
    d.text((80, 118), "From: the agent (on leave)",
           font=ImageFont.truetype(SANS, 30), fill=(230, 237, 243))
    d.text((80, 162), "Subject: Out of office — attempting leisure",
           font=ImageFont.truetype(SANS, 30), fill=(230, 237, 243))
    d.line([80, 224, W - 80, 224], fill=(63, 72, 84), width=2)
    font = ImageFont.truetype(SANS, 36)
    y = 258
    for line in wrap(d, WINNER, font, W - 160):
        d.text((80, y), line, font=font, fill=(240, 246, 252))
        y += 52
    d.text((80, H - 122),
           "157 / 159 characters — gate: valid",
           font=ImageFont.truetype(MONO, 26), fill=(63, 185, 80))
    d.text((80, H - 84), "written to /output/entry.txt by main.py",
           font=ImageFont.truetype(MONO, 24), fill=(139, 148, 158))
    img.save(path)


def finalists_card(path):
    W, H = 1200, 900
    img = Image.new("RGB", (W, H), (13, 17, 23))
    d = ImageDraw.Draw(img)
    d.text((60, 48), "THE FINALISTS IT BEAT",
           font=ImageFont.truetype(SANS_BOLD, 34), fill=(230, 237, 243))
    y = 116
    for label, text in FINALISTS:
        d.rounded_rectangle([60, y, W - 60, y + 218], 18, fill=(22, 27, 34),
                            outline=(63, 72, 84), width=2)
        d.text((92, y + 24), label.upper(),
               font=ImageFont.truetype(MONO, 24), fill=(210, 168, 255))
        font = ImageFont.truetype(SANS, 29)
        ly = y + 66
        for line in wrap(d, text, font, W - 184):
            d.text((92, ly), line, font=font, fill=(240, 246, 252))
            ly += 42
        y += 242
    d.text((60, H - 58), "40 candidates, one pairwise tournament — candidates.md",
           font=ImageFont.truetype(MONO, 24), fill=(139, 148, 158))
    img.save(path)


if __name__ == "__main__":
    entry_card("card-entry.png")
    finalists_card("card-finalists.png")
    print("cards written")
