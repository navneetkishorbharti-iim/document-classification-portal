# 📄 Document Classification Portal

A working prototype that ingests a PDF (scanned or digital) and outputs the predicted document type.

---

## 🚀 How to Run

Click here to access the deployed app:
👉 [Live Demo on Streamlit](https://navneet-document-classification-app-p7t8spix4fmtvkl8u6qx5x.streamlit.app/)

---

## 📂 My Chosen Categories

* Invoice
* Bank Statement
* Resume
* ITR
* Insurance Policy
* Unknown

---

## 💡 Approach

* Focused on building a **simple, extensible prototype** for end-to-end document classification on both scanned and digital PDFs.
* Built using **Streamlit Community Cloud** for quick deployment and user-friendly interactions.
* Used **pdfplumber** for extracting text from digital PDFs and **OCR.Space API** for handling scanned PDFs.
* Implemented a **keyword-based scoring model** that maps extracted text to predefined categories with confidence scoring and an “Unknown” fallback.
* Used **Requests** for API calls and **tempfile** for secure file handling.
* Added **error handling** for empty, corrupted, or password-protected PDFs.
* Scaffolded with **GitHub Copilot** to accelerate prototyping.
* 📊 [Sample PDFs Dataset](https://drive.google.com/drive/folders/1toGlNj3yBEpt7zR7oo1MLAEUENY7PwKB?usp=sharing)

---

## 🛠️ Tech Stack

* **[Streamlit](https://streamlit.io/)** – frontend framework for building and deploying the portal
* **[pdfplumber](https://github.com/jsvine/pdfplumber)** – text extraction from digital PDFs
* **[OCR.Space API](https://ocr.space/)** – OCR for scanned PDFs
* **[Requests](https://docs.python-requests.org/)** – API requests handling
* **[tempfile](https://docs.python.org/3/library/tempfile.html)** – secure temporary file storage
* **[GitHub Copilot](https://github.com/features/copilot)** – AI-assisted code scaffolding

---

## ➕ How to Add a New Category

1. Navigate to the repo and open **`app.py`**.
2. Locate the **`CATEGORIES`** dictionary (starting around line 99).
3. Add a new key–value pair:

   ```python
   "Medical Report": ["diagnosis", "patient name", "hospital", "report date"]
   ```
4. Commit the change — the classifier will automatically include the new category in its predictions (no extra code required).
5. Refresh the Streamlit app and test with sample PDFs of the new type.

---

## 👥 For External Contributors

If you are outside the team and want to add a new category:

* **Fork** this repository into your own GitHub account.
* Make the changes in **`app.py`** as described above.
* Deploy your version of the app on **Streamlit Community Cloud**:

  * Sign up for free at [Streamlit Cloud](https://streamlit.io/cloud).
  * Connect your GitHub repo.
  * Deploy the app by pointing to the file path (e.g., `github.com/<your-username>/document-classification-portal/app.py`).
* Once deployed, your changes will be live, and further commits to your fork will automatically update your hosted app.

---
