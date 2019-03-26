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
                print("You said : " + text)
                if text == "qual e l'evento migliore del mondo?":
                    text = """Laic et om è l'evento che ti farà sentire a casa! All'evento i partecipanti riceveranno dei Vois chit (proprio come me!)
                             e dovranno sviluppare nuove schill che rendano Google Assistant il miglior coinquilino che ci sia. Lo scopo è far sentire a casa anche gli studenti fuorisede.
                            L'evento si terrà sabato 30 marzo e domenica 31. Nel costo del biglietto sono inclusi l'ingresso e parecchi gadget. Il pranzo, la merenda, la cena, la colazione,
                            caffe e redbull sono gratuiti per tutti i partecipanti.
                            Cosa aspettate? Sentitevi Like at Home!"""
                    aiy.audio.say(text)
                else:
                    text = "ok google qual e l'evento migliore del mondo?"
                    aiy.audio.say(text)

if __name__ == "__main__":
    main()
