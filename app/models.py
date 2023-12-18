from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from connect import Session, session

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer(), primary_key=True)
    first_name =  Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    reviews = relationship("Review", backref=backref('customer'))
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def full_name(self):
        """
            Returns the full name of the customer, with the first name 
            and the last name  concatenated, Western style.
        """
        return f"{self.first_name} {self.last_name}"

    def get_reviews(self):
        """
            Renamed to 'get_reviews' to avoid name conflict
            insteady of 'reviews'

            Should return a collection of all the reviews that the `Customer` has left
        """
        return self.reviews
    
    def get_restaurants(self):
        """
            Renamed to 'get_restaurants' to avoid name conflict
            insteady of 'restaurants'

            should return a collection of all the restaurants that the `Customer` has 
            reviewed
        """
        return self.restaurants
    
    def favorite_restaurant(self):
        """
            Returns the restaurant instance that has the highest star rating from this customer
        """
        review = max(self.get_reviews(), key=lambda a: a.star_rating)
        return review.get_restaurant()
    
    def add_review(self, restaurant, rating):
        """
            Takes a `restaurant` (an instance of the `Restaurant` class) and a rating and
            creates a new review for the restaurant with the given `restaurant_id`
        """
        review = Review(
            customer_id=self.id,
            restaurant_id=restaurant.id,
            star_rating=rating)
        
        session = Session.object_session(self)
        session.add(review)
        session.commit()

    def delete_reviews(self, restaurant):
        """
            Takes a `restaurant` (an instance of the `Restaurant` class) and
            removes **all** their reviews for this restaurant you will have to delete rows 
            from the `reviews` table to get this to work!
        """
        session = Session.object_session(self)
        delete_q = Review.__table__.delete().where(Review.customer_id==self.id).where(Review.restaurant_id==restaurant.id)
        # reviews = session.query(Review).filter_by(customer_id=self.id, restaurant_id=restaurant.id)[0]
        session.execute(delete_q)
        session.commit()

    def __repr__(self):
        return f"<Customer first_name={self.first_name} last_name={self.last_name}>"
    


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    price = Column(Integer(), nullable=False)
    reviews = relationship("Review", backref=backref('restaurant'))
    customers = relationship("Customer", secondary="reviews", back_populates="restaurants")

    def get_reviews(self):
        """
            Renamed to 'get_reviews' to avoid name conflict
            insteady of 'reviews'

            Returns a collection of all the reviews for the `Restaurant`
        """
        return self.reviews
    
    def get_customers(self):
        """
            Renamed to 'get_customers' to avoid name conflict
            insteady of 'customers'

            Returns a collection of all the customers who reviewed the `Restaurant`
        """
        return self.customers
    
    def all_reviews(self):
        """
            Should return an list of strings with all the reviews for this restaurant
            formatted as follows:
        """
        reviews = [review.full_review() for review in self.get_reviews()]
        return reviews
    
    @classmethod
    def fanciest(cls):
        """
            Returns _one_ restaurant instance for the restaurant that has the highest   price
        """
        restaurant = session.query(cls).order_by(desc(cls.price)).first()
        return restaurant
    

    def __repr__(self):
        return f"<Restaurant name={self.name} price={self.price}>"
    

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer(), primary_key=True)
    star_rating = Column(Integer(), nullable=False)
    customer_id = Column(Integer(), ForeignKey('customers.id'), nullable=False)
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'), nullable=False)
    
    def get_customer(self):
        """
            Renamed to 'get_customer' to avoid name conflict
            insteady of 'customer'

            Should return the `Customer` instance for this review
        """
        return self.customer # from relationship in Customer class
    
    def get_restaurant(self):
        """
            Renamed to 'get_restaurant' to avoid name conflict
            insteady of 'restaurant'

            Should return the `Restaurant` instance for this review
        """
        return self.restaurant # from relationship in Restaurant class
    
    def full_review(self):
        """
            Should return a string formatted as follows: Review for 
            {insert restaurant name} by {insert customer's full name}: 
            {insert review star_rating} stars.
        """
        return f"Review for {self.get_restaurant().name} by {self.get_customer().full_name()}: {str(self.star_rating)} stars."

    
    def __repr__(self):
        return f"<Review star_rating={self.star_rating}>"
    

