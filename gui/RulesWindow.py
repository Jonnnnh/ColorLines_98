from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton


class RulesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Правила игры")
        self.textBrowser = QTextBrowser()
        self.okButton = QPushButton("OK!")
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(500, 500)
        layout = QVBoxLayout()

        self.textBrowser = QTextBrowser()
        self.textBrowser.setHtml("""
                   <html>
                   <head>
                           <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #ffffff;
                            color: #000000;
                            padding: 20px;
                        }
                        h1 {
                            color: #ff4500;
                            font-size: 24px;
                        }
                        h2 {
                            color: #ff4500;
                            font-size: 20px;
                        }
                        p, li {
                            line-height: 1.6;
                            font-size: 16px;
                        }
                        ul {
                            margin-left: 20px;
                        }
                        .container {
                            padding: 10px;
                            border: 1px solid #cccccc;
                            border-radius: 8px;
                            background-color: #f9f9f9;
                        }
                        .tips {
                            color: #32cd32;
                        }
                    </style>
                   </head>
                   <body>
                       <div class="container">
                           <h1>Правила игры "Линии 98"</h1>
                           <p>Цель игры "Линии 98" - собрать линии из 5 или более шаров одного цвета. При сборе такой линии шары исчезают с поля, а игроку начисляются очки.</p>
                           <h2>Как играть:</h2>
                           <ul>
                               <li>Щелкните по шару, чтобы выбрать его, затем щелкните на пустую ячейку, чтобы переместить выбранный шар туда.</li>
                               <li>Шар может быть перемещен в пустую ячейку, если между этими ячейками существует путь, по которому шар мог бы прокатиться, не встречая препятствий в виде других шаров.</li>
                               <li>За каждую успешно сформированную линию из 5 и более шаров одного цвета игроку начисляются очки.</li>
                               <li>После каждого хода на поле появляются 3 или 5 новых шара, в зависимости от уровня игры. Если новый шар появляется на месте, куда был перемещен последний шар, линии формируются автоматически.</li>
                               <li>Игра заканчивается, когда на поле не остается свободных клеток.</li>
                           </ul>
                           <h2 class="tips">Советы:</h2>
                           <ul>
                               <li>Стратегически планируйте свои ходы, чтобы максимизировать количество очков, получаемых за один ход.</li>
                               <li>Старайтесь предвидеть места появления новых шаров, чтобы они не мешали вашим планам.</li>
                           </ul>
                           <p>Удачной игры!</p>
                       </div>
                   </body>
                   </html>
               """)
        self.okButton = QPushButton("OK!")
        self.okButton.clicked.connect(self.close)

        layout.addWidget(self.textBrowser)
        layout.addWidget(self.okButton)

        self.setLayout(layout)
