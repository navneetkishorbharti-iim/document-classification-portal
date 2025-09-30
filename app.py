import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image

# Document categories and keywords for simple classification
CATEGORIES = {
    "Invoice": ["invoice", "Invoice", "total amount", "bill to", "invoice number","Invoice number", "Invoice Number", "billed to", "Bill to"],
    "Bank Statement": ["account number", "transaction", "balance", "statement period", "Bank Statement", "Account Transactions", "transactions", "Statement of Account","Account#"],
    "Resume": ["curriculum vitae", "resume", "skills", "education", "experience"],
    "ITR": ["income tax return", "assessment year", "pan", "tax paid"],
    "Offer Letter": ["offer letter", "position", "joining date", "salary", "welcome"],
}

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                # If page_text is None, possibly scanned PDF
                if page_text:
                    text += page_text + "\n"
                else:
                    # Try OCR on image
                    pil_image = page.to_image(resolution=300).original
                    ocr_text = pytesseract.image_to_string(pil_image)
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

# Streamlit UI
st.title("Document Classification Portal")
st.write("Upload a PDF (scanned or digital). The app predicts the document type.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.info("Processing your PDF...")
    text = extract_text_from_pdf(uploaded_file)
    if text and text.strip():
        doc_type, confidence = classify_document(text)
        st.success(f"Predicted Type: **{doc_type}**")
        st.write(f"Confidence Score: **{confidence}**")
        st.subheader("Extracted Text (sample):")
        st.code(text[:1000])  # Show first 1000 chars
    else:
        st.error("Could not extract any text from the PDF. Please check your file.")

st.markdown("---")
st.markdown("**Categories:** Invoice, Bank Statement, Resume, ITR, Offer Letter, Unknown")
st.markdown("**How to add a category?** Edit the `CATEGORIES` dictionary in `app.py`. ")
