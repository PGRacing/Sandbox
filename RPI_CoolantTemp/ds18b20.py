from w1thermsensor import W1ThermSensor, Sensor
from w1thermsensor.calibration_data import CalibrationData
from time import sleep, time
from threading import Thread

reference_low_point = 20.5
reference_high_point = 100.0

calibration_data = {
"0302977909b4" :  CalibrationData(
        measured_high_point=98.25,
        measured_low_point= 21.25,
        reference_high_point=reference_high_point,
        reference_low_point=reference_low_point,
    ),
"03029779503b" :  CalibrationData(
        measured_high_point=98.75,
        measured_low_point= 20.75,
        reference_high_point=reference_high_point,
        reference_low_point=reference_low_point, 
    ),
"03219779a7df":  CalibrationData(
        measured_high_point=97.75,
        measured_low_point= 20.25,
        reference_high_point=reference_high_point,
        reference_low_point=reference_low_point, 
    ),
"03049779e810":  CalibrationData(
        measured_high_point=99.25,
        measured_low_point= 20.5,
        reference_high_point=reference_high_point,
        reference_low_point=reference_low_point, 
    ), 
"030197794548":  CalibrationData(
        measured_high_point=99.75,
        measured_low_point=20.5,
        reference_high_point=reference_high_point,
        reference_low_point=reference_low_point, 
    ),
"030297790ae7":  CalibrationData(
        measured_high_point=100.25,
        measured_low_point=21.0,
        reference_high_point=reference_high_point,
        reference_low_point=reference_low_point, 
    ) }

class DS18B20(Thread):
	sensors = []
	temperatures = {}
	
	def __init__(self):
		super().__init__()
		self.sensors = []
		for sensor in W1ThermSensor.get_available_sensors():
			#self.sensors.append(W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensor.id))
			self.sensors.append(W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensor.id, calibration_data=calibration_data[sensor.id]))
			self.sensors[-1].set_resolution(10)
		print(self.sensors)
					
			
	def run(self):	
		counter = 0
		#if len(self.sensors) != 6:
		#	self.__init__()
		while True:
			for sensor in self.sensors:
				try:
					self.temperatures[sensor.id] = sensor.get_corrected_temperature()
					counter = 0				
				except:
					counter = counter + 1
					if counter == 10:
						exit()
			
