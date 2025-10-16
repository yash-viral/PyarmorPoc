"""scripts/seed_all_demo.py

Populate the database with demo data across all tables:
- Plans (starter, pro, enterprise)
- Users (demo users)
- Licenses (created via service to ensure license_data + signature)
- Agents (created by the service)

Run from project root:

    python scripts{}seed_all_demo.py

The script is idempotent: it will not duplicate existing plans/users/licenses.
""".format("\\")
import os
import sys

# Ensure project root is on sys.path so `import app` works when running the script
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from app.db import SessionLocal, init_db
from app import models, schemas
from app.services import license_service
from sqlalchemy.orm import Session


def ensure_plans(db: Session):
    plans = [
        {"name": "starter", "description": "Starter plan", "max_agents": 2, "rate_limit_per_min": 2, "duration_days": 30},
        {"name": "pro", "description": "Pro plan", "max_agents": 5, "rate_limit_per_min": 4, "duration_days": 30},
        {"name": "enterprise", "description": "Enterprise plan", "max_agents": 4, "rate_limit_per_min": 10, "duration_days":30},
    ]
    created = []
    for p in plans:
        existing = db.query(models.Plan).filter(models.Plan.name == p["name"]).first()
        if not existing:
            plan = models.Plan(name=p["name"], description=p["description"], max_agents=p["max_agents"], rate_limit_per_min=p["rate_limit_per_min"], duration_days=p["duration_days"])
            db.add(plan)
            db.commit()
            db.refresh(plan)
            created.append(plan)
            print(f"Created plan: {plan.name} (id={plan.id})")
        else:
            created.append(existing)
            print(f"Plan exists: {existing.name} (id={existing.id})")
    return created


def ensure_users(db: Session):
    users = [
        {"email": "demo@example.com", "name": "Demo User", "password_hash": "demo"},
        {"email": "alice@example.com", "name": "Alice", "password_hash": "alice"},
    ]
    created = []
    for u in users:
        existing = db.query(models.User).filter(models.User.email == u["email"]).first()
        if not existing:
            user = models.User(email=u["email"], name=u["name"], password_hash=u["password_hash"])
            db.add(user)
            db.commit()
            db.refresh(user)
            created.append(user)
            print(f"Created user: {user.email} (id={user.id})")
        else:
            created.append(existing)
            print(f"User exists: {existing.email} (id={existing.id})")
    return created


def ensure_licenses(db: Session):
    # Create some sample licenses using the service so signatures and agent rows are correct
    # Skip if a matching active license already exists for user+plan
    created = []

    # mapping: user_email -> (plan_name, agents, duration_days)
    tasks = [
        ("demo@example.com", "starter", ["agent1"], 7),
        ("alice@example.com", "pro", ["a1", "a2"], 30),
    ]

    for email, plan_name, agents, duration in tasks:
        user = db.query(models.User).filter(models.User.email == email).first()
        plan = db.query(models.Plan).filter(models.Plan.name == plan_name).first()
        if not user or not plan:
            print(f"Skipping license creation for {email}/{plan_name}: missing user or plan")
            continue

        # check existing active license for user+plan
        existing = db.query(models.License).filter(models.License.user_id == user.id, models.License.plan_id == plan.id, models.License.is_active == True).first()
        if existing:
            print(f"Active license exists for {email} / {plan_name} -> {existing.license_key}")
            created.append(existing)
            continue

        # Build request schema and call service
        req = schemas.LicenseCreate(user_id=user.id, plan=plan.name, agents=agents, duration_days=duration)
        # set plan_id and machine_id if schema supports it
        try:
            # prefer to set plan_id attribute if present on schema
            req.plan_id = plan.id
        except Exception:
            pass
        try:
            req.machine_id = None
        except Exception:
            pass

        try:
            resp = license_service.create_license(db, req)
            print(f"Created license for {email}: {resp.license_key}")
            created.append(resp)
        except Exception as e:
            print(f"Failed to create license for {email}/{plan_name}: {e}")

    return created


def seed_all():
    init_db()
    db = SessionLocal()
    try:
        ensure_plans(db)
        ensure_users(db)
        ensure_licenses(db)
        print("Seeding complete.")
    finally:
        db.close()


if __name__ == '__main__':
    seed_all()
