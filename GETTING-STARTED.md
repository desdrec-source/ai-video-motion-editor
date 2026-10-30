# Getting started (Windows)

A step-by-step setup for the AI Video Motion Editor, written for people who have never used a
terminal. Set aside about **30–45 minutes** the first time. You only do this once.

**What you'll end up with:** the toolkit on your PC, opened in Claude Code, and your first recording
cut for you.

**The short version:** to try it, you need a Claude plan and **one free AssemblyAI key**. Everything
else is optional until you want it.

---

## Two words you'll see everywhere

- **Claude Code** is an AI assistant that works on your computer. You talk to it in normal English,
  and it reads your files, runs commands and makes the edits. You direct; it does the typing.
- **A skill** is a written playbook for one job, like "cut this video" or "add sound effects".
  This toolkit is a set of these playbooks in order. You never open them. You say what you want,
  and Claude picks the right one.

A few more, explained the first time they come up:

- **Terminal:** a plain text window where you type commands instead of clicking buttons.
- **API key:** a long password that lets the toolkit use an online service on your account.
- **PATH:** the list of places Windows looks for programs. "Not recognized" errors usually mean a
  program isn't on it yet.

---

## Before you start

You'll need:

- **A Windows 10 or 11 PC.** (Mac users: see the [FAQ](#faq).)
- **A Claude plan that includes Claude Code.** There's no free tier; **Claude Pro** is the cheapest
  plan (check the current price on claude.com). Anthropic API credits also work.
- **A free AssemblyAI account** for transcription. Step 6 shows where to get the key.
- **About 2 GB of free disk space.**

Everything else is optional; see [What it costs](#what-it-costs).

---

## Step 1: Open a terminal

1. Press the **Windows key**, type **Terminal**, and press **Enter**.
2. A window with a blinking cursor opens. This is **PowerShell**. You'll paste commands here.

**How to run a command:** copy it from this page, right-click in the terminal to paste, then press
**Enter**. Wait until the cursor comes back before running the next one.

---

## Step 2: Install the tools the toolkit needs

Paste these **one at a time**. If Windows asks "Do you want to allow this app to make changes?",
click **Yes**.

```powershell
winget install --id Git.Git -e
```

```powershell
winget install --id Python.Python.3.12 -e
```

```powershell
winget install --id OpenJS.NodeJS.LTS -e
```

```powershell
winget install --id Gyan.FFmpeg -e
```

- **Git** downloads the toolkit and its updates. (Optional: you can download a ZIP instead in Step 4.)
- **Python** runs the editing tools.
- **Node.js** runs **Remotion**, the engine that draws the on-screen graphics.
- **FFmpeg** does the actual video cutting and converting.

**Optional: VS Code.** If you like having your files and a terminal in one window, also install
**VS Code**, a free code editor from Microsoft:

```powershell
winget install --id Microsoft.VisualStudioCode -e
```

**Important: close the terminal and open a new one** (Step 1 again). New programs only show up in a
fresh terminal.

**Check it worked.** Paste this into the new terminal:

```powershell
git --version; python --version; node --version; ffmpeg -version | Select-Object -First 1
```

You should see four short lines, each with a version number. Your numbers may be different from
anyone else's; that's fine, as long as you see four lines. If one says
*"not recognized"*, see [Troubleshooting](#troubleshooting).

---

## Step 3: Install Claude Code

Pick **one** of these:

- **The Claude desktop app (easiest).** Download it from
  [claude.com/download](https://claude.com/download), sign in, and use the **Code** tab.
- **In the terminal.** Paste:

  ```powershell
  irm https://claude.ai/install.ps1 | iex
  ```

  It keeps itself updated, so you only do this once. Close and reopen the terminal, then check it
  worked:

  ```powershell
  claude --version
  ```

  If that prints a version number, you're done.
- **Inside VS Code.** Click the **Extensions** icon on the left (or press **Ctrl+Shift+X**), search
  **Claude Code**, and install the one published by **Anthropic**. It adds a Claude chat panel to
  VS Code.

Whichever you pick, the first time you start Claude Code it opens your browser to sign in to your
Claude account.

---

## Step 4: Download the toolkit

### Option A: with Git (recommended, because updates are one command)

This puts the toolkit in a folder called `ai-video-motion-editor` inside your **Documents** folder.
Paste these one at a time:

```powershell
cd $HOME\Documents
```

```powershell
git clone https://github.com/desdrec-source/ai-video-motion-editor
```

```powershell
cd ai-video-motion-editor
```

(`cd` means "change directory": it walks you into a folder.)

### Option B: download a ZIP (no Git needed)

1. Open [github.com/desdrec-source/ai-video-motion-editor](https://github.com/desdrec-source/ai-video-motion-editor).
2. Click the green **Code** button, then **Download ZIP**.
3. Unzip it into your **Documents** folder. The folder is called `ai-video-motion-editor-main`.
4. In the terminal, go into it:

   ```powershell
   cd $HOME\Documents\ai-video-motion-editor-main
   ```

ZIP users don't get one-command updates: to update, download a new ZIP and copy your `.env` and
`videos` folder across.

### Install the toolkit's parts (everyone)

**Stay in the toolkit folder** for everything from here on. The tools look for your files starting
from the folder you're in.

```powershell
python -m venv venv
```

```powershell
venv\Scripts\python -m pip install -r requirements.txt
```

```powershell
cd remotion; npm install; npm run gen; cd ..
```

- The first command makes a **venv** ("virtual environment"): a private box for this toolkit's
  Python tools, so they don't clash with anything else on your PC.
- The second installs the tools on its shopping list (`requirements.txt`) into that box.
- The third installs the graphics engine and builds the list of graphics. It ends by printing a
  list of names like `BigStatement` and `EndCard`. That means it worked.

**Seen a red "certificate" error?** That's your antivirus, not you. See
[Certificate errors](#certificate-errors-antivirus) below.

**Seen a yellow `npm warn allow-scripts … esbuild` message?** That's harmless. You can ignore it.

---

## Step 5: See it working

Before you record anything, open the example graphics in your browser:

```powershell
cd remotion; npm run studio
```

**Remotion Studio** opens in your browser with the toolkit's **37 example graphics** listed on the
left. Click any one and press play. This is what the toolkit builds over your videos.

When you're done looking, click back in the terminal, press **Ctrl+C** to stop it, then go back to
the toolkit folder:

```powershell
cd ..
```

---

## Step 6: Add your keys

Your keys live in a file called `.env` in the toolkit folder. It **never** gets uploaded anywhere.

1. Make your own copy of the example file:

   ```powershell
   copy .env.example .env
   ```

2. Open it in Notepad (or click it in VS Code):

   ```powershell
   notepad .env
   ```

3. Paste each key straight after its `=` sign, with no spaces, so a line looks like
   `ASSEMBLYAI_API_KEY=abc123...`
4. **Save** (Ctrl+S) and close it.

| Key | What it does | Where to get it | Need it to start? |
|---|---|---|---|
| `ASSEMBLYAI_API_KEY` | Transcribes your video so Claude can read it and cut it | [assemblyai.com](https://www.assemblyai.com) → your dashboard → **API key** | **Yes.** The free tier is enough to try it |
| `ELEVENLABS_API_KEY` | Cleans your voice, makes sound effects and music | [ElevenLabs](https://tinyurl.com/Try-Eleven-Labs)\* | **No.** Paid. The voice clean-up has a free option (below) |
| `ELEVENLABS_VOICE_ID` | Your own AI voice, for AI voiceovers | Your ElevenLabs voice library | **No.** Only for AI voiceovers |
| `GEMINI_API_KEY` | Draws your thumbnails | [ai.google.dev](https://ai.google.dev) | **No.** Only when you make thumbnails |

**Two ways to keep your first run cheap:**

- **Free voice clean-up.** The voice step can use **RNNoise**, which runs on your own PC with no key
  and no cost. ElevenLabs does better on tough noise like wind, traffic or a busy cafe, but RNNoise
  is often enough for a quiet room.
- **YouTube needs no key.** Uploading uses a one-time sign-in in your browser instead. Set it up when
  you're ready to upload: the steps are in [`tools/yt_upload_SETUP.md`](tools/yt_upload_SETUP.md).

**Never share your `.env` file or paste your keys in a chat, a screenshot or a video.** Anyone with
your key can spend your credits.

\* *Affiliate link: if you sign up through it, I may earn a commission at no extra cost to you.*

---

## Step 7: Open the toolkit in Claude Code

- **Desktop app:** open the **Code** tab and choose the toolkit folder in your Documents.
- **Terminal:** from inside the toolkit folder, type `claude` and press **Enter**.
- **VS Code:** choose **File → Open Folder**, pick the toolkit folder, then open the Claude Code
  panel (the Claude icon at the top right), or open **Terminal → New Terminal** and type `claude`.

The skills come with the toolkit (in its `.claude/skills` folder), and Claude Code finds them
automatically. There's nothing to switch on.

Then just ask in plain English. **Start with your brand:**

> set up my brand

Claude asks about your channel name, colours, fonts, video size and sound taste, shows you a
proposal, and renders a preview card. If you skip this, your videos will look like
AI Video Motion's, not yours.

---

## Step 8: Your first video

1. **Record yourself** talking to camera, or recording your screen with your face in the corner.
   Keep the first one short (1–2 minutes).
2. **Make a folder for it** inside `videos`, for example `videos\video-1`, and put the recording in
   it. That's all: the skills create every other folder they need.
3. **Screen recordings: fix the frame rate first.** Most screen recorders (Panda, OBS, Loom and
   others) save a *variable* frame rate, which makes graphics drift away from your voice. Convert
   it to a steady 30 frames per second. Replace `recording.mp4` with your file's name:

   ```powershell
   ffmpeg -i videos\video-1\recording.mp4 -vf fps=30 -fps_mode cfr -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k videos\video-1\recording-30fps.mp4
   ```

   Then keep only the `-30fps` file in the folder, and move the original somewhere safe.
4. **Walk the pipeline**, one plain sentence at a time. Each step hands its work to the next, and
   you approve as you go:

   | Say this | What happens |
   |---|---|
   | `clean cut videos/video-1` | Transcribes your recording word by word, lists the ums, false starts and long pauses it would cut, and **waits for your OK** before cutting |
   | `add graphics to video-1` | Builds the on-screen graphics, each timed to the word you say it on |
   | `clean the audio for video-1` | Removes background noise from your voice |
   | `suggest sfx for video-1` | Adds quiet sound effects on the exact words that matter |
   | `package this video` | Writes one title and three thumbnail options |
   | `upload it as a private draft` | Uploads to YouTube as private, so you can check it before publishing |

Your original recording is never changed. Every step makes new files.

---

## The skills, one line each

You'll hear these names as you work. You never need to type them; Claude picks them for you.

| Skill | What it does |
|---|---|
| `brand-setup` | **Run this first.** Makes everything look like your channel. |
| `clean-cut` | Step 1. Cuts your raw recording into a clean master and notes when every word is said. |
| `make-tsx` | Step 2. Builds the on-screen graphics as code, synced to your words. |
| `fake-screencast` | Part of step 2. Turns screenshots into a realistic screen recording, cursor and clicks included. |
| `clean-audio` | Step 3. Removes the room noise from your voice and keeps your levels. |
| `suggest-sfx` | Step 4. Places sound effects on the exact word, from a library that grows every video. |
| `packaging` | Step 5. One title and three thumbnail options for YouTube's thumbnail test. |
| `thumbnail` | Makes and refines thumbnails on their own. |
| `vidtsx-2d-generator` | The rulebook that keeps graphics from crashing. You never call it directly. |

---

## What it costs

**The toolkit is free.** The services it uses are paid, on your own accounts. Prices change, so
check each provider before planning a big batch.

| Service | For | Cost |
|---|---|---|
| **Claude Code** | Running everything | Paid. No free tier; Claude Pro is the cheapest plan |
| **AssemblyAI** | The cut (step 1) | Free tier is enough to try it |
| **[ElevenLabs](https://tinyurl.com/Try-Eleven-Labs)**\* | Voice clean-up, sound effects, music | Paid. The voice clean-up has a free local option |
| **Gemini** | Thumbnails | Paid, and only if you make thumbnails |
| **YouTube** | Upload | Free, browser sign-in |

Also worth a look for voice work: **[Fish Audio](https://tinyurl.com/TryFishAudio)**\*, which I use for
voiceovers and voice cloning. It isn't wired into the toolkit's scripts yet.

\* *Affiliate link: if you sign up through it, I may earn a commission at no extra cost to you.*

---

## Getting updates

When I improve the toolkit, get the latest version by running this inside the toolkit folder:

```powershell
git pull
```

Your `.env` keys and your `videos` folder are not touched by updates. (Downloaded the ZIP? See
Step 4, Option B.)

---

## FAQ

**Do I need to know how to code?**
No. You type plain English and review what comes back. The only file you touch is `.env`, and
that's copy and paste.

**Is it really free?**
The toolkit is free and MIT-licensed. The services it calls are paid, on your own keys. The
cheapest way to try it is one free AssemblyAI key plus the free voice clean-up, so your first video
can cost close to nothing beyond your Claude plan.

**What's the smallest set of keys I need?**
One: a free AssemblyAI key. That runs the cut, which is the heart of it. Add the others when you
want voice clean-up, sound effects or thumbnails.

**Can I use my screen recordings?**
Yes. Just convert them to a steady 30 fps first (Step 8). The toolkit also builds graphics like
diagrams, title cards and mock app screens for you, so you don't have to film those.

**Does this work on a Mac?**
It should: Claude Code, Python, Node.js and FFmpeg all run on Mac. Install them with
[Homebrew](https://brew.sh) instead of `winget`, install Claude Code with
`curl -fsSL https://claude.ai/install.sh | bash`, and use `./venv/bin/python` wherever this guide
says `venv\Scripts\python`. This guide is tested on Windows.

**Something said "not recognized" or "ModuleNotFoundError". What now?**
See [Troubleshooting](#troubleshooting) just below.

---

## Troubleshooting

| What you see | What it means | Fix |
|---|---|---|
| `'git'` / `'python'` / `'node'` / `'ffmpeg'` / `'claude'` **is not recognized** | The terminal was opened before the install, or the program isn't on your PATH yet | Close the terminal, open a new one, try again |
| `python` opens the **Microsoft Store** | Windows' placeholder Python is in the way | Open a new terminal after Step 2. If it still happens: Windows Settings → search **"App execution aliases"** → turn off both **python** entries |
| **`CERTIFICATE_VERIFY_FAILED`** or **SSL** errors | Your antivirus scans secure web traffic | See [Certificate errors](#certificate-errors-antivirus) |
| **`ModuleNotFoundError`** (`requests`, `PIL`, `google`…) | A tool ran with the wrong Python | Run tools as `venv\Scripts\python tools\...`, from the toolkit folder |
| **`… not found in .env`** | A key is missing | Open `.env` (Step 6) and add it |
| Graphics **drift out of sync** with your voice | Variable frame rate recording | Convert to 30 fps first (Step 8) |
| **`npm warn allow-scripts`** about **esbuild** | A safety warning from npm | Harmless, ignore it |
| Anything else | | Copy the error, paste it into Claude Code, and ask "what does this mean and how do I fix it?" |

### Certificate errors (antivirus)

Antivirus programs like **AVG** and **Avast** check secure web traffic, and some tools don't
recognise their certificate.

1. **Update pip first.** Newer versions of pip (24.2 and later) trust your antivirus automatically:

   ```powershell
   venv\Scripts\python -m pip install --upgrade pip
   ```

   Then run the Step 4 install again.

2. **If updating pip itself fails** with the same error, point it at your antivirus certificate for
   that one command. For **AVG**:

   ```powershell
   venv\Scripts\python -m pip install --upgrade pip --cert "C:\ProgramData\AVG\Antivirus\wscert.pem"
   ```

   For **Avast**, use `"C:\ProgramData\Avast Software\Avast\wscert.pem"` instead. After that, pip
   is up to date and works normally.

**Don't** turn off your antivirus or use "trusted host" tricks to get around this.

---

## Want help?

Join the **[AI Video Motion community](https://tinyurl.com/AIVideoMotion)** for walkthroughs, help
getting set up, and how to make AI video and motion that looks finished.
