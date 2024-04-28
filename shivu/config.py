class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6995317382"
    sudo_users = "6995317382"
    GROUP_ID = -1002073720399
    TOKEN = "6794919354:AAG7In_R-ihk__GRnarRuc-5Xnw0KUJRicE"
    mongo_url = "mongodb+srv://osmon:m6KSjDgWc8kD5Aac@cluster0.mibzqh9.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://te.legra.ph/file/9f81d51fcc0cf0284a99f.jpg","https://te.legra.ph/file/9f81d51fcc0cf0284a99f.jpg"]
    SUPPORT_CHAT = "PokemonUniteGC"
    UPDATE_CHAT = "chuTiyaSupport"
    BOT_USERNAME = "graBxWaifuRobot"
    CHARA_CHANNEL_ID = "-1002111937813"
    api_id = 26626068
    api_hash = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
