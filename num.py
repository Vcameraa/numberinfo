import phonenumbers
print("\033[1;32;40m illuminati world secret socitey num info tool \n")
print("\033[1;32;40m  \n")
number = input("enter your number:::")
print("\033[1;32;40m you enter a number \n")
print(number)
print("\033[1;32;40m \n")
print("this number detail is")
from phonenumbers import geocoder
ch_nmber = phonenumbers.parse(number, "CH")
print(geocoder.description_for_number(ch_nmber, "en"))
from phonenumbers import carrier
service_nmber = phonenumbers.parse(number, "RO")
print(carrier.name_for_number(service_nmber, "en"))

