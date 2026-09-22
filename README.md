# EcoMeal AI - Campus Food Waste Reduction System 🍲🌱

**Amazon Code Conquest - AWS Student Community Day 2026**

## 📖 Project Overview
EcoMeal AI is an intelligent campus sustainability and resource optimization engine designed to eliminate food waste in institutional dining halls. By leveraging predictive headcount analysis and real-time surplus redistribution protocols, the system prevents food from ending up in landfills while simultaneously feeding those in need.

## 🚨 Problem Statement & Context
**The Problem:** Large-scale institutional dining halls (like university hostels) suffer from massive daily food waste due to unpredictable student attendance. 
**The Context:** When hundreds of portions of perfectly good cooked food go unconsumed, it results in severe financial loss, high carbon emissions (from landfill rot), and a missed opportunity to redirect surplus to food-insecure communities.

## 💡 Proposed Solution & Key Features
EcoMeal AI solves this through a three-tier optimization architecture:

1. **Task 1: Predictive Meal Portioning (Pre-Meal)** 
   - A student-facing portal polls students dynamically before meal prep.
   - The backend calculates exact required portions with a strict 5% safety buffer, generating actionable "Kitchen Directives" to stop overcooking before it starts.

2. **Task 2: Tier 1 - Campus Flash Claim (Mid-Meal)**
   - If surplus exists post-service, the Mess Manager triggers a "Flash Claim".
   - Campus students receive an instant 30-minute window to claim free/discounted surplus portions locally.

3. **Task 3: Tier 2 - Automated NGO Dispatch (Post-Claim)**
   - Unclaimed food after the 30-minute window is instantly logged and formatted into an `ALERT_BROADCAST`.
   - The system calculates real-time sustainability metrics (CO2 saved, kg diverted) and dispatches the alert directly to local NGO partners (e.g., Robin Hood Army) for immediate pickup within strict food safety windows.

## 🛠️ Technology Stack
* **Backend:** Python, FastAPI
* **Database:** SQLite (via SQLAlchemy ORM)
* **Frontend:** HTML, CSS, JavaScript (served via FastAPI)
* **API Validation:** Pydantic

## 🚀 Setup Instructions & Environment Requirements

### Prerequisites
* Python 3.10+ installed on your system.

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/RahulKumarPanigrahy/EcoMeal.git
   cd EcoMeal
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Rename the provided `.env.example` file to `.env` if you wish to override the default SQLite database path. For basic local usage, no environment configuration is required.
   *(Note: No passwords or API keys are committed to this repository per security guidelines).*

4. **Run the Application:**
   ```bash
   python -m uvicorn app:app --reload
   ```

5. **Access the Portals:**
   * **Manager Portal:** Open `http://127.0.0.1:8000/` in your browser.
   * **Student Portal:** Open `http://127.0.0.1:8000/student` in your browser.
   * **API Docs:** Open `http://127.0.0.1:8000/docs`.

---
*Built with ❤️ for Amazon Code Conquest 2026*
