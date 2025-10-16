"""
scripts/seed_demo.py

Creates a demo user and plan (id=1) for local testing.
Run from project root:

    python scripts\seed_demo.py

"""
from app.db import SessionLocal, init_db
from app import models
from sqlalchemy.orm import Session


def seed():
    init_db()
    db: Session = SessionLocal()
    try:
        # create demo plan if missing
        plan = db.query(models.Plan).filter(models.Plan.id == 1).first()
        if not plan:
            plan = models.Plan(id=1, name='starter', description='Demo starter plan', max_agents=2, rate_limit_per_min=5, duration_days=30)
            db.add(plan)
            print('Created demo Plan id=1')

        # create demo user if missing
        user = db.query(models.User).filter(models.User.id == 1).first()
        if not user:
            user = models.User(id=1, email='demo@example.com', name='Demo User', password_hash='demo')
            db.add(user)
            print('Created demo User id=1')

        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    seed()
    print('Seeding complete.')
