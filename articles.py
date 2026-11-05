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
  title="How to change the screensaver on Google TV and Android TV",
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
  updated="2026-11-05",
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
   <p>The trade-off is that you are changing your home screen. If you would rather not, use route 2.</p>"""),
   ("Route 2: ADB over Wi-Fi", """<p>ADB is Android's developer tool. You run it once, on a computer that is on the
   same Wi-Fi network as the TV, and the setting then stays on the TV.</p>

   <h3>1. Install ADB on your computer</h3>
   <p>ADB ships in Google's <strong>platform-tools</strong>. Pick the line for your system and run it in a terminal:</p>
   <pre><code># macOS (Homebrew)
brew install --cask android-platform-tools

# Windows (PowerShell)
winget install Google.PlatformTools

# Debian / Ubuntu
sudo apt install adb</code></pre>
   <p>Open a <strong>new</strong> terminal window and check it worked:</p>
   <pre><code>adb version</code></pre>
   <p>If you see <code>command not found: adb</code>, see the fixes below.</p>

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
   <code>adb shell settings delete secure screensaver_components</code>.</p>"""),
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
   <code>adb logcat -c</code>, press Start now, then <code>adb logcat -d | grep -i "forbid bind"</code>.
   A line mentioning <code>Unable to bind dream service</code> means the TV refused to start it.</p>"""),
   ("When ADB fails", """<h3>command not found: adb</h3>
   <p>The tools are not on your PATH, or your terminal opened before they were installed. Close
   the terminal, open a new one and try <code>adb version</code> again. Terminals that were already open
   do not notice newly installed commands.</p>

   <h3>no such file or directory: tv-ip</h3>
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
   <li><strong>Security software.</strong> If it still fails while <code>nc -z</code> reaches the port, use the
   relay in the section below.</li>
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
   <pre><code>nc -z -v 192.168.1.50 41234     # macOS / Linux
adb connect 192.168.1.50:41234</code></pre>
   <p>If <code>nc</code> says <em>succeeded</em> and ADB says <em>No route to host</em>, the network is fine
   and something is filtering ADB. Pausing the filter works, but the filter is often a system extension
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
   <p>Run it with the TV's address, then one <code>local:remote</code> pair for the pairing port and one
   for the connect port, and leave it running:</p>
   <pre><code>python3 relay.py 192.168.1.50 55001:37215 55002:41234</code></pre>
   <p>In a second terminal, use <code>127.0.0.1</code> and the local ports in place of the TV's address:</p>
   <pre><code>adb pair 127.0.0.1:55001 123456
adb connect 127.0.0.1:55002</code></pre>
   <p>Everything from step 5 then works as normal. Stop the script with Ctrl+C when you are done.</p>"""),
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
  title="How to put your Google Photos on your TV screensaver",
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
  title="Where to find free art for a Frame TV — and any other TV",
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
  title="How to turn any TV into a digital photo frame",
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
  title="Art mode without buying a Frame TV",
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
<link rel="canonical" href="{canon}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/images/social-1200x630.png?v=2">
<meta name="twitter:card" content="summary_large_image">
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
      <svg width="30" height="30" viewBox="0 0 30 30" fill="none" aria-hidden="true">
        <rect width="30" height="30" rx="3" fill="#1c2d42"/>
        <rect x="4.5" y="4.5" width="21" height="21" fill="none" stroke="#d4af37" stroke-width="1.8"/>
        <rect x="7" y="7" width="16" height="16" fill="none" stroke="#d4af37" stroke-width="0.9"/>
        <path d="M3 4.5 5.5 4.5 3 7Z" fill="#d4af37"/>
        <path d="M27 4.5 24.5 4.5 27 7Z" fill="#d4af37"/>
        <path d="M3 25.5 5.5 25.5 3 23Z" fill="#d4af37"/>
        <path d="M27 25.5 24.5 25.5 27 23Z" fill="#d4af37"/>
      </svg>
      <span class="brand-name">Art Frame <b>TV</b></span>
    </a>
    <ul class="nav-links">
      <li><a href="/#craft">The framing</a></li>
      <li><a href="/#materials">Materials</a></li>
      <li><a href="/#photos">Your photos</a></li>
      <li><a href="/articles/">Guides</a></li>
      <li><a href="/privacy">Privacy</a></li>
    </ul>
    <a class="btn btn-ghost btn-sm" href="/#get">Get the app</a>
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
 "mainEntityOfPage":{jstr(canon)},"datePublished":"2026-10-20","dateModified":"{a.get('updated','2026-10-20')}",
 "author":{{"@type":"Organization","name":"Digital Space Agency UG"}},
 "publisher":{{"@type":"Organization","name":"Art Frame TV"}}}},
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
    toc = "\n".join(
        f'          <li><a href="#{slug(t)}">{t}</a></li>' for t, _ in a["sections"])
    body = "\n".join(
        f'        <h2 id="{slug(t)}">{t}</h2>\n        {c.strip()}'
        for t, c in a["sections"])
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
          Free, no account, no ads. <a href="/">See how it works →</a></p>
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
