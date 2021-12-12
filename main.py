import os
import requests
from lxml import html           # type: ignore
from zwift import Client        # type: ignore
import servicesconfig as cfg

# login to Zwift and get user's activities
client = Client(cfg.zwift["user"], cfg.zwift["pass"])
activity = client.get_activity(cfg.zwift["player_id"])


def upload_fit(filename):
    # uploads filename.fit to SportTracks.mobi

    login_payload = {
        'name': cfg.sporttracks["user"],
        'pass': cfg.sporttracks["pass"],
        'form_id': 'user_login'
    }


    with requests.Session() as s:
        # creates a web session and sends login details to SportTracks
        # every login page has a unique form_build_id that we have to get
        login_page = s.get('https://sporttracks.mobi/login')
        login_tree = html.fromstring(login_page.content)
        login_form_build_id = login_tree.xpath(
            '//input[@name="form_build_id"]')[0].get("value")
        login_payload["form_build_id"] = login_form_build_id

        p = s.post('https://sporttracks.mobi/login', data=login_payload)

        # first we get the import page from SportTracks to find the
        # form_build_id and form_token. Then we upload filename.fit
        # to SportTracks using our form_build_id and form_token
        import_page = s.get('https://sporttracks.mobi/activity/import')
        import_tree = html.fromstring(import_page.content)
        import_form_build_id = import_tree.xpath(
            '//input[@name="form_build_id"]')[0].get("value")
        import_form_token = import_tree.xpath(
            '//input[@name="form_token"]')[0].get("value")

        import_payload = {
            'form_build_id': import_form_build_id,
            'form_token': import_form_token,
            'form_id': "sporttracks_base_form_delegate"
        }

        file = {'files[import-file]': open(filename, 'rb')}

        p2 = s.post("https://sporttracks.mobi/activity/import",
                    files=file, data=import_payload)

        # next two lines are for debugging
        # with open("output.html", "w") as outfile:
        #     outfile.write(p2.text)

        print(f"Uploaded {filename} to SportTracks")


def write_fit_files(count, upload):
    # writes the count newest activities to activities directory
    # if upload == True then any activity not found in activities 
    # directory is uploaded to SportTracks

    # create a list of count last activities
    activities = activity.list(start=0, limit=count)

    # chdir to activities
    if not os.path.exists("activities"):
        os.mkdir("activities")
    os.chdir("activities")


    existing_files = os.listdir()
    for act in activities:
        # for every activity find the start date and time. Write activity to 
        # directory if file does not alredy exist and upload to SportTracks
        # if upload == True
        mytime = act['startDate'][:19].replace(":", "-").replace("T", "-")
        if ((mytime + ".fit") not in existing_files):
            activity.write_FIT(act['id'], mytime)
            if upload:
                upload_fit(mytime + ".fit")

    os.chdir("..")


def delete_old(n):
    # deletes the n oldest activities in activities dir
    
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
    from distutils.util import strtobool

    parser = argparse.ArgumentParser(description="Dowloads activities from"
                                     + " Zwift and uploads them to Sporttracks.mobi")

    parser.add_argument("--count", type=int, default=10, help="int. Number"
                        + " of (newest) activities to download")
    parser.add_argument("--upload", type=str, default="true", help="bool. true"
                        + " or false. Do you want to upload to SportTracks?")

    args = parser.parse_args()

    write_fit_files(args.count, strtobool(args.upload))
    delete_old(args.count)
