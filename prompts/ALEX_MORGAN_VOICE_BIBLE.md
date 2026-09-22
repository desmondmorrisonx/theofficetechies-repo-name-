# ALEX & MORGAN — VOICE REPLICATION BIBLE (JOY FIX)

Old `voice-00` / `voice-01` **die in a new chat**. Recreate with `add_voice`, then lock ids.

**Why the last prompt failed:** Alex was auditioned on slow, grave copy (“pull up a chair… I have been behind a microphone a long time”). That **casts a tired narrator**. Alex must be auditioned on **live-show joy** or the model will never smile.

---

## 1. First turn — BOTH `add_voice` IN PARALLEL

Do not `generate_speech` until both battles resolve.

### Alex (Host A) — JOY IS THE CONSTRAINT

```
add_voice
  language: "en"
  voice_identity.gender: "masculine"
  voice_identity.use_case: "entertainment"
  text: "Wooo we are live and I am grinning! Folks this story is ridiculous and I love it. A gym, a donate button, confetti on zero dollars. Come on! Stay with me, this is going to be fun."
```

**Alex must sound like:** a man on a live show, full of excitement and joy, ready to laugh. Bright, awake, smiling. Not NPR. Not a eulogy. Not a documentary.

**Reject and increment `voice_identity.index` (keep the same joyful text) if Alex sounds:**
- flat, tired, whispery, sleepy
- old-grave “60 years of radio” funeral
- robotic / AI monotone
- angry, shouty, or hard-sell announcer
- childlike or tiny

Do **not** switch Alex to `narration` or `educational`. Those remove the joy. Stay on `entertainment`. If two entertainment pairs fail, try `use_case: "advertising"` **once**, same joyful audition, still masculine `en`. Then go back to entertainment + higher index.

### Morgan (Host B)

```
add_voice
  language: "en"
  voice_identity.gender: "feminine"
  voice_identity.use_case: "entertainment"
  text: "Ha I cannot stop laughing. I'm Morgan. Picture the email in all caps and a progress bar celebrating zero dollars. We tell it funny and we tell it true. Come on, let's talk like people."
```

Reject Morgan if she is whispery, childlike, or ad-bot flat. Increment `index`. Keep feminine + entertainment + `en`.

**Audition rules:** 30–45 words, ~15 seconds, plain words, no SSML, no brackets. Alex’s audition must contain energy words: *wooo, grinning, love it, come on, fun*. Never audition Alex on somber memoir copy.

After picks, write `/home/user/VOICE_LOCK.md`:

```
ALEX_VOICE_ID=voice-XX
MORGAN_VOICE_ID=voice-YY
language=en
alex_gender=masculine
morgan_gender=feminine
use_case=entertainment
alex_must_sound=joyful live-show man
```

Use **only** those ids. Never swap.

---

## 2. Who they are

### Alex
Masculine, English, lead host. **Joyful live-show man.** Excitement, grin, laughter in the talk. Funny and engaging. He can tell a long story **without** dropping into a sad-old-DJ register. Energy stays up even in the heavy beat. Senior architect at The Office 360.

### Morgan
Feminine, English, co-host. Fast, human, laughs, holds the screenshot and the punchline. Not an ad-reader.

---

## 3. Script shape (this keeps joy after casting)

Every Alex clip should **open on energy**, not on a eulogy:

**IN:** “Wooo we are live and I am grinning…” / “Come on, folks, this part is ridiculous and I love it…”  
**OUT:** “I have sat behind more microphones than I care to count…” as the *first* sentence of a clip. That line **kills joy in TTS**. If you need veteran craft, put it in the middle of a bright paragraph, never as the cold open.

Do: contractions, “ha”, “I love this”, “come on”, specific pictures.  
Do not: `(laughs)`, `[excited]`, “no sponsor in the chair”, slogan stacks.

Phonetics: `the office 360 dot com` · `S T U D I O 5 0` · `theofficetechies at gmail.com`
