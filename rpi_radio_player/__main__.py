import cProfile

from rpi_radio_player import app

if __name__ == '__main__':
    cProfile.run('app.run()')
