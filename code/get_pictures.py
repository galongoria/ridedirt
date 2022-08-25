from datetime import datetime
import pandas as pd
import regex as re
import os, urllib.request, facebook
from dotenv import load_dotenv
from searches import get_fb_groups

load_dotenv()
token = os.getenv("token")

RAW_DIR = os.path.join("data", "raw")
PIC_DIR = os.path.join("data", "pictures")
FB_GROUP_PATH = os.path.join(RAW_DIR, "facebook_group.csv")


def get_group_picture(group_id):

    graph = facebook.GraphAPI(access_token=token, version=3.1)
    name = re.sub(r"\s", "_", graph.request(f"/{group_id}/")["name"])
    pic = graph.request(f"/{group_id}/picture?type=large")["url"]
    datetime_string = re.sub(r"[\/\s]", "_", datetime.now().strftime("%m_%d_%Y_%H_%M"))
    os.makedirs(os.path.join(PIC_DIR, f"{name}"), exist_ok=True)
    urllib.request.urlretrieve(
        pic, os.path.join(PIC_DIR, f"{name}", f"{datetime_string}.jpg")
    )


def get_all_group_pictures():

    group_dict = get_fb_groups()
    id_list = list(get_fb_groups().values())
    trails = list(get_fb_groups().keys())

    for n, group_id in enumerate(id_list):
        print(trails[n])
        try:
            get_group_picture(str(group_id))
        except facebook.GraphAPIError:
            print(f'Need Permission for {trails[n]}.')



if __name__ == "__main__":

    get_all_group_pictures()
