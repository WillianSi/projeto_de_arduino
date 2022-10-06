#Importa a biblioteca
import serial
import mysql.connector
from mysql.connector import errorcode
import datetime

# Loop para a conexão com o Arduino, se conseguir, o loop se encerra
while True:
    try:
        arduino = serial.Serial('COM3', 9600)
        print('Serial Iniciada...\n')
        break
    except:
        print('Serial não conectada!\n')
        pass

 # Tenta se conectar ao banco de dados
try:
    db_connection = mysql.connector.connect(host='localhost', user='root', password='2bF83Jz@7', database='umidadearduino')
    print("Banco de Dados Conectado!\n")
except mysql.connector.Error as error:
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Banco de Dados Nao existe")
    elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Seu Nome ou Senha Esta Errado")
    else:
        print(error)

cursor = db_connection.cursor()

# Loop principal
while True:  
    umidade = str(arduino.readline())  # Lê os dados em formato de string
    umidade = umidade[2:-5]  # Fatia a string
    agora = datetime.datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M") 
    print('Umidade: ' + umidade + ' Data: ' + data + ' Hora: ' + hora)  # Imprime a saida
    add_umidade = "INSERT INTO umidade_arduino (umidade_umi, data_umi, hora_umi) VALUES ('"+umidade+"','"+data+"','"+hora+"')" #INSERT no banco
    cursor.execute(add_umidade) #INSERT no banco
    db_connection.commit() #INSERT no banco
    arduino.flush()  # Limpa a comunicação

cursor.close()
db_connection.close()
arduino.close()
