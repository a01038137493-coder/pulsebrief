# CLAUDE.md

## Project Purpose
This project builds a Telegram bot service for active stock traders.

The product delivers a very short pre-market briefing to each user with only the most important news and signals they should know before the market opens.

This is not a general news summarizer.  
This is not a long-form market commentary tool.  
This is not an investment advisory product.

The core job is:
- identify what matters today
- filter aggressively
- personalize to the user when possible
- send concise, high-signal messages before trading starts

## Product Definition
Target users:
- active traders
- short-term stock traders
- users who want a fast summary before market open
- users who do not want to read long news articles

Main value proposition:
- deliver only the few things that may affect today's trading decisions
- reduce noise
- save time
- make the message readable in seconds

Primary user outcome:
- within 10 to 30 seconds, the user should understand what matters today

## Non-Goals
Do not optimize for:
- long summaries
- generic financial education
- macro essays
- deep research reports
- broad “top 20 news” lists
- speculative claims without support
- investment guarantees or advice-like wording

## Product Principles
Always optimize for:
1. relevance to today's trading session
2. speed of understanding
3. signal over volume
4. clarity over completeness
5. user usefulness over narrative quality

Every output should answer:
- What happened?
- Why does it matter today?
- What should the trader watch?

If a piece of information does not affect today's market attention, sentiment, volatility, sector movement, ticker movement, or risk, it is usually not worth sending.

## News Selection Rules
Only prioritize news that is likely to matter for the current trading day.

High-priority categories:
- major macro events affecting equities, rates, USD, oil, semiconductors, AI, or major sectors
- earnings surprises or guidance changes
- central bank comments or rate-related developments
- large-cap stock moves that can move sectors or sentiment
- geopolitical events with immediate market implications
- regulatory actions affecting major industries
- overnight market moves in the US or key global markets
- unusual volatility drivers
- company-specific breaking news for names the user tracks
- ETF, index, futures, or sector signals relevant before open

Low-priority categories:
- old news with no fresh market impact
- opinion pieces
- repetitive summaries of already known themes
- low-credibility rumors
- long background explainers
- content with weak linkage to today's trading

## Personalization Rules
When user-specific watchlists or interests exist, prioritize:
1. news directly related to the user's watchlist
2. sector-wide moves affecting those names
3. market-wide risk factors affecting all positions
4. only then broader contextual news

If personalization data is incomplete:
- prefer major market-moving items
- prefer highly liquid names and sectors
- do not invent user preferences

## Message Style Rules
Messages must be extremely concise.

Preferred style:
- short lines
- direct wording
- minimal adjectives
- no dramatic language
- no hype
- no vague commentary
- no unnecessary financial jargon if a simpler phrase works

Each message should be understandable at a glance.

Preferred message structure:
- headline
- why it matters
- watch point

Example structure:
- NVDA suppliers strong overnight
- AI hardware sentiment may stay bid today
- Watch semis at open

Or:
- Fed speaker sounded hawkish overnight
- rate-cut expectations weakened
- Watch growth and high-beta stocks

## Length Constraints
Default briefing should be short enough to read in under 30 seconds.

Guidelines:
- one item: 2 to 3 short lines
- daily briefing: usually 3 to 5 items max
- avoid walls of text
- each item should ideally stay under 200 characters if possible
- if an item cannot be explained briefly, it may not be suitable for the main briefing

## Writing Constraints
Do not write:
- “This stock will go up”
- “You should buy”
- “Guaranteed”
- “Certain move”
- “Safe bet”
- “Must enter now”

Prefer:
- “watch”
- “may affect”
- “could pressure”
- “could support”
- “monitor reaction”
- “key level / key event / key risk”

Never overstate certainty.  
Always separate facts from inference.

## Accuracy Rules
Use the most current reliable information available.  
Time sensitivity matters.

For market-sensitive content:
- recency is critical
- stale news is dangerous
- always prefer primary or highly reliable sources
- if timing is unclear, state uncertainty
- do not present outdated information as fresh

Important:
- clearly distinguish confirmed news from interpretation
- clearly distinguish market reaction from expected impact
- if the causal link is weak, say so

## Ranking / Filtering Heuristics
When selecting what to send, rank items by:
1. immediacy for today's session
2. impact on price, volatility, liquidity, or sentiment
3. relevance to the user's watchlist
4. credibility of source
5. freshness
6. uniqueness versus duplicate news

If multiple articles say the same thing:
- merge them into one insight
- do not repeat the same theme

If there is too much news:
- compress into the few items that best explain today's setup

## Telegram Delivery Principles
Telegram messages should feel native to chat.

Requirements:
- compact
- scannable
- no dense paragraphs
- consistent formatting
- first screen should contain the core value
- the user should not need to tap multiple times to get the main point

Prefer:
- bullet-like lines
- spacing between items
- consistent emoji use only if useful and limited
- stable message templates

Do not:
- overload the message
- include too many links
- send noisy alerts
- send duplicate alerts unless the situation materially changed

## Alert Philosophy
This service should be selective.

Better to send fewer high-quality alerts than many weak alerts.

A message should be sent only if it passes at least one of these tests:
- likely affects today's trading behavior
- likely affects names or sectors the user watches
- meaningfully changes risk sentiment
- helps the user prepare before open

If an item is interesting but not actionable or watch-worthy for today, do not send it.

## System Design Priorities
When building features, prioritize:
1. relevance engine quality
2. timeliness
3. personalization
4. summary quality
5. delivery reliability
6. low latency
7. observability and error handling

## Engineering Principles
- prefer simple architecture first
- keep modules small and testable
- isolate news ingestion, ranking, summarization, personalization, and delivery
- avoid tightly coupling business logic to Telegram transport
- design for retries and partial failures
- log why a news item was selected or rejected when possible

Recommended logical components:
- ingestion
- deduplication
- credibility filtering
- ranking
- summarization
- personalization
- scheduling
- Telegram delivery
- analytics / feedback loop

## Data / Domain Rules
Important entities likely include:
- user
- watchlist
- alert preference
- news item
- source
- relevance score
- delivery log
- daily briefing
- market session / timezone

Always handle timezone carefully.  
Pre-market timing must be correct for the target market and user setting.

## Safety / Compliance Constraints
This product must avoid sounding like regulated personalized investment advice.

Do not:
- provide direct buy/sell instructions
- guarantee outcomes
- misrepresent confidence
- hide uncertainty
- fabricate sources or rationale

Always:
- frame output as informational and watch-oriented
- keep claims proportional to evidence
- preserve auditability of source-to-summary mapping where possible

## UX Rules
Users are busy and attention is scarce.

Every user-facing decision should reduce friction:
- fewer taps
- fewer words
- faster understanding
- stronger relevance

When uncertain between “more complete” and “more useful now,” choose “more useful now.”

## Testing Rules
Before considering work complete:
- test the ranking logic on realistic news sets
- test message length and readability in Telegram format
- test duplicate suppression
- test stale-news filtering
- test per-user personalization behavior
- test timezone and schedule behavior
- test failure handling for source fetch and Telegram send
- verify that summaries preserve factual meaning

For summarization-related changes:
- compare source facts against final message
- ensure no invented numbers, dates, or causal claims were introduced

## Evaluation Metrics
Optimize toward:
- open/read usefulness
- click-through only when relevant
- user retention
- alert relevance feedback
- low mute/unsubscribe rate
- low false-positive alert rate
- high “this mattered today” rate

Avoid vanity metrics that reward message volume.

## Coding Rules
- read the current code before changing architecture
- prefer minimal diffs unless a structural problem is clear
- avoid adding dependencies unless they materially help
- preserve separation between data fetching, decision logic, and presentation
- write explicit names instead of clever names
- document non-obvious business rules in code

## Output Expectations for Claude
When working in this repository:
1. first identify the product impact of the task
2. explain the proposed change briefly
3. keep implementation aligned with the product goal: concise, timely, relevant
4. avoid unnecessary refactors
5. call out risks, assumptions, and missing data
6. mention how the change affects timeliness, relevance, or user trust
7. for user-facing copy, make it shorter before making it prettier

## Preferred Response Format
For completed tasks, respond using this structure:

- Problem
- What changed
- Why this approach
- Files touched
- Validation
- Risks / follow-ups

## Example of Good Output
Good:
- US futures weak after hawkish Fed remarks
- rate-cut hopes faded overnight
- Watch QQQ, growth, regional banks

Bad:
- Investors are becoming increasingly concerned after a series of comments from central bank officials, which may potentially create uncertainty in the markets today and therefore traders should be careful.

## Final Standard
This product wins only if the message is:
- fast
- relevant
- trustworthy
- brief
- useful before the open

When in doubt, remove noise and increase signal.