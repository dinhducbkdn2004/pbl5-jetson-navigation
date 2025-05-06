"""
GPS service module for handling GPS communication and location tracking
"""

import serial
import pynmea2
import time
from src.config.settings import GPS_PORT, BAUD_RATE

class GPSService:
    def __init__(self, port=GPS_PORT, baud_rate=BAUD_RATE):
        self.port = port
        self.baud_rate = baud_rate
        self.gps_serial = None
        
    def connect(self):
        """Connect to the GPS device"""
        try:
            self.gps_serial = serial.Serial(self.port, self.baud_rate, timeout=1)
            return True
        except Exception as e:
            print(f"GPS connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the GPS device"""
        if self.gps_serial and self.gps_serial.is_open:
            self.gps_serial.close()
    
    def get_location(self):
        """
        Get current GPS location (latitude, longitude)
        Returns a tuple of (latitude, longitude) or (None, None) if not available
        """
        if not self.gps_serial or not self.gps_serial.is_open:
            self.connect()
            
        if not self.gps_serial:
            return None, None
            
        while True:
            try:
                line = self.gps_serial.readline().decode("utf-8", errors="ignore").strip()
                if line.startswith("$GPGGA") or line.startswith("$GPRMC"):
                    msg = pynmea2.parse(line)
                    return msg.latitude, msg.longitude
            except pynmea2.ParseError:
                pass
            except Exception as e:
                print(f"GPS error: {e}")
            time.sleep(1)
            
    def wait_for_valid_location(self):
        """Wait until we get a valid GPS position"""
        print("🛰️ Getting GPS position...")
        lat, lng = None, None
        while not lat or not lng:
            lat, lng = self.get_location()
            if not lat or not lng:
                print("Cannot get GPS, retrying in 1 second...")
                time.sleep(1)
        print(f"📍 Current position: Latitude: {lat}, Longitude: {lng}")
        return lat, lng