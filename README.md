[Resume Bot}()

A Streamlit app that “roasts” or reviews your resume using Google Gemini AI, providing line-by-line feedback, actionable improvement tips, overall takeaways, and an ATS compatibility score.


TLDR : It's just a wrapper, wanted to see how fast can I make this. (~15 mins)

Features
	•	Roast Mode: Brutal, witty feedback on each bullet or sentence, followed by concise improvement tips.
	•	Review Mode: Structured, section-by-section analysis (Summary, Strengths, Weaknesses, Improvements).
	•	Overall Takeaway: Digestible 2–3 bullet summary of top recommendations.
	•	ATS Compatibility Score: Numeric score (0–100) with rationale to help you optimize for applicant tracking systems.
	•	Clean, Minimal UI: Jost font, responsive layout, accent color highlights, sticky sidebar, form-based entry, and consistent controls.

```python
# Running Locally

streamlit run resume-roaster.py

# Open your browser at http://localhost:8501.
```