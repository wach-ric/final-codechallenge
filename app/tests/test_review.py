from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .conftest import SQLITE_URL
from models import Customer, Restaurant, Review

from .utils import clear_db

class TestReview:
    def test_creating_review_instance(self):
        review = Review(star_rating=10, customer_id=1, restaurant_id=1)

        assert review != None
        assert review.star_rating == 10

    def test_get_restaurant(self):
        """
            Should return the `Restaurant` instance for this review
        """
        engine = create_engine(SQLITE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        clear_db(session)

        customer = Customer(first_name="John", last_name="Doe")
        customer2 = Customer(first_name="John1", last_name="Doe1")
        session.add(customer)
        session.add(customer2)

        session.commit()

        customer = session.query(Customer).first()
        customer2 = session.query(Customer).all()[1]

        restaurant1 = Restaurant(name="R1", price=1000)
        restaurant2 = Restaurant(name="R2", price=2000)
        session.bulk_save_objects([restaurant1, restaurant2])

        session.commit()

        restaurant1 = session.query(Restaurant).first()
        restaurant2 = session.query(Restaurant).all()[1]

        review1c1 = Review(star_rating=5, customer_id=customer.id, restaurant_id=restaurant1.id)
        review2c1 = Review(star_rating=8, customer_id=customer.id, restaurant_id=restaurant2.id)
        review1c2 = Review(star_rating=6, customer_id=customer2.id, restaurant_id=restaurant1.id)
        review2c2 = Review(star_rating=10, customer_id=customer2.id, restaurant_id=restaurant2.id)

        session.bulk_save_objects([review1c1, review2c1, review1c2, review2c2])
        session.commit()

        review1c1 = session.query(Review).first()
        review2c1 = session.query(Review).all()[1]

        assert review1c1.get_restaurant().name == "R1"
        assert review1c1.get_restaurant().price == 1000
        assert review2c1.get_restaurant().name == "R2"
        assert review2c1.get_restaurant().price == 2000


        clear_db(session)

    def test_get_customer(self):
        """
            Should return the `Customer` instance for this review
        """
        engine = create_engine(SQLITE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        clear_db(session)

        customer = Customer(first_name="John", last_name="Doe")
        customer2 = Customer(first_name="John1", last_name="Doe1")
        session.add(customer)
        session.add(customer2)

        session.commit()

        customer = session.query(Customer).first()
        customer2 = session.query(Customer).all()[1]

        restaurant1 = Restaurant(name="R1", price=1000)
        restaurant2 = Restaurant(name="R2", price=2000)
        session.bulk_save_objects([restaurant1, restaurant2])

        session.commit()

        restaurant1 = session.query(Restaurant).first()
        restaurant2 = session.query(Restaurant).all()[1]

        review1c1 = Review(star_rating=5, customer_id=customer.id, restaurant_id=restaurant1.id)
        review2c1 = Review(star_rating=8, customer_id=customer.id, restaurant_id=restaurant2.id)
        review1c2 = Review(star_rating=6, customer_id=customer2.id, restaurant_id=restaurant1.id)
        review2c2 = Review(star_rating=10, customer_id=customer2.id, restaurant_id=restaurant2.id)

        session.bulk_save_objects([review1c1, review2c1, review1c2, review2c2])
        session.commit()

        review1c1 = session.query(Review).first()

        assert review1c1.get_customer().first_name == "John"
        assert review1c1.get_customer().last_name == "Doe"

        clear_db(session)

    def test_full_review(self):
        """
            Tests should return a string formatted as follows: Review for 
            {insert restaurant name} by {insert customer's full name}: 
            {insert review star_rating} stars.
        """
        engine = create_engine(SQLITE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        clear_db(session)

        customer = Customer(first_name="John", last_name="Doe")
        session.add(customer)

        session.commit()

        customer = session.query(Customer).first()

        restaurant1 = Restaurant(name="R1", price=1000)
        session.add(restaurant1)

        session.commit()

        restaurant1 = session.query(Restaurant).first()

        review1c1 = Review(star_rating=5, customer_id=customer.id, restaurant_id=restaurant1.id)

        session.add(review1c1)
        session.commit()

        review1c1 = session.query(Review).first()

        assert review1c1.full_review() == "Review for R1 by John Doe: 5 stars."

        clear_db(session)










