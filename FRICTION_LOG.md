# BlindSpot — Friction Log

## Issue 1: Dashboard rendering problem

**Task attempted:** Launch BlindSpot and inspect the dashboard.

**Steps taken:**
1. Started the FastAPI application locally.
2. Opened the dashboard in a browser.
3. Noticed literal `\n` characters appearing in the top-left corner.
4. Investigated the frontend HTML and corrected the affected content.
5. Reloaded the dashboard to check the result.

**Expected result:** The dashboard should display normally without unwanted characters.

**Actual result:** Literal `\n` characters appeared on the page, making the interface look broken and less polished.

**Severity:** Moderate. The issue affected the visual presentation but did not necessarily stop the application from running.

**Workaround used:** Corrected the affected frontend content and reloaded the page.

**Actionable suggestion:** Provide a frontend troubleshooting checklist covering malformed HTML, escaped characters, browser rendering, and visual testing before demonstrations.

**Impact:** Additional debugging and browser testing were needed before the dashboard was ready to demonstrate.
