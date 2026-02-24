import base64

from PIL import Image, ImageDraw, ImageFont, ImageFilter


def text_to_ico(text, output="icon.ico", size=64):
    # 创建透明画布
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # 字体（Windows 自带）
    font = ImageFont.truetype("arialbd.ttf", int(size * 0.28))

    # 自动换行
    lines = text.split("\n")

    # 计算整体高度
    line_height = font.getbbox("Hg")[3]
    total_height = line_height * len(lines)

    y_offset = (size - total_height) // 2

    # ====== 画发光层 ======
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        w = bbox[2]
        x = (size - w) // 2
        y = y_offset + i * line_height

        glow_draw.text((x, y), line, font=font, fill=(0, 180, 255, 120))

    glow = glow.filter(ImageFilter.GaussianBlur(4))
    img = Image.alpha_composite(img, glow)

    # ====== 渐变文字 ======
    gradient = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(gradient)

    for i in range(size):
        # 蓝 → 青 渐变
        r = 0
        g = int(150 + (105 * i / size))
        b = 255
        grad_draw.line((0, i, size, i), fill=(r, g, b, 255))

    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)

    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        w = bbox[2]
        x = (size - w) // 2
        y = y_offset + i * line_height
        mask_draw.text((x, y), line, font=font, fill=255)

    gradient.putalpha(mask)
    img = Image.alpha_composite(img, gradient)

    # ====== 轻微描边 ======
    outline = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    outline_draw = ImageDraw.Draw(outline)

    for dx in [-1, 1, 0, 0]:
        for dy in [0, 0, -1, 1]:
            for i, line in enumerate(lines):
                bbox = font.getbbox(line)
                w = bbox[2]
                x = (size - w) // 2 + dx
                y = y_offset + i * line_height + dy
                outline_draw.text((x, y), line, font=font, fill=(0, 0, 0, 200))

    img = Image.alpha_composite(outline, img)

    # 保存
    img.save(output, format="ICO", sizes=[(64, 64)])

    print("生成完成:", output)

    with open(output, "rb") as f:
        print(base64.b64encode(f.read()).decode())


if __name__ == "__main__":
    text_to_ico("Build\nAOSP\nImage")
