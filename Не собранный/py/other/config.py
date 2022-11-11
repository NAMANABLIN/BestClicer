import sqlite3

from pygame import mixer

mixer.init()

# звуки
click = mixer.Sound(r'music\sqek.mp3')
explosion = mixer.Sound(r'music\deltarune-explosion.mp3')
buy = mixer.Sound(r'music\undertale-save.mp3')

con = sqlite3.connect('players.db')
cur = con.cursor()

# константы для очистки/удаления аккаунта
DEL_AK = 'Вы уверены что\nхотите удалить аккаунт?\nДанные не востановить.'
CLEAR_AK = 'Вы уверены что\nхотите очистить аккаунт?\nДанные не востановить.'

# собирание инфы сколько скинов на данный момент и создание словаря с названиями, и их ценами
skins = 0
dskins = {}
for x in cur.execute(f'SELECT * FROM data'
                     f'  WHERE skin like "%"').fetchall():
    dskins[x[0]] = x[1], x[2]
    skins += 1
DSKINS = dskins
SKINS = skins
