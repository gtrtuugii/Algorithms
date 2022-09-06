

class Supplier:
    def __init__(self, city, contact_firstname, contact_lastname, contact_title, email, notes, phone, postcode, state, street_address):
        self.city = city
        self.contact_firstname = contact_firstname
        self.contact_lastname = contact_lastname
        self.contact_title = contact_title
        self.email = email
        self.notes = notes
        self.phone = phone
        self.postcode = postcode
        self.state = state
        self.street_address = street_address
    
    def getCity(self):
        return self.city
    
    def getContactFirstName(self):
        return self.contact_firstname
    
    def getContactLastName(self):
        return self.contact_lastname
    
    def getContactTitle(self):
        return self.contact_title

    def getEmail(self):
        return self.email

    def getNotes(self):
        return self.notes

    def getPhone(self):
        return self.phone

    def getPostCode(self):
        return self.postcode
    
    def getState(self):
        return self.state

    def getStreetAddress(self):
        return self.street_address

    def setPhone(self, phone_num):
        self.phone = phone_num

supp = Supplier("Perth", "John", "Doe", "Mr", "johndoe@abc.com", "", "9999", "6100", "WA", "Waterloo St")
supp.setPhone("(03) 9961-55555")
print(supp.getPhone())

