# Cosmos 3 & Imagen 4.0 AI Image Studio (Streamlit version)

This is a premium Streamlit web application ported from the React version. It allows users to:
1. Generate high-quality physics-realistic images using **NVIDIA Cosmos 3** (via Hugging Face API) and **Google Imagen 4.0** (via Gemini API).
2. Optimize simple prompts into highly-detailed, structured physical prompts using **Gemini 2.5 Flash**.
3. View the system architecture and learn about Mixture-of-Transformers (MoT) and mRoPE.
4. Access dynamic code integrations (Python & cURL) that auto-update with current GUI settings.

---

## 🛠️ Local Installation & Run

1. **Clone or Open this folder**:
   Ensure you are in the directory containing `app.py` and `requirements.txt`.

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**:
   ```bash
   streamlit run app.py
   ```

5. **Provide API Tokens**:
   - Open your browser to `http://localhost:8501`.
   - Enter your **Hugging Face Token** and **Gemini API Key** in the sidebar (or set them as environment variables / Streamlit Secrets, see below).

---

## ☁️ Deploying to Streamlit.io (Streamlit Community Cloud)

Streamlit Community Cloud allows you to deploy Python apps directly from a GitHub repository for free.

### Step 1: Push Code to GitHub

1. Initialize a git repository in this directory:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Cosmos 3 Streamlit App"
   ```
2. Create a new repository on [GitHub](https://github.com).
3. Link your local repo and push:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Streamlit Community Cloud

1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app**.
3. Select your repository, branch (`main`), and main file path (`app.py`).
4. (Optional but recommended) Click **Advanced settings...** and add your API secrets so users don't have to input them manually:
   ```toml
   HF_TOKEN = "your_huggingface_access_token_here"
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. Click **Deploy!** Your app will be live in a couple of minutes.
