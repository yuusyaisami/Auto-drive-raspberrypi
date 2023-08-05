import pygame as pg

# pygame 初期化
pg.init()

# ウィンドウサイズの設定
screen = pg.display.set_mode((400, 400))

# 色の設定（半透明）
color = pg.Color(132, 171, 192)
color.a = 0  # アルファ値を設定

# ゲームループ
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # 画面をクリア
    screen.fill(pg.Color("white"))

    # 色を描画
    rect = pg.Rect(100, 100, 200, 200)
    pg.draw.rect(screen, color, rect)

    # 画面更新
    pg.display.flip()

# pygame 終了処理
pg.quit()