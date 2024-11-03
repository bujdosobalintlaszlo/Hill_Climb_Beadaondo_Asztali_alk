import os
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Button, Label
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import StopApplication

class ResultMenuFrame(Frame):
    def __init__(self, screen):
        super(ResultMenuFrame, self).__init__(screen,
                                              screen.height,
                                              screen.width,
                                              has_border=True,
                                              title="Eredmények Menü")
        self.set_theme("bright")

        layout = Layout([1])
        self.add_layout(layout)

        self.results_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mapHandling', 'results')

        self.options = self.get_result_options()
        self.list_box = ListBox(5, self.options)
        layout.add_widget(self.list_box)

        layout.add_widget(Divider())

        layout.add_widget(Button("Megnéz", self._view_result))
        layout.add_widget(Button("Visszalép", self._exit))

        self.fix()

    def get_result_options(self):
        try:
            files = [f for f in os.listdir(self.results_directory) if f.endswith('.txt')]
            return [(f, i + 1) for i, f in enumerate(files) if os.path.isfile(os.path.join(self.results_directory, f))]
        except Exception as e:
            print(f"Error reading directory: {e}")
            return [("Error loading files", 0)]

    def _view_result(self):
        selected = self.list_box.value
        if selected:
            file_name = self.options[selected - 1][0]
            file_path = os.path.join(self.results_directory, file_name)
            data = self.read_data(file_path)
            if data:
                self.set_theme("bright")
                result_text = f'Átlagos lépésszám: {data[0]}, futtatások száma: {data[1]}'
                self.screen.play([Scene([ResultDisplayFrame(self.screen, result_text)], -1)])

    def read_data(self, file_path):
        try:
            with open(file_path, 'r') as r:
                return r.readline().strip().split(',')
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def _exit(self):
        self.screen.close()
        raise StopApplication("User pressed exit")

        

class ResultDisplayFrame(Frame):
    def __init__(self, screen, result_text):
        super(ResultDisplayFrame, self).__init__(screen,
                                                 screen.height,
                                                 screen.width,
                                                 has_border=True,
                                                 title="Eredmény")
        self.set_theme("bright")


        layout = Layout([1])
        self.add_layout(layout)

        result_label = Label(result_text, height=3,align="^")
        layout.add_widget(result_label)
        layout.add_widget(Divider())
        layout.add_widget(Button("Vissza a menübe", self._go_back))
        self.fix()

    def _go_back(self):
        self.screen.play([Scene([ResultMenuFrame(self.screen)], -2)])

def demo(screen):
    screen.play([Scene([ResultMenuFrame(screen)], -1)])

if __name__ == "__main__":
    Screen.wrapper(demo)
