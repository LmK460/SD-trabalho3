from concurrent.futures import thread
from threading import Thread
from measurer import Measurer

tempSensor = Measurer('temp', 20, 40, 5)
lightSensor = Measurer('light', 10, 30, 5)
humSensor = Measurer('hum', 50, 80, 7)

threadTemp = Thread(target=tempSensor.start)
threadLight = Thread(target=lightSensor.start)
threadHum = Thread(target=humSensor.start)

threadTemp.start()
threadLight.start()
threadHum.start()