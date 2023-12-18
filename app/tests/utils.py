from models import Customer, Restaurant, Review

def clear_db(session):
    session.query(Customer).delete()
    session.query(Restaurant).delete()
    session.query(Review).delete()
    session.commit()