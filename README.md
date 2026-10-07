# Sayd

Sayd is a small service that texts you a quote when you need one.

Every morning it sends a text asking if you want a quote. You reply with how you feel, and it sends back a quote that fits. Every quote is written by the author, and Sayd never makes one up.

> **Status:** design phase. Nothing is built yet. The design lives in [issue #1](../../issues/1), and the work is broken into tickets #2 to #14.

## How it works

1. The author adds you as a recipient, with your phone number and timezone.
2. Your first text starts a short setup. You reply with the time you want your morning text, like `8am` or `7:30pm`.
3. Each day at that time, Sayd texts you asking if you want a quote.
4. You reply with the trigger phrase and a mood:

   ```
   quote me: anxious about work
   ```

5. An agent maps your mood onto the author's tags, picks the best-fitting quote you haven't received yet, and Sayd texts it back word for word.

Other messages:

- `Help` explains how to ask for a quote.
- Any other message gets a short reminder: `quote me: <how you feel> or Help`.
- `STOP` and `START` pause and resume the texts.
- Messages from numbers the author hasn't added are ignored.

### No repeats

A recipient never receives the same quote twice until they have seen every quote for that mood. After that, the quotes for that tag are cleared and can be sent again, with nothing said.

### When nothing fits

If no quote fits a mood well, you get the closest match. Your exact words are saved in an author log, so the author knows which quotes to write next.

## For the author

You manage everything over SSH with a single command-line script. Planned commands:

| Command | What it does |
|---|---|
| `add-quote` | Add a quote with tags. Warns over 160 characters and asks before creating a new tag. |
| `list-quotes`, `edit-quote`, `delete-quote` | Manage your quotes. |
| `list-tags` | See your tags and how many quotes each has. |
| `add-recipient`, `list-recipients` | Allowlist people and see their state and send time. |
| `unmatched` | See the moods that had no good match, ranked by how often they came up. |
| `send-due` | Send the morning texts that are due. Cron runs it every minute. |
| `migrate` | Apply database migrations. |

## Design

- **The agent only picks.** A small Claude model maps a mood onto the author's existing tags and returns a quote ID. The code looks up the exact quote text, so a message can't contain words the author didn't write.
- **Pure decisions, thin edges.** Routing a text and choosing a quote are plain functions with no Twilio or LLM. Only the messaging client and the agent talk to the outside.
- **One database, raw SQL.** Postgres through `psycopg`, with no ORM, and a small custom migration runner that applies numbered `.sql` files. See [ADR 0001](docs/adr/0001-postgres-over-sqlite.md).
- **Fast webhook.** The webhook validates Twilio's signature, answers immediately, and does the slow work in the background, so Twilio never times out.

## Stack

- Python, FastAPI
- Postgres (`psycopg`, raw SQL)
- Twilio SMS
- Anthropic API (Claude Haiku)
- A single VPS running Postgres, the app under systemd, and Caddy for TLS (no containers)
- pip and venv, ruff, pyright, pytest
