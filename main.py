from kivy.app import App
from kivy.uix.label import Label
import requests
import threading
import time
from plyer import notification

TRAIN = "2113"
STATION = "NOVI LIGURE"

class MyApp(App):

    def build(self):
        self.label = Label(text="Monitor treno attivo...")
        threading.Thread(target=self.loop, daemon=True).start()
        return self.label

    def notify(self, msg):
        notification.notify(
            title="Treno 2113",
            message=msg,
            timeout=10
        )

    def loop(self):
        notified = False

        while True:
            try:
                data = requests.get(
                    f"http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno/treno/{TRAIN}"
                ).json()

                for f in data.get("fermate", []):
                    if STATION in f.get("stazione", "").upper():

                        ritardo = f.get("ritardo", 0)
                        self.label.text = f"{STATION} | Ritardo +{ritardo}"

                        if f.get("arrivoReale") and not notified:
                            self.notify(f"Arrivato (+{ritardo})")
                            notified = True

            except:
                pass

            time.sleep(60)

MyApp().run()
