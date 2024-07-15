import POST
import telebot
import time
import ASSIST
VIDEO_TOKEN = "vk1.a.7xYmZdr0bdBfwmAAbi66x0U8-rKgAE4hTfqvBDCk6dq2eoE4ZWCe93uohsYjFpWWMYXPPQjU6ldhyxzsEWmWL4TasnL4oiNrnzxmWhV0W8aIXM8D5IobacSAD-SZYuzMpfK-eiOPPZKhfBR5WTQqQd1Abf5fvelMdS60UkBfUynq8e1-0gPdmoAXK5TbF71oJfjXDXACRD5hl-Ewx-2IGA"
TOKEN_USER="vk1.a.ZoTtsX4iCL6-uHryL09mdes3XJv_UiYIufPRIgGMdBosWOuR9aTdWBOSsfm7ltMon2-k0wL6OkOoYO5qh6I5BLLEYCeCrWVh78nHW4UYK8DqRHSvUW0BRVuboN5zmBWzbZcu0OtpnjvOP2mBQDcN0UJxEMHncr01h-gJQhb8fraNYjXNpCU-BrmPyhFwsdhkTJs9l2PsIm7fCLmayX8TEg"
VERSION = "5.131"
DOMAIN = "chill_capybaras"
chat_id = "@FALLOUT1488"
TOKEN = "6235128854:AAHgq9C5aax9JumFiawqZfMg1sDV1t_zPvs"
bot = telebot.TeleBot(TOKEN)

post = POST.Get(TOKEN_USER, VIDEO_TOKEN, VERSION, DOMAIN, 1, 2)
with open("sent.txt", "r") as st:
    st = st.read().strip()
print("START")


while True:
    index = int(input())
    post1 = POST.Get(TOKEN_USER, VIDEO_TOKEN, VERSION, DOMAIN, index, 100)
    if post1 != "1488":
        post = post1
    if str(st) == str(post.get_id()):
        ...
    else:
        print("ENTR")
        if post.no_ad() is False:
            st = ASSIST.write(post.get_id())
            continue
        pics = post.get_pics()
        text = post.get_text()
        vid = post.get_videos()
        poll = post.check_for_poll()
        media = post.get_post(text, pics)
        bot.send_video(chat_id=chat_id, video=open(vid, 'rb'), caption=text, timeout=1000)
                
        os.remove(vid)
        try:
            if poll is True:
                text += "\n\n\n проголосовать можно здесь \n {}".format(post.get_link())
                media = post.get_post(text, pics)

            if len(media) != 0:
                bot.send_media_group(chat_id=chat_id, media=media)
                ...
            elif vid is not None:
                               
                bot.send_video(chat_id=chat_id, video=open(vid, 'rb'), caption=text, timeout=1000)
                
                os.remove(vid)
                ...
            elif text and poll:
                bot.send_message(text=text, chat_id=chat_id)

        except:
            pass

        st = ASSIST.write(post.get_id())
        print("111")
    time.sleep(1)
