from suds.client import Client
c = Client('http://localhost:8000/?wsdl')
print(c.service.say_hello('punk', 5))