def key_press_event_main(self, event, mixer, cur):
    # проверка нажатия клавиш m, M, ь, m
    if event.key() == 77 or event.key() == 109 or event.key() == 1100 or event.key() == 1068:
        cur.execute(f'UPDATE players\n'
                    f'SET shmusic = {not self.shmusic}\n'
                    f'WHERE login = "{self.log}"')
        self.shmusic = not self.shmusic
        if self.shmusic:
            mixer.music.set_volume(0.0)
        else:
            mixer.music.set_volume(self.music / 100)
    # проверка нажатия клавиш n,N,т,Т
    elif event.key() == 78 or event.key() == 110 or event.key() == 1090 or event.key() == 1058:

        cur.execute(f'UPDATE players\n'
                    f'SET shsound = {not self.shsound}\n'
                    f'WHERE login = "{self.log}"')
        self.shsound = not self.shsound
