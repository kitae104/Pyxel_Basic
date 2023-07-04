import pyxel

from js import navigator
from pyodide.ffi import to_js
from pyodide.ffi.wrappers import add_event_listener

import asyncio

#Utility function for converting py dicts to JS objects
def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries) 
    
class App:
    def __init__(self):      
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.askForSerial())
        

        self.num = 0  
        self.data = "kitae"
        pyxel.init(160, 120, title="Hello Pyxel")             # 화면 크기 지정
        pyxel.image(0).load(0, 0, "pyxel_logo_38x16.png")     # 이미지 로드        
        pyxel.run(self.update, self.draw)                     # update/draw 함수 지정
        
        

    async def askForSerial(self):       
        self.data = "serial connected"  
        pyxel.text(55, 41, self.data, pyxel.frame_count % 16)
        if not hasattr(navigator, 'serial'):
            warning = "This browser does not support WebSerial; see https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API#browser_compatibility for a list of compatible browsers."
            print(warning)
            raise NotImplementedError(warning)        
        
        self.port = await navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 9600}))       
        self.data = self.port 
        pyxel.text(55, 41, self.data, pyxel.frame_count % 16)

        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        inputStream = self.decoder.readable

        self.reader = inputStream.getReader();
        
    
    async def listenAndEcho(self):
        self.data = "listenAndEcho"
        '''Loop forever, echoing values received on the serial port to the JS console'''
        receivedValues = []
        while (True):
            response = await self.reader.read()
            value, done = response.value, response.done
            if ('\r' in value or '\n' in value):
                self.data = 0
                #Output whole line and clear buffer when a newline is received
                print(f"Received from Serial: {''.join(receivedValues)}")
                receivedValues = []
            elif (value):
                self.data = 0
                #Output individual characters as they come in
                print(f"Received Char: {value}")
                receivedValues.append(value)
                


    def update(self):
        self.loop.run_until_complete(self.listenAndEcho())
        #value = self.sm.get_value()

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT or value == 1):
            self.num = 1            
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT or value == 50):
            self.num = 2
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP or value == 100):            
            self.num = 3
        if pyxel.btnp(pyxel.KEY_Q):                           # Q키를 누르면
            pyxel.quit()                                       # 애니메이션 종료
         

    def draw(self):
        pyxel.cls(0)   
        pyxel.text(55, 100, self.data, pyxel.frame_count % 16)   # 문자열 표시
        if self.num == 0:                                               # 화면을 지우기
            pyxel.text(55, 41, "Test, Pyxel!", pyxel.frame_count % 16)   # 문자열 표시
        elif self.num == 1:
            pyxel.text(55, 41, "LEFT!!", pyxel.frame_count % 16)   # 문자열 표시
        elif self.num == 2:
            pyxel.text(55, 41, "RIGHT!!", pyxel.frame_count % 16)   # 문자열 표시
        elif self.num == 3:
            pyxel.text(55, 41, "UP!!", pyxel.frame_count % 16)   # 문자열 표시
        else :
            pyxel.text(55, 41, self.num, pyxel.frame_count % 16)   # 문자열 표시

        pyxel.blt(61, 66, 0, 0, 0, 38, 16)                            # 이미지 표시

#Create an instance of the SerialManager class when this script runs

a = App()
