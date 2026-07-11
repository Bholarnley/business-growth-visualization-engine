import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

CURRENCY_PATTERN = re.compile(r'[₦$](\d[\d,]*)')

MULTI_MONTH_WORDS = ["months after", "months from", "6 months", "months to file"]
SHORT_DEADLINE_WORDS = ["on or before", "must be remitted", "due by", "the following month"]
RISK_WORDS = ["penalty", "penalties", "risk", "boj", "best of judgment",
              "non-compliant", "warning", "fine"]
COMPARISON_WORDS = ["not all", "are not", "is not", "versus", "vs ", "not the same as"]
BEFORE_AFTER_WORDS = ["instead of", "used to be", "now becomes", "no longer", "moving from",
                       "rather than", "in the past", "manual", "compared to"]
GROWTH_WORDS = ["grew", "growth", "increased from", "year over year", "rose from",
                "over the years", "year-on-year", "climbed to", "doubled", "tripled"]

WORDS_PER_SECOND = 2.5

SECTION_HEADER_PATTERN = re.compile(r'\[[^\]]*\]')

SENTENCE_SPLIT_PATTERN = re.compile(
    r'(?<=[.!?])\s+(?=[A-Z0-9"\u2018\u201c])'
    r'|(?<=[.!?]["\u2019\u201d])\s+(?=[A-Z0-9"\u2018\u201c])'
)


def clean_and_split(script_text):
    text = SECTION_HEADER_PATTERN.sub('', script_text)
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = SENTENCE_SPLIT_PATTERN.split(text)
    return [s.strip() for s in sentences if s.strip()]


def estimate_scenes(script_text):
    sentences = clean_and_split(script_text)
    scenes = []
    unhandled_moments = []
    elapsed_seconds = 0.0

    for sentence in sentences:
        word_count = len(sentence.split())
        sentence_duration = word_count / WORDS_PER_SECOND
        start_time = round(elapsed_seconds, 1)
        lower = sentence.lower()

        currency_match = CURRENCY_PATTERN.search(sentence)
        has_multi_month = any(w in lower for w in MULTI_MONTH_WORDS)
        has_short_deadline = any(w in lower for w in SHORT_DEADLINE_WORDS)
        has_risk = any(w in lower for w in RISK_WORDS)
        has_comparison = any(w in lower for w in COMPARISON_WORDS)
        has_before_after = any(w in lower for w in BEFORE_AFTER_WORDS)
        has_growth = any(w in lower for w in GROWTH_WORDS)

        if has_risk:
            scenes.append({
                "template": "boj_alert", "frames_folder": "frames_boj_alert",
                "start_time": start_time, "duration": 4.0,
                "reason": f"Risk/warning language detected: \"{sentence}\"",
            })
        elif has_short_deadline:
            scenes.append({
                "template": "deadline_badge", "frames_folder": "frames_deadline_badge",
                "start_time": start_time, "duration": 4.0,
                "reason": f"Short/monthly deadline detected: \"{sentence}\"",
            })
        elif has_multi_month:
            duration = max(sentence_duration, 6.0)
            scenes.append({
                "template": "cit_timeline", "frames_folder": "frames_cit_timeline",
                "start_time": start_time, "duration": round(duration, 1),
                "reason": f"Multi-month deadline detected: \"{sentence}\"",
            })
        elif has_before_after:
            scenes.append({
                "template": "before_after_card", "frames_folder": "frames_before_after",
                "start_time": start_time, "duration": 4.2,
                "reason": f"Before/after language detected: \"{sentence}\"",
            })
        elif has_growth:
            scenes.append({
                "template": "growth_bar_chart", "frames_folder": "frames_growth_bar",
                "start_time": start_time, "duration": 4.5,
                "reason": f"Growth language detected: \"{sentence}\"",
            })
        elif has_comparison:
            scenes.append({
                "template": "comparison_table", "frames_folder": "frames_comparison_table",
                "start_time": start_time, "duration": 4.5,
                "reason": f"Comparison language detected: \"{sentence}\"",
            })
        elif currency_match:
            scenes.append({
                "template": "kpi_counter", "frames_folder": "frames_kpi",
                "start_time": start_time, "duration": 3.5,
                "reason": f"Currency amount detected: \"{sentence}\"",
            })

        elapsed_seconds += sentence_duration

    return {"scenes": scenes, "unhandled_moments": unhandled_moments}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_to_scene_lite.py <script_text_file.txt>")
    else:
        script_path = sys.argv[1]
        with open(script_path, "r", encoding="utf-8") as f:
            script_text = f.read()

        result = estimate_scenes(script_text)
        print(json.dumps(result, indent=2, ensure_ascii=False))

        output_path = os.path.join(HERE, "generated_scene_lite.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nSaved to: {output_path}")