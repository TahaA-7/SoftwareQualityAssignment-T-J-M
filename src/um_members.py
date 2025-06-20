from presentation_layer.home import Home
from DB_Startup import DB_Startup

if __name__ == '__main__':
    DB_Startup.startup()
    Home.start()
