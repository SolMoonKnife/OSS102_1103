import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        ### (#2 : 메인 레이아웃을 그리드로 변경)
        main_layout = QGridLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        # layout_operation = QHBoxLayout()
        layout_clear_equal = QHBoxLayout()
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        ### (#1 : 하나의 equation 창으로 통합하기 위해 위젯 하나만 생성으로 수정)
        label_equation = QLabel("Window: ")
        # label_solution = QLabel("Solution: ")
        self.equation = QLineEdit("")
        # self.solution = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        ### (#1 : 레이아웃에 하나의 창 위젯만 추가)
        layout_equation_solution.addRow(label_equation, self.equation)
        # layout_equation_solution.addRow(label_solution, self.solution)

        ### 사칙연산 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("Clear")
        button_backspace = QPushButton("Backspace")

        ### (#3 : mod와 CE 버튼을 만들고 시그널 설정)
        button_mod = QPushButton("%")
        button_mod.clicked.connect(lambda state, num = "%": self.number_button_clicked(num))
        layout_clear_equal.addWidget(button_mod)

        button_ce = QPushButton("CE")
        button_ce.clicked.connect(self.button_clear_clicked)
        layout_clear_equal.addWidget(button_ce)        

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        ### (#2 : 이퀄 버튼은 숫자 레이아웃으로 이동)
        layout_clear_equal.addWidget(button_clear)
        layout_clear_equal.addWidget(button_backspace)
        # layout_clear_equal.addWidget(button_equal)

         ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        ### (추가 : 사칙연산과 등호가 통합된 4*5 그리드. 추가 기능을 위한 3칸 남김)
        ### (수정 : 숫자 배열 순서 현재 오름차순에서 역-내림차순으로 변경)
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
        ### 숫자가 역-내림차순으로 정렬되도록 수정
        for i in range(1, 5):
            if i == 4:
                layout_number.addWidget(number_button_dict[0], 4, 1)
            else:
                for j in range(0, 3):
                    layout_number.addWidget(number_button_dict[j + 10 - (i*3)], i, j)


        ### 사칙연산 버튼을 layout_number 레이아웃에 추가
        layout_number.addWidget(button_plus, 3, 3)
        layout_number.addWidget(button_minus, 2, 3)
        layout_number.addWidget(button_product, 1, 3)
        layout_number.addWidget(button_division, 0, 3)

        ### 이퀄 버튼을 layout_number 레이아웃에 추가
        layout_number.addWidget(button_equal, 4, 3)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        ### (#2 : 확장된 숫자-연산자 그리드에 맞게 위치 조정)
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 4, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 4, 0)

        ### (#3 : 추가버튼 3종 : 역수, 제곱, 근호)
        button_rev = QPushButton("1/x")
        button_rev.clicked.connect(self.button_rev_clicked)
        layout_number.addWidget(button_rev, 0, 0)

        button_sqre = QPushButton("x^2")
        button_sqre.clicked.connect(self.button_sqre_clicked)
        layout_number.addWidget(button_sqre, 0, 1)

        button_root = QPushButton("√x")
        button_root.clicked.connect(self.button_root_clicked)
        layout_number.addWidget(button_root, 0, 2)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        ### (#2 : 그리드 레이아웃으로 재정렬)
        main_layout.addLayout(layout_equation_solution, 0, 0)
        # main_layout.addLayout(layout_operation)
        main_layout.addLayout(layout_clear_equal, 1, 0)
        main_layout.addLayout(layout_number, 2, 0)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    ### (#1 : 하나의 창에 표시하기 위해 결과를 equation 위젯 텍스트로 설정)
    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.equation.setText(str(solution))

    # (추가 : 역수 버튼)
    def button_rev_clicked(self):
        pass

    # (추가 : 제곱 버튼)
    def button_sqre_clicked(self):
        pass

    # (추가 : 근호 버튼)
    def button_root_clicked(self):
        pass

    ### (#2 : 창 통합으로 인한 솔루션 초기화 삭제)
    def button_clear_clicked(self):
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())