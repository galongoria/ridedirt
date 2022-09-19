from datetime import datetime
import pandas as pd
import regex as re
import os, urllib.request, facebook
from dotenv import load_dotenv
from searches import get_fb_groups
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://username:password@localhost:5432/ridedirt')

base = declarative_base()

class Trail(base):


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

    return name, datetime_string, pic


def get_all_group_pictures(local):

    group_dict = get_fb_groups()
    # id_list = list(get_fb_groups().values())
    # trails = list(get_fb_groups().keys())

    for trail, group_id in group_dict.keys():
        print(trail)
        try:
            name, datetime_string, pic = daget_group_picture(str(group_id))
        except facebook.GraphAPIError:
            print(f'Need Permission for {trail}.')

        if local:

            os.makedirs(os.path.join(PIC_DIR, f"{name}"), exist_ok=True)
            urllib.request.urlretrieve(
                pic, os.path.join(PIC_DIR, f"{name}", f"{datetime_string}.jpg")
                )
        else:
            with orm.db_session:
                for item in data:
                    Trail(name=name, price=)
