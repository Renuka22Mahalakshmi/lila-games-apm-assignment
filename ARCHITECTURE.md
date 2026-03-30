# Architecture Documentation: LILA BLACK Player Journey Tool

## Tech Stack & Rationale
- **Language:** Python 3.12
- **Framework:** Streamlit — Selected for its ability to transform data scripts into interactive shareable web apps instantly without complex frontend boilerplate.
- **Visualization:** Plotly Graphing Library — Chosen for its robust support for `layout_images`, allowing for precise pixel-perfect overlays of telemetry data on game minimaps.
- **Data Processing:** Pandas & PyArrow — Essential for handling high-frequency Parquet telemetry files efficiently.

## Data Flow
1. **Ingestion:** The app scans the `player_data` directory, dynamically identifying available match dates and unique Match IDs.
2. **Transformation:** Raw coordinates (X, Z) are extracted from Parquet files. Player types are categorized by checking if the `user_id` is a UUID (Human) or numeric (Bot).
3. **Coordinate Mapping (The "Tricky Part"):** - **Step 1: Normalization.** We convert world coordinates to a 0-1 scale (UV) using the formula: $u = (x - origin\_x) / scale$ and $v = (z - origin\_z) / scale$.
   - **Step 2: Pixel Translation.** We map these to the 1024x1024 map resolution. Since computer graphics coordinates start (0,0) at the top-left, we invert the V axis: $pixel\_y = (1 - v) \times 1024$.
4. **Rendering:** Plotly layers a scatter plot (for journeys) or a density heatmap (for combat zones) over the static minimap image.

## Assumptions & Ambiguities
- **Z-Axis/Elevation:** For the 2D prototype, the `y` (vertical) coordinate was ignored to focus on horizontal map flow.
- **Bot Identification:** Assumed any `user_id` that is purely numeric and shorter than a standard UUID represents an AI agent.
- **Coordinate Scale:** Used the provided Map Configuration constants to ensure the "Ambrose Valley," "Grand Rift," and "Lockdown" maps align with the telemetry.

## Trade-offs
| Feature | Decision | Reason |
| :--- | :--- | :--- |
| **Data Source** | Local Parquet Samples | Using a live database was overkill for a 24hr test; local Parquet ensures 100% uptime for the reviewer. |
| **Viz Type** | 2D Scatter/Heatmap | 3D paths are harder for Level Designers to parse quickly on a web UI. |
| **Sampling** | Representative Subset | Uploaded 2 days of data to GitHub to ensure the Streamlit Cloud RAM doesn't crash during the review. |
