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
    knowledge_cascade = 3


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


def xml2str(xmlElement):
    return ET.tostring(xmlElement, encoding='utf8').decode('utf-8')


class ReverseOption():
    def __init__(self, codification=1, text='.', optype=None):
        self.codification = codification
        self.type = optype
        self.text = text

    def toXml(self):
        opt = ET.Element('option')
        opt.set('codification', str(self.codification))
        opt.text = self.text if self.text is not None else '.'
        if self.type is not None:
            opt.set('type', self.type)
        return opt


class BasicQuestion():
    def __init__(self):
        self.id_x = 0
        self.name = 'P'
        self.title = ''
        self.type = None
        self.digits = 1
        self.group = None
        self.ns = True
        self.nc = True
        self.np = True
        self.body = None
        self.hint = None
        self.item = None


class ReverseQuestion(BasicQuestion):
    def __init__(self):
        super(ReverseQuestion, self).__init__()
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
        x_question.set('type', reverse_questionType(self.type) if self.type is not None else reverse_questionType(
            QuestionType.info))
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

    def toGruoped(self, items: list):
        b = ReverseGroup(self, items)
        return b

    def toGroupedSimple(self, strlist: list):
        subquestions = []
        for s, i in zip(strlist, range(len(strlist))):
            bq = BasicQuestion()
            bq.item = s
            bq.name = '{}.{}'.format(self.name, i + 1)
            subquestions.append(bq)
        return self.toGruoped(subquestions)

    def toBatterySimple(self, strlist: list, stride=10):
        b = ReverseBattery(self, strlist, stride)
        return b

    def getNCValue(self):
        return (10 ** self.digits) - 1

    def getNSValue(self):
        return (10 ** self.digits) - 2

    def getNPValue(self):
        return (10 ** self.digits) - 3

    def __str__(self):
        return ET.tostring(self.toXml(), encoding='utf8').decode('utf-8')


class InfoQuestion(ReverseQuestion):
    def __init__(self, body):
        super(InfoQuestion, self).__init__()
        self.body = body
        self.type = QuestionType.info
        self.name = ''
        self.ns = False
        self.nc = False
        self.np = False


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


class ReverseNumericalQuestion(ReverseQuestion):
    def __init__(self):
        super(ReverseNumericalQuestion, self).__init__()
        self.minoptions = 1
        self.maxoptions = 1
        self.type = QuestionType.numerical


class ReverseLikertNQuestion(ReverseSelectionQuestion):
    def __init__(self):
        super(ReverseLikertNQuestion, self).__init__()
        self.first_value = 0
        self.last_value = 10
        self.first_txt = 'muy mal'
        self.last_txt = 'muy bien'
        self.type = QuestionType.likertn

    def toXml(self):
        self.options = []
        for i in range(self.first_value, self.last_value + 1):
            opt = ReverseOption(codification=i)
            if i == self.first_value:
                opt.text = self.first_txt
            elif i == self.last_value:
                opt.text = self.last_txt
            else:
                opt.text = '.'
            self.options.append(opt)
        x_q = super(ReverseLikertNQuestion, self).toXml()
        return x_q


class ReverseGroup():
    def __init__(self, q: ReverseQuestion, items: list):
        self.subquestions = []
        for item in items:
            assert isinstance(item, BasicQuestion)
            self.subquestions.append(item)
        self.question = q
        self.N = len(self.subquestions)
        if self.N > 0:
            q.group = self.N

    def toXml(self):
        x_q = self.question.toXml()
        for ti in self.subquestions:
            assert isinstance(ti, BasicQuestion)
            x_subquestion = ET.Element('subquestion')
            if ti.name is not None:
                x_subquestion.set('name', ti.name)
            if ti.hint is not None:
                x_hint = ET.Element('hint')
                x_hint.text = ti.hint
                x_subquestion.append(x_hint)
            if ti.item is not None:
                x_item = ET.Element('item')
                x_item.text = ti.item
                x_subquestion.append(x_item)
            x_q.append(x_subquestion)
        return x_q

    def __str__(self):
        return ET.tostring(self.toXml(), encoding='utf-8').decode('utf-8')


class ReverseBattery():
    def __init__(self, q: ReverseQuestion, strList: list, stride=10):
        self.alt_question_bodies = []
        for item in strList:
            self.alt_question_bodies.append(item)
        self.question = q
        self.N = len(self.alt_question_bodies)
        self.startingId = q.id_x
        self.stride = stride
        self.name = self.question.name

    def toXml(self):
        x_block = ET.Element('collection')
        x_block.set('id', str(self.startingId))
        x_block.set('title', self.question.title)
        x_block.set('type', 'virtual')
        nextElementId = self.startingId + self.stride
        for chunk, i in zip(self.alt_question_bodies, range(len(self.alt_question_bodies))):
            self.question.id_x = nextElementId
            self.question.name = '{}.{}'.format(self.name, i + 1)
            self.question.item = chunk
            x_block.append(self.question.toXml())
            nextElementId = nextElementId + self.stride
        return x_block

    def __str__(self):
        return ET.tostring(self.toXml(), encoding='utf8').decode('utf-8')


class ReverseCascade():
    def __init__(self, info_question: InfoQuestion, main_question: ReverseQuestion, linked_question: ReverseQuestion,
                 strlist: list, stride=10):
        self.startingId = 0
        self.title = '.'
        self.info_question = info_question
        self.main_question = main_question
        self.linked_question = linked_question
        self.items = strlist
        self.stride = stride
        self.name = 'P'
        if self.info_question is not None:
            self.startingId = self.info_question.id_x
            self.title = self.info_question.title
            self.name = self.info_question.name
        else:
            self.startingId = self.main_question.id_x
            self.title = self.main_question.title
            self.name = self.main_question.name

    def toXml(self):
        x_block = ET.Element('collection')
        x_block.set('id', str(self.startingId))
        x_block.set('title', self.title)
        x_block.set('type', 'virtual')

        nextElementId = self.startingId + self.stride

        if self.info_question is not None:
            self.info_question.id_x = nextElementId
            x_iq = self.info_question.toXml()
            x_block.append(x_iq)
            nextElementId += self.stride

        for chunk, i in zip(self.items, range(len(self.items))):
            self.main_question.id_x = nextElementId
            self.main_question.name = '{}.{}.{}'.format(self.name, i + 1, 'A')
            self.main_question.item = chunk
            x_block.append(self.main_question.toXml())
            nextElementId += self.stride

            self.linked_question.id_x = nextElementId
            self.linked_question.name = '{}.{}.{}'.format(self.name, i + 1, 'B')
            self.linked_question.item = chunk
            x_block.append(self.linked_question.toXml())
            nextElementId += self.stride

        return x_block

    def __str__(self):
        return ET.tostring(self.toXml(), encoding='utf8').decode('utf-8')
