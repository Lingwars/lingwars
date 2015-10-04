
from pprint import pprint

data = """
Muchos años después, frente al pelotón de fusilamiento, el coronel Aureliano Buendía había de
recordar aquella tarde remota en que su padre lo llevó a conocer el hielo. Macondo era entonces
una aldea de veinte casas de barro y cañabrava construidas a la orilla de un río de aguas diáfanas
que se precipitaban por un lecho de piedras pulidas, blancas y enormes como huevos
prehistóricos. El mundo era tan reciente, que muchas cosas carecían de nombre, y para
mencionarlas había que señalarías con el dedo.
"""

from lingwars.text import Text, Word, Sentence

def dump_sentence(texto):
    print("----")
    s = Sentence(texto)
    [w.print() for w in s.pos_words]

#dump_sentence("Los dos lados de la cama")
dump_sentence("El Real Madrid ha ganado 20 copas de Europa")
#dump_sentence("ha querido dejárselo largo")
dump_sentence("La palabra adfadfsr acabo de inventármela ahora")
dump_sentence("los entregué a la policía.")

"""
# A little bit of text
text = Text(data)

from lingwars.text.word.filters import RemoveStopWords, RemovePunctuation, RemoveByEAGLES
filters = [RemoveStopWords(), RemovePunctuation()]
cnt = text.count_words(filters)
print(cnt.most_common(3))

filters = [RemoveStopWords(), RemovePunctuation(), RemoveByEAGLES(codes=['F', 'SPS', 'DA',])]
cnt = text.count_lemmas(filters=filters)
pprint(cnt)
"""