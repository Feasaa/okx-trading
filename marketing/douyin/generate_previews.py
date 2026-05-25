from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
IMG_DIR = ROOT / "imgs"
OUT_DIR = ROOT / "marketing" / "douyin"
W, H = 1080, 1920

FONT_REG = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient(size, top, bottom):
    w, h = size
    strip = Image.new("RGB", (1, h))
    pix = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        pix[0, y] = tuple(lerp(top[i], bottom[i], t) for i in range(3))
    return strip.resize((w, h))


def fit_cover(img, size):
    tw, th = size
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def fit_contain(img, size):
    tw, th = size
    iw, ih = img.size
    scale = min(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def draw_text(draw, xy, text, size, fill, bold=False, max_width=None, line_gap=12):
    f = font(size, bold)
    x, y = xy
    if not max_width:
        draw.text((x, y), text, font=f, fill=fill)
        return y + draw.textbbox((x, y), text, font=f)[3] - draw.textbbox((x, y), text, font=f)[1]

    lines = []
    current = ""
    for ch in text:
        test = current + ch
        width = draw.textbbox((0, 0), test, font=f)[2]
        if width <= max_width or not current:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)

    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        bbox = draw.textbbox((x, y), line, font=f)
        y += bbox[3] - bbox[1] + line_gap
    return y


def rounded_panel(base, box, radius, fill, outline=None, width=2):
    draw = ImageDraw.Draw(base, "RGBA")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def screenshot_card(base, img_name, box, accent):
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow, "RGBA")
    sd.rounded_rectangle((x1 + 18, y1 + 24, x2 + 18, y2 + 24), radius=34, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    base.alpha_composite(shadow)

    rounded_panel(base, box, 34, (255, 255, 255, 26), accent, 3)
    shot = Image.open(IMG_DIR / img_name).convert("RGB")
    shot = fit_cover(shot, (x2 - x1 - 28, y2 - y1 - 28)).convert("RGBA")
    mask = Image.new("L", shot.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, shot.size[0], shot.size[1]), radius=26, fill=255)
    base.paste(shot, (x1 + 14, y1 + 14), mask)


def chip(draw, x, y, text, fill, stroke=(255, 255, 255, 42)):
    f = font(32, True)
    bbox = draw.textbbox((0, 0), text, font=f)
    w = bbox[2] - bbox[0] + 38
    h = 58
    draw.rounded_rectangle((x, y, x + w, y + h), radius=26, fill=fill, outline=stroke, width=2)
    draw.text((x + 19, y + 11), text, font=f, fill=(255, 255, 255, 238))
    return x + w + 14


def make_cover(spec):
    bg = gradient((W, H), spec["top"], spec["bottom"]).convert("RGBA")
    src = Image.open(IMG_DIR / spec["image"]).convert("RGB")
    blur = fit_cover(src, (W, H)).filter(ImageFilter.GaussianBlur(30)).convert("RGBA")
    bg = Image.blend(blur, bg, 0.72)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    od.rectangle((0, 0, W, H), fill=(0, 0, 0, 82))
    od.ellipse((-230, 250, 430, 910), fill=spec["glow1"])
    od.ellipse((710, 80, 1260, 640), fill=spec["glow2"])
    od.ellipse((600, 1320, 1260, 2060), fill=spec["glow3"])
    overlay = overlay.filter(ImageFilter.GaussianBlur(38))
    bg.alpha_composite(overlay)

    draw = ImageDraw.Draw(bg, "RGBA")
    draw.rounded_rectangle((76, 82, 486, 150), radius=28, fill=(255, 255, 255, 30), outline=(255, 255, 255, 58), width=2)
    draw.text((104, 101), "OKX Trading / 90+ Stars", font=font(30, True), fill=(255, 255, 255, 232))

    y = 222
    y = draw_text(draw, (78, y), spec["title"], 86, (255, 255, 255, 255), True, 930, 10)
    y += 18
    y = draw_text(draw, (82, y), spec["subtitle"], 43, spec["accent_text"], True, 900, 8)

    cx = 82
    cy = y + 34
    for text in spec["chips"]:
        cx = chip(draw, cx, cy, text, spec["chip"])

    screenshot_card(bg, spec["image"], (78, 720, 1002, 1232), spec["accent"])

    rounded_panel(bg, (78, 1308, 1002, 1610), 34, (4, 11, 20, 150), (255, 255, 255, 38), 2)
    draw = ImageDraw.Draw(bg, "RGBA")
    draw_text(draw, (116, 1354), spec["takeaway"], 47, (255, 255, 255, 248), True, 850, 14)
    draw_text(draw, (116, 1498), spec["detail"], 32, (220, 232, 245, 222), False, 840, 8)

    draw.rounded_rectangle((78, 1682, 1002, 1778), radius=34, fill=spec["accent_soft"], outline=spec["accent"], width=2)
    draw.text((116, 1703), spec["cta"], font=font(38, True), fill=(255, 255, 255, 245))

    draw.text((82, 1832), "仅技术研究｜不构成投资建议", font=font(28, True), fill=(255, 255, 255, 205))
    draw.text((680, 1832), "github.com/ralph-wren/okx-trading", font=font(22, False), fill=(255, 255, 255, 175))

    out = OUT_DIR / spec["file"]
    bg.convert("RGB").save(out, quality=94)
    return out


def make_contact_sheet(paths):
    thumb_w, thumb_h = 270, 480
    sheet = Image.new("RGB", (thumb_w * 4, thumb_h), (12, 16, 24))
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(img, (i * thumb_w, 0))
    out = OUT_DIR / "douyin-preview-contact-sheet.jpg"
    sheet.save(out, quality=92)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    specs = [
        {
            "file": "cover-01-ai-strategy.jpg",
            "image": "img_2.png",
            "title": "AI 写量化策略",
            "subtitle": "一句话生成 Java/Ta4j 交易策略",
            "chips": ["DeepSeek", "动态编译", "热更新"],
            "takeaway": "不是玩概念，是能进回测系统跑起来。",
            "detail": "输入策略想法，生成代码，编译加载，再用历史 K 线验证收益、回撤和交易质量。",
            "cta": "这套开源项目已经 90+ Stars",
            "top": (11, 22, 34),
            "bottom": (8, 58, 76),
            "accent": (34, 211, 238, 190),
            "accent_text": (129, 232, 244, 255),
            "accent_soft": (20, 184, 166, 86),
            "chip": (14, 116, 144, 170),
            "glow1": (20, 184, 166, 72),
            "glow2": (34, 211, 238, 58),
            "glow3": (16, 185, 129, 52),
        },
        {
            "file": "cover-02-backtest-score.jpg",
            "image": "img_5.png",
            "title": "250+ 策略回测",
            "subtitle": "33 个风险指标自动评分",
            "chips": ["Ta4j", "批量回测", "夏普/回撤"],
            "takeaway": "策略多不可怕，怕的是没有统一评分。",
            "detail": "收益、最大回撤、胜率、VaR、CVaR、Sortino、Calmar 等指标统一沉淀，方便横向比较。",
            "cta": "从策略库到评分榜，一条链路",
            "top": (18, 20, 36),
            "bottom": (68, 35, 76),
            "accent": (251, 191, 36, 195),
            "accent_text": (253, 224, 71, 255),
            "accent_soft": (234, 179, 8, 82),
            "chip": (146, 64, 14, 170),
            "glow1": (245, 158, 11, 62),
            "glow2": (244, 63, 94, 52),
            "glow3": (251, 191, 36, 46),
        },
        {
            "file": "cover-03-live-trading.jpg",
            "image": "img_7.png",
            "title": "策略跑到实盘",
            "subtitle": "OKX WebSocket + 自动下单 + 交易提醒",
            "chips": ["OKX", "实盘引擎", "通知告警"],
            "takeaway": "回测不是终点，自动执行才是工程难点。",
            "detail": "订阅实时 K 线，识别买卖信号，执行订单，记录持仓和盈亏，并推送交易提醒。",
            "cta": "生成 -> 回测 -> 实盘 -> 复盘",
            "top": (14, 23, 42),
            "bottom": (22, 72, 54),
            "accent": (52, 211, 153, 195),
            "accent_text": (167, 243, 208, 255),
            "accent_soft": (34, 197, 94, 82),
            "chip": (21, 128, 61, 170),
            "glow1": (34, 197, 94, 64),
            "glow2": (59, 130, 246, 48),
            "glow3": (16, 185, 129, 48),
        },
        {
            "file": "cover-04-engineering-stack.jpg",
            "image": "img_3.png",
            "title": "一个人的量化系统",
            "subtitle": "Spring Boot + React + MySQL/Redis/Kafka",
            "chips": ["Java 21", "Docker", "Swagger"],
            "takeaway": "它不是单脚本，而是一套完整工程。",
            "detail": "策略管理、行情缓存、回测结果、订单记录、Kafka 数据管道和前后端分离都已经搭好。",
            "cta": "适合研究 AI + 量化工程落地",
            "top": (18, 22, 42),
            "bottom": (47, 38, 88),
            "accent": (168, 85, 247, 185),
            "accent_text": (216, 180, 254, 255),
            "accent_soft": (147, 51, 234, 82),
            "chip": (88, 28, 135, 170),
            "glow1": (99, 102, 241, 54),
            "glow2": (168, 85, 247, 58),
            "glow3": (59, 130, 246, 42),
        },
    ]
    paths = [make_cover(spec) for spec in specs]
    sheet = make_contact_sheet(paths)
    print("Generated:")
    for path in paths + [sheet]:
        print(path)


if __name__ == "__main__":
    main()
