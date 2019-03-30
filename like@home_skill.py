"""
This skills provides a quick description about the event 
Like@Home organized by the Mu Nu Chapter of IEEE-Eta Kappa Nu
"""
import aiy.assistant.grpc
import aiy.voice.audio
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
import aiy.voice.tts

import sys


def main():
    with Board() as board:
        hints = get_hints(args.language)
        client = CloudSpeechClient()
        while True:
            print('Press button to send commands to the robot')
            board.wait_for_press()
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text:
                print("You said : " + text)
                if text == "Qual è l'evento migliore del mondo?":
                    text = """Laic et om è l'evento che ti farà sentire a casa! All'evento i partecipanti riceveranno dei Vois chit (proprio come me!)
                             e dovranno sviluppare nuove schill che rendano Google Assistant il miglior coinquilino che ci sia. Lo scopo è far sentire a casa anche gli studenti fuorisede.
                            L'evento si terrà sabato 30 marzo e domenica 31. Nel costo del biglietto sono inclusi l'ingresso e parecchi gadget. Il pranzo, la merenda, la cena, la colazione,
                            caffe e redbull sono gratuiti per tutti i partecipanti.
                            Cosa aspettate? Sentitevi Like at Home!"""
                    aiy.voice.tts.say(text)
                else:
                    text = "ok google qual e l'evento migliore del mondo?"
                    aiy.voice.tts.say(text)

if __name__ == "__main__":
    main()
