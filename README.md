# NutriChat AI - AI Nutrition Coach on WhatsApp

NutriChat AI is an end-to-end HealthTech platform designed to serve as a personal AI Nutritionist inside WhatsApp. By simply snapping a photo of food, recording a voice description, scanning a grocery barcode, or texting, users receive instant, highly personalized nutritional analysis and long-term coaching recommendations.

---

## 🚀 Key Features

*   **Multimodal Log Intake**: Accepts food photos, voice notes, text messages, restaurant menus, barcode scans, and nutrition labels.
*   **Indian Food Optimization**: Vision AI tuned for mixed Indian plate dishes (e.g. dal, paneer, papad, roti, rice) and street foods.
*   **Portion Size Estimation**: Converts bounding shapes and food types into approximate weights (grams) and counts.
*   **Detailed Nutrition Breakdown**: Fetches verified calorie, macro, and micro metrics via Edamam and Open Food Facts APIs.
*   **Interactive AI Coaching**: Retains conversational memory for answering user queries based on profile targets.
*   **Admin Dashboard Web Portal**: Real-time analytical dashboard built with React + Next.js for tracking user activity, API usage, and system health.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend (Dashboard)** | React, Next.js, Tailwind CSS |
| **Backend API** | Python FastAPI, Uvicorn |
| **Database** | PostgreSQL |
| **Cache & Queue** | Redis |
| **AI Processing** | Gemini 2.5 / GPT-4 Vision / Claude |
| **Third-Party Integrations** | WhatsApp Cloud API, Edamam Nutrition API, Open Food Facts |
| **Containerization** | Docker, Docker Compose |

---

## 🏛️ System Architecture

Below is a block level representation of the NutriChat AI data flows:

```
                  +--------------------------------+
                  |         User (WhatsApp)        |
                  +--------------------------------+
                                  |
                                  v
                  +--------------------------------+
                  |     Meta WhatsApp Cloud API    |
                  +--------------------------------+
                                  |
                                  v
                  +--------------------------------+
                  |         FastAPI Backend        |
                  +---------------+----------------+
                                  |
            +---------------------+---------------------+
            |                     |                     |
            v                     v                     v
    +---------------+     +---------------+     +---------------+
    |  PostgreSQL   |     |     Redis     |     |   Cloudinary  |
    | (Users, Meals)|     | (Cache, Rate) |     |  (Image Store)|
    +---------------+     +---------------+     +---------------+
            |                     |                     |
            +---------------------+---------------------+
                                  |
                                  v
                  +--------------------------------+
                  |       AI Pipeline Logic        |
                  | (Vision AI, OCR, Gemini/GPT)   |
                  +---------------+----------------+
                                  |
                                  v
                  +--------------------------------+
                  |       External Services        |
                  |    (Edamam API, Open Food)     |
                  +--------------------------------+
```

---

## 📁 Repository Directory Structure

```
NutriChat-AI/
├── backend/            # FastAPI source application code
│   ├── ai/             # Core LLM prompt templates and pipeline integrations
│   ├── database/       # SQLAlchemy configurations and migrations
│   ├── models/         # Database models and Pydantic schemas
│   ├── routes/         # API routers (auth, logs, webhooks)
│   ├── services/       # Edamam, Open Food Facts, WhatsApp wrappers
│   └── utils/          # Security, auth, caching helper files
├── frontend/           # Next.js web application for the admin dashboard
├── docker/             # Docker configuration files
├── docs/               # Unified markdown guides
├── tests/              # Pytest backend and Cypress frontend test suites
├── AGENTS.md           # Governance details of the autonomous team
├── SKILLS.md           # Unified capabilities checklist
├── RULES.md            # Mandatory project constraints rules
├── WORKFLOWS.md        # Automation workflows
├── TASK.md             # Master project checklist
└── PROGRESS.md         # Current sprint milestone checklist
```

---

## ⚙️ Installation & Local Setup

### Pre-requisites
*   Docker & Docker Compose
*   Python 3.11+
*   Node.js 18+

### Setup steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-repo/NutriChat-AI.git
    cd NutriChat-AI
    ```

2.  **Environment Configuration**
    Copy default env files and set your credentials:
    ```bash
    cp backend/.env.example backend/.env
    cp frontend/.env.example frontend/.env
    ```

3.  **Run with Docker Compose**
    Launch the database, Redis cache, FastAPI app, and NextJS dashboard simultaneously:
    ```bash
    docker-compose up --build
    ```
    *   FastAPI backend runs at: `http://localhost:8000`
    *   Dashboard web page runs at: `http://localhost:3000`

---

## 🤝 Contributing
Contributions are welcome! Please review the [CONTRIBUTING.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/CONTRIBUTING.md) guide and adhere to the [CODE_OF_CONDUCT.md](file:///c:/Users/tejas/Documents/Projects/NutriChat-AI/CODE_OF_CONDUCT.md) standards.

---

## 📄 License
This project is licensed under the MIT License.
