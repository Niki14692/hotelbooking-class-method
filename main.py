import pandas

df = pandas.read_csv("hotels.csv", dtype={'id': str})
df_card = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pandas.read_csv("card_security.csv", dtype=str)

class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """hotel is available so book ticket and availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

class SpaHotel(Hotel):
    def book_spa_package(self):
        pass

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank You for your reservation!
        Here your booking details:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "cvc": cvc, "holder": holder}
        if card_data in df_card:
            return True
        else:
            return False

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank You for your SPA reservation!
        Here your booking details:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content
print(df)
hotel_Id = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_Id)

if hotel.available():
    Number= input("Enter your card number: ")
    credit_card = SecureCreditCard(number=Number)
    Expiration = input("Enter your expiration date: ")
    name_holder = input("Enter card holder name: ")
    CVC = input("Enter your 3 digit cvc number: ")
    if credit_card.validate(expiration=Expiration, holder=name_holder, cvc=CVC):
        type_password = input("Enter your security password: ")
        if credit_card.authenticate(given_password=type_password):
            hotel.book()
            name = input("Please enter your name: ")
            reservation = ReservationTicket(customer_name=name, hotel_object=hotel )
            print(reservation.generate())
            spa_book = input("Do you want to book spa package? ")
            if spa_book == "yes":
                hotel.book_spa_package()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())

        else:
            print("Your password is wrong")
    else:
        print("please try again.card details is wrong.")
else:
    print("Hotel is not free.")