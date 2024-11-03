import subprocess
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Button
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import StopApplication

class MenuFrame(Frame):
    def __init__(self, screen):
        super(MenuFrame, self).__init__(screen,
                                        screen.height,
                                        screen.width,
                                        has_border=True,
                                        title="Hill climb beadandó menü")
        self.set_theme("bright")
        layout = Layout([2])
        self.add_layout(layout)

        options = [
            ("Map generálás", 1),
            ("Map megjelenítése", 2),
            ("Szimuláció futtatása", 3),
            ("Adatok megtekintése", 4),
            ("Pont számolása",5),
            ("Resultok ürítése",6)
        ]
        self.list_box = ListBox(3, options)
        layout.add_widget(self.list_box)

        layout.add_widget(Divider())
        layout.add_widget(Button("Inditás", self._select))
        layout.add_widget(Button("Kilépés", self._exit))

        self.fix()

    def _select(self):
        self.screen.clear()
        self.screen.refresh()
        self.fix()
        selected = self.list_box.value
        if selected == 1:
            subprocess.run(["python", "./mapHandling/mapGen.py"], check=True)
        elif selected == 2:
            subprocess.run(["python", "./mapHandling/display3dMap.py"], check=True)
        elif selected == 3:
            subprocess.run(["python", "algo/hillClimb.py"])
        elif selected == 4:
            subprocess.run(["python", "mapHandling/displayResult.py"])
        elif selected == 5:
            subprocess.run(["python", "mapHandling/results/pointCounter.py"], check=True)
        elif selected == 6:
            subprocess.run(["python","mapHandling/results/clearResults.py"])

        
        input()
        self.screen.clear()
        self.screen.refresh()
        self.fix()

    def _exit(self):
        raise StopApplication("User pressed exit")

def demo(screen):
    screen.play([Scene([MenuFrame(screen)], -1)])

Screen.wrapper(demo)
