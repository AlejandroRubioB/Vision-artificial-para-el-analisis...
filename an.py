#open calle111-46.txt file and read all the lines get the fist value of each line and save it in a list
archivo = open("calle1-13-19.txt","r")
lista = archivo.readlines()

lista3 = []
for line in lista:
    lista3.append(line.split(",")[0])
#valuef is the result of the addition of all the values in the list3
valuef = 0
for i in lista3:
    valuef = valuef + int(i)
archivo.close()
#repeat the same proces with calle2-13-02.txt
archivo2 = open("calle2-13-18.txt","r")
lista2 = archivo2.readlines()
lista4 = []
for line in lista2:
    lista4.append(line.split(",")[0])
valuef2 = 0
for i in lista4:
    valuef2 = valuef2 + int(i)
archivo2.close()
#compare the values of the two final values and print wich one is bigger
if valuef > valuef2:
    print("callle 1 tiene mas autos")
elif valuef < valuef2:
    print("callle 2 tuvo mas carros")
print (lista)
print(lista3)
print(lista4)
print(valuef)
print(valuef2)