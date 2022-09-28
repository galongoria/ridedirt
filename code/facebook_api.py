from datetime import datetime
import pandas as pd
import regex as re
import os, urllib.request, facebook
from dotenv import load_dotenv
from searches import get_fb_groups


RAW_DIR = os.path.join("data", "raw")
PICREF_DIR = os.path.join("data", "pictures_backup")
PIC_DIR = os.path.join("data", "pictures")
FB_GROUP_PATH = os.path.join(RAW_DIR, "facebook_group.csv")

load_dotenv()
token = os.getenv("token")


def get_fb_groups():

    return {
    'Antills': {'id':'534322359952442', 'location': '1001 S Dairy Ashford Rd, Houston, TX 77077'},
    'Cypress Creek Trails': {'id': '160122897466548', 'location' : '14234 W Cypress Forest Dr, Houston, TX 77070'},
    'Memorial Park Trails': {'id': '134220983339617', 'location': 'N Picnic Ln, Houston, TX 77007'},
    'Brazos River Trails': {'id': '157990614387212', 'location': '8125 Homeward Way, Sugar Land, TX 77479'},
    'Pearland MTB Trail': {'id': '768933773193257', 'location': 'Province Village Dr, Pearland, TX 77581'},
    'Fonteno Park Trails': {'id': '667149480730957', 'location': '14350 1/2 Wallisville Rd, Houston, TX 77049'},
    'League City Trails':{'id': '1417274005224393', 'location': '100 Alderwood St, League City, TX 77573'},
    'Bridgeland Trails': {'id': '1034914603303904', 'location': '18310 House Hahl Rd, Cypress, TX 77433'},
    'Chisenhall Trails': {'id':'579687176161531', 'location': '500 W Hidden Creek Pkwy, Burleson, TX 76028'},
    }

def get_group_picture(group_id):

    """Input the Facebook Group ID and output the picture url, group name, and time of request"""

    graph = facebook.GraphAPI(access_token=token, version=3.1)
    name = re.sub(r"\s", "_", graph.request(f"/{group_id}/")["name"])
    pic = graph.request(f"/{group_id}/picture?type=large")["url"]
    datetime_string = datetime.now().strftime("%y_%m_%d_%H_%M")
    return name, datetime_string, pic

def save_image(name, datetime_string, pic):

    """Input the name and datetime to save as the directory and file name for the inputted picture"""

    os.makedirs(os.path.join(PIC_DIR, f"{name}"), exist_ok=True)
    urllib.request.urlretrieve(
    pic, os.path.join(PIC_DIR, f"{name}", f"{datetime_string}.jpg"))
    return os.path.abspath(os.path.join(PIC_DIR, f"{name}", f"{datetime_string}.jpg"))

def compare_picture(abspath, trail_name):

    """Compares the picture with reference pictures that indicate a trail is open or closed.
        Outputs the trail status.

    """
    for ref_pic_name in os.listdir(os.path.join(PICREF_DIR, trail_name)):
        ref_pic = open(os.path.join(PICREF_DIR, trail_name, ref_pic_name), 'rb').read()
        pic = open(abspath, 'rb').read()
        if pic == ref_pic:
            if 'open' in ref_pic_name:
                return 'open'
            elif 'closed' in ref_pic_name:
                return 'closed'
        else:
            status = 'no_match'
    return status

def compare_all():

    """Gets pictures and runs the compare method for every group in the dictionary"""

    group_dict = get_fb_groups()
    d = {}

    for trail, value in group_dict.items():
        print(f'Looking at {trail}')
        try:
            name, datetime_string, pic = get_group_picture(str(value['id']))
            abspath = save_image(name, datetime_string, pic)
            d[name] = compare_picture(abspath, name)
        except facebook.GraphAPIError as error:
            d[name] = 'check_id'
    return d

def get_static():

    """Gets information for static columns"""

    group_dict = get_fb_groups()
    l = []

    for trail, value in group_dict.items():
        print(f'Looking at {trail}')
        try:
            name, datetime_string, pic = get_group_picture(str(value['id']))
            l.append((trail, name, value['id'], f'https://www.facebook.com/groups/{value["id"]}',value['location'],''))
        except facebook.GraphAPIError as error:
            print('!!! Check_id !!!')
    return l



