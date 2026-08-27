# Style

Typographic and formatting patterns. Every one of these is caught deterministically by `tools/lint.sh`, so there is no excuse for any of them reaching a draft. Run the linter.

| # | Pattern |
| --- | --- |
| 13 | Em Dashes (zero tolerance) |
| 14 | Overuse of Boldface |
| 15 | Inline-Header Vertical Lists |
| 16 | Title Case in Headings |
| 17 | Emojis |
| 18 | Curly quotation marks and apostrophes |

---

### 13. Em Dashes (zero tolerance)

**Rule:** ZERO em dashes (`—`) allowed. Replace every instance with a comma, period, colon, or parentheses. No exceptions.

**Problem:** LLMs use em dashes far more than humans, mimicking "punchy" sales writing. AI detectors specifically flag em dash frequency.

**Before:**

> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After:**

> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

### 14. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**

> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**

> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

---

### 15. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**

> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**

> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

### 16. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**

> ## Strategic Negotiations And Global Partnerships

**After:**

> ## Strategic negotiations and global partnerships

---

### 17. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**

> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:**

> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

---

### 18. Curly quotation marks and apostrophes

**Problem:** ChatGPT uses curly quotes ("\u201c...\u201d") and curly apostrophes (\u2019) instead of straight quotes ("...") and straight apostrophes (').

**Before:**

> He said \u201cthe project is on track\u201d but others disagreed. It\u2019s a known issue that doesn\u2019t affect users.

**After:**

> He said "the project is on track" but others disagreed. It's a known issue that doesn't affect users.

---

## COMMUNICATION PATTERNS

---
