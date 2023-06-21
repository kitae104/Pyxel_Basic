import pyxel

from js import navigator
from pyodide.ffi import to_js
from pyodide.ffi.wrappers import add_event_listener

class App:
    def __init__(self):      
        self.num = 0  
        self.data = "kitae"
        pyxel.init(160, 120, title="Hello Pyxel")             # 화면 크기 지정
        pyxel.image(0).load(0, 0, "pyxel_logo_38x16.png")     # 이미지 로드        
        pyxel.run(self.update, self.draw)                     # update/draw 함수 지정

    def update(self):

        #value = self.sm.get_value()

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT or value == 1):
            self.num = 1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT or value == 50):
            self.num = 2
        if pyxel.btnp(pyxel.KEY_Q):                           # Q키를 누르면
            pyxel.quit()                                      # 애니메이션 종료
         

    def draw(self):
        pyxel.cls(0)   
        pyxel.text(55, 100, self.data, pyxel.frame_count % 16)   # 문자열 표시
        if self.num == 0:                                               # 화면을 지우기
            pyxel.text(55, 41, "Test, Pyxel!", pyxel.frame_count % 16)   # 문자열 표시
        elif self.num == 1:
            pyxel.text(55, 41, "LEFT!!", pyxel.frame_count % 16)   # 문자열 표시
        elif self.num == 2:
            pyxel.text(55, 41, "RIGHT!!", pyxel.frame_count % 16)   # 문자열 표시
        else :
            pyxel.text(55, 41, self.num, pyxel.frame_count % 16)   # 문자열 표시

        pyxel.blt(61, 66, 0, 0, 0, 38, 16)                            # 이미지 표시

#Create an instance of the SerialManager class when this script runs

a = App()