import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .conftest import SQLITE_URL
from models import Customer, Restaurant, Review

from .utils import clear_db

class TestRestaurant:
    def test_creating_restaurant_instance(self):
        restaurant = Restaurant(name="R", price=1000)

        assert restaurant != None
        assert restaurant.name == "R"
        assert restaurant.price == 1000

    def test_get_reviews(self):
        """
            Returns a collection of all the reviews for the `Restaurant`
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

        restaurant1 = session.query(Restaurant).first()
        restaurant2 = session.query(Restaurant).all()[1]

        assert len(restaurant1.get_reviews()) == 2
        assert len(restaurant2.get_reviews()) == 2

        clear_db(session)

    def test_get_customers(self):
        """
            Test returns a collection of all the customers who reviewed the `Restaurant`
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

        customer = session.query(Customer).first()
        customer2 = session.query(Customer).all()[1]

        assert len(restaurant1.get_reviews()) == 2
        assert len(restaurant2.get_customers()) == 2

        clear_db(session)

    @pytest.mark.skip(reason="class session issue")
    def test_fanciest(cls):
        """
            Test returns _one_ restaurant instance for the restaurant that has the highestprice
        """
        engine = create_engine(SQLITE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        clear_db(session)

        restaurant1 = Restaurant(name="R1", price=1000)
        restaurant2 = Restaurant(name="R2", price=2000)
        restaurant3 = Restaurant(name="R3", price=3000)
        restaurant4 = Restaurant(name="R4", price=4000)
        session.bulk_save_objects([restaurant1, restaurant2, restaurant3, restaurant4])

        session.commit()

        restaurant = Restaurant.fanciest()

        assert restaurant.name == "R4"
        assert restaurant.price == 4000

        clear_db(session)

    def test_all_reviews(self):
        """
            Test should return an list of strings with all the reviews for this restaurant
            formatted as follows:
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
        session.add(restaurant1)

        session.commit()

        restaurant1 = session.query(Restaurant).first()

        review1c1 = Review(star_rating=5, customer_id=customer.id, restaurant_id=restaurant1.id)
        review2c1 = Review(star_rating=8, customer_id=customer.id, restaurant_id=restaurant1.id)

        session.bulk_save_objects([review1c1, review2c1])
        session.commit()

        restaurant1 = session.query(Restaurant).first()

        assert restaurant1.all_reviews() == [
            "Review for R1 by John Doe: 5 stars.",
            "Review for R1 by John Doe: 8 stars."
        ]

        clear_db(session)









