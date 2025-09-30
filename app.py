import streamlit as st
import pdfplumber
import requests
import tempfile

# Updated Document categories and keywords for simple classification
CATEGORIES = {
    "Invoice": [
        "invoice", "Invoice", "total amount", "bill to", "invoice number",
        "Invoice number", "Invoice Number", "billed to", "Bill to"],
    "Bank Statement": [
        "account number", "transaction", "balance", "statement period",
        "Bank Statement", "Account Transactions", "transactions",
        "Statement of Account", "Account#"],
   
    "ITR": ["income tax return", "assessment year", "pan", "tax paid"],
    "Job Description": ["About us", "position", "About the Role", "Qualifications", "Employer", "why join us","Responsibilities","Benefits", "compensation", "Required skills", "required skill", "nice to have","Job Title", "Employment type", "about"],
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
        st.warning(f"OCR.space error: {e}")
        return ""

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += page_text + "\n"
                else:
                    # Use OCR.Space for scanned page
                    img = page.to_image(resolution=300).original
                    with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_img:
                        img.save(temp_img.name)
                        temp_img.seek(0)
                        ocr_text = ocr_space_image_bytes(temp_img.read())
                        text += ocr_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

def classify_document(text):
    scores = {}
    text_lower = text.lower()
    for cat, keywords in CATEGORIES.items():
        score = sum([text_lower.count(k.lower()) for k in keywords])
        scores[cat] = score
    best_cat = max(scores, key=scores.get)
    confidence = scores[best_cat] / (sum(scores.values()) + 1e-6)
    if scores[best_cat] == 0:
        return "Unknown", 0.0
    return best_cat, round(confidence, 2)

st.title("Document Classification Portal")
st.write("Upload a PDF (scanned or digital). The app predicts the document type.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.info("Processing your PDF...")
    text = extract_text_from_pdf(uploaded_file)
    if text and text.strip():
        doc_type, confidence = classify_document(text)
        if doc_type == "Unknown":
            st.warning("The document type could not be identified. Result: **Unknown**")
        else:
            st.success(f"Predicted Type: **{doc_type}**")
        st.write(f"Confidence Score: **{confidence}**")
        st.subheader("Extracted Text (sample):")
        st.code(text[:1000])  # Show first 1000 chars
    else:
        st.error("Could not extract any text from the PDF. Please check your file.")

st.markdown("---")
st.markdown("**Categories:** Invoice, Bank Statement, Resume, ITR, Job Description, Unknown")
st.markdown("**How to add a category?** Edit the `CATEGORIES` dictionary in `app.py`.")
