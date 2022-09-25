class QA(object):
    question = None
    answer = None
    ratio = None

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.ratio = 0.0

    def __str__(self):
        return 'question: %s, answer: %s' % (self.question, self.answer)

    def copy(self):
        return QA(self.question, self.answer)

    def set_ratio(self, ratio):
        self.ratio = ratio

