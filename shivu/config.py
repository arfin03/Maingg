class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6783092268"
    sudo_users = "6783092268"
    GROUP_ID = -1002095006471
    TOKEN = "6956301291:AAE6amoBvaKj9Dc1Kaz8bXFjdbqQNKvI194"
    mongo_url = "mongodb+srv://xjie276:sUF$e7pzitFXCGH@cluster0.ecfztel.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "zekauu"
    UPDATE_CHAT = "zekauu"
    BOT_USERNAME = "TheGreatLevi2Robot"
    CHARA_CHANNEL_ID = "-1002095006471"
    api_id = 28213805
    api_hash = "8f80142dfef1a696bee7f6ab4f6ece34"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
