import csv
import sys
from time import sleep

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from py.other.basedef import key_press_event_main
from py.other.config import *
from py.other.password import check_password, check_login
from py.other.sorting import quick_sort
from py.ui.Clicker import BestClickerForm
from py.ui.check import CheckForm
from py.ui.enter import EnterForm
from py.ui.register import RegisterForm
from py.ui.settings import SettingsForm
from py.ui.shop import ShopForm
from py.ui.tutorial import TutorialForm


class Enter(QMainWindow):
    def __init__(self):
        super(Enter, self).__init__()
        QFontDatabase.addApplicationFont('ofont.ru_Toyz.ttf')
        self.ui = EnterForm()
        self.ui.setupUi(self)

        self.ui.registerbt.clicked.connect(self.register)
        self.ui.enter.clicked.connect(self.enter)
        self.ui.help.clicked.connect(self.tutorial)

        # такие вставки сделаны чтобы PyCharm
        # не жаловался на такие переменные для форм
        self.register_form, self.tutor_form, self.Bclicker = '', '', ''

    def register(self):
        self.register_form = Register()
        self.register_form.show()
        self.close()

    def enter(self):
        log = self.ui.loginle.text()
        pasw = self.ui.passwordle.text()
        if log == '':
            self.ui.statusbar.showMessage('Логин не введён')
        elif pasw == '':
            self.ui.statusbar.showMessage('Пароль не введён')
        else:
            for login in cur.execute(f'SELECT login FROM players'
                                     f'  WHERE login like "%"').fetchall():
                if login[0] == log:
                    if pasw in cur.execute(f'SELECT password FROM players'
                                           f'   WHERE login = "{log}"').fetchone():
                        self.Bclicker = BClicker(log)
                        self.Bclicker.show()
                        self.close()
                    else:
                        self.ui.statusbar.showMessage('Пароль не подходит')
                        return None
            self.ui.statusbar.showMessage('Такого пользователя не сущ')

    def tutorial(self):
        self.tutor_form = Tutorial()
        self.tutor_form.show()


class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        self.ui = RegisterForm()
        self.ui.setupUi(self)

        self.ui.register2bt.clicked.connect(self.register)
        self.ui.returnbt.clicked.connect(self.return1)
        self.ui.help.clicked.connect(self.tutorial)

        self.tutor_form, self.enter_form, self.Bclicker = '', '', ''

    def register(self):
        log = self.ui.loginle.text()
        pasw = self.ui.passwordle.text()
        pasw2 = self.ui.password2le.text()
        ans = check_login(log)
        if log in cur.execute(f'SELECT login FROM players'
                              f'  WHERE login like "%"').fetchone():
            self.ui.statusbar.showMessage('Есть пользователь с таким логином')
        elif ans == 'ОК':
            ans = check_password(pasw, pasw2)
            if ans == 'ОК':
                a = f"INSERT INTO players" \
                    f"(login,password,skin,unskins,money,moneyup,autoclick,energy,energyup," \
                    f"music,sound, shsound, shmusic)" \
                    f"VALUES('{log}','{pasw}',1,'1',0,1,0,100,1000,80,80,0,0)"
                cur.execute(a)
                con.commit()
                self.Bclicker = BClicker(log)
                self.Bclicker.show()
                self.close()
            else:
                self.ui.statusbar.showMessage(ans)
        else:
            self.ui.statusbar.showMessage(ans)

    def return1(self):
        self.enter_form = Enter()
        self.enter_form.show()
        self.close()

    def tutorial(self):
        self.tutor_form = Tutorial()
        self.tutor_form.show()


class Tutorial(QMainWindow):
    def __init__(self):
        super(Tutorial, self).__init__()
        self.ui = TutorialForm()
        self.ui.setupUi(self)


class BClicker(QMainWindow):
    def __init__(self, log):
        super(BClicker, self).__init__()
        self.log = log
        self.ui = BestClickerForm()
        self.ui.setupUi(self)

        a = cur.execute(f'SELECT money, moneyup, autoclick FROM players'
                        f'  WHERE login = "{log}"').fetchone()
        self.money, self.moneyup, self.autoclick = a[0], a[1], a[2]
        a = cur.execute(f'SELECT energy, energyup FROM players'
                        f'  WHERE login = "{log}"').fetchone()
        self.energy, self.energyup = a[0], a[1]
        a = cur.execute(f'SELECT music, sound FROM players'
                        f'  WHERE login = "{log}"').fetchone()
        self.music, self.sound = a[0], a[1]
        a = cur.execute(f'SELECT skin FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.skin = a[0]
        a = cur.execute(f'SELECT shmusic, shsound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.shmusic, self.shsound = a[0], a[1]

        click.set_volume(self.sound / 100)
        explosion.set_volume(self.sound / 100)
        buy.set_volume(self.sound / 100)

        if self.shmusic:
            mixer.music.set_volume(0.0)
        else:
            mixer.music.set_volume(self.music / 100)

        mixer.music.stop()
        mixer.music.load(r'music\Toby Fox - Uwa! So Temperate♫.mp3')
        mixer.music.play(-1)

        self.ui.moneyint.setText(str(self.money))
        self.ui.energyint.setText(str(self.energy // 10))
        self.ui.clickbt.clicked.connect(self.click)
        self.ui.settingsbt.clicked.connect(self.settings)
        self.ui.shopbt.clicked.connect(self.shop)

        width, height = self.ui.mousekek.width(), self.ui.mousekek.height()  # координаты зоны подзарядки
        pos = self.ui.mousekek.pos()
        self.min_x, self.max_x = pos.x(), pos.x() + width
        self.mix_y, self.max_y = pos.y(), pos.y() + height

        self.ui.clickpng.setPixmap(QPixmap(f'images/{DSKINS[self.skin][0]}'))
        self.ui.mousekek.setPixmap(QPixmap(r'images\mouse2.png'))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_db)
        self.timer.start(1000)

        self.shop_form, self.settings_form = '', ''

    def click(self):
        if not self.shsound:
            click.play()
        if self.energy - 10 < 0:
            return None
        self.money += self.moneyup
        self.energy -= 10

        cur.execute(f'UPDATE players\n'
                    f'SET money = {self.money}\n'
                    f'WHERE login = "{self.log}"')
        cur.execute(f'UPDATE players\n'
                    f'SET energy = {self.energy}\n'
                    f'WHERE login = "{self.log}"')

        self.ui.moneyint.setText(str(self.money))
        self.ui.energyint.setText(str(self.energy // 10))

    def mouseMoveEvent(self, event):
        x1, y1 = event.x(), event.y()
        if self.min_x <= x1 <= self.max_x and self.mix_y <= y1 <= self.max_y and self.energy != self.energyup:
            self.energy += 1
            self.ui.energyint.setText(str(self.energy // 10))
            cur.execute(f'UPDATE players\n'
                        f'SET energy = {self.energy}\n'
                        f'WHERE login = "{self.log}"')

    def shop(self):
        self.shop_form = Shop(self.log, self)
        self.shop_form.show()

    def settings(self):
        self.settings_form = Settings(self.log, self.music, self.sound, self)
        self.settings_form.show()

    def update_lb(self):
        a = cur.execute(f'SELECT money, moneyup, autoclick FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.money, self.moneyup, self.autoclick = a[0], a[1], a[2]
        self.ui.moneyint.setText(str(self.money))
        self.ui.energyint.setText(str(self.energy // 10))
        a = cur.execute(f'SELECT skin FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()[0]
        if self.skin != a:
            self.skin = a
            self.ui.clickpng.setPixmap(QPixmap(f'images/{DSKINS[a][0]}'))

    def update_db(self):
        self.money += self.autoclick
        self.ui.moneyint.setText(str(self.money))
        cur.execute(f'UPDATE players\n'
                    f'SET money = {self.money}\n'
                    f'WHERE login = "{self.log}"')
        a = cur.execute(f'SELECT energy, energyup FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.energy, self.energyup = a[0], a[1]
        a = cur.execute(f'SELECT music, sound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.music, self.sound = a[0], a[1]
        a = cur.execute(f'SELECT shmusic, shsound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.shmusic, self.shsound = a[0], a[1]
        con.commit()

    def closeEvent(self, event):
        mixer.music.set_volume(0.0)
        if not self.shsound:
            explosion.set_volume(self.sound / 100)
            explosion.play()
            sleep(2)
        con.close()

    def keyPressEvent(self, event):
        key_press_event_main(self, event, mixer, cur)


class Shop(QMainWindow):
    def __init__(self, log, bc):
        super(Shop, self).__init__()
        self.log = log
        self.bc = bc
        self.ui = ShopForm()
        self.ui.setupUi(self)

        self.leaderboard = []
        for row in cur.execute('SELECT login, unskins, money, moneyup, autoclick FROM players').fetchall():
            self.leaderboard.append([row[0], str(round(len(str(row[1])) / SKINS * 100)) + '%', row[2], row[3], row[4]])

        self.update_db()
        a = cur.execute(f'SELECT skin, unskins FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.skin, self.skins, self.skinchange = a[0], str(a[1]), a[0]

        self.ui.clickup.clicked.connect(self.dclickup)
        self.ui.autoclickup.clicked.connect(self.dautoclickup)
        self.ui.energyup.clicked.connect(self.denergyup)

        self.ui.clickup.setText(str(50 + self.moneyup * 30))
        self.ui.autoclickup.setText(str(150 + self.autoclick * 100))
        self.ui.energyup.setText(str(10 + (self.energyup - 1000) // 10 * 10))
        self.ui.buyskin.clicked.connect(self.buy_skin)
        self.ui.changeskin.clicked.connect(self.choose_skin)
        self.ui.leftskins.clicked.connect(self.flip_skins)
        self.ui.rightskins.clicked.connect(self.flip_skins)

        self.ui.skin.setPixmap(QPixmap(f'images/{DSKINS[self.skin][0]}'))
        self.ui.buyskin.setText(str(DSKINS[self.skin][1]))
        self.ui.buyskin.setDisabled(True)
        self.ui.changeskin.setDisabled(True)

        self.ui.progressBar.setValue(round((len(self.skins) - 1) / (SKINS - 1) * 100))
        mixer.music.load(r'music\Toby Fox - Shop.mp3')
        mixer.music.play(-1)
        a = cur.execute(f'SELECT shmusic, shsound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.shmusic, self.shsound = a[0], a[1]
        if self.shmusic:
            mixer.music.set_volume(0.0)
        else:
            mixer.music.set_volume(self.music / 100)

        self.updatelb()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_db)
        self.timer.start(1000)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.updatelb)
        self.timer2.start(400)

    def dclickup(self):
        if not self.shsound:
            buy.play()
        a = int(self.ui.clickup.text())
        cur.execute(f'UPDATE players\n'
                    f'SET money = {self.money - a}\n'
                    f'WHERE login = "{self.log}"')
        cur.execute(f'UPDATE players\n'
                    f'SET moneyup = {self.moneyup + 1}\n'
                    f'WHERE login = "{self.log}"')
        con.commit()
        BClicker.update_lb(self.bc)
        self.moneyup += 1
        self.money -= a
        self.ui.clickup.setText(str(a + 30))
        self.updatelb()

    def dautoclickup(self):
        if not self.shsound:
            buy.play()
        a = int(self.ui.autoclickup.text())
        cur.execute(f'UPDATE players\n'
                    f'SET money = {self.money - a}\n'
                    f'WHERE login = "{self.log}"')
        cur.execute(f'UPDATE players\n'
                    f'SET autoclick = {self.autoclick + 1}\n'
                    f'WHERE login = "{self.log}"')
        con.commit()
        BClicker.update_lb(self.bc)
        self.autoclick += 1
        self.money -= a
        self.ui.autoclickup.setText(str(a + 100))
        self.updatelb()

    def denergyup(self):
        if not self.shsound:
            buy.play()
        a = int(self.ui.energyup.text())
        cur.execute(f'UPDATE players\n'
                    f'SET money = {self.money - a}\n'
                    f'WHERE login = "{self.log}"')
        cur.execute(f'UPDATE players\n'
                    f'SET energyup = {self.energyup + 10}\n'
                    f'WHERE login = "{self.log}"')
        con.commit()
        BClicker.update_lb(self.bc)
        self.energyup += 10
        self.money -= a
        self.ui.energyup.setText(str(a + 10))
        self.updatelb()

    def buy_skin(self):
        self.skins = self.skins + str(self.skin)
        cur.execute(f'UPDATE players\n'
                    f'SET money = {self.money - DSKINS[self.skin][1]}\n'
                    f'WHERE login = "{self.log}"')
        con.commit()
        BClicker.update_lb(self.bc)
        self.money -= DSKINS[self.skin][1]
        cur.execute(f'UPDATE players\n'
                    f'SET unskins = {self.skins}\n'
                    f'WHERE login = "{self.log}"')
        self.ui.progressBar.setValue(round((len(self.skins) - 1) / (SKINS - 1) * 100))
        self.ui.changeskin.setDisabled(False)
        self.ui.buyskin.setDisabled(True)

    def choose_skin(self):
        cur.execute(f'UPDATE players\n'
                    f'SET skin = {self.skin}\n'
                    f'WHERE login = "{self.log}"')
        con.commit()
        BClicker.update_lb(self.bc)
        self.ui.changeskin.setDisabled(True)
        self.skinchange = self.skin

    def flip_skins(self):
        arrow = self.sender().text()
        if arrow == '<--':
            if self.skin - 1 <= 0:
                self.skin = SKINS
            else:
                self.skin -= 1
        else:
            if self.skin + 1 > SKINS:
                self.skin = 1
            else:
                self.skin += 1
        self.ui.skin.setPixmap(QPixmap(f'images/{DSKINS[self.skin][0]}'))
        self.ui.buyskin.setText(str(DSKINS[self.skin][1]))
        self.skinchange = cur.execute(f'SELECT skin FROM players'
                                      f'  WHERE login = "{self.log}"').fetchone()[0]
        self.updatelb()

    def updatelb(self):
        if self.money < int(self.ui.autoclickup.text()):
            self.ui.autoclickup.setDisabled(True)
        else:
            self.ui.autoclickup.setDisabled(False)

        if self.money < int(self.ui.clickup.text()):
            self.ui.clickup.setDisabled(True)
        else:
            self.ui.clickup.setDisabled(False)

        if self.money < int(self.ui.energyup.text()):
            self.ui.energyup.setDisabled(True)
        else:
            self.ui.energyup.setDisabled(False)

        if self.skin == self.skinchange:
            self.ui.buyskin.setDisabled(True)
            self.ui.changeskin.setDisabled(True)
        elif str(self.skin) in self.skins:
            self.ui.changeskin.setDisabled(False)
            self.ui.buyskin.setDisabled(True)
        else:
            self.ui.changeskin.setDisabled(True)
            if self.money < DSKINS[self.skin][1]:
                self.ui.buyskin.setDisabled(True)
            else:
                self.ui.buyskin.setDisabled(False)

    def update_db(self):
        a = cur.execute(f'SELECT money, moneyup, autoclick FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.money, self.moneyup, self.autoclick = a[0], a[1], a[2]
        a = cur.execute(f'SELECT energy, energyup FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.energy, self.energyup = a[0], a[1]
        a = cur.execute(f'SELECT music, sound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.music, self.sound = a[0], a[1]
        a = cur.execute(f'SELECT shmusic, shsound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.shmusic, self.shsound = a[0], a[1]

        new_list = []
        kek = []
        for row in cur.execute('SELECT login, unskins, money, moneyup, autoclick FROM players').fetchall():
            row1 = [row[0], round((len(str(row[1])) - 1) / (SKINS - 1) * 100), row[2], row[3], row[4]]
            if row[0] == self.log:
                kek = row1
            new_list.append(row1)
        with open('leaderboard.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            quick_sort(new_list)
            playing_player = True
            if len(new_list) < 10:
                rng = len(new_list)
            else:
                rng = 10
            for i in range(rng):
                a = new_list[i]
                if a == kek:
                    playing_player = False
                writer.writerow(new_list[i])
            if playing_player:
                writer.writerow(kek)
        with open('leaderboard.csv', 'r', newline='', encoding="utf8") as f:
            reader = csv.reader(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.ui.Leaderboard.setRowCount(0)
            for i, row in enumerate(reader):
                self.ui.Leaderboard.setRowCount(
                    self.ui.Leaderboard.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.ui.Leaderboard.setItem(
                        i, j, QTableWidgetItem(elem))
            self.leaderboard = new_list

        con.commit()

    def keyPressEvent(self, event):
        key_press_event_main(self, event, mixer, cur)

    def closeEvent(self, event):
        mixer.music.load('music/Toby Fox - Uwa! So Temperate♫.mp3')
        mixer.music.play(-1)
        if self.shmusic:
            mixer.music.set_volume(0.0)
        else:
            mixer.music.set_volume(self.music / 100)


class Settings(QMainWindow):
    def __init__(self, log, music, sound, bc):
        super(Settings, self).__init__()
        self.bc = bc
        self.log = log
        self.music, self.sound = music, sound
        self.ui = SettingsForm()
        self.ui.setupUi(self)
        a = cur.execute(f'SELECT shmusic, shsound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.shmusic, self.shsound = a[0], a[1]
        if self.shmusic:
            self.ui.slidermusic.setDisabled(True)
        else:
            self.ui.slidermusic.setDisabled(False)
        if self.shsound:
            self.ui.Slidersound.setDisabled(True)
        else:
            self.ui.Slidersound.setDisabled(False)
        self.ui.slidermusic.setValue(music)
        self.ui.Slidersound.setValue(sound)
        self.ui.bttutorial.clicked.connect(self.tutorial)
        self.ui.slidermusic.valueChanged.connect(self.dmusic)
        self.ui.slidermusic.sliderMoved.connect(self.dmusic)
        self.ui.Slidersound.valueChanged.connect(self.dsound)
        self.ui.Slidersound.sliderMoved.connect(self.dsound)
        self.ui.delak.clicked.connect(self.del_ak)
        self.ui.clearak.clicked.connect(self.clear_ak)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_db)
        self.timer.start(1000)

        self.tutor_form, self.choose_form = '', ''

    def tutorial(self):
        self.tutor_form = Tutorial()
        self.tutor_form.show()

    def dmusic(self):
        self.music = self.ui.slidermusic.value()
        if not self.shmusic:
            mixer.music.set_volume(self.music / 100)

    def dsound(self):
        self.sound = self.ui.Slidersound.value()
        if not self.shsound:
            click.set_volume(self.sound / 100)
            explosion.set_volume(self.sound / 100)
            buy.set_volume(self.sound / 100)

    def del_ak(self):
        self.choose_form = Check(self.log, DEL_AK, self.bc)
        self.choose_form.show()

    def clear_ak(self):
        self.choose_form = Check(self.log, CLEAR_AK, self.bc)
        self.choose_form.show()

    def keyPressEvent(self, event):
        key_press_event_main(self, event, mixer, cur)

    def update_db(self):
        cur.execute(f'UPDATE players\n'
                    f'SET music = {self.music}\n'
                    f'WHERE login = "{self.log}"')
        cur.execute(f'UPDATE players\n'
                    f'SET sound = {self.sound}\n'
                    f'WHERE login = "{self.log}"')
        a = cur.execute(f'SELECT shmusic, shsound FROM players'
                        f'  WHERE login = "{self.log}"').fetchone()
        self.shmusic, self.shsound = a[0], a[1]
        if self.shmusic:
            self.ui.slidermusic.setDisabled(True)
        else:
            self.ui.slidermusic.setDisabled(False)
        if self.shsound:
            self.ui.Slidersound.setDisabled(True)
        else:
            self.ui.Slidersound.setDisabled(False)
        con.commit()


class Check(QMainWindow):
    def __init__(self, log, lb, bc):
        super(Check, self).__init__()
        self.log = log
        self.lb = lb
        self.bc = bc

        self.ui = CheckForm()
        self.ui.setupUi(self)

        self.ui.label.setText(lb)
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.rejected.connect(self.cancel)

    def ok(self):
        pasw = cur.execute(f'SELECT password from players\n'
                           f'WHERE login = "{self.log}"').fetchone()[0]
        cur.execute(f'DELETE from players\n'
                    f'WHERE login = "{self.log}"')
        if self.lb == CLEAR_AK:
            a = f"INSERT INTO players" \
                f"(login,password,skin,unskins,money,moneyup,autoclick,energy,energyup," \
                f"music,sound, shsound, shmusic)" \
                f"VALUES('{self.log}','{pasw}',1,'1',0,1,0,100,1000,80,80,0,0)"
            cur.execute(a)
            con.commit()
            BClicker.update_lb(self.bc)
            BClicker.update_db(self.bc)
            BClicker.close(self.bc)
            self.close()
        else:
            con.commit()
            BClicker.close(self.bc)
        self.close()

    def cancel(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enter()
    ex.show()
    sys.exit(app.exec())
