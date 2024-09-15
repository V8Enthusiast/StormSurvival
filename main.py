from app import App

if __name__ == '__main__':
    try:
        game = App(1000, 800, False, False)
        game.run()
    except:
        pass

#tests