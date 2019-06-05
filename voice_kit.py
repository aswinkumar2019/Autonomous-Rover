import logging
from gpiozero import Buzzer
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
from time import sleep
from aiy.pins import (PIN_A, PIN_B, PIN_C, PIN_D)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def main():
    text = None
    bz1=Buzzer(PIN_A)
    bz2=Buzzer(PIN_B)
    bz3=Buzzer(PIN_C)
    bz3=Buzzer(PIN_D)
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    with aiy.audio.get_recorder():
            status_ui.status('ready')
            while True:
                print('Press the button and speak')
                button.wait_for_press()
                status_ui.status('listening')
                print('Listening...')
                text, audio = assistant.recognize()
                if text.lower().find('nehru')>=0:
                  aiy.audio.say("Ok,let me find where Jawaharlal Nehru is")
                  bz1.on()
                  bz2.off()
                  bz3.off()
                  bz4.off()
                elif text.find('gandhi')>=0:
                  aiy.audio.say("Ok,let me find where Mahatma Gandhi is")
                  bz1.off()
                  bz2.on()
                  bz3.off()
                  bz4.off()

main()


