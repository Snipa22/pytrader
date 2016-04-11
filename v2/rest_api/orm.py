from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Index, Date, Text
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.ip_address import IPAddressType
from sqlalchemy_utils.types.encrypted import EncryptedType
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import datetime

Base = declarative_base()

"""
Classes are laid out as follows:
class Sample(Base):
    __tablename__ = 'sample'
    # Table data storage columns

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


This is to keep the file straight and sorted.  If you're refactoring code and something in ORM is broken, look at the
column names to keep it all straight.

Please define a column name for any column you add.  This will allow references to change much more easily
"""


# Class wide support functions
def get_random_salt():
    import random
    import string
    return ''.join(random.SystemRandom()
                   .choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(32))


class IDClass(Base):
    """
    Simple base class to include the required ID per table.

    Added Columns:
    id - Unique ID to identify the record
    """
    # Table data storage columns
    id = Column('id', Integer, primary_key=True)

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class TimeBaseClass(IDClass):
    """
    Base class to deal with any class that needs to store creation/update timers

    Added Columns:
    date_created - Creation date of the record
    date_updated - Record of last change to the record, auto-updates
    """
    # Table data storage columns
    date_created = Column('date_created', DateTime, default=datetime.datetime.now)
    date_updated = Column('date_updated', DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class OwnedClass(TimeBaseClass):
    """
    Adds basic user tracking

    Added Columns:
    user_id - User ID Storage, Numeric
    user - Foreign keyed relationship to get the user record in cases where it's needed.
    """
    # Table data storage columns

    # Foreign Key References
    user_id = Column('user_id', Integer, ForeignKey('users.id'))

    # Relationships to other tables
    user = relationship('Users', foreign_keys=[user_id])

    # Indexes (If applicable)

    # Class Functions (If applicable)


class TestBases(TimeBaseClass):
    """
    Class for holding the base configuration for other classes that need access to classifier/prediction tests.
    """
    # Table data storage columns

    # Foreign Key References
    classifier_test_id = Column('classifier_test_id', Integer, ForeignKey('ClassifierTests.id'))
    prediction_test_id = Column('prediction_test_id', Integer, ForeignKey('PredictionTests.id'))

    # Relationships to other tables
    classifier_test = relationship('ClassifierTests')
    prediction_test = relationship('PredictionTests')

    # Indexes (If applicable)

    # Class Functions (If applicable)


class AddDeleteTrackClass(TimeBaseClass):
    """
    Adds fields to the base time class to help track who's adding/deleting things in the database

    Added Columns:
    created_user_id - Track the user who's creating the record
    created_user - Track the user who's creating the record
    date_deleted - Date the record was flagged as deleted
    deleted - Track if the record is deleted or not.
    deleted_user_id - Track the user whom deleted the record
    deleted_user - Track the user whom deleted the record
    """
    # Table data storage columns
    date_deleted = Column('date_deleted', DateTime, default=datetime.datetime.now)
    deleted = Column('deleted', Boolean)

    # Foreign Key References
    created_user_id = Column('created_user_id', Integer, ForeignKey('Users.id'))
    deleted_user_id = Column('deleted_user_id', Integer, ForeignKey('Users.id'))

    # Relationships to other tables
    created_user = relationship('Users', foreign_keys=[created_user_id])
    deleted_user = relationship('Users', foreign_keys=[deleted_user_id])

    # Indexes (If applicable)

    # Class Functions (If applicable)


class Users(AddDeleteTrackClass):
    """
    Primary user tracking class, maintains usernames, secret keys, and a whole lotta fkeys.

    """
    __tablename__ = 'Users'
    # Table data storage columns
    username = Column('username', String(length=256), nullable=False)
    secret_key = Column('secret_key', EncryptedType(String(length=256)))
    secret_key_salt = Column('secret_key_salt', String(length=32), default=get_random_salt)

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class Workers(OwnedClass):
    """
    Table for tracking all the remote workers that need to log work into the system
    """
    __tablename__ = 'Workers'
    # Table data storage columns
    ip_address = Column('ip_address', IPAddressType)
    last_check_in = Column('last_check_in', DateTime)
    tasks_complete = Column('tasks_complete', Integer, default=0)

    # Foreign Key References
    task_id = Column('task_id', Integer, ForeignKey('Tasks.id'))

    # Relationships to other tables
    task = relationship('Tasks')

    # Indexes (If applicable)

    # Class Functions (If applicable)


class OAuthAuth(TimeBaseClass):
    """
    Storage for OAuth Authorization tokens so you can get your access tokens.
    """
    __tablename__ = 'OAuthAuth'
    # Table data storage columns
    token = Column('token', String(length=256))

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class OAuthAccess(OwnedClass):
    """
    Storage for OAuth Access tokens so you can get at the APIs
    """
    __tablename__ = 'OAuthAccess'
    # Table data storage columns
    date_expires = Column('date_expires', DateTime)
    grants = Column('grants', Integer)
    token = Column('token', String(length=256))

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class PerformanceComparison(AddDeleteTrackClass, OwnedClass):
    """
    Storage for performance comparisons
    These take the NN recommendations and validates them against the actual performance seen.
    """
    __tablename__ = 'PerformanceComparison'
    # Table data storage columns
    actual_movement = Column('actual_movement', Float)
    delta = Column('delta', Float)
    directionally_same = Column('directionally_same', Boolean)
    neural_network_rec = Column('neural_network_rec', Float)
    percent_buy = Column('percent_buy', Float)
    percent_hold = Column('percent_hold', Float)
    percent_sell = Column('percent_sell', Float)
    price_time_range_start = Column('price_time_range_start', DateTime)
    price_time_range_end = Column('price_time_range_end', DateTime)
    recommendation_count = Column('recommendation_count', Integer)
    tr_time_range_start = Column('tr_time_range_start', DateTime)
    tr_time_range_end = Column('tr_time_range_end', DateTime)
    weighted_average_neural_rec = Column('weighted_average_neural_rec', Float)

    # Foreign Key References
    recommendation_id = Column('recommendation_id', Integer, ForeignKey('TradeRecommendations.id'))
    symbol_pair_id = Column('symbol_pair_id', Integer, ForeignKey('SymbolPairs.id'))

    # Relationships to other tables
    recommendation = relationship('TradeRecommendations')
    symbol_pair = relationship('SymbolPairs')

    # Indexes (If applicable)

    # Class Functions (If applicable)


class TradeSites(TimeBaseClass):
    """
    Listing of all sites that we permit data retrieval and/or trading at.
    """
    __tablename__ = 'TradeSites'
    # Table data storage columns
    api_uri = Column('api_uri', String(length=256))
    name = Column('name', String(length=256))
    uri = Column('uri', String(length=256))

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class Tasks(TestBases, OwnedClass):
    """
    Listing of all tasks to be run remotely,
    """
    __tablename__ = 'Tasks'
    # Table data storage columns
    date_last_failure = Column('date_last_failure', DateTime)
    date_last_success = Column('date_last_success', DateTime)
    date_last_ran = Column('date_last_ran', DateTime)

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)


class TaskResults(TestBases):
    """
    Results from all the remote tasks.
    """
    __tablename__ = 'TaskResults'
    # Table data storage columns
    average_diff = Column('average_diff')
    output = Column('output', Text(length=65535))
    percent_correct = Column('percent_correct', Integer)
    prediction_size = Column('prediction_size', Integer)
    profit_loss_float = Column('profit_loss_float', Float)
    profit_loss_int = Column('profit_loss_int', Integer)
    run_time = Column('run_time', Float)
    score = Column('score', Integer)

    # Foreign Key References
    worker_id = Column('worker_id', Integer, ForeignKey('Workers.id'))
    task_id = Column('task_id', Integer, ForeignKey('Tasks.id'))

    # Relationships to other tables
    worker = relationship('Workers')
    task = relationship('Tasks')

    # Indexes (If applicable)

    # Class Functions (If applicable)


class BaseTest(AddDeleteTrackClass):
    """
    Fields shared by both Classifier and Prediction tests

    Added Fields:
    test_type - Defines if this is a live or mock test.
    data_set_inputs - Number of inputs to be sent to the NN/Classifier
    granularity - Resolution in seconds of preferred data sets.
    minutes_back - How much data should be pulled?
    training_set_length - How long in minutes do we want to use for training, remainder is verification.
    site/_id - Site ID that this test is running against
    symbol_pair/_id - Symbol pair that this test is running against.
    """
    TEST_TYPES = [
        ('mock', 'Mock'),
        ('live', 'Live'),
    ]
    # Table data storage columns
    test_type = Column('test_type', ChoiceType(TEST_TYPES))
    data_set_inputs = Column('data_set_inputs', Integer)
    granularity = Column('granularity', Integer)
    minutes_back = Column('minutes_back', Integer)
    training_set_length = Column('training_set_length', Integer)

    # Foreign Key References
    site_id = Column('task_id', Integer, ForeignKey('TradeSites.id'))
    symbol_pair_id = Column('worker_id', Integer, ForeignKey('SymbolPairs.id'))

    # Relationships to other tables
    site = relationship('TradeSites')
    symbol_pair = relationship('SymbolPairs')

    # Indexes (If applicable)

    # Class Functions (If applicable)


class PredictionTest(BaseTest):
    """
    Variables that go into a prediction (NN) test
    """
    __tablename__ = 'PredictionTest'
    # Table choice information
    PREDICTION_TYPES = [

    ]

    # Table data storage columns
    prediction_type = Column('prediction_type': ChoiceType(PREDICTION_TYPES))
    bias = Column('bias', Boolean)
    recurrent = Column('recurrent', Boolean)
    weight_delay = Column('weight_delay', Float)
    hidden_neurons = Column('hidden_neurons', Integer)
    epochs = Column('epochs', Integer)
    momentum = Column('momentum', Float)
    learning_rate = Column('learning_rate', Float)

    # Foreign Key References

    # Relationships to other tables

    # Indexes (If applicable)

    # Class Functions (If applicable)