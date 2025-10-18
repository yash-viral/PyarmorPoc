from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    max_agents = Column(Integer, default=1)
    rate_limit_per_min = Column(Integer, default=2)
    duration_days = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)

    licenses = relationship("License", back_populates="plan")

    def __repr__(self):
        return f"<Plan {self.name}>"