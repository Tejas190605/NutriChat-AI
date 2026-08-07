"""Public legal and compliance routes for Meta/WhatsApp integration approval.

Exposes /privacy, /terms, and /data-deletion HTML pages.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

LAST_UPDATED = "August 7, 2026"


def _build_page_html(
    title: str,
    active_path: str,
    content_body: str,
) -> str:
    """Constructs a responsive HTML page with dark header navigation and clean typography."""
    privacy_active = 'class="active"' if active_path == "/privacy" else ""
    terms_active = 'class="active"' if active_path == "/terms" else ""
    deletion_active = 'class="active"' if active_path == "/data-deletion" else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - NutriChat AI</title>
    <style>
        :root {{
            --primary: #10b981;
            --primary-dark: #059669;
            --bg-dark: #0f172a;
            --bg-card: #ffffff;
            --bg-page: #f8fafc;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            line-height: 1.6;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}
        header {{
            background-color: var(--bg-dark);
            color: #ffffff;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }}
        .header-container {{
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .logo {{
            font-size: 1.35rem;
            font-weight: 700;
            color: #ffffff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .logo span {{
            color: var(--primary);
        }}
        nav {{
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}
        nav a {{
            color: #94a3b8;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            transition: all 0.2s ease;
        }}
        nav a:hover {{
            color: #ffffff;
            background-color: rgba(255, 255, 255, 0.08);
        }}
        nav a.active {{
            color: #ffffff;
            background-color: var(--primary);
        }}
        main {{
            flex: 1;
            max-width: 900px;
            width: 100%;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }}
        .card {{
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border);
        }}
        .page-header {{
            border-bottom: 2px solid #f1f5f9;
            padding-bottom: 1.25rem;
            margin-bottom: 2rem;
        }}
        h1 {{
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--bg-dark);
            margin-bottom: 0.5rem;
        }}
        .meta-date {{
            font-size: 0.875rem;
            color: var(--text-muted);
        }}
        section {{
            margin-bottom: 2rem;
        }}
        h2 {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--bg-dark);
            margin-bottom: 0.75rem;
            margin-top: 1.5rem;
        }}
        p {{
            margin-bottom: 1rem;
            color: #334155;
            font-size: 0.975rem;
        }}
        ul {{
            margin-bottom: 1rem;
            padding-left: 1.5rem;
            color: #334155;
        }}
        li {{
            margin-bottom: 0.5rem;
            font-size: 0.975rem;
        }}
        strong {{
            color: var(--bg-dark);
        }}
        .alert-box {{
            background-color: #f0fdf4;
            border-left: 4px solid var(--primary);
            padding: 1.25rem;
            border-radius: 6px;
            margin: 1.5rem 0;
        }}
        .alert-box p {{
            margin-bottom: 0;
            color: #166534;
            font-weight: 500;
        }}
        footer {{
            background-color: var(--bg-dark);
            color: #94a3b8;
            padding: 2rem 1.5rem;
            text-align: center;
            font-size: 0.875rem;
            margin-top: auto;
        }}
        footer a {{
            color: var(--primary);
            text-decoration: none;
        }}
        footer a:hover {{
            text-decoration: underline;
        }}
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }}
        @media (max-width: 640px) {{
            .card {{
                padding: 1.5rem;
            }}
            h1 {{
                font-size: 1.5rem;
            }}
            .header-container {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-container">
            <a href="/privacy" class="logo">
                🥦 NutriChat <span>AI</span>
            </a>
            <nav>
                <a href="/privacy" {privacy_active}>Privacy Policy</a>
                <a href="/terms" {terms_active}>Terms of Service</a>
                <a href="/data-deletion" {deletion_active}>Data Deletion</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="card">
            <div class="page-header">
                <h1>{title}</h1>
                <div class="meta-date">Last updated: {LAST_UPDATED}</div>
            </div>
            {content_body}
        </div>
    </main>

    <footer>
        <div class="footer-links">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
            <a href="/data-deletion">Data Deletion Instructions</a>
        </div>
        <p>&copy; 2026 NutriChat AI. All rights reserved. Powered by Artificial Intelligence.</p>
    </footer>
</body>
</html>
"""


@router.get("/privacy", response_class=HTMLResponse, summary="NutriChat AI Privacy Policy")
async def get_privacy_policy() -> HTMLResponse:
    """Returns the public Privacy Policy webpage for NutriChat AI."""
    content = """
    <section>
        <h2>1. Overview & Service Purpose</h2>
        <p>NutriChat AI ("we", "our", or "us") is an artificial intelligence-powered nutrition and wellness assistant. Our service enables users to log meals, estimate macronutrients, track daily dietary intake, and receive personalized nutrition insights by interacting via WhatsApp messages or our web dashboard.</p>
        <p>We are committed to respecting your privacy and protecting personal information shared with us through our application.</p>
    </section>

    <section>
        <h2>2. Information We Collect</h2>
        <p>Depending on how you interact with NutriChat AI, we collect the following types of information:</p>
        <ul>
            <li><strong>Information You Provide Voluntarily:</strong> Profile inputs such as your name, age, gender, height, weight, daily activity level, and target wellness goals.</li>
            <li><strong>WhatsApp Messages & Media:</strong> Messages, food photos, meal descriptions, and barcodes sent to NutriChat AI via WhatsApp to perform food identification and nutrition analysis.</li>
            <li><strong>Nutritional & Meal Logs:</strong> AI-estimated calories, protein, carbohydrates, fat, fiber, and meal consumption timestamps saved to your personal history diary.</li>
            <li><strong>Technical & Session Data:</strong> Technical identifiers required to operate the service, including your WhatsApp phone number, session state tokens, and diagnostic logging entries.</li>
        </ul>
    </section>

    <section>
        <h2>3. How Information Is Used</h2>
        <p>Your information is used strictly to provide, maintain, and improve the NutriChat AI service:</p>
        <ul>
            <li>To process food photos and meal text queries using artificial intelligence model providers to estimate macronutrient values.</li>
            <li>To compute daily nutritional progress against your active calorie and macro target goals.</li>
            <li>To generate and deliver automated nutrition summary replies via WhatsApp and display history on your web dashboard.</li>
            <li>To monitor system performance, troubleshoot technical errors, and prevent malicious abuse.</li>
        </ul>
    </section>

    <section>
        <h2>4. Third-Party Infrastructure & AI Services</h2>
        <p>To deliver NutriChat AI, we utilize trusted third-party infrastructure and service providers:</p>
        <ul>
            <li><strong>Meta WhatsApp Cloud API:</strong> Facilitates the transmission and reception of messaging communication and media attachments.</li>
            <li><strong>Google Gemini AI:</strong> Processes food images and text queries to generate structured nutritional estimations and guidance.</li>
            <li><strong>Cloud Hosting & Databases:</strong> Applications, Redis caching, and PostgreSQL databases hosted on Render platform infrastructure.</li>
        </ul>
        <p>Third-party service providers handle data in accordance with their respective privacy and security protocols.</p>
    </section>

    <section>
        <h2>5. Security Practices & Data Retention</h2>
        <p>We implement reasonable administrative, technical, and physical safeguards designed to protect user data against unauthorized access, loss, or misuse.</p>
        <p>Meal logs and user profile details are retained to provide ongoing tracking history for as long as your account remains active or until you submit a data deletion request.</p>
    </section>

    <section>
        <h2>6. User Rights & Data Deletion Requests</h2>
        <p>You have the right to access, review, or request deletion of your personal data stored by NutriChat AI at any time.</p>
        <p>To request data deletion, you can send the <code>/reset</code> command in your WhatsApp chat or follow the instructions on our <a href="/data-deletion">Data Deletion Page</a>.</p>
    </section>

    <div class="alert-box">
        <p><strong>Informational Disclaimer:</strong> NutriChat AI is an educational self-tracking assistant. AI-generated nutrition estimates are approximations and do not constitute professional medical advice, clinical diagnosis, or dietary treatment. Always consult a qualified physician or dietitian for medical decisions.</p>
    </div>

    <section>
        <h2>7. Policy Changes & Contact Information</h2>
        <p>We may update this Privacy Policy periodically. Any modifications become effective upon posting to this URL.</p>
        <p>If you have any questions or privacy inquiries, please contact us at <strong>support@nutrichat.ai</strong>.</p>
    </section>
    """
    html = _build_page_html("Privacy Policy", "/privacy", content)
    return HTMLResponse(content=html, status_code=200)


@router.get("/terms", response_class=HTMLResponse, summary="NutriChat AI Terms of Service")
async def get_terms_of_service() -> HTMLResponse:
    """Returns the public Terms of Service webpage for NutriChat AI."""
    content = """
    <section>
        <h2>1. Acceptance of Terms</h2>
        <p>By accessing or using NutriChat AI via WhatsApp or our web interface, you agree to be bound by these Terms of Service. If you do not agree with any part of these terms, you should not use the service.</p>
    </section>

    <section>
        <h2>2. Description of NutriChat AI</h2>
        <p>NutriChat AI is an automated nutrition tracking and wellness assistant. The service processes text and image inputs (such as food photos) to estimate nutritional composition, track daily caloric intake, and provide automated recommendations.</p>
    </section>

    <div class="alert-box">
        <p><strong>Medical & Healthcare Disclaimer:</strong> NutriChat AI is provided solely for informational and personal self-monitoring purposes. The service DOES NOT provide professional medical advice, diagnosis, or clinical treatment. Never disregard professional medical advice or delay seeking treatment because of information generated by NutriChat AI.</p>
    </div>

    <section>
        <h2>3. Responsible Use & AI Limitations</h2>
        <p>You agree to use NutriChat AI responsibly and acknowledge the following operational boundaries:</p>
        <ul>
            <li><strong>AI Estimation Accuracy:</strong> Nutritional calculations are estimates based on computer vision models and AI reasoning. Actual nutritional values may vary based on ingredients, portion sizes, and preparation methods.</li>
            <li><strong>Prohibited Conduct:</strong> You agree not to upload malicious files, attempt unauthorized access to application systems, or send abusive content through our messaging channels.</li>
        </ul>
    </section>

    <section>
        <h2>4. User Responsibilities</h2>
        <p>You are responsible for ensuring the accuracy of personal profile metrics (such as age, height, and weight) entered into the service, as well as maintaining the security of your WhatsApp account and mobile device.</p>
    </section>

    <section>
        <h2>5. Third-Party Integrations</h2>
        <p>NutriChat AI integrates with third-party APIs including Meta WhatsApp Cloud API and Google Gemini AI. Availability and behavior of these features may depend on third-party platform policies and uptime.</p>
    </section>

    <section>
        <h2>6. Intellectual Property & Brand Ownership</h2>
        <p>All software code, user interface designs, logos, and brand elements associated with NutriChat AI are the intellectual property of NutriChat AI and its developers.</p>
    </section>

    <section>
        <h2>7. Limitation of Liability & Service Termination</h2>
        <p>NutriChat AI is provided on an "AS IS" and "AS AVAILABLE" basis without warranties of any kind. We are not liable for decisions made or actions taken based on AI nutrition outputs. We reserve the right to restrict or terminate access to users who violate these terms.</p>
    </section>

    <section>
        <h2>8. Changes to Terms & Contact</h2>
        <p>We reserve the right to revise these Terms of Service at any time. Continued use of NutriChat AI following updates constitutes acceptance. For inquiries regarding these terms, contact <strong>support@nutrichat.ai</strong>.</p>
    </section>
    """
    html = _build_page_html("Terms of Service", "/terms", content)
    return HTMLResponse(content=html, status_code=200)


@router.get("/data-deletion", response_class=HTMLResponse, summary="NutriChat AI User Data Deletion Instructions")
async def get_data_deletion_instructions() -> HTMLResponse:
    """Returns the public User Data Deletion Instructions webpage for NutriChat AI."""
    content = """
    <section>
        <h2>Meta Developer App Data Deletion Compliance</h2>
        <p>NutriChat AI provides straightforward and accessible data deletion procedures for users wishing to delete their account profile, WhatsApp chat sessions, or logged meal history records.</p>
    </section>

    <section>
        <h2>How to Request Data Deletion</h2>
        <p>You can request complete deletion of your user data through either of the following methods:</p>

        <h3>Option 1: Direct WhatsApp Command (Instant Reset)</h3>
        <p>Open your NutriChat AI chat on WhatsApp and send the following text command:</p>
        <div class="alert-box">
            <p><code>/reset</code></p>
        </div>
        <p>Sending <code>/reset</code> clears your active onboarding state and session data stored in our Redis cache system.</p>

        <h3>Option 2: Email Data Deletion Request</h3>
        <p>Send an email request to our support team at:</p>
        <p><strong>Email:</strong> <code>support@nutrichat.ai</code><br>
        <strong>Subject Line:</strong> Data Deletion Request</p>
    </section>

    <section>
        <h2>Information Required in Request</h2>
        <p>When requesting data deletion via email, please include:</p>
        <ul>
            <li>Your registered <strong>WhatsApp Phone Number</strong> (including country code, e.g. <code>+919876543210</code>).</li>
            <li>Or your registered <strong>Account Email Address</strong> if created via the web dashboard.</li>
        </ul>
    </section>

    <section>
        <h2>Data Handling & Processing Workflow</h2>
        <p>Upon receiving a verified deletion request:</p>
        <ul>
            <li>Your user record, profile metrics, goal settings, weight history, and logged meal entries will be permanently removed from our PostgreSQL database.</li>
            <li>Active session tokens and cached parameters will be deleted from our Redis cache.</li>
            <li>Email deletion requests are processed within <strong>7 business days</strong>, and confirmation will be sent to your email.</li>
        </ul>
    </section>

    <section>
        <h2>Data Retention Exceptions</h2>
        <p>Certain non-identifying, aggregated system logs or transaction records may be retained temporarily where required for security audit compliance or mandatory legal obligations.</p>
    </section>
    """
    html = _build_page_html("User Data Deletion Instructions", "/data-deletion", content)
    return HTMLResponse(content=html, status_code=200)
