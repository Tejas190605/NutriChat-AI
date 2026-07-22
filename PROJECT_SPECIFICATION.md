NutriChat AI – Complete Mini Project Specification (Expanded Version)
________________________________________
1. Project Overview
Project Name
NutriChat AI – AI Nutrition Coach on WhatsApp
Domain
HealthTech • AI • Computer Vision • NLP • Nutrition • Conversational AI
Platform
•	WhatsApp AI Chatbot
•	Optional Admin Dashboard (Web)
Project Type
End-to-End AI Product
________________________________________
2. Vision
NutriChat AI aims to become an AI Nutritionist that lives inside WhatsApp.
Instead of opening calorie tracking apps and manually logging meals, users simply:
•	Take a photo
•	Send it on WhatsApp
•	Receive instant nutritional analysis
•	Get personalized AI coaching
•	Track long-term health automatically
The vision is to make healthy eating as simple as chatting with a friend.
________________________________________
3. Problem Statement
Current nutrition apps suffer from:
•	Manual food logging
•	Time-consuming interfaces
•	Poor Indian food recognition
•	Generic recommendations
•	Low user retention
•	Separate mobile app installation
•	Poor conversational experience
Research on AI dietary assessment and nutrition chatbots consistently identifies manual logging as one of the biggest reasons users abandon nutrition apps, motivating vision-based and conversational approaches. (arXiv)
________________________________________
4. Proposed Solution
NutriChat AI transforms WhatsApp into an intelligent nutrition assistant.
The system accepts:
•	📷 Food Photos
•	🎤 Voice Messages
•	💬 Text Messages
•	📦 Barcode Images
•	🥗 Restaurant Menus
•	🛒 Grocery Photos
•	🧾 Nutrition Labels
and responds with personalized nutritional insights.
________________________________________
5. Core Objectives
Primary Objectives
•	Simplify calorie tracking
•	Promote healthier eating
•	Reduce manual effort
•	Personalize nutrition advice
•	Improve user consistency
•	Increase health awareness
Secondary Objectives
•	Learn user eating habits
•	Recommend healthier alternatives
•	Track long-term progress
•	Encourage healthy lifestyle habits
________________________________________
6. Target Users
Primary
•	Weight loss users
•	Muscle gain users
•	Fitness enthusiasts
•	College students
•	Busy professionals
Secondary
•	Dieticians
•	Personal trainers
•	Families
•	Diabetic patients
•	Nutrition coaches
________________________________________
7. Core Technologies
Layer	Technology
Frontend Dashboard	React + Next.js
Styling	Tailwind CSS
Backend	FastAPI
Database	PostgreSQL
Cache	Redis
Authentication	JWT
AI Models	Gemini 2.5 / GPT-4.1 Vision / Claude
OCR	Vision LLM
Nutrition APIs	Edamam, Open Food Facts
Messaging	WhatsApp Cloud API
Image Storage	Cloudinary
Deployment	Docker + AWS/Render
Nutrition APIs like Edamam support natural-language food parsing, nutrition analysis, chatbot workflows, and meal planning, while Open Food Facts provides open product, ingredient, and barcode data. (Edamam)
________________________________________
8. Functional Modules
Module 1 – User Management
Stores
•	Profile
•	Goal
•	Weight
•	Height
•	Preferences
•	Allergies
•	Activity Level
________________________________________
Module 2 – Food Recognition
Accepts
•	Images
•	Voice
•	Text
Recognizes
•	Indian Food
•	Street Food
•	Restaurant Food
•	Homemade Food
•	Mixed Plates
•	Multiple Dishes
Example
Instead of
Indian Meal
Returns
•	Dal
•	Rice
•	Paneer
•	Roti
•	Salad
•	Pickle
•	Papad
________________________________________
Module 3 – Portion Estimation
AI estimates
•	Serving Size
•	Number of Pieces
•	Approximate Weight
Example
Pizza
↓
2 slices
↓
240g
↓
580 kcal
Vision-based dietary assessment systems generally separate food recognition from portion/volume estimation before nutrition calculation. (arXiv)
________________________________________
Module 4 – Nutrition Engine
Calculates
•	Calories
•	Protein
•	Carbohydrates
•	Fat
•	Fiber
•	Sugar
•	Sodium
•	Cholesterol
•	Saturated Fat
________________________________________
Module 5 – AI Explanation Engine
Instead of
"High Calories"
AI explains
•	Deep fried
•	Excess oil
•	High sugar
•	Refined carbs
•	Large portion
and suggests healthier alternatives.
________________________________________
Module 6 – AI Coach
Answers questions like
•	Can I eat pizza?
•	Healthy breakfast?
•	Protein-rich snacks?
•	Can diabetics eat mango?
using the user's profile and conversation history.
________________________________________
Module 7 – Meal Memory
Stores
•	Breakfast
•	Lunch
•	Dinner
•	Snacks
Allows commands such as
•	Today's Meals
•	Yesterday's Meals
•	Delete Last Meal
________________________________________
Module 8 – Analytics
Provides
Daily Dashboard
Weekly Report
Monthly Insights
Shows
•	Calories
•	Protein
•	Meal Trends
•	Goal Progress
•	Eating Habits
________________________________________
Module 9 – Recommendation Engine
Suggests
•	Healthier foods
•	Dinner ideas
•	Snacks
•	Recipes
•	Grocery choices
based on remaining calorie and protein targets.
________________________________________
Module 10 – OCR
Reads
•	Nutrition labels
•	Ingredients
•	Restaurant menus
•	Food packets
________________________________________
Module 11 – Barcode Scanner
User scans product
↓
AI fetches
•	Ingredients
•	Nutrition
•	Rating
•	Health summary
Open Food Facts provides barcode-based product lookup together with ingredients and nutrition metadata for packaged foods. (Open Food Facts)
________________________________________
Module 12 – Exercise Tracking
Logs
•	Walking
•	Running
•	Cycling
Adjusts daily calorie budget accordingly.
________________________________________
9. AI Pipeline
Image / Voice / Text

↓

Input Processing

↓

Vision AI

↓

Food Detection

↓

Portion Estimation

↓

Nutrition API

↓

User Profile

↓

LLM Reasoning

↓

Recommendation Engine

↓

WhatsApp Reply
________________________________________
10. Backend Workflow
WhatsApp

↓

WhatsApp Cloud API

↓

Webhook

↓

FastAPI

↓

Authentication

↓

AI Processing

↓

Nutrition Engine

↓

Database

↓

Response Generator

↓

WhatsApp Reply
________________________________________
11. Database Design
Users
•	ID
•	Name
•	Height
•	Weight
•	Goal
Meals
•	Meal Name
•	Calories
•	Protein
•	Time
•	Image URL
Reports
•	Daily
•	Weekly
•	Monthly
Chat History
Stores
•	Questions
•	AI Replies
•	Meal Logs
Notifications
Stores
•	Reminder
•	Status
•	Schedule
________________________________________
12. Frontend
User Side
WhatsApp only
No app installation required.
Admin Dashboard
•	User Analytics
•	Daily Active Users
•	Reports
•	Logs
•	Feedback
•	AI Monitoring
•	API Health
•	Database Statistics
________________________________________
13. Security
•	HTTPS
•	JWT Authentication
•	Password Hashing
•	API Rate Limiting
•	Secure Image Storage
•	Environment Variables
•	Audit Logs
•	Input Validation
________________________________________
14. Deployment Architecture
User

↓

WhatsApp

↓

Meta WhatsApp Cloud API

↓

FastAPI Backend

↓

AI Services

↓

Nutrition APIs

↓

Redis

↓

PostgreSQL

↓

Cloudinary
________________________________________
15. Folder Structure
NutriChat-AI/

backend/

frontend/

ai/

vision/

ocr/

database/

services/

prompts/

models/

routes/

utils/

config/

tests/

docker/

docs/

README.md
________________________________________
16. Unique Selling Points (USP)
•	WhatsApp-first experience
•	No app installation
•	Indian food recognition
•	Multimodal AI (Photo + Voice + Text)
•	Personalized coaching
•	Meal memory
•	Context-aware conversations
•	Automatic food logging
•	Weekly and monthly analytics
•	Long-term health insights
________________________________________
18. Expected Learning Outcomes
This project demonstrates practical experience in:
•	Computer Vision
•	Natural Language Processing
•	Large Language Models (LLMs)
•	Multimodal AI
•	OCR
•	Prompt Engineering
•	FastAPI
•	REST API Development
•	PostgreSQL
•	Redis
•	WhatsApp Cloud API Integration
•	Authentication & Security
•	Docker
•	Cloud Deployment
•	Recommendation Systems
•	Analytics Dashboards
•	Production AI System Design
________________________________________
19. Project Deliverables
•	✅ WhatsApp AI Chatbot
•	✅ FastAPI Backend
•	✅ PostgreSQL Database
•	✅ AI Vision & Nutrition Pipeline
•	✅ Admin Dashboard
•	✅ REST APIs
•	✅ Dockerized Deployment
•	✅ Technical Documentation
•	✅ Source Code Repository
•	✅ Final Year Project Report
This scope is ambitious but achievable as an MVP, and it showcases a broad range of AI engineering skills—from multimodal input processing and conversational AI to backend development, cloud deployment, and real-world API integration—making it an excellent flagship portfolio project.

