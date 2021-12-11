# Zwift to SportTracks sync

[SportTracks.mobi](https://sporttracks.mobi) cannot connect directly to [Zwift](https://zwift.com). 

This script downloads the latest Zwift acitivities to your computer and uploads them to SportTracks.mobi. The solution is quite inelegant since I cannot get the SportTracks.mobi API to work (to make matters worse their API documentation website has been removed). 

There is no duplicate checking before uploading to SportTracks. By default the script downloads the 10 latest activities from Zwift. Any one of those activities that are not already downloaded are uploaded to SportTracks.mobi. If there are more than 10 FIT files in your directory, the oldest ones are deleted.

## Setup
- Install [Zwift Mobile API Client](https://github.com/jsmits/zwift-client) into your env by `pip install zwift-client`.
- Rename `servicesconfig_example.py` to `servicesconfig.py`
- Edit your information in the config file. You can find your Zwift player ID by visiting [https://zwift.com/feed]() and clicking on one of your activities. Press the cog-icon and hover over the `Download FIT file` button. The URL format should be something like `amazonaws.com/prod/55555/...` where `55555` would be your player ID.

## Automation
I have set up a LaunchAgent on my Mac to run this script every hour (using the correct Python environment).

Some information on how to set up LaunchAgent using `launchctl` 2.0 is available here: [https://babodee.wordpress.com/2016/04/09/launchctl-2-0-syntax/]()

My launchagent `.plist`-file, for reference 👇 
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>some sensible name</string>
    <key>WorkingDirectory</key>
    <string>path to working directory</string>
    <key>ProgramArguments</key>
    <array>
        <string>path to python env bin</string>
        <string>path to script main.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
</dict>
</plist>
```