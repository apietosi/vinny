# 🚗 Vinny | The Friendly VIN Checker

**Vinny** is a lightweight, privacy-focused web application that helps car buyers instantly decode VINs, check for safety recalls, and generate professional PDF reports—all for free.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)

---

## ✨ Features

- **Instant Decoding:** Powered by the NHTSA vPIC API for official manufacturer data.
- **Safety First:** Automatically checks for active safety recalls.
- **PDF Reports:** Generate a clean, one-page spec sheet for any vehicle.
- **Smart History:** Remembers your last 5 searches using local browser storage (no database needed!).
- **Deep Links:** One-click access to full vehicle history reports.

## 🛠️ Tech Stack

- **Backend:** Python / Flask
- **Frontend:** Bootstrap 5 / JavaScript (ES6)
- **PDF Engine:** FPDF2
- **Data Source:** NHTSA (National Highway Traffic Safety Administration) API

---

## 🚀 Quick Start (Local Setup)

If you want to run Vinny on your own machine:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/vinny.git](https://github.com/YOUR_USERNAME/vinny.git)
   cd vinny
