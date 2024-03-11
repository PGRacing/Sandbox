from ds18b20 import DS18B20
from time import sleep,strftime,localtime, time
import csv 
import os
import can

#import logging
#from systemd.journal import JournaldLogHandler


sensor_map = {"engine_out" : "03219779a7df",
"engine_in" : "03029779503b" ,
 "radiator_l_in" : "03049779e810",
"radiator_l_out":"030197794548", 
"radiator_r_in":"030297790ae7",
"radiator_r_out":"0302977909b4" }

header = ["timestamp", "engine_out", "engine_in", "radiator_l_in","radiator_l_out", "radiator_r_in","radiator_r_out"] 

file_path = "log/" + strftime("%Y_%m_%d", localtime()) + "/"
file_name = "cooling_system_temp_" + strftime("%H_%M_%S", localtime())+".csv"

#logger = logging.getLogger(__name__)
#journald_handler = JournaldLogHandler()

#journald_handler.setFormatter(logging.Formatter(
#'[%(levelname)s] %(message)s'
#))
#logger.addHandler(journald_handler)

#logger.setLevel(logging.DEBUG)


def temperatures_to_csv_row(temperatures):
	data = [time()]
	for name in header:
		if name == "timestamp":
			continue
		try:
			data.append("{t:.2f}".format(t=temperatures[sensor_map[name]]))
		except:
			data.append("-1.0")
			
	return data

def temperatures_to_can_msg(temperatures):
	data=[]
	for name in header:
		if name == "timestamp":
			continue
		try:
			data.append(int(temperatures[sensor_map[name]]*2))
		except:
			data.append(int(255))		
			
	return can.Message(arbitration_id = 0x634,
						data = data,
						is_extended_id = False)

if __name__ == "__main__":	
	d = DS18B20()
	
	os.system("sudo ifconfig can0 down")
	os.system("sudo ip link set can0 type can bitrate 1000000")
	os.system("sudo ifconfig can0 up")
	bus = can.Bus(channel="can0", bustype="socketcan")
	counter = 0
	
	if not os.path.exists(file_path):
		os.mkdir(file_path)
	
	with open(file_path + file_name, "w", encoding="UTF8", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(header)
		
		d.start()
		sleep(3)
		while True:
			#start = time()
			try:
				data = temperatures_to_csv_row(d.temperatures)
				writer.writerow(data)
				msg = temperatures_to_can_msg(d.temperatures)
				bus.send(msg)
				print(data)
				f.flush()
				counter = 0
			except:
				counter = counter + 1
				if counter == 10:
					exit()
			#sleep(1 - (time()-start))
			sleep(1.0)
	 
	exit()

