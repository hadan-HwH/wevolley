"""숫자 카드 그림(assets/numbers.png)을 tools/numbers.json 으로 다시 그린다.

쓰기: python tools/render_numbers.py --fonts <Pretendard · Archivo · IBM Plex Mono 폰트 폴더>
색은 앱 VOLT 팔레트(잉크 #17181A, 볼트 #C8F135, 오프화이트 #F5F6F1). 2배 크기로 그려 선명하게 보인다.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INK, VOLT, OFF, GRAY, LINE = (23, 24, 26), (200, 241, 53), (245, 246, 241), (142, 143, 137), (58, 59, 56)
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", type=Path, required=True)
    a = ap.parse_args()
    f = lambda name, size: ImageFont.truetype(str(a.fonts / name), size)  # noqa: E731
    data = json.loads((ROOT / "tools" / "numbers.json").read_text(encoding="utf-8"))
    cells, cols, pad, top, rh = data["cells"], 4, 72, 140, 220
    rows = -(-len(cells) // cols)
    W, H = 1760, top + rows * rh + 24
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), 40, fill=INK)
    mono = f("IBMPlexMono-SemiBold.ttf", 28)
    d.text((pad, 58), "WEVOLLEY  BY  THE  NUMBERS", font=mono, fill=VOLT)
    d.text((W - pad, 58), data["date"], font=f("IBMPlexMono-Medium.ttf", 28), fill=GRAY, anchor="ra")
    cw = (W - 2 * pad) / cols
    for i, (num, label, sub) in enumerate(cells):
        r, c = divmod(i, cols)
        x, y = pad + c * cw, top + r * rh
        if c:
            d.line((x - 24, y + 18, x - 24, y + rh - 40), fill=LINE, width=2)
        d.text((x, y), num, font=f("Archivo-BlackItalic.ttf", 92), fill=VOLT)
        d.text((x + 2, y + 118), label, font=f("Pretendard-SemiBold.otf", 32), fill=OFF)
        d.text((x + 2, y + 162), sub, font=f("Pretendard-Regular.otf", 24), fill=GRAY)
    for r in range(1, rows):  # 줄 사이에만 가로선
        d.line((pad, top + r * rh - 12, W - pad, top + r * rh - 12), fill=LINE, width=2)
    out = ROOT / "assets" / "numbers.png"
    img.save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    main()
