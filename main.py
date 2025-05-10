from random import choice, shuffle

from data import *

SHOW_COUNTER = True

class App:
    def __init__(self):
        # 0 - menu mode
        # 1 - missed letter mode
        # 2 - mode new word
        # 3 - tutorial mode
        # 4 - statistic mode
        # 5 - exit
        self.mode = 0

        json_file_checking()

        data = json_read("data.json")
        self.all_words = data["words"]
        self.all_similar_letters = data["letters"]
        self.all_letters = set(i for j in self.all_similar_letters for i in j)

        statistic = json_read("statistic.json")
        self.question_counter = statistic["questions"]
        self.right_answer_counter = statistic["right_answers"]
        self.errors_statistic = statistic["errors"]

    def menu(self):
        answer = None
        while answer is None:
            print("\n[ Меню | СловоЕГЭ ]")
            print("0) Меню")
            print("1) Слова")
            print("2) Добавить новое слово")
            print("3) Гайд")
            print("4) Статистика")
            print("5) Выход")
            try:
                answer = int(input(">> "))
                if answer not in [0, 1, 2, 3, 4, 5]:
                    raise ValueError
            except ValueError:
                answer = None
        self.mode = answer

    def missed_letter(self):
        answer = None
        right_answer_counter = 0
        question_counter = 0
        while answer != 0:
            random_wrd = choice(self.all_words)
            question, right_letter = from_wrd_to_question(random_wrd)
            similar = similar_ltrs(self.all_similar_letters, right_letter)
            shuffle(similar)
            answers = [f"{i+1}) {similar[i]}" for i in range(len(similar))]
            
            if not answers:
                print(f"Не найдены пары для буквы '{right_letter}'")
                print("Исправьте файл 'data.json'")
                exit(1)

            while answer is None:
                if SHOW_COUNTER:
                    print(f'\n{right_answer_counter}/{question_counter}')
                    print('# ' + question)
                else:
                    print('\n# ' + question)
                print("\t".join(answers))
                try:
                    answer = int(input(">> "))
                    if (answer < 0) or (answer > len(similar)):
                        raise ValueError
                except ValueError:
                    answer = None

            if answer:
                if similar[answer-1] == right_letter:
                    print("Все верно! Правильная буква - " + right_letter)
                    self.right_answer_counter += 1
                    right_answer_counter += 1
                else:
                    print("Увы, ответ неверный, правильная буква - " + right_letter)
                    if random_wrd in self.errors_statistic:
                        self.errors_statistic[random_wrd] += 1
                    else:
                        self.errors_statistic[random_wrd] = 1
                    input("[нажмите enter]")
                self.question_counter += 1
                question_counter += 1
                answer = None
        else:
            self.mode = 0

    def new_word(self):
        answer = None
        print("\n[ Добавление нового слова ]")
        print("Введи слово, выделив трудную букву знаком '_' с двух сторон")
        print("[для выхода введите '0']")
        while answer is None:
            answer = input(">> ").lower()
            if answer != '0':
                if answer.count("_") == 2:
                    lindex = answer.find("_")
                    rindex = answer.rfind("_")
                if answer.count("_") != 2 or rindex - lindex != 2:
                    print("Неверный формат ввода")
                elif answer[lindex+1] not in self.all_letters:
                    print(f"Буквы '{answer[lindex+1]}' нет в data.json")
                else:
                    self.all_words.append(answer)
                    data = {"words": self.all_words,
                            "letters": self.all_similar_letters}
                    json_write("data.json", data)
                    print(f"Слово '{answer.replace("_", "")}' добавлено")
                answer = None
            else:
                self.mode = 0

    def tutorial(self):
        answer = None
        while answer != '0':
            print("\n[ Гайд ]")
            print("Как пользоваться СловоЕГЭ?")
            print(" - главный функционал программы в режиме 'слова'")
            print(" - навигация происходит на основе введённого вами")
            print(" - чтобы добавлять трудные для вас слова пользуйтесь режимом 'добавить новое слово'")
            print("Теперь вводите '0' и отправляйтесь в 'Меню'")
            answer = input(">> ")
        else:
            self.mode = 0         

    def statistic(self):
        answer = None
        while answer != '0':
            print("\n[ Статистика ]")
            print("Всего сделано: ", self.question_counter)
            print("Правильно: ", self.right_answer_counter)
            errors = sorted(self.errors_statistic.items(), 
                            key=lambda x: x[1], reverse=True)
            if errors:
                print("Ошибки в словах:")
                for word, quentity in errors:
                    print(f" {word.replace("_", "")} - {quentity}")
            print("Вводите '0', чтобы отправиться в 'Меню'")
            answer = input(">> ")
        else:
            self.mode = 0

    def main_loop(self):
        try:
            while True:
                match self.mode:
                    case 0:
                        self.menu()
                    case 1:
                        if not self.all_words:
                            print("Для тренировки сначала добавьте слова")
                            input("[нажмите enter]")
                            self.mode = 0
                            continue          
                        self.missed_letter()
                    case 2:
                        self.new_word()
                    case 3:
                        self.tutorial()
                    case 4:
                        self.statistic()
                    case 5:
                        self.completion_work()
        except KeyboardInterrupt:
            self.completion_work()
        except Exception as e:
            self.completion_work(e)
    
    def completion_work(self, error=None):
        data = {"questions": self.question_counter, 
                "right_answers": self.right_answer_counter,
                "errors": self.errors_statistic}
        json_write("statistic.json", data)

        if error:
            print(error)

        exit(int(bool(error)))
            

if __name__ == "__main__":
    app = App()
    app.main_loop()
