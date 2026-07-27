
# Uniti Backend

The robust Django REST Framework (DRF) backend powering Uniti, a modern property management and tenant billing platform.

## Live Services & Documentation
* **Production API Base URL:** [https://uniti-backend.onrender.com](https://uniti-backend.onrender.com)
* **Interactive API Documentation (Swagger UI):** [https://uniti-backend.onrender.com/api/docs/](https://uniti-backend.onrender.com/api/docs/)
* **OpenAPI Schema Endpoint:** [https://uniti-backend.onrender.com/api/schema/](https://uniti-backend.onrender.com/api/schema/)

---

## Tech Stack
* **Framework:** Django & Django REST Framework (DRF)
* **API Documentation:** `drf-spectacular` (OpenAPI 3)
* **Database:** PostgreSQL (Production) / SQLite (Local Development)
* **WSGI Server:** Gunicorn
* **Hosting & Deployment:** Render (Free Tier Web Service)

---

## Core App Architecture
* **`accounts/`**: User management, roles (Landlords, Tenants, House Hunters), registration, and token authentication.
* **`invoicing/`**: Automated and manual billing records, itemized invoicing, tracking paid amounts, and statuses.
* **`payments/`**: Integration layers for payment gateways including MPesa STK push callbacks, dispute resolution, and payment handling.
* **`properties/` & `listings/`**: Real estate property mapping, unit configurations, and available rental listings.
* **`tenant/` & `tickets/`**: Tenant portal features, maintenance tracking, and support ticketing systems.
* **`core/`**: Shared utilities, system health check views, and dashboard summary views.

---


1. **Clone the repository:**
   git clone [https://github.com/jeankariuki-sudo/unitiback.git](https://github.com/jeankariuki-sudo/unitiback.git)
   cd unitiback



2. **Create and activate a virtual environment:**
python3 -m venv venv
source venv/bin/activate




3. **Install dependencies:**
pip install -r requirements.txt



4. **Configure environment variables:**
Create a `.env` file in the root directory containing your database credentials, secret keys, and integration credentials.
5. **Run database migrations:**
python manage.py migrate




6. **Start the local development server:**
python manage.py runserver





## API Documentation Generation

To update or test the OpenAPI schema locally:

python manage.py spectacular --file schema.yml




