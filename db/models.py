from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# связь преподаватель ↔ студент (many-to-many)
subscriptions = Table(
    'subscriptions', Base.metadata,
    Column('teacher_id', Integer, ForeignKey('users.id')),
    Column('student_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    yadisk_token = Column(String, nullable=True)

    # подписки: кто на кого подписан
    # students — мои студенты; teachers — мои преподаватели
    students = relationship(
        'User',
        secondary=subscriptions,
        primaryjoin=id == subscriptions.c.teacher_id,
        secondaryjoin=id == subscriptions.c.student_id,
        backref='teachers'
    )

    tracked_folders = relationship('TrackedFolder', back_populates='owner')


class TrackedFolder(Base):
    __tablename__ = 'tracked_folders'

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='tracked_folders')
