# Zwift to SportTracks sync

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

[SportTracks.mobi](https://sporttracks.mobi) cannot pull activities directly from [Zwift](https://zwift.com). 

This Python script downloads the latest Zwift acitivities to your computer and uploads them to SportTracks.mobi. The solution is quite inelegant since I cannot get the SportTracks.mobi API to work (to make matters worse, their API documentation website has been removed). 

There is no duplicate checking before uploading to SportTracks. By default the script downloads the 10 latest activities from Zwift. Any one of those activities that are not already downloaded are uploaded to SportTracks.mobi. If there are more than 10 FIT files in your directory, the oldest ones are deleted.

## Setup
- Install [Zwift Mobile API Client](https://github.com/jsmits/zwift-client) into your env by `pip install zwift-client`.
- Rename `servicesconfig_example.py` to `servicesconfig.py`
- Edit your information in the config file. You can find your Zwift player ID by visiting [https://zwift.com/feed]() and clicking on one of your activities. Press the cog icon and hover over the `Download FIT file` button. The URL format should be something like `amazonaws.com/prod/55555/...` where `55555` would be your player ID.

## Usage
`python main.py` runs the script with default values. It downloads the 10 newest activities from Zwift and uploads them to SportTracks.mobi.

`python main.py --count 5 --upload true` downloads the 5 newest activities and uploads every activity that is not found on your hard drive to SportTracks. `--count` accepts any int (haven't checked what happens if you choose something far greater than your amount of Zwift activities) and `--upload` is a boolean that accepts `true` or `false` (or yes/no/1/0).

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
    <string>my sensible launchagent name</string>
    <key>WorkingDirectory</key>
        <string>path to working directory</string>
    <key>ProgramArguments</key>
    <array>
        <string>path to python env bin</string>
        <string>path to script main.py</string>
        <string>--count</string>
        <string>10</string>
        <string>--upload</string>
        <string>true</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
</dict>
</plist>
```
