# Document-classification-portal
How to run?
> To run this prototype you need to click this link: https://navneet-document-classification-app-p7t8spix4fmtvkl8u6qx5x.streamlit.app/
My chosen categories
> Invoice, Bank Statement, Resume, ITR, Insurance Policy, Unknown
Approach
> My approach was focused on shipping a simple, extensible prototype that demonstrates end-to-end document classification for both scanned and digital PDFs. I used Streamlit Community Cloud to deploy an interactive web-based portal, achieving quick deployment and user-friendly interactions. 
> For text extraction, we combined pdfplumber (for digital PDFs) with OCR.Space API (for scanned PDFs), enabling robust handling of diverse input formats. 
> Classification logic was implemented using a keyword-based scoring model, mapping extracted text against predefined categories (Invoice, Bank Statement, Resume, ITR, Insurance Policy) with confidence scoring and an “Unknown” fallback. Requests were used for API calls and tempfile for handling uploads securely. 
> Error handling was built in for empty, corrupted, or password-protected PDFs.
> The codebase was scaffolded using GitHub Copilot to accelerate prototyping.
> My sample set: https://drive.google.com/drive/folders/1toGlNj3yBEpt7zR7oo1MLAEUENY7PwKB?usp=sharing

How to add a new category
> To add a new category, navigate to my GitHub repo, access app.py file and simply extend the CATEGORIES dictionary in the code(starting from line 99) by creating a new key-value pair. 
> The key is the name of the category (e.g., "Medical Report") and the value is a list of representative keywords/phrases that are unique to that document type (e.g., ["diagnosis", "patient name", "hospital", "report date"]). 
> Once added, commit the change and the classifier will automatically score this new category against extracted text and include it in the prediction pipeline, no further code changes are required. 
> Now simply refresh the Streamlit app, try uploading the new PDFs and changes should be visible on the internet hosted app.
(Assumption: this repo is being used within a team hence anyone within a team can access, or else fork the project, do the changes in the code as mentioned above, re-deploy the app on Streamlit using your account(this is a one time step)->sign up free->Streamlit Community Cloud -> GitHub deploy -> use your git repo URL for eg: github.com/<the new user or persons account name>/document-classification-portal/app.py-> the app is deployed. Any code changes will reflect here.)
