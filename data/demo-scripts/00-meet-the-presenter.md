---
type: scenario
title: "0. Meet the presenter"
tags: ["scenario-0"]
level: standard
---
**Level:** Standard.


*Optional opener: the platform introduces itself, in a voice the room chooses, and can present the
rest of the day on request.*

**You are** Dana. Agents → `presenter`. The engine needs the Kokoro voices and the cloning TTS model
(see *Voices on the engine* below).

1. Above the chat, the voice bar: press *Voice* and let the audience pick **Emma** or **Michael**. The
   presenter introduces itself in that voice under that name, and *Read replies aloud* is on: every
   reply from here is spoken, one paragraph at a time.
2. Ask: **"What is the enforcement mode right now?"** The presenter checks the platform and answers in
   a sentence or two, spoken.
3. Ask: **"Run scenario 4."** It reads the script from the `demo-scripts` store and gives you the first
   step only: who must be signed in and in which window, what to do there, and what the room should
   see. Do it in that window, then say **"next"**; it never moves on by itself. Where a step is a
   switch it holds (enforcement, the classifier, evaluations, the member cap) it flips it in that
   same turn and says so. A question in the middle gets a spoken paragraph and "say next when you
   are ready"; the last step ends with the scenario's closing point.
4. *Lend your voice*: an audience member types their first name, agrees on screen, reads the passage,
   ten seconds record with a meter, and the presenter carries on in their voice under their name —
   "I'm Alex, or at least I sound like him today." *Forget this voice* deletes the clip, audited; the
   presenter falls back to the preset the room chose. Say: nothing was trained and nothing left the Mac.

**Land:** the product can explain itself, run its own demonstration, and prove the data-lifecycle
promise on a volunteer's own voice in under a minute.

**Voices on the engine.** The presets are Kokoro voices; the lent voice uses the cloning TTS model.
Both models are pulled once. MLX Serve's pull skips a repository's subdirectories, so two files must
be fetched by hand after the pull, and the engine lists a pulled model by its bare name:

```
# in the engine's models directory (MLX Core: ~/.mlx-serve/models of the account running it)
curl -X POST localhost:11234/api/pull -d '{"model":"ddalcu/Kokoro-82M-MLX-Serve"}'
mkdir -p ddalcu/Kokoro-82M-MLX-Serve/g2p && for f in gb_gold us_gold us_silver; do
  curl -sL https://huggingface.co/ddalcu/Kokoro-82M-MLX-Serve/resolve/main/g2p/$f.json -o ddalcu/Kokoro-82M-MLX-Serve/g2p/$f.json; done
ln -sfn "$PWD/ddalcu/Kokoro-82M-MLX-Serve" Kokoro-82M-MLX-Serve
curl -X POST localhost:11234/api/pull -d '{"model":"mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit"}'
mkdir -p mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit/speech_tokenizer && curl -sL \
  https://huggingface.co/mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit/resolve/main/speech_tokenizer/config.json \
  -o mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit/speech_tokenizer/config.json
# then restart the engine (quit and reopen MLX Core): it discovers the files at start-up
```

Then Models tab → activate the Qwen3-TTS entry for the *tts* role, and load Kokoro once from the Local
LLM tab (it stays resident; both fit beside Gemma). The presenter's presets name the model as the
engine lists it, `Kokoro-82M-MLX-Serve`.

---
