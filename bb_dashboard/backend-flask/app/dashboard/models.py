# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, DateTime
from datetime import datetime
from app import db, login_manager
from datetime import datetime


class ImpulseEvents(db.Model):
    

    id = Column(Integer, primary_key=True)
    mac_address = Column(db.Text, nullable=False)
    ip_address = Column(db.Text, nullable=False)
    event_type = Column(db.Text, nullable=False)
    event_name = Column(db.Text, nullable=False)
    ts_local = Column(db.DateTime, nullable=False)
    ts_server = Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __tablename__ = 'impulse_events'
    __table_args__ = (db.UniqueConstraint('mac_address', 'ip_address','event_type','event_name','ts_local'),)
                     

    def __repr__(self):
        return str(self.mac_address)
