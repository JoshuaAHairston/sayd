# Sayd

A service that texts curated quotes to recipients. Each morning it asks a recipient if they want a quote, and the recipient replies with a mood to receive a quote that fits it.

## Language

**Quote**:
A piece of text written by the author of the service, delivered verbatim to recipients. Never generated or altered when sent.
_Avoid_: Saying, message

**Author**:
The person who writes the quotes and operates the service (the owner).
_Avoid_: Admin, owner

**Recipient**:
A person who receives the morning text and may reply to it.
_Avoid_: User, subscriber, sender

**Morning text**:
The daily outbound message, sent at the recipient's chosen time, that asks whether they want a quote and starts the loop. It does not contain a quote.
_Avoid_: Daily blast, notification

**Reply**:
An inbound text from a recipient, in response to a morning text or otherwise.
_Avoid_: Message, request (unless it has passed the gate)

**Trigger phrase**:
The phrase `quote me:` that a reply must begin with to be treated as a request._Avoid_: Command, keyword

**Tag**:
A label the author assigns to a quote to say which moods it suits. Tags are what requests are filtered by.
_Avoid_: Category, topic, theme

**Mood**:
The feeling or situation a recipient states after the trigger phrase, in free text (e.g. "anxious about work"). It is interpreted into one or more tags.
_Avoid_: Topic, theme, query

**Request**:
A reply that passed the gate: it contains the trigger phrase followed by a mood.
_Avoid_: Query, ask

**Help text**:
The reply, explaining how to ask for a quote, sent only when a recipient texts `Help`.
_Avoid_: Error message

**Best match**:
The quote chosen from several candidates as the best fit for a mood.
_Avoid_: Result, hit

**Closest match**:
The quote sent when no quote fits a mood well; the best available fallback.
_Avoid_: Fallback quote, random quote

**Unmatched request**:
A request that could only be answered with a closest match. The recipient's raw mood text is kept in the author log so the author can write quotes for that mood.
_Avoid_: Miss, failed request

**Visited**:
A quote that has already been sent to a given recipient. A recipient is never sent a visited quote again until it is reset.
_Avoid_: Seen, used, sent

**Exhausted tag**:
A tag for which a recipient has visited every quote carrying it.
_Avoid_: Empty category

**Reset**:
Clearing a recipient's visited quotes that carry an exhausted tag so they can be sent again.

**Setup**:
The short first conversation in which a newly added recipient chooses the time of their morning text, and which they can repeat later to change it.
_Avoid_: Onboarding, signup

**Usage hint**:
The short reply, `quote me: <how you feel> or Help`, sent when a reply is neither a request, `Help`, nor a stop or start.
_Avoid_: Error message, fallback

**Author log**:
The record the author reads to see unmatched requests, exhausted tags and resets, each logged as its own kind of entry and ranked by frequency.
_Avoid_: Notifications, alerts
