import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")             # 화면 크기 지정
        pyxel.image(0).load(0, 0, "pyxel_logo_38x16.png")     # 이미지 로드        
        pyxel.run(self.update, self.draw)                     # update/draw 함수 지정

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):                           # Q키를 누르면
            pyxel.quit()                                      # 애니메이션 종료

    def draw(self):
        pyxel.cls(0)                                                  # 화면을 지우기
        pyxel.text(55, 41, "Test, Pyxel!", pyxel.frame_count % 16)   # 문자열 표시
        pyxel.blt(61, 66, 0, 0, 0, 38, 16)                            # 이미지 표시


App()
