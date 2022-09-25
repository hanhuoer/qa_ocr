from qa import QA


class QAV(object):
    question = None
    answer = None
    ratio = None

    def __init__(self, question, answer, ratio):
        self.question = question
        self.answer = answer
        self.ratio = ratio

    def __str__(self):
        return '{"question": "%s", "answer": "%s", "ratio": "%f"}' % (self.question, self.answer, self.ratio)

    def copy(self, qa):
        return QA(qa.question, qa.answer)

    def set_ratio(self, ratio):
        self.ratio = ratio
