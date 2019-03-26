"""
This skills provides a quick description about the event 
Like@Home organized by the Mu Nu Chapter of IEEE-Eta Kappa Nu
"""
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import sys

aiy.i18n.set_language_code('it-IT')

def main():
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()
    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press button to send commands to the robot')
            button.wait_for_press()
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text:
                if text == "ok google qual'è l'evento migliore del mondo?":
                    text = "Ti piace programmare? Hai sempre nuove idee ma nessuna opportunità per realizzarle? Giunge anche quest'anno l'occasione per farti valere! Partecipa a Laic et om! La sfida consiste nell’ideare e sviluppare nuove schills per un om Assistant; atte ad assistere gli studenti fuorisede nella loro vita casalinga."
                    aiy.audio.say(text)
                else:
                    text = "parlami di laic et om"
                    aiy.audio.say(text)

if __name__ == "__main__":
    main()
