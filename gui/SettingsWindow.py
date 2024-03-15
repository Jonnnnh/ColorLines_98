from functools import partial

from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QLabel, QButtonGroup

class SettingsWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.settings = {'count_cells': 9, 'count_colors': 7, 'count_balls_line': 5, 'difficulty': 'standard'}
        self.init_ui()

    def init_ui(self):
        self.setGeometry(0, 0, 400, 200)
        self.setWindowTitle("Settings")
        layout = QGridLayout(self)

        options = {
            'Area size': [(9, '9 X 9', 'count_cells'), (11, '11 X 11', 'count_cells'), (13, '13 X 13', 'count_cells')],
            'Colour count': [(7, '7', 'count_colors'), (6, '6', 'count_colors'), (5, '5', 'count_colors')],
            'Number of balls in line': [(4, '4', 'count_balls_line'), (5, '5', 'count_balls_line'),
                                        (6, '6', 'count_balls_line')],
            'Difficulty': [('standard', 'Standard', 'difficulty'), ('hard', 'Hard', 'difficulty')]
        }

        row = 0
        for setting_name, setting_options in options.items():
            layout.addWidget(QLabel(setting_name), row, 0)
            button_group = QButtonGroup(self)
            for index, (value, text, setting_key) in enumerate(setting_options):
                radio_button = QRadioButton(text)
                radio_button.setChecked(str(self.settings[setting_key]) == str(value))
                radio_button.toggled.connect(partial(self.update_setting, setting_key, value))
                layout.addWidget(radio_button, row + 1, index)
                button_group.addButton(radio_button)
            row += 2

    def update_setting(self, key, value, checked):
        if checked:
            self.settings[key] = value

    @property
    def count_cells(self):
        return self.settings['count_cells']

    @property
    def count_colors(self):
        return self.settings['count_colors']

    @property
    def count_balls_line(self):
        return self.settings['count_balls_line']

    @property
    def difficulty(self):
        return self.settings['difficulty']