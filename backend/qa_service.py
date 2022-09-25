import Levenshtein
import jieba

from qa import QA
from qav import QAV


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self.uniqueInstance = None

    def __call__(self):
        if self.uniqueInstance is None:
            self.uniqueInstance = self._cls()
        return self.uniqueInstance

@Singleton
class QAService(object):
    qa_file = None
    qa_list = None

    def __init__(self):
        self.qa_file = './qa.txt'
        self.qa_list = []
        self.__init_qa__()
        print('init qa.')

    def __init_qa__(self):
        if self.qa_list is None or len(self.qa_list) == 0:
            self.qa_list = []
            self.__load_qa__()

    def __load_qa__(self):
        with open(self.qa_file, encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                q = lines[i].replace('\n', '')
                a = lines[i + 1].replace('\n', '')
                self.qa_list.append(QA(q, a))

    def reload_qa(self):
        self.qa_list = []
        self.__load_qa__()

    def parse_to_content(self, res):
        content = ''
        for item in res:
            text = item[1]
            text = text.replace('\n', '')
            content += text
        content = self.__content_filter(content)
        return content

    def matchs(self, content):
        match_result = self.match(content)
        result_list = []
        for item in match_result:
            result_list.append(item.__str__())
        # return result_list[0:10]
        return result_list

    def __content_filter(self, content):
        content = content.replace('、', '')
        content = content.replace(' ', '')

        for i in range(0, 10):
            content = content.replace(str(i), '')

        low = 'abcdefghijklmnopqrstuvwxyz'
        for i in low:
            content = content.replace(i, '')

        up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in up:
            content = content.replace(i, '')

        content = content.replace('?', '？')
        head, sep, tail = content.partition('？')
        content = head + sep
        head, sep, tail = content.partition('。')
        content = head + sep
        return content


    def match(self, content):
        qav_list = []
        for item in self.qa_list:
            distance = Levenshtein.distance(content, item.question)
            qav = QAV(item.question, item.answer, distance)
            qav_list.append(qav)
        qav_list = sorted(qav_list, key=lambda i: i.ratio, reverse=False)
        return qav_list

    def match1(self, content):
        qav_list = []
        for item in self.qa_list:
            seqratio = self.seqratio(item, content)
            qav = QAV(item.question, item.answer, seqratio)
            qav_list.append(qav)
        qav_list = sorted(qav_list, key=lambda i: i.ratio, reverse=True)
        return qav_list

    def seqratio(self, qa, content):
        result = 0.0
        ql = list(jieba.cut(qa.question))
        cl = list(jieba.cut(content))
        result = Levenshtein.seqratio(ql, cl)
        return result

