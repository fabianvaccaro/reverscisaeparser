from reverseinput import *

info_question = InfoQuestion(
    'Recientemente se han realizado obras de reforma en la Alameda de Málaga, ¿conoce usted como ha quedado esta calle? ¿Le gusta mucho, bastante, poco o nada?')
info_question.title = 'BLOQUE 3. TEMAS DE ACTUALIDAD DE MÁLAGA'
info_question.id_x = 710
info_question.name = 'P15'
info_question.hint = '(Nota: se trata de dos preguntas en una, solo si dice que los conoce se les debe dejar que los valores)'

main_question = ReverseSelectionQuestion()
main_question.body = 'Grado de conocimiento'
main_question.hint = '(Nota: no hace falta que la haya visitado para valorarla, puede haber seguido la reforma por los medios de comunicación)'
main_question.options = [
    ReverseOption(codification=1, text='Si conoce (FILTRO) (Sólo esta opción pasa a 15B)'),
    ReverseOption(codification=2, text='2.	No conoce (Pasar a P16)'),
]
main_question.ns = True
main_question.nc = True
main_question.np = False

linked_question = ReverseSelectionQuestion()
linked_question.body = 'Grado de valoración'
linked_question.hint = ''
linked_question.options = [
    ReverseOption(codification=1, text='Le gusta mucho como ha quedado'),
    ReverseOption(codification=2, text='Le gusta bastante como ha quedado'),
    ReverseOption(codification=3, text='Ni mucho ni poco (NO LEER)'),
    ReverseOption(codification=4, text='Le gusta poco como ha quedado'),
    ReverseOption(codification=5, text='No le gusta nada'),
]
linked_question.ns = True
linked_question.nc = True
linked_question.np = False

cascade = ReverseCascade(info_question=info_question, main_question=main_question, linked_question=linked_question,
                         strlist=['AAAAAAAAAAAAAAAAAAAA', 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'])
print(cascade)
