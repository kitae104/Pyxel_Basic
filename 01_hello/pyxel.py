import pyxel

from js import navigator
from pyodide.ffi import to_js
from pyodide.ffi.wrappers import add_event_listener

#Utility function for converting py dicts to JS objects
def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries)

class SerialManager():
    
    def __init__(self):
        self.value = 0

    def get_value(self):
        return self.value

    '''
    Class for managing reads and writes to/from a serial port
    Not very clean! No error handling, no way to stop listening etc.
    '''
    async def askForSerial(self):        

        '''
        Request that the user select a serial port, and initialize
        the reader/writer streams with it
        '''
        if not hasattr(navigator, 'serial'):
            warning = "This browser does not support WebSerial; see https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API#browser_compatibility for a list of compatible browsers."
            print(warning)
            raise NotImplementedError(warning)
        
        self.port = await navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 9600}))
        js.console.log("OPENED PORT")

        # Set up encoder to write to port
        self.encoder = js.TextEncoderStream.new()
        outputDone = self.encoder.readable.pipeTo(self.port.writable)

        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        inputStream = self.decoder.readable

        self.reader = inputStream.getReader();
        await self.listenAndEcho()

    async def writeToSerial(self, data):
        '''Write to the serial port'''
        outputWriter = self.encoder.writable.getWriter()
        outputWriter.write(data + '\n')
        outputWriter.releaseLock()
        js.console.log(f"Wrote to stream: {data}")

    async def listenAndEcho(self): 

        print("===> 호출 !!!!")
        '''Loop forever, echoing values received on the serial port to the JS console'''
        receivedValues = []
        while (True):
            response = await self.reader.read()
            value, done = response.value, response.done
            self.value = value
            if ('\r' in value or '\n' in value):
                #Output whole line and clear buffer when a newline is received
                print(f"Received from Serial: {''.join(receivedValues)}")
                receivedValues = []
            elif (value):
                #Output individual characters as they come in
                print(f"Received Char: {value}")
                receivedValues.append(value)



#A helper function - to point the py-click attribute of one of our buttons to
async def sendValueFromInputBox(sm: SerialManager):
    '''
    Get the value of the input box and write it to serial
    Also clears the input box
    '''
    textInput = js.document.getElementById("text")
    value = textInput.value
    textInput.value = ''
    print(f"Writing to Serial Port: {value}")

    await sm.writeToSerial(value)


class App:
    def __init__(self):
        self.num = 0
        self.sm = SerialManager()        
        pyxel.init(160, 120, title="Hello Pyxel")             # 화면 크기 지정
        pyxel.image(0).load(0, 0, "pyxel_logo_38x16.png")     # 이미지 로드        
        pyxel.run(self.update, self.draw)                     # update/draw 함수 지정

    def update(self):

        value = self.sm.get_value()

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT or value == 1):
            self.num = 1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT or value == 50):
            self.num = 2
        if pyxel.btnp(pyxel.KEY_Q):                           # Q키를 누르면
            pyxel.quit()                                      # 애니메이션 종료
         

    def draw(self):
        pyxel.cls(0)   
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

App()
