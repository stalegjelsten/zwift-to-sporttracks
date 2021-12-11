from distutils.util import strtobool
from email import parser
import os
import requests
from zwift import Client
from lxml import html
import servicesconfig as cfg


client = Client(cfg.zwift["user"], cfg.zwift["pass"])

activity = client.get_activity(cfg.zwift["player_id"])

def upload_fit(filename):

    login_payload = {
        'name': cfg.sporttracks["user"],
        'pass': cfg.sporttracks["pass"],
        'form_id': 'user_login'
    }

    with requests.Session() as s:
        login_page = s.get('https://sporttracks.mobi/login')
        tree = html.fromstring(login_page.content)
        form_build_id = tree.xpath('//input[@name="form_build_id"]')[0].get("value")
        login_payload["form_build_id"] = form_build_id

        p = s.post('https://sporttracks.mobi/login', data=login_payload)

        import_page = s.get('https://sporttracks.mobi/activity/import')

        tree = html.fromstring(import_page.content)
        form_build_id = tree.xpath('//input[@name="form_build_id"]')[0].get("value")
        form_token = tree.xpath('//input[@name="form_token"]')[0].get("value")

        import_payload = {
            'form_build_id': form_build_id, 
            'form_token': form_token,
            'form_id': "sporttracks_base_form_delegate"
        }
        fil = {'files[import-file]': open(filename, 'rb')}

        p2 = s.post("https://sporttracks.mobi/activity/import", files=fil, data=import_payload)

        # next two lines are for debugging
        # with open("output.html", "w") as outfile:
        #     outfile.write(p2.text)

        print(f"Uploaded {filename} to SportTracks")
       


def write_fit_files(count, upload):
    activities = activity.list(start=0, limit=count)
    if not os.path.exists("activities"):
        os.mkdir("activities")
    os.chdir("activities")

    existing_files = os.listdir()
    for act in activities:
        mytime = act['startDate'][:19].replace(":", "-").replace("T", "-")
        if ((mytime + ".fit") not in existing_files):
            activity.write_FIT(act['id'], mytime)
            if upload:
                upload_fit(mytime + ".fit")
    
    os.chdir("..")


def delete_old(n):
    os.chdir("activities")
    existing_files = os.listdir()
    num_files = len(existing_files)
    if num_files > 10:
        i = 1
        for file in existing_files:
            if num_files - i > n:
                os.remove(file)
            i += 1
    
    os.chdir("..")


if __name__ == "__main__":
    import argparse
 
    parser = argparse.ArgumentParser(description="Dowloads activities from"\
        + " Zwift and uploads them to Sporttracks.mobi")

    parser.add_argument("--count", type=int, default=10, help="int. Number of (newest) activities to download")
    parser.add_argument("--upload", type=str, default="True", help="bool. True or False. Do you want to upload to SportTracks?")

    args = parser.parse_args()


    

    write_fit_files(args.count, strtobool(args.upload))
    delete_old(args.count)

