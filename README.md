# Multiple Access Techniques Comparison Tool

This project is a full‑stack web application built with **Flask**, **Bootstrap 5**, **Chart.js**, **NumPy**, and **ReportLab**. It lets users:

* Learn about FDMA, TDMA, CDMA, OFDMA, and SDMA.
* Compare FDMA with the other four techniques.
* Input system parameters (bandwidth, users, data‑rate, SNR, network conditions, channel model) and obtain calculated performance metrics.
* Visualise results with interactive charts.
* Download a PDF report.
* See a history of past analyses stored in SQLite.

## Folder structure
```
wireless_access_analyzer/
├── app.py
├── calculations.py
├── database.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── techniques.html
│   ├── comparison.html
│   ├── analysis.html
│   ├── results.html
│   ├── history.html
│   ├── standards.html
│   └── about.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── reports/   # generated PDFs
└── database/
    └── analysis.db   # created automatically
```

## Setup & run (Windows)
```powershell
# 1. Create a virtual environment
py -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
py -m pip install -r requirements.txt

# 4. Run the app
py app.py
```

Open a browser and go to **http://127.0.0.1:5000**.

---
**Note:** The app has been tested on Windows 10/11 with Python 3.11+. All calculations are performed server‑side; no random or hard‑coded numbers are used.
