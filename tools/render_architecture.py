"""아키텍처 그림(assets/architecture.png)을 그린다. 숫자 카드와 같은 VOLT 팔레트 · 폰트.

쓰기: python tools/render_architecture.py --fonts <Pretendard · Archivo · IBM Plex Mono 폰트 폴더>
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INK, VOLT, OFF, GRAY = (23, 24, 26), (200, 241, 53), (245, 246, 241), (142, 143, 137)
BOX, PANEL, LINE, ARROW = (36, 37, 40), (29, 30, 33), (62, 63, 60), (150, 151, 145)
ROOT = Path(__file__).resolve().parents[1]
W, H = 1760, 1010


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", type=Path, required=True)
    a = ap.parse_args()
    f = lambda name, size: ImageFont.truetype(str(a.fonts / name), size)  # noqa: E731
    title, sub, small = f("Pretendard-SemiBold.otf", 32), f("Pretendard-Regular.otf", 24), f("Pretendard-Regular.otf", 22)
    mono, mono_s = f("IBMPlexMono-SemiBold.ttf", 28), f("IBMPlexMono-Medium.ttf", 22)

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), 40, fill=INK)
    d.text((72, 58), "WEVOLLEY  ARCHITECTURE", font=mono, fill=VOLT)
    d.text((W - 72, 58), "Expo Router · Supabase · Vercel", font=mono_s, fill=GRAY, anchor="ra")

    def box(x1, y1, x2, y2, head, lines=(), fill=BOX, fg=OFF, fg2=GRAY):
        d.rounded_rectangle((x1, y1, x2, y2), 22, fill=fill, outline=None if fill == VOLT else LINE, width=2)
        d.text((x1 + 28, y1 + 24), head, font=title, fill=fg)
        for i, s in enumerate(lines):
            d.text((x1 + 28, y1 + 72 + i * 34), s, font=sub, fill=fg2)

    def arrow(points, dashed=False):
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            if dashed:
                n = int(max(abs(x2 - x1), abs(y2 - y1)) // 14)
                for k in range(0, n, 2):
                    t0, t1 = k / n, min(1, (k + 1) / n)
                    d.line((x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0, x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1), fill=ARROW, width=3)
            else:
                d.line((x1, y1, x2, y2), fill=ARROW, width=3)
        (px, py), (qx, qy) = points[-2], points[-1]
        ux, uy = (qx - px), (qy - py)
        n = max(1e-6, (ux * ux + uy * uy) ** 0.5)
        ux, uy = ux / n, uy / n
        s = 16
        d.polygon([(qx, qy), (qx - s * ux + s * 0.55 * uy, qy - s * uy - s * 0.55 * ux),
                   (qx - s * ux - s * 0.55 * uy, qy - s * uy + s * 0.55 * ux)], fill=ARROW)

    def label(x, y, text, pill=False, anchor="mm"):
        if pill:
            l, t, r, b = d.textbbox((x, y), text, font=small, anchor=anchor)
            d.rounded_rectangle((l - 16, t - 10, r + 16, b + 10), 18, fill=INK, outline=LINE, width=2)
        d.text((x, y), text, font=small, fill=GRAY, anchor=anchor)

    # 왼쪽: 한 코드베이스의 두 클라이언트
    box(72, 170, 392, 330, "모바일 앱", ["Android · iOS", "EAS Build · OTA"])
    box(72, 420, 392, 580, "웹 SPA", ["react-native-web", "Vercel"])
    d.text((72, 620), "한 코드베이스", font=f("Pretendard-SemiBold.otf", 26), fill=VOLT)
    d.text((72, 654), "Expo Router 화면 112개", font=sub, fill=GRAY)

    # 가운데: Supabase
    d.rounded_rectangle((552, 140, 1160, 800), 30, fill=PANEL, outline=LINE, width=2)
    d.text((584, 166), "SUPABASE", font=mono_s, fill=VOLT)
    box(584, 210, 1128, 380, "Postgres", ["91 테이블 · 전부 RLS · RPC 137", "pg_cron · pg_net"], fill=VOLT, fg=INK, fg2=INK)
    box(584, 440, 856, 560, "Realtime", ["채팅"])
    box(584, 620, 1128, 768, "Edge Functions", ["share-page · send-push · place-search"])

    # 오른쪽: 공유 링크 · 푸시
    box(1288, 170, 1688, 290, "카톡 · 슬랙 미리보기", ["OG 크롤러"])
    box(1288, 370, 1688, 560, "/s/{type}/{id}", ["Vercel Node 서버리스", "OG HTML 프록시", "사람은 원본 URL 로"])
    box(1288, 640, 1688, 768, "Expo Push", ["기기로 알림"])

    # 화살표
    arrow([(392, 250), (584, 250)])
    label(488, 226, "supabase-js")
    arrow([(392, 500), (584, 500)])
    label(488, 476, "supabase-js")
    arrow([(1000, 380), (1000, 620)])
    label(1000, 500, "알림 INSERT → 트리거", pill=True)
    arrow([(1488, 290), (1488, 370)])
    arrow([(1288, 520), (1224, 520), (1224, 650), (1128, 650)])
    arrow([(1128, 728), (1288, 728)])
    label(1208, 704, "send-push")

    # 아래: 배포 · 운영
    chips = [("GITHUB ACTIONS", "CI · 매일 DB 백업 · 공유 링크 점검"), ("EAS", "development · preview · production + OTA"),
             ("VERCEL", "웹 배포 · 정식 도메인으로 이동")]
    x = 72
    for head, text in chips:
        tw = d.textlength(head, font=mono_s) + 18 + d.textlength(text, font=sub) + 56
        d.rounded_rectangle((x, 860, x + tw, 930), 35, fill=BOX, outline=LINE, width=2)
        d.text((x + 28, 895), head, font=mono_s, fill=VOLT, anchor="lm")
        d.text((x + 28 + d.textlength(head, font=mono_s) + 18, 895), text, font=sub, fill=OFF, anchor="lm")
        x += tw + 20

    out = ROOT / "assets" / "architecture.png"
    img.save(out, optimize=True)
    print(out)


if __name__ == "__main__":
    main()
