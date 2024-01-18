class Completer():
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # Если какой-то текст передан в метод
            if text:
                # вернуть список слов из списка, которые начинаются на текст
                self.matches = [s for s in self.options if s and s.startswith(text.lstrip())]
            else:
                # иначе вернуть весь список
                self.matches = self.options[:]

        # Вернуть элемент состояния из списка совпадений, если их много. 

        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


