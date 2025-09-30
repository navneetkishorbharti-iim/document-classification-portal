import streamlit as st
import pdfplumber
import requests
import tempfile

# --- Dark/Light Mode Toggle in Top-Right ---
col1, col2 = st.columns([8, 1])
with col2:
    mode = st.toggle("🌗", value=False, help="Toggle dark mode", label_visibility="visible")

if mode:
    st.markdown("""
        <style>
        html, body, .main, .block-container, .stApp {
            background-color: #181818 !important;
            color: #F0F0F0 !important;
        }
        div[data-testid="stHeader"] {
            background: #181818 !important;
        }
        .stButton>button, .stTextInput>div>div>input, .stFileUploader>div>div, .stTextArea textarea, .stSelectbox select, .stCode, .stMarkdown, .stAlert {
            background-color: #222 !important;
            color: #F0F0F0 !important;
            border-color: #555 !important;
        }
        code {
            background: #222 !important;
            color: #F0F0F0 !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #F0F0F0 !important;
        }
        .stAlert {
            background-color: #222 !important;
            color: #FFD700 !important;
        }
        .stAlert[data-testid="stSuccess"] {
            background-color: #233C2F !important;
            color: #48FF99 !important;
        }
        .stAlert[data-testid="stWarning"] {
            background-color: #322B0A !important;
            color: #FFD700 !important;
        }
        .stAlert[data-testid="stError"] {
            background-color: #3C2323 !important;
            color: #FF6F6F !important;
        }
        .stSpinner > div > div {
            color: #F0F0F0 !important;
        }
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        html, body, .main, .block-container, .stApp {
            background-color: #FAFAFA !important;
            color: #212121 !important;
        }
        div[data-testid="stHeader"] {
            background: #FAFAFA !important;
        }
        .stButton>button, .stTextInput>div>div>input, .stFileUploader>div>div, .stTextArea textarea, .stSelectbox select, .stCode, .stMarkdown, .stAlert {
            background-color: #FFF !important;
            color: #212121 !important;
            border-color: #CCC !important;
        }
        code {
            background: #EEE !important;
            color: #212121 !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #212121 !important;
        }
        .stAlert {
            background-color: #FFF8DC !important;
            color: #212121 !important;
        }
        .stAlert[data-testid="stSuccess"] {
            background-color: #E6FFED !important;
            color: #036C23 !important;
        }
        .stAlert[data-testid="stWarning"] {
            background-color: #FFF3CD !important;
            color: #856404 !important;
        }
        .stAlert[data-testid="stError"] {
            background-color: #F8D7DA !important;
            color: #721C24 !important;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("Document Classification Portal")
st.write("Upload a PDF (scanned or digital). The app predicts the document type.")

CATEGORIES = {
    "Invoice": [
        "invoice", "Invoice", "total amount", "bill to", "invoice number",
        "Invoice number", "Invoice Number", "billed to", "Bill to"
    ],
    "Bank Statement": [
        "account number", "transaction", "balance", "statement period",
        "Bank Statement", "Account Transactions", "transactions",
        "Statement of Account", "Account#"
    ],
    "Resume": ["curriculum vitae", "resume", "skills", "education", "experience","University","college","TECHNICAL SKILLS","PROJECTS"],
    "ITR": ["income tax return", "assessment year", "pan", "tax paid"],
    "Insurance Policy": ["Issued By", "Insurance Policy", "policy date","Agent","Insured", "PREMIUM" "Life Insurance", "insurance", "Insurance Company"]
}

OCR_SPACE_API_KEY = "K89824515488957"

def ocr_space_image_bytes(image_bytes, api_key=OCR_SPACE_API_KEY):
    payload = {
        'isOverlayRequired': False,
        'apikey': api_key,
        'language': 'eng',
    }
    files = {'file': ('image.jpg', image_bytes)}
    try:
        r = requests.post('https://api.ocr.space/parse/image', files=files, data=payload)
        result = r.json()
        return result['ParsedResults'][0]['ParsedText']
    except Exception as e:
        return ""  # OCR errors handled in extract_text_from_pdf

def extract_text_from_pdf(pdf_file):
    # Error handling for empty/corrupt/PW-protected/malformed/huge PDFs
    try:
        # Check for empty file (0 bytes)
        if pdf_file.size == 0:
            return None, "❌ Uploaded file is empty, please try again with a valid PDF."
        # Save to temp for pdfplumber (for some checks)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            tmp_path = tmp.name
        # Try to open with pdfplumber
        with pdfplumber.open(tmp_path) as pdf:
            # Check for no pages
            if not pdf.pages or len(pdf.pages) == 0:
                return None, "❌ PDF contains no pages. Please upload a valid PDF."
            text = ""
            for page in pdf.pages:
                try:
                    page_text = page.extract_text()
                except Exception:
                    page_text = None
                if page_text and page_text.strip():
                    text += page_text + "\n"
                else:
                    # Use OCR.Space for scanned page
                    try:
                        img = page.to_image(resolution=300).original
                        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_img:
                            img.save(temp_img.name)
                            temp_img.seek(0)
                            ocr_text = ocr_space_image_bytes(temp_img.read())
                            text += ocr_text + "\n"
                    except Exception:
                        pass  # Ignore image/OCR errors, treat as no text
        # If no text is found, maybe it's password protected, corrupted, or just blank
        if not text or text.strip() == "":
            return None, "❌ Could not extract any text from the PDF. It may be corrupted, password protected, or empty."
        return text, None
    except Exception as e:
        # MemoryError/Timeout/Corruption
        if "password" in str(e).lower():
            return None, "❌ PDF is password protected. Please upload an unlocked PDF."
        elif "EOF" in str(e) or "corrupt" in str(e).lower():
            return None, "❌ PDF is corrupted or malformed. Please try with a different file."
        elif "MemoryError" in str(type(e)):
            return None, "❌ PDF is too large or caused a memory error. Please upload a smaller file."
        return None, f"❌ Uploaded file is not a valid PDF or can't be processed. Error: {str(e)}"

def classify_document(text):
    scores = {}
    text_lower = text.lower()
    for cat, keywords in CATEGORIES.items():
        score = sum([text_lower.count(k.lower()) for k in keywords])
        scores[cat] = score
    best_cat = max(scores, key=scores.get)
    confidence = scores[best_cat] / (sum(scores.values()) + 1e-6)
    if scores[best_cat] == 0 or confidence < 0.55:
        return "Unknown", round(confidence, 2)
    return best_cat, round(confidence, 2)

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Processing your PDF..."):
        text, error_message = extract_text_from_pdf(uploaded_file)
        if error_message:
            st.error(error_message)
        elif text and text.strip():
            doc_type, confidence = classify_document(text)
            if doc_type == "Unknown":
                st.warning("The document type could not be identified. Result: **Unknown**")
            else:
                st.success(f"Predicted Type: **{doc_type}**")
            st.write(f"Confidence Score: **{confidence}**")
            st.subheader("Extracted Text (sample):")
            st.code(text[:1000])
        else:
            st.error("❌ Uploaded file is empty or not a valid PDF, please try again.")

st.markdown("---")
st.markdown("**Categories:** Invoice, Bank Statement, Resume, ITR, Insurance Policy, Unknown")
st.markdown("**Prototype built by:** Navneet Kishor Bharti, feel free to drop a message at: `navneetkishor.bharti@gmail.com`.")

