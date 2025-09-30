import streamlit as st
import pdfplumber
import requests
import tempfile

# Updated Document categories and keywords for simple classification
CATEGORIES = {
    "Invoice": [ "invoice", "Invoice", "total amount", "bill to", "invoice number", "Invoice number", "Invoice Number", "billed to", "Bill to", "Invoice", "Invoice Number", "Invoice No.", "Bill", "Billing Date", "Invoice Date", "Due Date", "Payment Due", "Bill To", "Sold To", "Ship To", "From", "To", "Vendor", "Supplier", "Customer", "Client", "Description", "Item", "Quantity", "Qty", "Rate", "Price", "Unit Price", "Amount", "Total Amount", "Subtotal", "VAT", "GST", "CGST", "SGST", "IGST", "Tax Rate", "Taxable Value", "Discount", "Grand Total", "Total Due", "Payment Terms", "Net 30", "Payable", "Account Number", "PO Number", "Purchase Order", "Invoice Total", "Balance Due", "Paid", "Amount Paid", "Outstanding", "Currency", "USD", "INR", "EUR", "Remit To", "Bank Details", "SWIFT", "IBAN", "Terms and Conditions", "Thank You", "Receipt", "Tax Invoice", "Proforma Invoice", "Final Invoice"],
    "Bank Statement": ["account number", "transaction", "balance", "statement period", "Bank Statement", "Account Transactions", "transactions", "Statement of Account", "Account#", "Bank Statement", "Account Statement", "Statement Period", "Opening Balance", "Closing Balance", "Available Balance", "Account Number", "Account Holder", "Transaction Date", "Value Date", "Description", "Particulars", "Narration", "Deposit", "Credit", "Withdrawal", "Debit", "Cheque Number", "CHQ", "ATM", "NEFT", "RTGS", "IMPS", "UPI", "Transfer", "Interest", "Charges", "Fees", "Balance", "Running Balance", "Bank Name", "Branch", "IFSC", "MICR", "Customer ID", "Statement Date", "Page of", "Total Debits", "Total Credits", "Net Balance", "Electronic Statement", "e-Statement", "Account Summary", "Transaction History", "Salary Credit", "EMI Debit", "Minimum Balance", "SMS Alert", "Online Banking"],
    "Resume": ["curriculum vitae", "cv","professional summary", "profile", "resume", "skills", "education", "experience", "Resume", "CV", "Curriculum Vitae", "Professional Summary", "Career Objective", "Work Experience", "Employment History", "Job Title", "Company Name", "Duration", "Responsibilities", "Achievements", "Education", "Degree", "University", "School", "Graduation Date", "Skills", "Technical Skills", "Soft Skills", "Certifications", "Projects", "Internships", "Languages", "Contact Information", "Email", "Phone Number", "LinkedIn", "Portfolio", "Address", "References", "Objective", "Summary", "Core Competencies", "Professional Experience", "Academic Background", "Tools", "Technologies", "Awards", "Publications", "Volunteer Work", "Hobbies", "Nationality", "Date of Birth", "Gender", "Marital Status"],
    "ITR": ["Income Tax Return", "income tax return", "assessment year", "pan", "tax paid", "ITR", "ITR-1", "ITR-2", "ITR-3", "ITR-4", "Assessment Year", "Financial Year", "PAN", "Permanent Account Number", "Aadhaar", "Taxpayer", "Gross Total Income", "Total Income", "Taxable Income", "Deductions", "Section 80C", "Section 80D", "TDS", "Tax Deducted at Source", "Refund", "Tax Payable", "Advance Tax", "Self Assessment Tax", "Form 26AS", "Schedule", "Filing Status", "Verified", "E-Verified", "Acknowledgement Number", "CPC", "Centralized Processing Centre", "Residential Status", "Salary Income", "House Property", "Capital Gains", "Business Income", "Other Sources", "Bank Account Details", "IFSC", "Challan", "ITR-V", "Digital Signature", "Tax Return", "Income Details", "Exempt Income", "Agricultural Income", "Tax Relief", "Foreign Assets", "Balance Sheet", "Profit and Loss"],
    "Insurance Policy": ["Insurance Policy", "Policy Document", "Certificate of Insurance", "Policy Schedule", "Policy Number", "Policy No.", "Policy ID", "Certificate Number", "Policyholder", "Insured", "Insured Name", "Proposer", "Beneficiary", "Nominee", "Insurer", "Insurance Company", "Coverage Amount", "Sum Assured", "Death Benefit", "Premium Amount", "Annual Premium", "Monthly Premium", "Total Premium", "Policy Effective Date", "Start Date", "Expiry Date", "Policy Term", "Coverage Period", "Coverage Details", "Benefits", "What is Covered", "Exclusions", "Inclusions", "Claims Procedure", "How to File a Claim", "General Terms", "Definitions", "Free Look Period", "Grace Period", "Surrender Value", "Riders", "Add-on Covers", "Authorized Signatory", "Issued By", "Policy Issuance Date", "Master Policy", "Third-party Liability", "IDV", "No Claim Bonus", "Network Hospitals", "Pre-existing Disease", "Maturity Benefit", "Waiting Period", "Structure Coverage"],
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
