# 🎓 Student Academic Risk Prediction System

A machine learning-based system that automatically flags at-risk students using attendance, backlog, and internal marks data — replacing manual, one-by-one review with a scalable, data-driven solution.

## 📊 Overview

This project applies a **Decision Tree classification model** to predict academic risk status for students, achieving an **88% F1 score** across 500 student records. It's designed to support proactive counseling and early intervention, and is built to scale to university populations spanning thousands of students.

## ✨ Features

- **Predictive Risk Model**: Decision Tree classifier trained on attendance, backlog count, and internal marks
- **Interactive Dashboard**: Streamlit-based web interface with three tabs — Student Search, Risk Analysis, and Visualizations
- **Roll-Number Lookup**: Enter any student's roll number to retrieve their risk status in real time
- **Data Pipeline**: Automated cleaning and preprocessing of raw academic data using Pandas

## 🛠️ Tech Stack

- **Language**: Python
- **ML/Data**: Scikit-learn, Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit
- **Styling**: CSS

## 📁 Project Structure

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation & Run (Windows)

1. Clone the repository:
```bash
   git clone https://github.com/mohdismail-ds/StudentAcademic_project.git
   cd StudentAcademic_project
```

2. Double-click `run_code.bat`, or run manually:
```bash
   pip install -r requirements.txt
   python -m streamlit run code.py
```

The dashboard will open automatically in your default browser.

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| F1 Score | 88% |
| Records Processed | 500 |
| Algorithm | Decision Tree Classifier |

## 🎯 Use Case

Educational institutions can use this tool to identify students at risk of academic failure early, enabling counselors and faculty to intervene before issues escalate — turning reactive record-keeping into proactive support.

## 📝 Author

**Mohammed Ismail**  
Data Scientist | Machine Learning & SQL Analytics  
[LinkedIn](https://linkedin.com/in/mohammed-ismail-ds) • [GitHub](https://github.com/mohdismail-ds)
