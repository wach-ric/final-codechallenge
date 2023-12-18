#!/usr/bin/env python3

import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, Restaurant, Review

def generate_fake_data(fake, num_records):
    return [fake() for _ in range(num_records)]

if __name__ == '__main__':
    # Initialize Faker and create an SQLite database session
    fake = Faker()
    engine = create_engine('sqlite:///restaurant.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Create tables
        Base.metadata.create_all(engine)

        # Clear existing data
        session.query(Customer).delete()
        session.query(Restaurant).delete()
        session.query(Review).delete()
        session.commit()

        # Rest of your code to generate and seed data

        print("Data seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
