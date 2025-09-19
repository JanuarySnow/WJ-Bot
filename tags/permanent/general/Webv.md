## Install/Repair WebView2
Please install/repair WebView2 by following the following steps

Repair WebView2 using the Evergreen Bootstrapper found [here](https://developer.microsoft.com/en-us/microsoft-edge/webview2#download)

If the installation fails with:
`Installation failed. Microsoft Edge WebView2 Runtime is already been installed for the system.`

Remove remnants of the broken WebView2 first:

1. Press Windows key + R, type regedit, and press Enter to open the Registry Editor.  Click Yes if you receive a elevated prompt from 'User Account Control'.
2. Copy the following string
    `HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}`
3. Go to Registry Editor address bar, clear it, paste above string and press Enter.
4. Right-click the key `{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}` and choose Export.
5. Save the Export the WebView2 registry key to a file where you can restore it from in case of issues.
6. Now right click and delete the key instead of exporting, and try running the Evergreen Bootstrapper again.
