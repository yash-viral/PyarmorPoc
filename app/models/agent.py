from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("licenses.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    last_request_time = Column(DateTime, nullable=True)
    request_count = Column(Integer, default=0)

    license = relationship("License", back_populates="agents")

    def __repr__(self):
        return f"<Agent {self.agent_name}>"