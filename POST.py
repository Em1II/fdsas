import requests
import urllib.request
import time
import ASSIST
import telebot
import requests
import youtube_dl

class Get:

    def __init__(self, TOKEN_USER, VIDEO_TOKEN, VERSION, DOMAIN, index, count):
        self.post = "1488"
        self.token = TOKEN_USER
        self.v = VERSION
        self.video_token = VIDEO_TOKEN
        for attmpt in range(25):
            response = requests.get('https://api.vk.com/method/wall.get',
                params={'access_token': TOKEN_USER,
                'v': VERSION,
                'domain': DOMAIN,
                'count': count,
                })
            try:
                self.post = response.json()['response']['items'][index]
                break
            except:
                print(response.json())
                time.sleep(20)
        print(self.post)
    def get_comments(self):
        response = requests.get('https://api.vk.com/method/wall.getComments',
                params={'access_token': self.token,
                'owner_id':self.get_owner_id(),
                "post_id":self.get_id(),
                'count': 1,
                'v': self.v,})
        return response.json()["response"]["items"]

    def get_owner_id(self):
        return self.post["from_id"]
    def get_comlink(self):
        comms = self.get_comments()
        owner_id = self.get_owner_id()
        for com in comms:
            if com["from_id"] == owner_id:
                link = com["text"]
                break
        return link
    def check_for_poll(self):
        attchs = self.post["attachments"]
        for att in attchs:
            if att["type"] == "poll":
                return True
        return False
    def get_link(self):
        return f"https://vk.com/chill_capybaras?w=wall{self.get_owner_id()}_{self.get_id}"
    def get_id(self):
        return self.post['id']
    def get_market(self):
        attchs = self.post["attachments"]
        info = ""
        for att in attchs:
            if att["type"] == "market":
                info = (str(att["market"]["owner_id"]) + "_" + str(att["market"]["id"]))
        return info
    def get_post(self, text, pics=[], video=[]):
        media = []
        for index, image in enumerate(pics):
            media.append(telebot.types.InputMediaPhoto(image.read(), caption = text if index == 0 else '', parse_mode='HTML'))
        for index, v in enumerate(video):
            media.append(telebot.types.InputMediaVideo(v.read(), caption = text if index == 0 else '', parse_mode='HTML'))
        
        return media
    def get_pics(self):
        attchs = self.post["attachments"]
        pics = []
        for att in attchs:
            if att["type"] == "photo":
                x = ""
                y = ""
                z = ""
                m = ""
                for size in att["photo"]["sizes"]:
                    if size["type"] == "z":
                        z = (urllib.request.urlopen(size["url"]))
                    elif size["type"] == "y":
                        y = (urllib.request.urlopen(size["url"]))
                    elif size["type"] == "x":
                        x = urllib.request.urlopen(size["url"])
                    elif size["type"] == "m":
                        m = urllib.request.urlopen(size["url"])
                if z != "":
                    pics.append(z)
                elif x != "":
                    pics.append(x)
                elif y != "":
                    pics.append(y)
                elif m != "":
                    pics.append(m)
                

        return pics

    def get_text(self):
        text = self.post["text"]
        return text

    def is_link_in_com(self):
        if ASSIST.comm_assist(self.get_text().lower().split()):
            try:
                link = self.get_comlink()
                if "http" in link:
                    return True
            except:
                pass
        return False

    def is_market(self):
        mrkt = self.get_market()

        if mrkt != "":
            return True
        return False
    def get_from_id(self):
        return self.post["owner_id"]
    def no_repost(self):
        return self.get_from_id() == self.get_owner_id()
    def no_ad(self):

        if self.is_link_in_com() is False and self.is_market() is False and ASSIST.link_assist(self.get_text().split()) is True and self.post['marked_as_ads'] != 1 and self.no_repost():
            return True
        return False
    def get_conncret_video(self, id, owner_id):
        response = requests.get('https://api.vk.com/method/video.get',
                params={'access_token': self.video_token,
                'owner_id': owner_id,
                'videos':f"{owner_id}_{id}",
                "count":3,
                'v': self.v,})
        return response.json()["response"]["items"][0]["player"]
    def get_videos(self):
        attchs = self.post["attachments"]
        url = None
        for att in attchs:
            if att["type"] == "video":
                title = att["video"]["title"]
                url = self.get_conncret_video(att["video"]["id"],att["video"]["owner_id"])
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                url = f'{title}-{str(att["video"]["owner_id"])}_{att["video"]["id"]}.mp4'

        return url
        




