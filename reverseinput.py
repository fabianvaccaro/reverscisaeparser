from enum import Enum
import xml.etree.ElementTree as ET


class QuestionType(Enum):
    likertn = 1
    singleselection = 2
    multiselection = 3
    ranking = 4
    filteroption = 5
    numerical = 6
    info = 7
    audio = 8
    end = 9


class QuestionEnclosure(Enum):
    simple = 1
    battery = 2
    knowledge_battery = 3


def reverse_questionType(qt):
    assert isinstance(qt, QuestionType)
    revs = {
        QuestionType.likertn: 'likertn',
        QuestionType.singleselection: 'singleselection',
        QuestionType.multiselection: 'multiselection',
        QuestionType.ranking: 'ranking',
        QuestionType.filteroption: 'filteroption',
        QuestionType.numerical: 'numerical',
        QuestionType.info: 'info',
        QuestionType.audio: 'audio',
        QuestionType.end: 'end'
    }
    return revs[qt]


class ReverseOption():
    def __init__(self):
        self.codification = 1
        self.type = None
        self.text = '.'

    def toXml(self):
        opt = ET.Element('option')
        opt.set('codification', str(self.codification))
        opt.text = self.text if self.text is not None else '.'
        if self.type is not None:
            opt.set('type', self.type)
        return opt


class ReverseQuestion():
    def __init__(self):
        self.id_x = 0
        self.name = 'P'
        self.title = ''
        self.type = QuestionType.singleselection
        self.digits = 1
        self.group = None
        self.ns = True
        self.nc = True
        self.np = True
        self.body = None
        self.hint = None
        self.item = None

    def toXml(self):
        x_question = ET.Element('question')
        x_question.set('id', str(self.id_x))
        x_question.set('name', self.name)
        x_question.set('title', self.title)
        x_question.set('type', reverse_questionType(self.type))
        x_question.set('digits', str(self.digits))
        if self.group is not None:
            x_question.set('group', str(self.group))
        x_body = ET.Element('body')
        x_body.text = self.body if self.body is not None else ' '
        x_hint = ET.Element('hint')
        x_hint.text = self.hint if self.hint is not None else ' '
        x_ns = ET.Element('ns')
        x_ns.set('display', 'show' if self.ns else 'hidden')
        x_nc = ET.Element('nc')
        x_nc.set('display', 'show' if self.nc else 'hidden')
        x_np = ET.Element('np')
        x_np.set('display', 'show' if self.np else 'hidden')
        x_question.append(x_body)
        if self.item is not None:
            x_item = ET.Element('item')
            x_item.text = self.item
            x_question.append(x_item)
        x_question.append(x_hint)
        x_question.append(x_ns)
        x_question.append(x_nc)
        x_question.append(x_np)
        return x_question

    def __str__(self):
        return str(ET.tostring(self.toXml()))


class ReverseSelectionQuestion(ReverseQuestion):
    def __init__(self):
        super(ReverseSelectionQuestion, self).__init__()
        self.minoptions = 1
        self.maxoptions = 1
        self.options = []

    def toXml(self):
        x_q = super(ReverseSelectionQuestion, self).toXml()
        if len(self.options) > 0:
            x_options = ET.Element('options')
            x_options.set('minoptions', str(self.minoptions))
            x_options.set('maxoptions', str(self.maxoptions))
            for opt in self.options:
                assert isinstance(opt, ReverseOption)
                x_opt = opt.toXml()
                x_options.append(x_opt)
            x_q.append(x_options)
        return x_q


class ReverseLikertNQuestion(ReverseSelectionQuestion):
    def __init__(self):
        super(ReverseLikertNQuestion, self).__init__()
        self.first_value = 0
        self.last_value = 10
        self.first_txt = 'muy mal'
        self.last_txt = 'muy bien'

    def toXml(self):
        for i in range(self.first_value, self.last_value + 1):
            opt = ReverseOption()
            opt.codification = i
            if i == self.first_value:
                opt.text = self.first_txt
            elif i == self.last_value:
                opt.text = self.last_txt
            else:
                opt.text = '.'
            self.options.append(opt)
        x_q = super(ReverseLikertNQuestion, self).toXml()
        return x_q