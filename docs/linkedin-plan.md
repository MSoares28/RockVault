# RockVault — LinkedIn Content Plan

This file tracks the planned LinkedIn posts for the RockVault project.
Each post is tied to a development phase and should be published when that phase is complete.

---

## Post 1 — End of Phase 2 ✅ READY TO POST
**Theme:** "I built an API that downloads MP3s from YouTube in less than a day"

**What to show:**
- Screenshot of Swagger UI with /download and /files routes
- Screenshot of the terminal showing the .mp3 file in the downloads/ folder
- Brief explanation of the tech choices: FastAPI, yt-dlp, headless Ubuntu Server

**Tone:** Humble and technical. Not "I built an amazing project" but
"I solved a real problem and learned how APIs work from the inside."

---

## Post 2 — End of Phase 3
**Theme:** "I connected a frontend to my backend — and finally understood
what really happens inside an HTTP request"

**What to show:**
- Short video or GIF of the UI working in the browser
- The full flow explained: button click → POST request → yt-dlp → MP3 saved
- One thing that surprised you during the process

**Tone:** Focus on learning, not on the feature itself.

---

## Post 3 — Phase 4 (most differentiated post)
**Theme:** "I studied my own API as if I were an attacker"

**What to show:**
- Screenshot of Wireshark or server logs showing a real request flowing through
- Something you saw that you didn't expect
- What security question that raised for you

**Tone:** Technical curiosity. This post separates you from 90% of junior candidates.

---

## Post 4 — Phase 5 (the portfolio post)
**Theme:** "I found and fixed vulnerabilities in my own application"

**What to show:**
- The vulnerability (e.g. SSRF on the /download endpoint)
- How you discovered it
- How you fixed it
- Link to the GitHub repo with the full documented commit history

**Tone:** This is the post that lands in front of security recruiters.
Not "look what I built" — "look how I think."

---

## Golden Rule

Never post "I finished X."
Always post "I learned Y by doing X, and here is what that means in practice."
That difference is what separates a portfolio from a hobby.