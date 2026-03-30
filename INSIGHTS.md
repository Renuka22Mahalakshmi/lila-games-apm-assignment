# Level Design Insights: LILA BLACK

### 1. The "First Contact" Chokepoints
- **Observation:** In Ambrose Valley, a significant cluster of combat events (Heatmap "Hot Zones") appears near the central bridge within the first 15% of match time.
- **The Data:** Human player paths converge here immediately after the initial drop, while bot paths remain scattered.
- **Actionable:** Move high-tier loot crates away from this bridge to decentralized locations. 
- **Metric Affected:** Average Match Duration (prevents early-game churn) and Player Retention.
- **Why it matters:** Designers want players to gear up before fighting; instant deaths lead to player frustration.

### 2. Bot Pathing Predictability
- **Observation:** Bot "Position" events follow perfectly straight lines between waypoints, unlike the erratic "looting" patterns of humans.
- **The Data:** Visualization shows "laser-straight" journeys for IDs tagged as Bots.
- **Actionable:** Implement a "Perlin Noise" offset to bot movement to simulate human-like strafing and looting behavior.
- **Metric Affected:** Bot Kill Difficulty and Player Immersion.
- **Why it matters:** If bots are too easy to distinguish, the competitive tension of the extraction shooter is lost.

### 3. Underutilized Map Quadrants ("Dead Zones")
- **Observation:** The North-East quadrant of the "Grand Rift" map shows almost zero player activity across multiple sample matches.
- **The Data:** The Heatmap shows a "Loot Desert" where no interaction events are logged.
- **Actionable:** Introduce a temporary "High-Value Extraction Point" or a "Boss Spawn" in these empty zones.
- **Metric Affected:** Map Utilization % and Encounter Frequency.
- **Why it matters:** Large empty spaces waste server resources and make the game world feel "unfinished."
