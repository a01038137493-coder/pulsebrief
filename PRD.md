# PRD.md

## Product Name
Working name: Pre-Market Telegram Briefing Bot

## One-Line Summary
A Telegram bot that sends each active stock trader a very short, high-signal pre-market briefing with only the few things they should know before the market opens.

## Problem
Active traders face too much noise before the market opens.
They do not have time to read long articles, browse multiple apps, or manually filter what actually matters for today's session.

Most financial news products fail in one of these ways:
- too long
- too broad
- too generic
- too delayed
- not personalized
- not useful for immediate trading preparation

## Goal
Help users understand what matters today in under 30 seconds before they start trading.

## Target Users
Primary users:
- active stock traders
- short-term traders
- users who check markets before open
- users who want concise, actionable watchpoints

Secondary users:
- swing traders who want a fast morning market setup
- users with a defined watchlist

## Core User Job
Before the market opens, the user wants to quickly know:
- what happened
- why it matters today
- what to watch at the open

## Non-Goals
This product is not:
- a full research terminal
- a long-form market newsletter
- a portfolio management tool
- a social feed
- a direct buy/sell signal engine
- a guaranteed alpha product
- a fully autonomous trading agent

## Main Use Case
Each morning before the target market opens:
1. the system gathers relevant market-moving news
2. filters and ranks it
3. personalizes it if the user has a watchlist
4. summarizes the top items in a very short format
5. sends the message through Telegram

## User Stories
### Core
- As an active trader, I want a very short morning message so I know what matters before I trade.
- As a trader with a watchlist, I want the briefing to prioritize names and sectors I care about.
- As a busy user, I want the bot to cut noise and avoid spam.
- As a user, I want the message to be readable in seconds, not minutes.

### Trust / Quality
- As a user, I want only credible and fresh information.
- As a user, I do not want repeated alerts for the same story unless something materially changed.
- As a user, I want facts separated from interpretation.

## MVP Scope
The MVP should include:

### 1. User onboarding
- Telegram bot start flow
- user timezone setting
- market preference setting
- optional watchlist input
- optional sector interest input

### 2. News ingestion
- pull from selected trusted news sources
- ingest headlines, timestamps, source, symbols if available
- support deduplication

### 3. Relevance engine
- rank news by likely impact on today's session
- detect market-wide, sector-wide, and ticker-specific relevance
- prioritize freshness
- prioritize user watchlist relevance

### 4. Summarization
- compress selected items into ultra-short text
- preserve factual accuracy
- avoid hype and advice-like language

### 5. Telegram delivery
- send a pre-market briefing at user-configured time
- support one daily main briefing in MVP
- basic formatting for fast reading

### 6. Basic analytics
- delivery success / failure
- open proxy if measurable
- user mute / unsubscribe events
- feedback options like “useful / not useful”

## Out of Scope for MVP
- intra-day continuous alerts
- advanced portfolio analytics
- broker integration
- auto-trading
- chart generation
- deep LLM conversational assistant
- multilingual support beyond initial target language unless specifically planned

## Product Principles
The product must be:
- concise
- timely
- trustworthy
- personalized
- low-noise

Decision rule:
If a feature improves volume but reduces relevance, reject it.

## Content Principles
Every item in the briefing should answer:
1. What happened?
2. Why does it matter today?
3. What should the user watch?

If it does not influence today's likely market attention, volatility, sentiment, or key watchlist names, it should usually not be included.

## Briefing Format
Default daily briefing:
- 3 to 5 items max
- each item extremely short
- total reading time under 30 seconds
- market-wide items first unless watchlist-specific items are more urgent

Example:

1. Fed tone turned hawkish overnight  
   Rate-cut expectations eased  
   Watch growth and high-beta

2. NVDA supply chain names strong in Asia  
   May support semi sentiment at open  
   Watch SOXX and AI names

3. Oil jumped on geopolitical tension  
   Energy may outperform  
   Watch XLE and airlines

## Personalization Logic
Priority order:
1. direct watchlist relevance
2. sector relevance to watchlist names
3. broader market regime or risk signals
4. major macro developments

If the user has no watchlist:
- default to the most important market-moving developments

## Source Quality Rules
Preferred source types:
- major financial news wires
- primary company disclosures
- official macro / central bank releases
- highly reliable market data sources

Avoid:
- low-credibility rumors
- opinion-driven social posts unless clearly labeled and independently confirmed
- stale summaries without fresh information

## Ranking Logic
Each news item should be scored on:
- freshness
- market impact
- user relevance
- source credibility
- uniqueness
- likely usefulness before open

## Delivery Timing
The core delivery window is pre-market.

Examples:
- US market users: before US cash open
- other markets: based on user-selected market and timezone

The system must not send too early if information will likely change materially.
The system must not send too late when the user already started trading.

## UX Principles
The Telegram message should:
- fit naturally in chat
- avoid large blocks of text
- be scannable
- show the key point immediately
- minimize taps and expansion

## Compliance / Risk Principles
The product should avoid sounding like regulated personalized investment advice.

Do not:
- tell the user to buy or sell
- state certainty where none exists
- imply guaranteed outcomes
- hide uncertainty

Preferred tone:
- informative
- concise
- watch-oriented
- neutral

## Success Metrics
Primary metrics:
- % of users who keep receiving the briefing
- low mute / unsubscribe rate
- user-rated relevance
- % of briefings judged useful by users

Secondary metrics:
- delivery reliability
- briefing latency
- duplicate rate
- stale-news rate
- average read length / engagement proxy

## Failure Conditions
The product is failing if:
- users feel the messages are repetitive
- users think the messages are too long
- users say the news is already old
- too many low-impact items are included
- personalization is weak
- the tone feels like generic summarization

## MVP Tech Notes
Suggested components:
- Telegram bot service
- scheduler
- news ingestion service
- deduplication and ranking service
- summarization module
- user preference storage
- delivery log and feedback capture

## Future Extensions
Possible later features:
- intra-day urgent alerts
- earnings-day special mode
- portfolio-linked prioritization
- user feedback loop for personalization
- sector-specific morning briefings
- market regime mode
- weekend prep summary