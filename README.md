# 🚀 Resume & JD Enhancer - Local ML Pipeline

A **local machine learning-based resume enhancement and matching system** that analyzes your resume against a job description, identifies skill gaps, and provides actionable enhancement suggestions.

## Features

✅ **Text Extraction** - Supports PDF and TXT formats  
✅ **Preprocessing Pipeline** - Normalization, tokenization, stop word removal  
✅ **Named Entity Recognition (NER)** - Extracts skills, experience, education, projects, achievements  
✅ **Resume-JD Matching** - Calculates similarity scores (Skills, Experience, Education)  
✅ **Skill Gap Analysis** - Shows missing skills from JD not in your resume  
✅ **Token Frequency Analysis** - Visualizes keyword distribution  
✅ **ATS Optimization Suggestions** - Recommendations for improving your resume  
✅ **No External API Calls** - Everything runs locally using spaCy and scikit-learn  

## Installation

### Requirements

- Python 3.8+
- pip / conda

### Step 1: Install Dependencies

```bash
cd /home/ishita/Desktop/Major_sor
pip install -r requirements.txt
```

### Step 2: Download spaCy Models

The app uses spaCy's transformer model for accurate NER and parsing:

```bash
python3 -m spacy download en_core_web_trf
```

Alternatively, if you prefer a faster (but slightly less accurate) model:

```bash
python3 -m spacy download en_core_web_sm
```

### Step 3: Verify Installation

```bash
python3 -c "import streamlit_app; print('✅ App is ready!')"
```

If you see warnings about Streamlit session state, that's normal—they only appear when running outside `streamlit run`.

## Usage

### Run the Streamlit App

```bash
streamlit run /home/ishita/Desktop/Major_sor/streamlit_app.py
```

This will open a local web server (typically at `http://localhost:8501`).

### Using the App

1. **Input Your Resume**
   - Upload a PDF/TXT file or paste text directly

2. **Input Job Description** (Optional)
   - Upload a JD file or paste text
   - If omitted, the app will still analyze your resume

3. **Click "Run Enhancement"**
   - The app will run the full preprocessing and analysis pipeline

4. **Review Results**
   - **Token Frequency**: See which keywords dominate your resume and JD
   - **Named Entities**: View extracted skills, projects, education, etc.
   - **Match Scores**: See how well your resume aligns with the JD (Skills %, Experience %, Education %)
   - **Skill Gaps**: Know exactly which skills from the JD are missing in your resume
   - **Enhancement Suggestions**: Get actionable recommendations

5. **Download Enhanced Resume**
   - Download an enhanced version with suggested improvements as a `.txt` file

## Project Structure

```
Major_sor/
├── streamlit_app.py              # Main Streamlit application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── CV/
│   ├── main.py                   # CV preprocessing pipeline (legacy)
│   ├── tokenization.py
│   ├── normalization.py
│   ├── stop_word_removal.py
│   ├── NER.py
│   └── ... (other preprocessing files)
│
└── 2.o/                          # MAIN BACKEND PIPELINE
    ├── preprocessing.py          # Full pipeline orchestrator
    ├── normalization.py          # Text normalization
    ├── tokenization.py           # spaCy-based tokenization
    ├── stop_word_removal.py      # NLTK-based stopword filtering
    ├── NER.py                    # Named Entity Recognition + keyword extraction
    ├── parsing.py                # spaCy dependency parsing
    ├── text_extractor.py         # PDF/TXT extraction
    │
    ├── Similarity/
    │   └── Resume_JD_Matching.py # Cosine similarity matching
    │
    ├── Rewriter/
    │   └── rewriter.py           # Resume enhancement (HF API based)
    │
    ├── NER_output_CV/            # Sample NER outputs
    ├── NER_output_JD/
    ├── preprocessing_output_CV/  # Sample preprocessed texts
    └── preprocessing_output_JD/
```

## How It Works

### Pipeline Flow

```
Resume/JD Input
    ↓
Text Extraction (PDF/TXT)
    ↓
Normalization (lowercase, remove special chars)
    ↓
Tokenization (spaCy)
    ↓
Stop Word Removal (NLTK)
    ↓
Named Entity Recognition (spaCy + keyword matching)
    ↓
Resume-JD Similarity Matching (cosine similarity on skills, experience, education)
    ↓
Skill Gap Analysis & Enhancement Suggestions
    ↓
Download Enhanced Resume
```

### Key Technologies

- **spaCy** (`en_core_web_trf`): NER, tokenization, dependency parsing
- **NLTK**: Stopword lists, corpora
- **scikit-learn**: TF-IDF vectorization, cosine similarity
- **PyMuPDF (fitz)**: PDF text extraction
- **Streamlit**: Web UI

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'frontend'`

**Solution**: Install/reinstall PyMuPDF:
```bash
pip install --upgrade pymupdf
```

### Issue: `OSError: [E050] Can't find model 'en_core_web_trf'`

**Solution**: Download the spaCy model:
```bash
python3 -m spacy download en_core_web_trf
```

### Issue: App is slow to start

**Reason**: spaCy's transformer model (`en_core_web_trf`) is large (~600MB) and takes time to load on first run.

**Solution**: Use the smaller model instead (less accurate but faster):
```bash
python3 -m spacy download en_core_web_sm
```

Then update `2.o/tokenization.py` and `2.o/NER.py` to use `en_core_web_sm` instead of `en_core_web_trf`.

### Issue: "Session state does not function when running a script without `streamlit run`"

**Reason**: This is a normal Streamlit warning. It only appears when importing the module directly (not via `streamlit run`).

**Solution**: Always run with `streamlit run streamlit_app.py`, not `python3 streamlit_app.py`.

## Performance Tips

1. **Smaller Model**: Use `en_core_web_sm` for 2-3x faster processing
2. **Resume Length**: Works best with resumes < 1000 words
3. **First Run**: Downloading spaCy models (~600MB) takes time; subsequent runs are much faster

## Example Output

### Match Scores
```
Skills Match: 72.5%
Experience Match: 65.3%
Education Match: 80.0%
Overall Match: 72.3% → Good
```

### Skill Gaps
```
Skills in JD but missing from Resume:
• AWS Lambda
• Docker
• Kubernetes
• GraphQL
• Microservices Architecture
```

### Enhancement Suggestions
```
1. 🎯 Add these skills to your resume: AWS Lambda, Docker, Kubernetes, GraphQL, Microservices
2. 📝 You have 34 keywords matching the JD. Good alignment!
3. ✂️ Consider making your resume more concise (currently 650 words).
```

## Next Steps

- **Integrate with LLM Rewriter**: To auto-generate enhanced sentences, use `2.o/Rewriter/rewriter.py` with a HuggingFace API token
- **Create PDF Output**: Generate beautifully formatted PDF resumes from the enhanced text
- **Batch Processing**: Process multiple resumes against different JDs at scale

## Support & Contributing

For issues or feature requests, feel free to extend the app. Key files to modify:

- `streamlit_app.py` - Add new visualizations or features
- `2.o/NER.py` - Improve entity extraction logic
- `2.o/Similarity/Resume_JD_Matching.py` - Refine matching algorithm

---

**Happy Resume Optimizing! 🎉**
