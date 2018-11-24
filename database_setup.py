import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class DuesRecord(Base):
    __tablename__ = 'dues_record'

    roll_no = Column(
        String(10),
        primary_key = True
    )
    name = Column(
        String(80),
        nullable = True
    )
    due = Column(
        Integer,
        nullable = True
    )
    
    @property
    def serialize(self):
        return {
            'roll_no': self.roll_no,
            'name': self.name,
            'due': self.due,
        }
    

###################end#of#file###################

engine = create_engine('sqlite:///dues_record.db')
Base.metadata.create_all(engine)