# FSHD Early Screening API

FastAPI backend for FSHD early screening with two clearly separated analysis lanes:

- `LLM lane`: image-based screening through an OpenAI-compatible vision model
- `CV lane`: MediaPipe + rule-based scoring for the three required facial actions

No plaintext secret is stored in the repository. All credentials must be provided through environment variables.

## Endpoints

- `POST /api/inference`
  - Legacy single-image endpoint kept for backward compatibility
  - Returns `status`, `probability`, `advice`, `image_url`

- `POST /api/analyze`
  - LLM screening endpoint
  - Accepts `files`
  - Returns a structured screening result with:
    - `report_id`
    - `source`
    - `risk_level`
    - `confidence`
    - `completeness`
    - `missing_required_actions`
    - `actions`
    - `key_findings`
    - `recommendations`
    - `disclaimer`
    - `analysis_valid`
    - `invalid_reason`

- `POST /api/analyze/cv`
  - CV screening endpoint
  - Accepts exactly three files:
    - `close_eye_force`
    - `pout`
    - `puff_cheek`
  - Returns a structured CV result with:
    - `risk_score`
    - `risk_level`
    - `action_scores`
    - `action_metrics`
    - `top_abnormal_features`
    - `visual_regions`
    - `short_advice`

## Quick Start

```bash
git clone https://github.com/sealofyou/fshd-early-screening.git
cd fshd-early-screening
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

Use `.env.example` as the template.

Required for real LLM inference:

- `OPENAI_API_KEY` or `SILICONFLOW_API_KEY`

Recommended:

- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `OPENAI_TWO_PASS`

For local mock LLM testing:

- `SCREENING_ALLOW_MOCK=true`

## Verification

Run API contract tests:

```bash
python -m unittest tests.test_api_contracts
```

Open docs:

```text
http://127.0.0.1:8000/docs
```

## Notes

- The CV lane depends on `numpy`, `opencv-python`, and `mediapipe`.
- CV scoring config lives in `app/cv_risk_config.json`.
- This repo intentionally keeps LLM and CV interfaces separate so frontend or orchestration layers can choose one lane explicitly.
