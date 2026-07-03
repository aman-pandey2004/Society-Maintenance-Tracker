# 🏢 SocietyCare - Centralized Society Maintenance & Audit Tracker

A modern, high-visibility decentralized audit logging and workflow framework built to manage, track, and streamline residential society maintenance complaints, broadcast announcements, and lifecycle metrics in real-time.

---

## 🚀 Key Features

- **Resident Portal:** Clean, modern interface for residents to securely sign in, log structural/maintenance faults, upload visual proof attachments, and track live status tickets.
- **Admin Control Subsystem:** Dedicated administrative matrix dashboard to update operational states (`Open` -> `In Progress` -> `Resolved`), append detailed log notes, and broadcast community-wide urgent pinning notices.
- **Automated Lifecycle Audit Trail:** Complete transparency with historical compliance streams that log timestamps and actor interactions for every ticket transaction.
- **Overdue Exception Trigger:** Real-time indicator system to flag lingering unresolved operational faults automatically.
- **Premium Dark UI Layout:** High-contrast custom **Slate & Cyber Emerald Green** minimalist dashboard designed specifically for readability and responsive screen layouts.

---

## 🛠️ Tech Stack & Keywords

- **Backend Architecture:** Python, Django Framework (MVC / MTV architecture)
- **Database Model Engine:** Django ORM, SQLite (Local Ledger Subsystem) / PostgreSQL compatibility
- **Frontend Layer:** HTML5, CSS3, Custom Minimalist Grid Overrides, Bootstrap v5.3, Inter Font
- **Deployment Platform:** Render Environment
- **Key Security & Routing:** Django Authentication System, CSRF Protection Tokens, Secure Session Middleware

---

## 📂 Project Structure Overview

```text
├── core/
│   ├── templates/
│   │   └── core/
│   │       ├── dashboard.html   # Main Architectural Audit Workspace
│   │       ├── login.html       # Clean Slate Resident Sign-In Terminal
│   │       └── register.html    # Node Initialization Registration Sheet
│   ├── models.py                # Database Core Schemas (Complaints, Notices, Logs)
│   ├── views.py                 # Core Transaction Flow & Validation Logic
│   └── urls.py                  # Component Route Navigation Nodes
├── society_tracker/
│   ├── settings.py              # Environment Global Configuration & Core Security
│   └── urls.py                  # Master Router & Admin Interface CSS Overrides
└── manage.py                    # Django Command Line Utility Node
