# movie_review_booking_llm

Architecture
┌───────────────────────────┐
│        USER INPUT         │
│ "Find good movies         │
│  for this weekend"        │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      INTENT AGENT         │
│ Recommendation? Booking?  │
│ Search? Preferences?      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│    MEMORY RETRIEVAL       │
│ PostgreSQL + pgVector     │
│ Past movies & preferences │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│      PLANNER AGENT        │
│ Decide which tools        │
│ and agents to invoke      │
└───────┬─────────┬─────────┘
        │         │
        │         │
        ▼         ▼

┌────────────────┐    ┌────────────────┐
│ TMDB SEARCH    │    │ IMDB SEARCH    │
│ AGENT          │    │ AGENT          │
└───────┬────────┘    └───────┬────────┘
        │                     │
        │                     │
        ▼                     ▼

┌────────────────┐    ┌────────────────┐
│ REDDIT REVIEW  │    │ THEATRE SEARCH │
│ AGENT          │    │ AGENT          │
└───────┬────────┘    └───────┬────────┘
        │                     │
        └──────────┬──────────┘
                   │
                   ▼

┌───────────────────────────┐
│      AGGREGATOR NODE      │
│ Merge all movie results   │
│ Remove duplicates         │
└─────────────┬─────────────┘
              │
              ▼

┌───────────────────────────┐
│      RANKING AGENT        │
│ Score movies based on     │
│ reviews + preferences     │
└─────────────┬─────────────┘
              │
              ▼

┌───────────────────────────┐
│  RECOMMENDATION AGENT     │
│ Explain WHY each movie    │
│ was selected              │
└─────────────┬─────────────┘
              │
              ▼

┌───────────────────────────┐
│     VALIDATOR AGENT       │
│ Check:                    │
│ - Movie exists            │
│ - Ratings available       │
│ - Theatre info present    │
│ - No hallucinations       │
└───────┬─────────┬─────────┘
        │ PASS    │ FAIL
        │         │
        ▼         ▼

┌────────────────┐    ┌────────────────┐
│ SHOW RESULTS   │    │ RETRY NODE     │
│ TO USER        │◄───│ Retry failed   │
└───────┬────────┘    │ search only    │
        │             └────────────────┘
        ▼

┌───────────────────────────┐
│ USER CONFIRMATION         │
│ "Book Movie #2"           │
└─────────────┬─────────────┘
              │
              ▼

┌───────────────────────────┐
│ BOOKING AGENT             │
│ Select theatre & timing   │
└─────────────┬─────────────┘
              │
              ▼

┌───────────────────────────┐
│ BOOKING VALIDATOR         │
│ Seat available?           │
│ Timing valid?             │
└───────┬─────────┬─────────┘
        │ PASS    │ FAIL
        ▼         ▼

┌────────────────┐   ┌────────────────┐
│ GENERATE DUMMY │   │ RETRY BOOKING  │
│ BOOKING ID     │   │ FLOW           │
└───────┬────────┘   └────────────────┘
        │
        ▼

┌───────────────────────────┐
│ SUCCESS RESPONSE          │
│ Booking ID: MOV-12345     │
└───────────────────────────┘

Langgraph representation
START
  │
  ▼
Intent Node
  │
  ▼
Memory Node
  │
  ▼
Planner
  │
  ├──► TMDB Search
  ├──► IMDB Search
  ├──► Reddit Search
  └──► Theatre Search
          │
          ▼
      Aggregator
          │
          ▼
      Ranking
          │
          ▼
 Recommendation
          │
          ▼
      Validator
      ├─ PASS ─► User Confirmation
      └─ FAIL ─► Retry Node
                    │
                    └────► Search Nodes
                              │
                              ▼
                        Aggregator