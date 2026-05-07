# CareerCraft: AI-Powered Resume Analyzer

CareerCraft is a Streamlit web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). By leveraging the power of Google's Gemini AI, this tool provides an in-depth analysis of your resume against any job description, offering actionable insights to improve your chances of landing an interview.

## 🌐 Live Demo

<a href="https://careercraft-git7bqwmgypzwie2chk3fk.streamlit.app" target="_blank" style="text-decoration:none;">
  CareerCraft
</a>

## 🚀 Features

- **ATS Resume Analysis**: Compares your resume to a job description to identify alignment.
- **Skill Gap Detection**: Pinpoints skills mentioned in the job description that are missing from your resume.
- **Keyword Optimization**: Highlights relevant keywords to include in your resume.
- **Resume Matching Score**: Provides a percentage score indicating how well your resume matches the job requirements.
- **AI-Generated Suggestions**: Offers concrete advice on how to improve your resume's content and structure.
- **Personalized Profile Summary**: Can be used to generate a compelling summary based on your experience and the target role.

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Google Gemini (`gemini-2.5-flash-lite`)
- **PDF Processing**: PyPDF2
- **Environment Management**: python-dotenv

## ⚙️ Setup and Installation

Follow these steps to run the application locally.

### 1. Prerequisites

- Python 3.9+
- A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository

```bash
git clone https://github.com/sidhu17/AI-Powered-Resume-Analyzer.git
cd AI-Powered-Resume-Analyzer
```

### 3. Install Dependencies

Install the required Python packages using `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory of the project and add your Gemini API key:

```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 5. Run the Application

Start the Streamlit server with the following command:

```bash
streamlit run app.py
```

The application will open in your default web browser.

## ☁️ Running with GitHub Codespaces

For a seamless one-click setup, you can use GitHub Codespaces.

1.  Click the **Code** button on the repository page.
2.  Select the **Codespaces** tab.
3.  Click **Create codespace on main**.

The development environment will be automatically configured, all dependencies will be installed, and the application will start. The application preview will open automatically in a new tab in your browser.

## 📄 How It Works

1.  **Paste Job Description**: Copy the full text of the job description you are applying for and paste it into the designated text area.
2.  **Upload Resume**: Upload your resume in PDF format. The application will extract the text for analysis.
3.  **Analyze**: Click the "🔍 Analyze Resume" button.
4.  **Get Results**: The application sends the job description and your resume text to the Gemini model. The AI provides a detailed analysis, including:
    - ATS Match Percentage
    - Missing Skills
    - Key Strengths
    - Improvement Suggestions

## 📜 License

Open Source — Free to use, modify, and distribute with proper credit.

## 👨‍💻 Author

Developed by **Siddharath Negi**

- GitHub: https://github.com/sidhu17
- LinkedIn: https://www.linkedin.com/in/siddharath-negi