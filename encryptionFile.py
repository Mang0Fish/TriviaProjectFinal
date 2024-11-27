from encodings.utf_8_sig import encode

from cryptography.fernet import Fernet



mes = "TRy"

key = "ex-un4oLEmt7TrN4i3iHyDXCtT_uNg8-A40MFMPSy4A="

fernet = Fernet(key)

encMes = fernet.encrypt(mes.encode())
decMes = fernet.decrypt(encMes).decode()

print(Fernet.generate_key(), str(encMes)[2:-1], type(encMes), type('gd'))


strEncMes = str(encMes)
try1 = strEncMes.encode(encoding="utf-8")
print(type(try1),try1[2:-1])
print(encMes, strEncMes)
decTry1 = fernet.decrypt((try1[2:-1]).decode())
print(str(decTry1))

password = "Trying again"
encPassword = fernet.encrypt(password)
encFinal = encPassword.decode()
decPassword = fernet.decrypt(encPassword)
print(password, encPassword, decPassword)




