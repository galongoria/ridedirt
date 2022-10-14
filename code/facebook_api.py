from datetime import datetime
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
                return "Everything's open!"
            elif 'closed' in ref_pic_name:
                return 'Trails are too muddy today.'
        else:
            status = 'No match.'
    return status

def compare_all():

    """Gets pictures and runs the compare method for every group in the dictionary"""

    group_dict = get_fb_groups()
    db_list = []

    for trail, options in group_dict.items():
        if options['group_photo']:
            print(f'Looking at {trail}')
            try:
                name, datetime_string, pic = get_group_picture(str(options['id']))
                abspath = save_image(name, datetime_string, pic)
                status = compare_picture(abspath, name)
                
            except facebook.GraphAPIError as error:
                status = 'check parameters'
            db_list.append((trail, name, options['id'], f'https://www.facebook.com/groups/{options["id"]}',options['location'],status, datetime.now()))
    return db_list


