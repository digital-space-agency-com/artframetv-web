"""Build the Art Frame TV guides hub.

Every article here is pinned to a query with real US volume from DataForSEO
(via OpenSEO, Oct 2026). Volumes and difficulty are in ARTICLES below so the
targeting is auditable rather than guessed.
"""
import os, sys, html, re

OUT = sys.argv[1]
SITE = "https://getframetv.com"

ARTICLES = [
 dict(
  slug="google-tv-screensaver",
  kw="android tv screensaver", vol=390, kd=2,
  updated="2026-11-05",
  title="Change the screensaver on Google TV (2026)",
  desc="Three ways to change the screensaver on Google TV or Android TV, including how to use a third-party screensaver that Ambient Mode normally blocks.",
  intro="""Google TV and Android TV handle screensavers differently, and the setting most
people look for — pick any installed app as the screensaver — is hidden on Google TV. Here is
what works on each, in order of how much effort it takes.""",
  sections=[
   ("Google TV: Ambient Mode is the screensaver", """<p>On Google TV there is no "screensaver"
   menu. What idles on screen is <strong>Ambient Mode</strong>, and Google reserves it for its own
   sources.</p>
   <p>Go to <strong>Settings → System → Ambient mode → Source</strong>. You get three choices:
   Google Photos, Art gallery (Google's own curated set), and an Experimental option. Third-party
   apps do not appear in that list, which is the single most common reason people conclude their
   screensaver app is broken when it is installed correctly.</p>"""),
   ("Android TV: the classic screensaver menu", """<p>Older Android TV builds keep the standard
   Android daydream picker. Go to <strong>Settings → Device Preferences → Screen saver</strong>.
   Any installed app that registers a <code>DreamService</code> shows up here, so you can select it
   directly. You can also set how long the TV waits before it starts.</p>"""),
   ("Using a third-party screensaver on Google TV", """<p>Two routes work, and neither requires
   rooting the TV.</p>
   <h3>A launcher that exposes the setting</h3>
   <p>Replacement launchers such as <strong>Projectivy Launcher</strong> or <strong>FLauncher</strong>
   add a screensaver override that Google TV itself does not offer. Install one, then look for
   <strong>Settings → Screensaver Override</strong> and pick the app you want.</p>
   <h3>One ADB command</h3>
   <p>If you would rather not change launcher, you can set it once over ADB. First enable developer
   options: <strong>Settings → System → About</strong>, then click <strong>Android TV OS build</strong>
   seven times. Then turn on <strong>Wireless debugging</strong> under Developer options, and from
   a computer on the same network:</p>
   <p>Wireless debugging has to be paired with your computer once before it will connect, and the
   port is not 5555. The step-by-step version, with the commands and the fixes for the errors people
   hit, is in <a href="/articles/set-up-art-frame-tv">How to set up Art Frame TV as your screensaver</a>.
   The command that does the work is:</p>
   <pre><code>adb shell settings put secure screensaver_components team.dsa.artframetv/.service.ArtFrameDreamService
adb shell settings put secure screensaver_enabled 1</code></pre>
   <p>This survives reboots. It does not always survive a system update, so keep the command
   somewhere you can find it again.</p>"""),
   ("Turning the screensaver off", """<p>On Google TV, <strong>Settings → System → Ambient mode</strong>
   and set the timer to Off, or set the source to something you do not mind seeing. On Android TV,
   <strong>Settings → Device Preferences → Screen saver → When to start</strong> and choose Never.
   Note that many TVs have a separate panel-level sleep timer; turning off the screensaver does not
   stop the TV switching itself off.</p>"""),
  ],
  faq=[
   ("Why can't I select my screensaver app on Google TV?",
    "Google TV replaced the Android screensaver picker with Ambient Mode, which only accepts Google Photos, Google's Art gallery, or the experimental source. Third-party apps are not listed. Use a launcher with a screensaver override, such as Projectivy or FLauncher, or set it once over ADB."),
   ("How do I change the screensaver on Android TV?",
    "Settings → Device Preferences → Screen saver. Any installed app that provides a DreamService appears in the list, and you can also set the idle delay there."),
   ("Does changing the screensaver over ADB survive a reboot?",
    "Yes. The setting is written to secure settings and persists across restarts. It can be reset by a system update, in which case you run the same command again."),
   ("Can I use my own photos as the screensaver?",
    "Yes. On Google TV, set the Ambient mode source to Google Photos and choose an album. On Android TV, install a photo screensaver app and select it in the Screen saver menu."),
  ]),
 dict(
  slug="set-up-art-frame-tv",
  kw="set up art frame tv screensaver", vol=0, kd=0,
  updated="2026-11-06", picker=True,
  title="How to set up Art Frame TV as your screensaver",
  desc="Step-by-step setup for Art Frame TV on Google TV and Android TV: the no-computer launcher route, the ADB route with pairing, and fixes for the errors people actually hit.",
  intro="""Installing Art Frame TV takes a minute. Making it the screensaver takes one extra step,
because Google TV keeps its own Ambient Mode in the way. This guide covers every route, starting
with the ones that need no computer, and the fixes for the errors that stop people on the ADB route.""",
  sections=[
   ("Which route do you need?", """<p>Install <strong>Art Frame TV</strong> from Google Play on the TV
   and open it once. Then check <strong>Settings → Device Preferences → Screen saver</strong>.</p>
   <ul>
   <li><strong>Art Frame TV is in that list:</strong> select it. You are done.</li>
   <li><strong>There is no Screen saver menu, only Ambient mode (most Google TV devices):</strong>
   Google does not let Ambient mode use other apps. Use a launcher (route 1) or ADB (route 2).</li>
   </ul>
   <p>Use <strong>version 1.0.5 or later</strong>. Earlier versions close the screensaver the moment it
   starts, so update from Google Play first.</p>
   <p>You never have to set the screensaver up to use the app. It works fully from its own icon;
   the screensaver is for when you want the frame to appear by itself once the TV goes idle.</p>"""),
   ("Route 1: a launcher with Screensaver Override", """<p>No computer, no terminal, and no pairing. Replacement
   launchers such as <strong>Projectivy Launcher</strong> or <strong>FLauncher</strong> add the
   screensaver choice that Google TV hides.</p>
   <ol>
   <li>Install the launcher from Google Play and make it the home screen when asked.</li>
   <li>Open its settings and find <strong>Screensaver Override</strong>.</li>
   <li>Choose <strong>Art Frame TV Screensaver</strong>.</li>
   </ol>
   <p>The trade-off is that you are changing your home screen. If you would rather not, use route 2.</p>""", "launcher"),
   ("Route 2: ADB over Wi-Fi", """<p>ADB is Android's developer tool. You run it once, on a computer that is on the
   same Wi-Fi network as the TV, and the setting then stays on the TV.</p>

   <h3>1. Install ADB on your computer</h3>
   <p>ADB ships in Google's <strong>platform-tools</strong>. Run the line for your system in a terminal<span data-os="win">
   (open <strong>PowerShell</strong> from the Start menu)</span><span data-os="mac"> (open <strong>Terminal</strong>
   from Launchpad or Spotlight)</span>:</p>
   <pre data-os="mac"><code>brew install --cask android-platform-tools</code></pre>
   <pre data-os="win"><code>winget install Google.PlatformTools</code></pre>
   <pre data-os="linux"><code>sudo apt install adb</code></pre>
   <p>Open a <strong>new</strong> terminal window and check it worked:</p>
   <pre><code>adb version</code></pre>
   <p>If you see <code data-os="mac linux">command not found: adb</code><code data-os="win">'adb' is not recognized</code>,
   see the fixes below.</p>
   <p data-os="win"><strong>Windows without winget:</strong> download <em>SDK Platform-Tools for Windows</em> from
   <a href="https://developer.android.com/tools/releases/platform-tools" rel="noopener">developer.android.com/tools/releases/platform-tools</a>,
   right-click the zip and choose <strong>Extract All</strong>, then open the extracted
   <code>platform-tools</code> folder, click its address bar, type <code>powershell</code> and press Enter.
   In that window, put <code>.\\</code> in front of every <code>adb</code> command in this guide, for example
   <code>.\\adb version</code>.</p>

   <h3>2. Turn on Wireless debugging on the TV</h3>
   <p>Go to <strong>Settings → System → About</strong> and click <strong>Android TV OS build</strong>
   seven times. Developer options now appear under <strong>Settings → System</strong>. Open them and
   turn on <strong>Wireless debugging</strong>.</p>

   <h3>3. Pair (once)</h3>
   <p>Wireless debugging will not talk to a computer until the two are paired. On the TV, open
   <strong>Wireless debugging → Pair device with pairing code</strong>. A dialog shows an address with a
   port, and a six-digit code. Keep it open, and on the computer run:</p>
   <pre><code>adb pair 192.168.1.50:37215 123456</code></pre>
   <p>Use <strong>your</strong> address, port and code from the dialog; the numbers above are examples.
   Do not type the angle brackets or placeholder words from other guides. You should see
   <code>Successfully paired</code>. The port and code are temporary: they change every time the dialog opens.</p>

   <h3>4. Connect</h3>
   <p>Close the pairing dialog. The main Wireless debugging screen shows
   <strong>IP address &amp; Port</strong>, a different port from the pairing one. It is not 5555.</p>
   <pre><code>adb connect 192.168.1.50:41234
adb devices</code></pre>
   <p>The device should be listed as <code>device</code>. If the TV asks <strong>Allow debugging?</strong>,
   accept it.</p>

   <h3>5. Set the screensaver</h3>
   <pre><code>adb shell settings put secure screensaver_components team.dsa.artframetv/.service.ArtFrameDreamService
adb shell settings put secure screensaver_enabled 1</code></pre>
   <p>Check that it stuck:</p>
   <pre><code>adb shell settings get secure screensaver_components</code></pre>
   <p>That should print <code>team.dsa.artframetv/.service.ArtFrameDreamService</code>. To see it
   straight away, use <strong>Start now</strong> in your TV's screensaver menu (on Google TV it is
   under <strong>Ambient screensaver</strong>). If Start now does nothing, go to the next section.</p>
   <p>The setting survives restarts. A system update can reset it, in which case run the two
   <code>settings put</code> lines again. To undo it, run
   <code>adb shell settings delete secure screensaver_components</code>.</p>""", "adb"),
   ("If Start now does nothing (TCL and some other brands)", """<p>Some manufacturers add their own gatekeeper that refuses to start any app in the background
   unless it has been given an <strong>auto-start</strong> permission. The screensaver is exactly that:
   the TV starts it for you. TCL TVs do this, and so can others. The signs are that the settings above
   are correct, Start now does nothing, and the screensaver never appears when the TV idles.</p>
   <p>With ADB connected (steps 1 to 4), grant the permission:</p>
   <pre><code>adb shell appops set team.dsa.artframetv AUTO_START allow
adb shell appops get team.dsa.artframetv AUTO_START</code></pre>
   <p>The second command should print <code>AUTO_START: allow</code>. Then press <strong>Start now</strong>
   again. If the TV answers <em>Unknown operation</em>, it has no such permission and this is not your problem.
   Look in the TV's own settings for an <strong>Auto-start</strong> or <strong>App permissions</strong> screen
   and allow Art Frame TV there.</p>
   <p>If you are comfortable reading logs, this confirms the diagnosis. Run
   <code>adb logcat -c</code>, press Start now, then <code data-os="mac linux">adb logcat -d | grep -i "forbid bind"</code><code data-os="win">adb logcat -d | Select-String "forbid bind"</code>.
   A line mentioning <code>Unable to bind dream service</code> means the TV refused to start it.</p>""", "adb"),
   ("When ADB fails", """<h3 data-os="mac linux">command not found: adb</h3>
   <h3 data-os="win">'adb' is not recognized</h3>
   <p>The tools are not on your PATH, or your terminal opened before they were installed. Close
   the terminal, open a new one and try <code>adb version</code> again. Terminals that were already open
   do not notice newly installed commands. <span data-os="win">If a new PowerShell still cannot find it, use the
   manual download above and run <code>.\\adb</code> from inside the <code>platform-tools</code> folder.</span></p>

   <h3 data-os="mac linux">no such file or directory: tv-ip</h3>
   <h3 data-os="win">The '&lt;' operator is reserved for future use</h3>
   <p>You typed a placeholder literally. In many guides <code>&lt;tv-ip&gt;</code> stands for your TV's
   address, and the shell reads the <code>&lt;</code> as a file redirect. Replace the whole thing,
   brackets included, with the address from the TV.</p>

   <h3>error: protocol fault on adb pair</h3>
   <p>The pairing handshake did not complete. Try these in order, and after each one reopen
   <strong>Pair device with pairing code</strong> on the TV so you have a fresh port and code, because each
   code works for one attempt only:</p>
   <ol>
   <li><strong>Use the pairing port.</strong> It is the one in the pairing dialog, not the one on the main
   Wireless debugging screen. Type it straight after the address, then the code when asked.</li>
   <li><strong>Restart the ADB server.</strong> A stale background process is the most common cause. Run
   <pre><code>adb kill-server</code></pre> then pair again. The server restarts by itself.</li>
   <li><strong>Keep the TV awake.</strong> If the dialog closes or the screen sleeps, the code is gone.</li>
   <li><strong>Security software.</strong> If it still fails while <code data-os="mac linux">nc -z</code><code data-os="win">Test-NetConnection</code> reaches the port<span data-os="win"> (it says <code>True</code>)</span>, use the relay in the section below.</li>
   </ol>
   <p>A wrong <em>code</em> usually reports a plain failure to pair instead.</p>

   <h3>failed to connect … No route to host</h3>
   <p>Despite the wording, this is rarely a real routing problem, especially if the TV answers
   <code>ping</code>. Work through these in order:</p>
   <ol>
   <li><strong>Not paired yet.</strong> Do step 3 first. Connecting an unpaired computer fails.</li>
   <li><strong>Stale port.</strong> The connect port changes whenever Wireless debugging is switched off and
   on, and sometimes after a restart. Read it again from the TV.</li>
   <li><strong>Different network.</strong> The computer and TV must be on the same network. Guest Wi-Fi and
   some mesh systems isolate devices from each other.</li>
   <li><strong>Security software.</strong> See below.</li>
   </ol>

   <h3>Security software blocks only ADB</h3>
   <p>Some VPNs and antivirus suites filter network traffic per application. They can block
   <code>adb</code> while <code>ping</code> and everything else works. You can tell it is happening if a
   plain connection to the TV's port succeeds but ADB fails:</p>
   <pre data-os="mac linux"><code>nc -z -v 192.168.1.50 41234
adb connect 192.168.1.50:41234</code></pre>
   <pre data-os="win"><code>Test-NetConnection 192.168.1.50 -Port 41234
adb connect 192.168.1.50:41234</code></pre>
   <p>If the first check succeeds (<span data-os="mac linux"><code>nc</code> says <em>succeeded</em></span><span data-os="win">Windows shows
   <code>TcpTestSucceeded : True</code></span>) and ADB says <em>No route to host</em> or <em>cannot connect</em>,
   the network is fine and something is filtering ADB.<span data-os="win"> On Windows that is usually a third-party antivirus
   or VPN rather than Windows Defender Firewall; if Defender asks whether to let <code>adb.exe</code>
   through, allow it on <strong>Private networks</strong>.</span> Pausing the filter works, but the filter is often a system extension
   that keeps running after you disconnect a VPN, so it may need to be switched off in the security
   software itself. If you would rather leave it on, forward the ports through Python, which these filters
   normally allow. Save this as <code>relay.py</code>:</p>
   <pre><code>import socket, sys, threading

host = sys.argv[1]

def pipe(src, dst):
    try:
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

def serve(local, remote):
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", local))
    srv.listen(8)
    while True:
        client, _ = srv.accept()
        try:
            upstream = socket.create_connection((host, remote), 5)
        except OSError:
            client.close()
            continue
        threading.Thread(target=pipe, args=(client, upstream), daemon=True).start()
        threading.Thread(target=pipe, args=(upstream, client), daemon=True).start()

for pair in sys.argv[2:]:
    local, remote = map(int, pair.split(":"))
    threading.Thread(target=serve, args=(local, remote), daemon=True).start()
threading.Event().wait()</code></pre>
   <p>You need Python 3 for this <span data-os="win">(install it from the Microsoft Store or python.org, and tick
   <em>Add python.exe to PATH</em>)</span><span data-os="mac linux">(it is already installed on most Macs and Linux systems; check with <code>python3 --version</code>)</span>. Run the script with the TV's address, then one <code>local:remote</code>
   pair for the pairing port and one for the connect port, and leave it running:</p>
   <pre data-os="mac linux"><code>python3 relay.py 192.168.1.50 55001:37215 55002:41234</code></pre>
   <pre data-os="win"><code>py relay.py 192.168.1.50 55001:37215 55002:41234</code></pre>
   <p>In a second terminal, use <code>127.0.0.1</code> and the local ports in place of the TV's address:</p>
   <pre><code>adb pair 127.0.0.1:55001 123456
adb connect 127.0.0.1:55002</code></pre>
   <p>Everything from step 5 then works as normal. Stop the script with Ctrl+C when you are done.</p>""", "adb"),
  ],
  faq=[
   ("Do I have to set Art Frame TV as the screensaver?",
    "No. The app works fully from its own icon. The screensaver only matters if you want the frame to appear by itself when the TV goes idle."),
   ("What is the easiest way to set it as the screensaver on Google TV?",
    "A launcher with a screensaver override, such as Projectivy Launcher or FLauncher. Install it, open Screensaver Override in its settings and choose Art Frame TV Screensaver. It needs no computer."),
   ("Why does adb connect say No route to host?",
    "Usually because the computer has not been paired with the TV yet, the Wireless debugging port has changed, or security software is blocking ADB specifically. It is rarely a genuine network fault."),
   ("Why does adb pair say protocol fault?",
    "You almost certainly used the wrong port. adb pair needs the port shown in the Pair device with pairing code dialog, which is different from the port on the main Wireless debugging screen, and it changes every time the dialog opens."),
   ("Is port 5555 right for Wireless debugging?",
    "No. Wireless debugging on Android 11 and later uses a random port for pairing and another random port for connecting. Port 5555 belongs to the older USB-then-tcpip method."),
   ("Why does Start now do nothing on my TCL TV?",
    "TCL's auto-start manager blocks apps from starting in the background unless they have the AUTO_START permission. Connect with ADB and run adb shell appops set team.dsa.artframetv AUTO_START allow, then press Start now again."),
   ("Does it need root, and can I undo it?",
    "It does not need root. The command only writes a normal secure setting. To undo it, run adb shell settings delete secure screensaver_components, or choose another screensaver in the TV's settings."),
  ]),
 dict(
  slug="google-photos-on-tv",
  kw="google tv screensaver photos", vol=90, kd=27,
  title="Google Photos as a Google TV screensaver",
  desc="Set Google Photos as your Google TV or Android TV screensaver, choose a specific album, and fix the common problem of photos not showing.",
  intro="""Google TV can idle on your own photos instead of stock landscapes. The setup takes
a minute; the part that trips people up is album selection and the handful of reasons photos
silently fail to appear.""",
  sections=[
   ("Setting it up", """<p>On the Google TV home screen go to <strong>Settings → System →
   Ambient mode</strong>. Choose <strong>Google Photos</strong> as the source, then sign in with the
   account that holds the photos. By default it will show a mix from your whole library.</p>
   <p>To narrow it down, pick <strong>albums</strong> and select the ones you want. Creating an album
   specifically for the TV is worth the two minutes — it is the only reliable way to control exactly
   what the room sees.</p>"""),
   ("When photos don't show up", """<p>Four causes account for nearly all of it.</p>
   <ul>
     <li><strong>Wrong account.</strong> The TV uses the account signed in to Google TV, not
     necessarily the one that owns the album. Check under Settings → Accounts &amp; Sign In.</li>
     <li><strong>The album is shared, not owned.</strong> Shared albums do not always appear in the
     picker. Copy the photos into an album you own.</li>
     <li><strong>A TV-level setting overrides it.</strong> Several manufacturers ship their own
     backdrop or art mode that takes precedence. If your choices in Ambient mode have no effect,
     look for a separate screensaver setting in the manufacturer's menu.</li>
     <li><strong>Not enough recent photos.</strong> Some builds filter to recent items and will look
     empty if the album is all older uploads.</li>
   </ul>"""),
   ("Why it stays online-only", """<p>Ambient Mode streams from Google Photos. If the TV loses its
   connection, the screensaver falls back to Google's own images or shows nothing. Apps that
   download your selection to the TV first — including Art Frame TV — keep working offline, which
   matters more than it sounds if your TV is on a congested network.</p>"""),
   ("Picking photos that actually look good on a TV", """<p>A television is a landscape panel, so
   portrait photos get pillarboxed or cropped. Favour landscape shots. Avoid anything with small
   text. And drop the TV's backlight: photos shot in daylight look harsh at the brightness most
   sets ship with.</p>"""),
  ],
  faq=[
   ("How do I add photos to the Google TV screensaver?",
    "Settings → System → Ambient mode → Source → Google Photos, then sign in and choose which albums to use."),
   ("Why is my Google TV screensaver not showing my Google Photos?",
    "Usually the TV is signed in to a different Google account, the album is shared rather than owned, or the manufacturer's own backdrop setting is overriding Ambient mode."),
   ("Can I show only one album on the TV screensaver?",
    "Yes. In Ambient mode, choose Google Photos then select specific albums. Making an album just for the TV is the most reliable way to control what appears."),
   ("Do Google Photos screensavers work offline?",
    "No. Ambient Mode streams the images, so it needs a connection. Apps that download your chosen photos to the TV first keep working without one."),
  ]),
 dict(
  slug="free-art-for-frame-tv",
  kw="free art for samsung frame tv", vol=70, kd=0,
  title="Free Frame TV art: where to download it",
  desc="Public-domain sources for free, high-resolution art you can display on a Samsung Frame TV, a Hisense Canvas, or any Google TV, without an Art Store subscription.",
  intro="""Samsung's Art Store is a subscription. The art itself does not have to be. Millions
of works are in the public domain and available as high-resolution files from museums that paid to
digitise them, and nothing stops you putting those on a television.""",
  sections=[
   ("What 'public domain' actually means here", """<p>A work is in the public domain when its
   copyright has expired — in most of the world, the author's life plus 70 years. For paintings that
   generally means anything before roughly the 1900s is free to use. The museum's <em>photograph</em>
   of the painting is a separate question, but major institutions have explicitly released their
   scans: the Met, Rijksmuseum, Art Institute of Chicago and Getty all publish open-access images
   precisely so people can use them.</p>"""),
   ("The sources worth using", """<ul>
     <li><strong>Wikimedia Commons</strong> — the broadest collection, and where most other sites
     source from. Search the work, then take the largest resolution offered.</li>
     <li><strong>The Met's Open Access collection</strong> — roughly 490,000 images released under
     Creative Commons Zero.</li>
     <li><strong>Rijksmuseum Rijksstudio</strong> — very high resolution Dutch Golden Age work, free
     to download.</li>
     <li><strong>Art Institute of Chicago</strong> — a clean public API and open-access images.</li>
     <li><strong>Getty Open Content</strong> — paintings, drawings and photography.</li>
     <li><strong>NASA image library</strong> — not art exactly, but free of copyright and
     spectacular on a large panel.</li>
   </ul>"""),
   ("Getting the resolution right", """<p>A 4K panel is 3840×2160. Anything smaller gets upscaled,
   and brush texture is the first thing to go. Aim for at least 1920 pixels on the long edge, and
   prefer 3840 where the museum offers it.</p>
   <p>Aspect ratio is the harder problem. Almost no painting is 16:9. You have three options: crop
   it (and lose composition), stretch it (never do this), or <strong>mat it</strong> — put the
   painting inside a border so the full work is visible and the leftover screen becomes mount board.
   Matting is what a real framer does, and it is the only one of the three that does not damage the
   picture.</p>"""),
   ("Doing it without a Frame TV", """<p>None of this needs Samsung hardware. Any Google TV or
   Android TV can display the same files — the difference is that The Frame has a matte anti-glare
   panel and a physical bezel, while a standard TV is glossy and black-rimmed. You can close most of
   that gap in software by matting the image and dropping the backlight to 25–35%, which is the
   single biggest factor in whether a screen reads as a print.</p>
   <p><a href="/">Art Frame TV</a> does exactly this on Google TV and Android TV: it mats the image
   with a real bevelled passe-partout, and ships 30 images including seven public-domain
   masterworks, free, with no subscription.</p>"""),
  ],
  faq=[
   ("Is there free art for the Samsung Frame TV?",
    "Yes. The Art Store is a paid subscription, but public-domain works from Wikimedia Commons, the Met, the Rijksmuseum, the Art Institute of Chicago and Getty are free to download and display, and the Frame can show your own uploads."),
   ("What resolution should Frame TV art be?",
    "At least 1920 pixels on the long edge, ideally 3840 for a 4K panel. Below that the upscaler softens brush texture noticeably."),
   ("Can I use public domain paintings on my TV legally?",
    "Yes, where copyright has expired — generally the author's life plus 70 years. Major museums including the Met and the Rijksmuseum also release their photographs of those works under open-access terms."),
   ("Do I need a Samsung Frame TV to display art?",
    "No. Any Google TV or Android TV can display the same images. The Frame's advantages are a matte anti-glare panel and a physical bezel; the software side can be matched by matting the image and lowering the backlight."),
  ]),
 dict(
  slug="tv-as-digital-photo-frame",
  kw="digital photo frame app for tv", vol=140, kd=16,
  title="Use your TV as a digital picture frame",
  desc="Four ways to use a smart TV as a digital picture frame, what each one costs you in picture quality, and the TV settings that make a screen look like a print.",
  intro="""A television is a far better digital photo frame than most digital photo frames — it
is bigger, it is already on the wall, and it is already paid for. What stops it looking like one is
usually brightness and framing, not resolution.""",
  sections=[
   ("The four approaches", """<ol>
     <li><strong>The TV's built-in ambient mode.</strong> Easiest, no installation. Google TV and
     most manufacturer skins have one. Limited to the sources the maker allows, and generally
     requires a connection.</li>
     <li><strong>A dedicated app.</strong> Full control over framing, interval and sources, and it
     can store images locally so it works offline. Needs a one-off setup.</li>
     <li><strong>A USB stick.</strong> Most TVs will run a slideshow from a USB drive with no network
     at all. Crude, no matting, but completely private and offline.</li>
     <li><strong>Casting from a phone.</strong> Fine for showing someone holiday photos; useless as a
     permanent frame, since it ties up the phone.</li>
   </ol>"""),
   ("The settings that matter more than the app", """<p>This is where most setups fail. A TV is
   lit from behind and ships configured to look bright in a showroom. Real artwork and real prints
   reflect light, they do not emit it.</p>
   <ul>
     <li><strong>Backlight 25–35%.</strong> The single biggest change. A dim screen reads as paper.</li>
     <li><strong>Picture mode: Warm, or Filmmaker Mode.</strong> Kills the blue cast that makes a
     screen look like a screen.</li>
     <li><strong>Reduce contrast slightly.</strong> Lowers digital glare.</li>
     <li><strong>Turn off motion smoothing.</strong> Irrelevant for still images but it sometimes
     introduces artefacts on slow pans.</li>
   </ul>"""),
   ("Framing, and why letterboxing ruins it", """<p>Photographs are usually 3:2 or 4:3. Televisions
   are 16:9. Something has to give. Filling the screen crops the picture; fitting it leaves black
   bars, which reads unmistakably as "a screen showing an image".</p>
   <p>The third option is to treat the leftover area as mount board rather than dead space — a
   passe-partout, the way a framer would. A bevelled mat with a visible cut edge, slightly wider at
   the bottom than the top, is what makes the eye read "framed print" instead of "letterbox".</p>"""),
   ("Burn-in, if you have an OLED", """<p>A static image held for hours is the one thing OLED panels
   genuinely dislike. Any app you use for this should either move the image slightly over time or
   change it often enough that no edge sits on the same pixels. Combined with a low backlight — which
   you want anyway — the risk is small.</p>"""),
  ],
  faq=[
   ("Can I use my smart TV as a digital picture frame?",
    "Yes. Use the TV's built-in ambient mode, a dedicated photo frame app, or a USB slideshow. The app route gives the most control and can work offline."),
   ("What is the best TV setting for displaying photos?",
    "Drop the backlight to 25–35%, set the picture mode to Warm or Filmmaker Mode, and reduce contrast slightly. Real artwork does not emit light, and lowering brightness is what completes the illusion."),
   ("Will displaying a photo for hours burn my OLED TV?",
    "It is the main risk with static images. Use an app that drifts the image slightly or changes it regularly, and keep the backlight low. Both together make burn-in unlikely."),
   ("How do I stop black bars around photos on my TV?",
    "Either crop to 16:9 and lose part of the composition, or mat the image so the leftover screen becomes a deliberate mount board instead of a black bar."),
  ]),
 dict(
  slug="what-is-a-passe-partout",
  kw="passe partout matting", vol=90, kd=0,
  title="What is a passe-partout? Mat board, bevels and the 18% rule",
  desc="What a passe-partout is, why the bevel is cut at 45 degrees, and why framers make the bottom border wider than the top.",
  intro="""A passe-partout — mat, matboard, mount — is the card border between a picture and its
frame. It looks like decoration. It is actually doing three jobs, and the details that make it work
are small enough that most people never consciously notice them.""",
  sections=[
   ("What it is for", """<p>Three things, in order of how old the reason is.</p>
   <ul>
     <li><strong>It keeps the artwork off the glass.</strong> Paper touching glass traps moisture and
     eventually sticks. The mat's thickness is an air gap.</li>
     <li><strong>It gives the image somewhere to end.</strong> A picture that runs to the frame feels
     cramped; the border is visual breathing room.</li>
     <li><strong>It makes a small picture look deliberate.</strong> A wide mat around a modest print
     reads as a decision rather than a shortage of wall.</li>
   </ul>"""),
   ("The bevel", """<p>Mat board is typically 1.4mm thick, and the window is not cut straight down —
   it is cut at <strong>45 degrees</strong>. That exposes the board's inner core, which is usually
   white or cream even when the surface is coloured.</p>
   <p>That thin angled edge catches light along the top and left, and falls into shadow at the bottom
   and right. It is a tiny detail, perhaps a millimetre and a half wide, and it is the single
   strongest cue your eye uses to decide that something is matted rather than simply cropped. A
   straight cut looks flat. A bevel looks cut.</p>"""),
   ("The 18% rule", """<p>Here is the part that surprises people: a well-cut mat is not symmetrical.
   The bottom border is wider than the top and sides, conventionally by around 15–20%.</p>
   <p>The reason is that optical centre and geometric centre are not the same place. A picture
   centred by measurement appears to sit low in its frame, because we read the bottom edge as the
   base of the object. Making the bottom border wider pushes the image up slightly, and it then
   looks centred. Frames hung above eye level exaggerate the effect, which is why gallery framing
   leans on the convention harder than high-street framing does.</p>"""),
   ("Colour, and why it is nearly always off-white", """<p>Conservation mat board comes in hundreds
   of colours and professional framers use perhaps six. Warm white, eggshell, antique cream, charcoal,
   a muted sage, a greyed blue. The reason is that the mat is not meant to be seen — it is meant to
   separate the picture from the wall. A saturated colour competes with the artwork and dates badly.
   Off-whites do neither.</p>
   <p>Acid-free matters too, for anything you care about. Ordinary cardboard yellows and burns a
   brown line into the paper it touches within a decade or two.</p>"""),
   ("Doing it on a screen", """<p>All of the above is why a television showing a photograph
   edge-to-edge does not look like a framed print, no matter how good the panel is. There is no
   border, no bevel, no depth. <a href="/">Art Frame TV</a> rebuilds these in software for Google TV
   and Android TV — a 45° bevelled core, bottom-weighted borders, and the depth shadow the mat's
   thickness casts onto the print beneath it.</p>"""),
  ],
  faq=[
   ("What is a passe-partout in framing?",
    "A passe-partout is the card border placed between artwork and the frame — also called a mat, matboard or mount. It holds the artwork off the glass, gives the image visual breathing room, and makes a small picture look deliberate."),
   ("Why is mat board cut at an angle?",
    "The 45-degree bevel exposes the board's pale inner core, which catches light along the top and left and falls into shadow at the bottom and right. That thin lit edge is the main visual cue that a picture is matted rather than cropped."),
   ("Why is the bottom of a mat wider than the top?",
    "Because optical centre sits slightly above geometric centre. A mat with equal borders makes the picture look like it is sliding downward, so framers make the bottom border roughly 15–20% wider."),
   ("What colour should a passe-partout be?",
    "Almost always an off-white — warm white, eggshell or cream — or a deep neutral. The mat's job is to separate picture from wall, not to be noticed, and saturated colours compete with the artwork."),
  ]),
 dict(
  slug="art-mode-without-a-frame-tv",
  kw="art mode tv", vol=260, kd=12,
  title="Art mode without a Frame TV: how to get it",
  desc="What Samsung's The Frame actually gives you, which parts are hardware and which are software, and how close an ordinary Google TV can get.",
  intro="""The Frame made art mode mainstream, and it is a genuinely good product. But a lot of
what people are paying for is software, and software is the part you can replicate on a TV you
already own. Here is an honest split.""",
  sections=[
   ("What is genuinely hardware", """<ul>
     <li><strong>The matte anti-glare panel.</strong> This is the real differentiator and it cannot be
     replicated in software. A glossy screen reflects the room; a matte one scatters that reflection
     the way paper does.</li>
     <li><strong>The physical bezel.</strong> Magnetic wooden frames that clip over the edge. Third
     parties sell these for other TVs too, from around $100.</li>
     <li><strong>The flush wall mount.</strong> The Frame sits almost flat against the wall. A
     standard slim mount gets reasonably close.</li>
     <li><strong>The brightness and motion sensor.</strong> Dims to suit the room and turns off when
     nobody is there. Some non-Samsung sets have equivalents.</li>
   </ul>"""),
   ("What is just software", """<ul>
     <li><strong>Displaying art when idle.</strong> Every Google TV can do this.</li>
     <li><strong>The art library.</strong> Samsung's Art Store is a subscription. The public-domain
     works inside it are free elsewhere — see our guide to
     <a href="/articles/free-art-for-frame-tv">finding free art</a>.</li>
     <li><strong>Mats and frame styles.</strong> Entirely a rendering choice. This is the part that
     makes the biggest visual difference and it costs nothing to do well.</li>
   </ul>"""),
   ("Getting an ordinary TV close", """<p>In rough order of effect:</p>
   <ol>
     <li><strong>Drop the backlight to 25–35%</strong> and set picture mode to Warm or Filmmaker
     Mode. This is most of the gap, and it is free.</li>
     <li><strong>Mat the image</strong> rather than filling the screen or letterboxing it. A bevelled
     border with a bottom weight is what reads as "framed".</li>
     <li><strong>Consider a stick-on bezel</strong> if the black plastic rim bothers you.</li>
     <li><strong>Mind the glare.</strong> You cannot make a glossy panel matte, so place the TV
     where it is not facing a window.</li>
   </ol>
   <p>What you will not match is the panel finish in a bright room. If your TV lives opposite a large
   window in daylight, that is the one case where The Frame's hardware genuinely earns its price.</p>"""),
  ],
  faq=[
   ("Can I get art mode on a TV that isn't a Samsung Frame?",
    "Yes, for the software side. Any Google TV or Android TV can display art when idle, with mats and frame styles. What you cannot replicate is The Frame's matte anti-glare panel."),
   ("Is the Samsung Art Store worth it?",
    "It is a convenience subscription. The public-domain works it includes are available free from museum open-access collections, and the Frame will display your own uploads at no cost."),
   ("What makes a TV look like a real framed picture?",
    "Lowering the backlight to 25-35% and setting a warm picture mode does most of it. After that, matting the image with a bevelled border rather than filling or letterboxing the screen."),
   ("Do I need a special TV to display art?",
    "No. The main hardware advantage of an art TV is a matte anti-glare panel, which matters most in a bright room. Everything else is software or a clip-on bezel."),
  ]),
 dict(
  slug="samsung-frame-tv-alternative",
  kw="samsung frame tv alternative", vol=170, kd=4,
  updated="2026-11-13",
  title="Samsung Frame TV alternative: 3 cheaper ways",
  desc="Three ways to get a Frame-style art display without buying The Frame: a clip-on bezel, an art-mode app on Google TV, or both. What each costs and what you give up.",
  intro="""The Frame is a good product with a price to match. If what you want is a television that
looks like a framed print when it is idle, you have three realistic alternatives, and one of them
costs nothing. Here is how they compare, including the one thing none of them can fix.""",
  sections=[
   ("The short answer", """<p>If you already own a Google TV or Android TV, the cheapest alternative to a
   Frame TV is an app that frames your photos and art on the idle screen. Add a clip-on bezel if the
   black plastic rim bothers you. You will not match The Frame's matte anti-glare panel, which only
   matters in a bright room.</p>"""),
   ("Option 1: an art-mode app on a Google TV or Android TV", """<p>The software side of art mode, which is
   most of what people notice, runs on any Google TV. An app such as
   <a href="https://play.google.com/store/apps/details?id=team.dsa.artframetv">Art Frame TV</a> mounts
   your Google Photos or public-domain art inside a rendered frame and passe-partout mat and runs it as
   the screensaver. It is free, with no account and no ads.</p>
   <p><strong>What you give up:</strong> the brightness and motion sensor, and the matte panel.</p>"""),
   ("Option 2: a clip-on bezel", """<p>Third parties sell magnetic or snap-on wooden bezels that fit
   popular TV sizes, typically from around $100. This changes how the TV looks when it is off as well as
   when it is showing art, which software cannot do. Pair it with Option 1 for the closest overall match.</p>"""),
   ("Option 3: a different art-first TV", """<p>Other makers sell lifestyle TVs with art modes and
   matte-style panels. These close the hardware gap but cost more than a standard TV, so they only make
   sense if you are buying a new set anyway.</p>"""),
   ("What no alternative fixes", """<p>A glossy panel reflects the room. If your TV faces a large window,
   no software setting changes that, and it is the one case where The Frame's panel earns its price.
   Everywhere else, lower the backlight to 25-35%, use a warm picture mode, and mat the image. Our guide to
   <a href="/articles/art-mode-without-a-frame-tv">art mode without buying a Frame TV</a> walks
   through each step.</p>"""),
  ],
  faq=[
   ("What is the best Samsung Frame TV alternative?",
    "For most people, an art-mode app on a TV they already own, optionally with a clip-on bezel. It costs little or nothing, and the main thing you lose is the matte anti-glare panel."),
   ("Can I make a normal TV look like a Frame TV?",
    "Mostly. Lower the backlight, use a warm picture mode, and display art inside a matted frame rather than full screen. A clip-on bezel completes the look when the TV is off."),
   ("Is there a free alternative to the Samsung Art Store?",
    "Yes. Many museums publish public-domain works free to use, and an art-mode app can display them. See our guide to free art for Frame-style TVs."),
   ("Do alternatives work on Google TV?",
    "Yes. Art Frame TV runs on Google TV and Android TV, and works as the screensaver or from the app."),
  ]),
 dict(
  slug="google-tv-ambient-mode",
  kw="google tv ambient mode", vol=140, kd=6,
  updated="2026-11-13",
  title="Google TV Ambient Mode: how to set it up, change it and turn it off",
  desc="Where Ambient Mode lives on Google TV, what the three sources do, how to change the timer, and why third-party screensaver apps don't appear in the list.",
  intro="""Ambient Mode is what Google TV shows when you stop using it. It is easy to find once you
know where to look, and easy to get stuck on the wrong source. Here is how it works and how to change
what it shows.""",
  sections=[
   ("What Ambient Mode is", """<p>On Google TV, Ambient Mode replaces the classic screensaver. It starts
   after a period of inactivity and shows photos, art or other content full screen until you press a
   button on the remote.</p>"""),
   ("Where to find it", """<p>Go to <strong>Settings → System → Ambient mode</strong>. Menu names shift a
   little between TV makers and software versions, so if you do not see it, check
   <strong>Settings → Display &amp; Sound</strong> as well.</p>"""),
   ("Choosing a source", """<p>Under <strong>Source</strong> you get Google Photos, Art gallery, and an
   Experimental option.</p>
   <ul>
     <li><strong>Google Photos</strong> shows your own albums, which you pick in the Google Home app.</li>
     <li><strong>Art gallery</strong> is Google's curated set.</li>
     <li><strong>Experimental</strong> is a fallback if the others do not work for you.</li>
   </ul>
   <p>If your photos do not appear, see <a href="/articles/google-photos-on-tv">Google Photos on TV</a>.</p>"""),
   ("Changing or turning off the timer", """<p>In the same Ambient mode screen you can set how long the TV
   waits before it starts, or turn it off. A separate panel sleep timer can still switch the TV off
   independently, so check both if the screen goes dark sooner than you expect.</p>"""),
   ("Using your own screensaver instead", """<p>Third-party apps do not appear in the Ambient mode source
   list on Google TV, which is why many people think their screensaver app is broken. There are two
   working routes: a launcher that exposes the setting, or a one-time ADB command. Both are explained in
   <a href="/articles/google-tv-screensaver">how to change the screensaver on Google TV</a>, and the full
   walkthrough for Art Frame TV is in <a href="/articles/set-up-art-frame-tv">the setup guide</a>.</p>"""),
  ],
  faq=[
   ("Where is Ambient Mode on Google TV?",
    "Settings, then System, then Ambient mode. On some TVs it sits under Display and Sound."),
   ("How do I turn off Ambient Mode?",
    "Open Ambient mode in Settings and set the timer to Off, or choose a source you are happy to see."),
   ("Why can't I choose my own screensaver app?",
    "Google TV limits the Ambient mode source list to Google's own options. A launcher with a screensaver override or one ADB command sets a third-party screensaver."),
   ("Why are my Google Photos not showing in Ambient Mode?",
    "Albums are chosen in the Google Home app, not on the TV. See our Google Photos on TV guide for the usual fixes."),
  ]),
 dict(
  slug="turn-android-tv-into-art",
  kw="turn tv into art", vol=0, kd=0,
  published="2026-11-16", updated="2026-11-16",
  title="How to turn your Android TV into art",
  desc="Turn an Android TV or Google TV into framed wall art in four steps: dim the panel, pick public-domain art, add a real mat and frame, and let it run as the screensaver.",
  intro="""You do not need a special television to have art on the wall. A Google TV or Android TV
you already own can show a painting that reads as a framed print, as long as you fix the brightness,
the framing and the source of the art. Here are the four steps, in the order they matter.""",
  sections=[
   ("Step 1: dim the panel", """<p>A TV ships bright enough for a showroom. Art does not glow, it reflects light, so the
   biggest single change is to turn the backlight down to <strong>25 to 35%</strong> and set the picture mode to
   <strong>Warm</strong> or <strong>Filmmaker Mode</strong>. Do this before anything else. A dim, warm screen already
   looks more like paper than a bright, blue one.</p>"""),
   ("Step 2: choose art you are allowed to display", """<p>Millions of paintings are in the public domain, and
   several museums publish high-resolution photographs of them for anyone to use, including the Met's Open Access
   collection and Wikimedia Commons. That means you can show a famous painting on your own TV without a
   subscription. Our guide to <a href="/articles/free-art-for-frame-tv">free art for Frame-style TVs</a> lists the
   sources worth using, and what resolution to aim for.</p>"""),
   ("Step 3: mat and frame it, do not stretch it", """<p>Paintings are rarely 16:9. Cropping loses part of the picture and
   black bars look like a screen. A framer's answer is a <strong>mat</strong>: a card border with a bevelled cut edge,
   slightly wider at the bottom than the top. Add a frame moulding around it and the whole screen reads as one
   framed print. <a href="/articles/what-is-a-passe-partout">What a passe-partout is and why the bevel matters</a>
   explains the detail.</p>
   <p><a href="/">Art Frame TV</a> does this for you on Google TV and Android TV. It ships with 30 bundled images,
   including public-domain masterworks, and draws a bevelled mat, a frame and a soft shadow around each one.
   The free version includes all of that with a Dark Walnut frame or no frame.</p>"""),
   ("Step 4: let it appear by itself", """<p>You can open the app from the home screen any time, so the TV becomes a
   picture on demand. If you want the art to appear when the TV goes idle, set it as the screensaver. On Android TV
   that is <strong>Settings → Device Preferences → Screen saver</strong>. Google TV hides that menu behind Ambient
   Mode, so it needs one extra step, covered in <a href="/articles/set-up-art-frame-tv">the setup guide</a>.</p>"""),
   ("What you will not get", """<p>A glossy panel reflects the room, and no software setting makes it matte. If the
   TV faces a window, move it or accept some glare. Our comparison of
   <a href="/articles/samsung-frame-tv-alternative">Samsung Frame alternatives</a> covers that gap honestly.</p>"""),
  ],
  faq=[
   ("Can any Android TV show art when it is idle?",
    "Yes. Any Google TV or Android TV running Android 8.0 or newer can run an art app, either from its icon or as the screensaver."),
   ("Is it free to turn my TV into art?",
    "It can be. Art Frame TV's free version includes 30 bundled images, the full framing look with a Dark Walnut frame or no frame, and the screensaver. There is no subscription. Extra frames, mats and art packs are one-time purchases."),
   ("Will this look like a Samsung Frame TV?",
    "Close, apart from the panel finish. A Frame has a matte anti-glare screen that a normal TV cannot match, but dimming the backlight and matting the image gets most of the way there."),
   ("Why does my TV look like a screen and not a picture?",
    "Usually brightness and framing. Drop the backlight to 25 to 35 percent, use a warm picture mode, and put the image inside a mat instead of filling the screen or leaving black bars."),
  ]),
 dict(
  slug="free-art-screensaver-android-tv",
  kw="free art screensaver android tv", vol=0, kd=0,
  published="2026-11-16", updated="2026-11-16",
  title="Free art screensaver for Android TV and Google TV",
  desc="How to get a free art screensaver on Android TV or Google TV: what free actually includes, what is a paid extra, and how to switch it on.",
  intro="""A good art screensaver should not need an account, a subscription or an ad break. Art Frame TV is
free to install and use, with optional one-time purchases for more frames, mats and art. This page is
plain about which is which.""",
  sections=[
   ("What is free", """<p>The free version of <a href="/">Art Frame TV</a> includes:</p>
   <ul>
     <li>All 30 bundled images, including public-domain masterworks</li>
     <li>The full framing look: a bevelled mat, depth shadow and glazing</li>
     <li>A Dark Walnut frame, or no frame</li>
     <li>The screensaver, with no time limit</li>
   </ul>
   <p>There is no account to create and there are no ads.</p>"""),
   ("What costs extra", """<p>Studio Unlock is a <strong>one-time</strong> purchase. It adds your own Google Photos
   and shared albums, all six mouldings, all six mat colours and finer control of the look. Frame packs and art packs
   are separate one-time purchases. Nothing renews, and nothing is required to keep using the free version.</p>"""),
   ("Where the art comes from", """<p>The bundled artwork is in the public domain. The works are sourced from
   Wikimedia Commons and the Met's Open Access collection, so there is no copyright issue in showing them on your
   wall. Read more in our guide to <a href="/articles/free-art-for-frame-tv">free art for your TV</a>.</p>"""),
   ("How to switch it on as a screensaver", """<p>Install Art Frame TV from Google Play on the TV. On Android TV, pick it
   under <strong>Settings → Device Preferences → Screen saver</strong>. On Google TV, Google's Ambient Mode does not
   list third-party apps, so you set it once with a launcher that has a screensaver override, or with one ADB command.
   The <a href="/articles/set-up-art-frame-tv">step-by-step setup guide</a> covers both, and you can always just open
   the app from its icon.</p>"""),
   ("Privacy", """<p>The app has no account system and no analytics SDKs, and your photos stay on the TV. The
   <a href="/privacy">privacy policy</a> has the details.</p>"""),
  ],
  faq=[
   ("Is there a free art screensaver for Android TV?",
    "Yes. Art Frame TV is free to install and includes 30 bundled images, framing and the screensaver, with no account and no ads."),
   ("Does the free version have a time limit?",
    "No. The free version has no time limit and no trial period. The paid options are optional, one-time purchases."),
   ("Is there a subscription?",
    "No. Studio Unlock, frame packs and art packs are one-time purchases, and nothing renews."),
   ("Can I use it as the screensaver on Google TV?",
    "Yes, with one extra step, because Google TV's Ambient Mode only lists Google's own sources. See the setup guide for the launcher and ADB routes."),
  ]),
 dict(
  slug="best-android-tv-screensaver-art",
  kw="best android tv screensaver art", vol=0, kd=0,
  published="2026-11-16", updated="2026-11-16",
  title="Choosing an art screensaver for Android TV: what to look for",
  desc="A practical checklist for choosing an art screensaver on Android TV or Google TV: where the art comes from, how it is framed, price model, privacy and whether it works as a real screensaver.",
  intro="""There are several ways to get art on an idle Android TV, from Google's own Ambient Mode to
third-party apps. Rather than rank them, here is a checklist that tells you which one suits your TV and your
taste, plus where Art Frame TV fits.""",
  sections=[
   ("1. Can it be your actual screensaver?", """<p>On Google TV, Ambient Mode only lists Google's sources, so a
   third-party app needs a launcher override or an ADB command to become the screensaver. Check that the app tells
   you how. If it also works when opened from its icon, you lose nothing by trying it first. See
   <a href="/articles/google-tv-screensaver">how to change the screensaver on Google TV</a>.</p>"""),
   ("2. Where does the art come from?", """<p>Look for public-domain or properly licensed images. Art from museum
   open-access collections is free to show on your wall. If an app does not say where its images come from, assume
   you cannot use them commercially, and ask.</p>"""),
   ("3. Does it frame the picture?", """<p>Many screensavers show the image full screen. That crops the picture or
   leaves black bars. A mat and frame makes the TV read as a print. Art Frame TV's whole purpose is this, with a
   bevelled mat, frame mouldings and a depth shadow.</p>"""),
   ("4. How does it charge?", """<p>Prefer one-time purchases over subscriptions for something you will leave on a
   wall. Check what the free version includes, and whether it has a trial that quietly expires. Art Frame TV's free
   version has no time limit, and its paid options are one-time.</p>"""),
   ("5. What does it do with your data?", """<p>A screensaver has no reason to need an account. Check the privacy
   policy, and whether your own photos are uploaded anywhere. Art Frame TV has no account system and keeps photos on
   the TV.</p>"""),
   ("6. Will it look good on your panel?", """<p>Whatever you choose, lower the backlight to 25 to 35% and use a warm
   picture mode. See <a href="/articles/turn-android-tv-into-art">how to turn your Android TV into art</a> for the
   settings, and the <a href="/articles/samsung-frame-tv-alternative">Samsung Frame alternatives</a> page for how a
   normal TV compares with a Frame.</p>"""),
  ],
  faq=[
   ("What is the best art screensaver for Android TV?",
    "It depends on what you value. Choose one that can run as the screensaver, uses properly licensed art, frames the picture, has fair pricing and respects your privacy. Art Frame TV is built around those points."),
   ("Does Google TV have a built-in art screensaver?",
    "Yes. Ambient Mode has an Art gallery source with Google's own curated images. It does not add frames or mats, and it does not accept third-party sources."),
   ("Are art screensavers safe for OLED TVs?",
    "Static images are the risk. Choose an app that changes the picture regularly or drifts it slightly, and keep the backlight low."),
   ("Should I pay for a screensaver app?",
    "Only if the free version proves it is worth it. A one-time purchase for extra frames or art is fairer than a subscription for a wall display."),
  ]),
 dict(
  slug="tv-photo-frame-app",
  kw="tv photo frame", vol=5400, kd=18,
  published="2026-11-22", updated="2026-11-22",
  title="TV photo frame app: show photos on your TV",
  desc="How to turn a Google TV or Android TV into a photo frame with an app: what to look for, how to show your own photos, and how to make them look like prints.",
  intro="""A television is a large, sharp screen that is idle most of the day, which makes it a good photo
frame. The catch is that a photo simply filling a TV looks like a slideshow, not a frame. Here is how to
show your own photos on a Google TV or Android TV, and how to make them look like they belong on a wall.""",
  sections=[
   ("The three ways to show photos on a TV", """<p>On a Google TV or Android TV you have three realistic options:</p>
   <ul>
     <li><strong>Google Photos in Ambient Mode.</strong> Built in and free, but it only shows full-screen photos and
     only from albums you pick in the Google Home app. See <a href="/articles/google-photos-on-tv">Google Photos on TV</a>.</li>
     <li><strong>A photo frame app.</strong> An app that runs on the TV and shows your photos with its own layout,
     borders and timing.</li>
     <li><strong>Casting from a phone.</strong> Works for a one-off, but the phone has to stay on and connected.</li>
   </ul>"""),
   ("What a good photo frame app does", """<p>Look for four things:</p>
   <ul>
     <li><strong>It runs as a screensaver,</strong> so photos appear when the TV is idle, without you opening anything.</li>
     <li><strong>It frames the photo.</strong> A mat and frame around a picture is what makes a screen read as a print.
     <a href="/articles/what-is-a-passe-partout">What a passe-partout is</a> explains why.</li>
     <li><strong>It keeps your photos on the TV,</strong> with no account needed for it to work.</li>
     <li><strong>It does not charge a subscription</strong> for a wall display.</li>
   </ul>"""),
   ("Showing your own photos with Art Frame TV", """<p><a href="/">Art Frame TV</a> runs on Google TV and Android TV. The free
   version includes 30 bundled images, a bevelled mat, depth shadow and glazing, and the screensaver, with no account
   and no ads. Showing your own photos from Google Photos and shared albums is part of Studio Unlock, a one-time
   purchase. Nothing renews.</p>"""),
   ("Make the photos look like prints", """<p>Whatever app you use, three TV settings matter more than the app. Turn the
   backlight down to about 25 to 35%, switch the picture mode to Warm or Filmmaker Mode, and avoid stretching photos to
   16:9. The full list is in <a href="/articles/tv-as-digital-photo-frame">how to use your TV as a digital picture frame</a>.</p>"""),
   ("Set it up as the screensaver", """<p>On Android TV, pick the app under <strong>Settings → Device Preferences → Screen
   saver</strong>. Google TV hides third-party screensavers behind Ambient Mode, so it needs one extra step. The
   <a href="/articles/set-up-art-frame-tv">setup guide</a> covers both routes.</p>"""),
  ],
  faq=[
   ("What is the best photo frame app for a TV?",
    "One that runs as a screensaver, frames the photo instead of stretching it, keeps photos on the TV and does not need a subscription. Art Frame TV meets all four on Google TV and Android TV."),
   ("Can I show my own photos on Google TV?",
    "Yes. Google Photos in Ambient Mode shows full-screen photos from albums you choose in the Google Home app. Art Frame TV can show your Google Photos and shared albums inside a mat and frame with Studio Unlock."),
   ("Do I need to leave my phone connected?",
    "Not for an app that runs on the TV. Casting needs the phone connected, an app does not."),
   ("Will a photo frame app harm my TV screen?",
    "Showing changing images at a lower brightness is gentler than leaving a static bright image up. Keep the backlight low and use a slideshow rather than one fixed picture."),
  ]),
 dict(
  slug="art-screensaver-for-tv",
  kw="tv art screensaver", vol=210, kd=3,
  published="2026-11-22", updated="2026-11-22",
  title="Art screensaver for TV: free ways to get one",
  desc="How to put famous paintings on your TV as a screensaver: Google's Art gallery source, public-domain art, and an app that frames each painting like a print.",
  intro="""Turning your TV into a rotating art gallery when it is idle is easy and can be free. There are
two good routes on Google TV and Android TV, and they suit different tastes. Here is what each one gives you.""",
  sections=[
   ("Route 1: Google's Art gallery", """<p>On Google TV, open <strong>Settings → System → Ambient mode → Source</strong> and
   choose <strong>Art gallery</strong>. Google supplies the images, they rotate automatically, and it costs nothing. The
   trade-offs are that you cannot choose the artworks and nothing is framed or matted. See
   <a href="/articles/google-tv-ambient-mode">Google TV Ambient Mode</a> for the menu.</p>"""),
   ("Route 2: a framed art app", """<p><a href="/">Art Frame TV</a> ships with 30 bundled images, including public-domain
   masterworks, and draws a bevelled mat, a frame and a soft shadow around each one. The free version includes all
   30 images, a Dark Walnut frame or no frame, and the screensaver, with no account and no ads. More frames, mats
   and art packs are one-time purchases.</p>"""),
   ("Where public-domain art comes from", """<p>Museums such as the Met publish high-resolution scans of works in the public
   domain, and Wikimedia Commons hosts many more. That is why famous paintings can be shown on a TV without a licence.
   Our guide to <a href="/articles/free-art-for-frame-tv">free art for your TV</a> lists the best sources.</p>"""),
   ("Make it look like art, not a screen", """<p>Dim the backlight to about 25 to 35%, use a warm picture mode and keep the
   painting inside a mat. <a href="/articles/turn-android-tv-into-art">How to turn your Android TV into art</a> walks
   through the four steps in order.</p>"""),
   ("Which should you choose?", """<p>If you want zero setup, use Art gallery. If you want a framed look, control over
   which images appear, or your own photos next to the paintings, use an app. You can try the app free, since the free
   version has no time limit.</p>"""),
  ],
  faq=[
   ("Is there a free art screensaver for my TV?",
    "Yes. Google TV's Ambient Mode has a free Art gallery source, and Art Frame TV is free to install with 30 bundled images and no account."),
   ("Where do I find the Art gallery option?",
    "On Google TV: Settings, then System, then Ambient mode, then Source, and choose Art gallery."),
   ("Can I choose which paintings appear?",
    "Not in Google's Art gallery. An app such as Art Frame TV lets you pick from its bundled images and add art packs."),
   ("Does the art screensaver work on Android TV too?",
    "Yes. On Android TV you pick the screensaver under Settings, Device Preferences, Screen saver."),
  ]),
 dict(
  slug="nvidia-shield-screensaver",
  kw="nvidia shield screensaver", vol=110, kd=8,
  published="2026-11-22", updated="2026-11-22",
  title="Nvidia Shield screensaver: change it to art",
  desc="How to change the screensaver on an Nvidia Shield TV, set the start time, and use a third-party art screensaver instead of the default.",
  intro="""The Nvidia Shield TV runs Android TV, which means it has the classic screensaver menu that newer
Google TV devices hide. That makes it one of the easiest boxes to set up. Here is where the setting is and how
to put art on it.""",
  sections=[
   ("Open the screensaver settings", """<p>On a Shield TV, go to <strong>Settings → Device Preferences → Screen saver</strong>.
   Menu names can differ slightly between Shield software versions. If you do not see it, look under
   <strong>Settings → Device Preferences</strong> for the nearest match.</p>"""),
   ("Change the screensaver", """<p>Under <strong>Screen saver</strong> pick the one you want from the list. The default is
   Backdrop, which shows photos and scenes. Any screensaver app you install from Google Play appears in the same list,
   which is the main reason Shield is easier than a Google TV device.</p>"""),
   ("Set when it starts", """<p>In the same menu choose <strong>When to start</strong> and set the idle time. Pick a short
   delay if you want the TV to behave like a picture on the wall, a longer one if you often pause and come back.</p>"""),
   ("Use art as the screensaver", """<p>Install <a href="/">Art Frame TV</a> from Google Play on the Shield, then select it
   in the Screen saver list. The free version has 30 bundled images in a bevelled mat and frame, no account and no
   ads. Full steps are in the <a href="/articles/set-up-art-frame-tv">setup guide</a>.</p>"""),
   ("If it does not appear in the list", """<p>Restart the Shield and reopen the Screen saver menu. If it still is not there,
   see <a href="/articles/google-tv-screensaver">how to change the screensaver on Google TV and Android TV</a> for the
   launcher and ADB routes.</p>"""),
  ],
  faq=[
   ("Where is the screensaver setting on Nvidia Shield?",
    "Settings, then Device Preferences, then Screen saver."),
   ("How do I change the screensaver start time on Shield?",
    "In the Screen saver menu, choose When to start and select the idle time."),
   ("Can I use my own screensaver app on Shield?",
    "Yes. Android TV lists installed screensaver apps in the Screen saver menu, so an app such as Art Frame TV appears there after you install it."),
   ("Why is my Shield showing the same screensaver every time?",
    "The default Backdrop screensaver rotates its own images. Choose a different screensaver in the same menu if you want something else."),
  ]),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Art Frame TV</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#121820">
<meta name="color-scheme" content="dark">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Art Frame TV">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/images/social-1200x630.png?v=2">
<meta property="og:image:alt" content="A painting hung on a TV inside a walnut frame with a cream mat">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/images/social-1200x630.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="/images/icon-16.png?v=3">
<link rel="icon" type="image/png" sizes="32x32" href="/images/icon-32.png?v=3">
<link rel="icon" type="image/png" sizes="48x48" href="/images/icon-48.png?v=3">
<link rel="icon" type="image/png" sizes="192x192" href="/images/icon-192.png?v=3">
<link rel="apple-touch-icon" href="/images/icon-180.png?v=3">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav}
"""

NAV = """<header class="nav" id="nav">
  <div class="wrap nav-in">
    <a class="brand" href="/" aria-label="Art Frame TV, home">
      <img class="brand-mark" src="/images/icon-192.png?v=3" width="30" height="30" alt="" aria-hidden="true">
      <span class="brand-name">Art Frame <b>TV</b></span>
    </a>
    <ul class="nav-links">
      <li><a href="/#craft">The framing</a></li>
      <li><a href="/#materials">Materials</a></li>
      <li><a href="/#photos">Your photos</a></li>
      <li><a href="/articles/">Guides</a></li>
      <li><a href="/privacy">Privacy</a></li>
    </ul>
    <a class="btn btn-ghost btn-sm" href="https://play.google.com/store/apps/details?id=team.dsa.artframetv">Get it on Google Play</a>
  </div>
</header>
"""

FOOT = """<footer class="foot">
  <div class="wrap">
    <p class="foot-legal">
      © <span id="year">2026</span> Digital Space Agency UG ·
      <a href="/">Art Frame TV</a> · <a href="/articles/">Guides</a> ·
      <a href="/privacy">Privacy</a> · <a href="mailto:info@dsa.team">info@dsa.team</a><br>
      Art Frame TV is not affiliated with, endorsed by, or sponsored by Google or Samsung.
      Google TV, Android TV and Google Photos are trademarks of Google LLC.
    </p>
  </div>
</footer>
<script>document.getElementById('year').textContent = new Date().getFullYear();
const nav=document.getElementById('nav');const f=()=>{nav.dataset.stuck=String(scrollY>12)};f();addEventListener('scroll',f,{passive:true});</script>
</body>
</html>
"""

PICKER = """        <div class="picker" id="picker" hidden>
          <div class="picker-group" data-group="route">
            <span class="picker-label">How</span>
            <button type="button" data-value="adb">ADB (computer)</button>
            <button type="button" data-value="launcher">Launcher (no computer)</button>
          </div>
          <div class="picker-group" data-group="os">
            <span class="picker-label">Your computer</span>
            <button type="button" data-value="mac">macOS</button>
            <button type="button" data-value="win">Windows</button>
            <button type="button" data-value="linux">Linux</button>
          </div>
        </div>
        <script>
        (function(){
          var picker=document.getElementById('picker'); if(!picker) return;
          var st={route:'adb',os:'mac'};
          try{
            var ua=(navigator.userAgentData&&navigator.userAgentData.platform)||navigator.platform||'';
            if(/win/i.test(ua)) st.os='win'; else if(/linux|x11/i.test(ua)&&!/android/i.test(navigator.userAgent)) st.os='linux';
            var saved=JSON.parse(localStorage.getItem('setupPrefs')||'{}');
            if(saved.os) st.os=saved.os; if(saved.route) st.route=saved.route;
          }catch(e){}
          function apply(){
            document.querySelectorAll('[data-os]:not(button)').forEach(function(el){
              el.hidden = el.getAttribute('data-os').split(' ').indexOf(st.os)<0 || st.route!=='adb';
            });
            document.querySelectorAll('[data-route]').forEach(function(el){ el.hidden = el.getAttribute('data-route')!==st.route; });
            picker.querySelector('[data-group=os]').hidden = st.route!=='adb';
            picker.querySelectorAll('button').forEach(function(b){
              var on = st[b.parentNode.getAttribute('data-group')]===b.getAttribute('data-value');
              b.setAttribute('aria-pressed', on); });
            try{ localStorage.setItem('setupPrefs', JSON.stringify(st)); }catch(e){}
          }
          picker.addEventListener('click',function(e){
            var b=e.target.closest('button'); if(!b) return;
            st[b.parentNode.getAttribute('data-group')]=b.getAttribute('data-value'); apply();
          });
          function init(){ picker.hidden=false; apply(); }
          if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
        })();
        </script>"""

def fmt_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"

def schema_for(a, canon):
    faq = ",\n".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jstr(q), jstr(ans)) for q, ans in a["faq"])
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"Article","headline":{jstr(a['title'])},"description":{jstr(a['desc'])},
 "mainEntityOfPage":{jstr(canon)},"image":{jstr(SITE + '/images/social-1200x630.png')},
 "datePublished":"{a.get('published','2026-10-20')}","dateModified":"{a.get('updated','2026-10-20')}",
 "author":{{"@type":"Organization","name":"Digital Space Agency UG","url":{jstr(SITE + '/')}}},
 "publisher":{{"@type":"Organization","name":"Art Frame TV","url":{jstr(SITE + '/')},
  "logo":{{"@type":"ImageObject","url":{jstr(SITE + '/images/icon-192.png')}}}}}}},
{{"@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Home","item":{jstr(SITE + '/')}}},
 {{"@type":"ListItem","position":2,"name":"Guides","item":{jstr(SITE + '/articles/')}}},
 {{"@type":"ListItem","position":3,"name":{jstr(a['title'])}}}]}},
{{"@type":"FAQPage","mainEntity":[
{faq}]}}
]}}</script>"""

def jstr(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def slug(text):
    """Stable heading anchor, so the table of contents and the <h2> ids agree."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

os.makedirs(OUT, exist_ok=True)

for a in ARTICLES:
    canon = f"{SITE}/articles/{a['slug']}"
    def rattr(sec):
        return f' data-route="{sec[2]}"' if len(sec) > 2 else ""
    toc = "\n".join(
        f'          <li{rattr(x)}><a href="#{slug(x[0])}">{x[0]}</a></li>' for x in a["sections"])
    body = "\n".join(
        f'        <section{rattr(x)}>\n        <h2 id="{slug(x[0])}">{x[0]}</h2>\n        {x[1].strip()}\n        </section>'
        for x in a["sections"])
    if a.get("picker"):
        body = PICKER + "\n" + body
    faq = "\n".join(
        f'''        <details>
          <summary>{html.escape(q)}</summary>
          <div class="answer">{html.escape(ans)}</div>
        </details>''' for q, ans in a["faq"])
    related = "\n".join(
        f'            <li><a href="/articles/{o["slug"]}">{o["title"]}</a></li>'
        for o in ARTICLES if o["slug"] != a["slug"])

    page = HEAD.format(title=html.escape(a["title"]), desc=html.escape(a["desc"]),
                       canon=canon, site=SITE, schema=schema_for(a, canon), nav=NAV)
    page += f"""
<main id="main" class="doc">
  <div class="wrap">
    <div class="doc-head">
      <p class="eyebrow"><a href="/articles/" style="color:inherit;text-decoration:none">Guides</a></p>
      <h1>{html.escape(a['title'])}</h1>
      <p class="lede">{a['intro'].strip()}</p>
      <div class="doc-meta">
        <span><strong style="color:var(--muted)">Updated</strong> <time datetime="{a.get('updated','2026-10-20')}">{fmt_date(a.get('updated','2026-10-20'))}</time></span>
        <span><strong style="color:var(--muted)">For</strong> Google TV &amp; Android TV</span>
      </div>
    </div>

    <div class="doc-body">
      <aside class="toc" aria-label="On this page">
        <h4>On this page</h4>
        <ol>
{toc}
          <li><a href="#faq">Common questions</a></li>
        </ol>
      </aside>

      <article class="prose">
{body}

        <h2 id="faq">Common questions</h2>
        <div class="faq" style="border-top:0">
{faq}
        </div>

        <div class="callout" style="margin-top:44px">
          <p><strong>Art Frame TV</strong> puts your photos and gallery classics inside
          photorealistic frames with real passe-partout matting, on Google TV and Android TV.
          Free, no account, no ads. <a href="https://play.google.com/store/apps/details?id=team.dsa.artframetv">Get it on Google Play →</a> · <a href="/">See how it works</a></p>
        </div>

        <h2 id="more">More guides</h2>
        <ul>
{related}
        </ul>
      </article>
    </div>
  </div>
</main>
"""
    page += FOOT
    open(os.path.join(OUT, a["slug"] + ".html"), "w").write(page)

# ---- hub ----------------------------------------------------------------
cards = "\n".join(f"""        <article class="craft-cell">
          <h3 style="margin-bottom:10px"><a href="/articles/{a['slug']}" style="text-decoration:none">{html.escape(a['title'])}</a></h3>
          <p>{html.escape(a['desc'])}</p>
        </article>""" for a in ARTICLES)

hub = HEAD.format(
    title="Guides", desc="Practical guides to screensavers, art and photo framing on Google TV and Android TV.",
    canon=f"{SITE}/articles/", site=SITE, nav=NAV,
    schema=f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"Art Frame TV Guides",
"url":{jstr(SITE + '/articles/')},"hasPart":[{",".join(
  '{"@type":"Article","headline":%s,"url":%s}' % (jstr(a['title']), jstr(SITE + '/articles/' + a['slug']))
  for a in ARTICLES)}]}}</script>""")
hub += f"""
<main id="main" class="doc">
  <div class="wrap">
    <div class="doc-head">
      <p class="eyebrow">Guides</p>
      <h1>Screensavers, art and framing on Google TV</h1>
      <p class="lede">
        What we learned building a framing engine for the television — the settings that matter,
        the ones that don't, and how to get a screen to read as a print.
      </p>
    </div>
    <div class="craft">
{cards}
    </div>
  </div>
</main>
"""
hub += FOOT
open(os.path.join(OUT, "index.html"), "w").write(hub)
print("\n".join(a["slug"] for a in ARTICLES))
print("index.html")
