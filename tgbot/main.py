from os import getenv
from handlers.handler import bot
from helpers.api import TGAdminAPI


def exists_director() -> bool:
    director_id: int = int(getenv('TG_DIRECTOR_ID'))

    admins = TGAdminAPI.get_tg_admins()
    if admins:
        for admin in admins:
            if admin['user_id'] == director_id:
                return True

    return TGAdminAPI.create_tg_admin({
        'user_id': director_id,
        'name': getenv('TG_DIRECTOR_USERNAME'),
        'can_appoint': True
    }) is not None


if __name__ == "__main__":
    if getenv('TG_TOKEN') is None:
        print("TG_TOKEN not found in .env")
        exit(0)

    if not exists_director():
        print("Can't create director in server")
        exit(0)

    bot.infinity_polling()
