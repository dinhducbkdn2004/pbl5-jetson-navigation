"""
Main module for Jetson Navigation application
"""
from src.services.gps import GPSService
from src.services.api import APIService
from src.speech.voice import VoiceService
from src.navigation.navigator import Navigator
from src.config.settings import MAX_REROUTE_ATTEMPTS

def main():
    print("Starting Jetson Navigation System...")
    
    # Initialize services
    gps_service = GPSService()
    voice_service = VoiceService()
    api_service = APIService()
    
    # Initialize navigator
    navigator = Navigator(gps_service, voice_service, api_service)
    
    # Get destination from user
    destination = navigator.get_destination_from_user()
    
    # Get initial GPS position
    initial_lat, initial_lng = gps_service.wait_for_valid_location()
    
    # Navigation loop
    reroute_attempts = 0
    
    while reroute_attempts < MAX_REROUTE_ATTEMPTS:
        print(f"🗺️ Đang yêu cầu lộ trình từ API (Lần {reroute_attempts + 1})...")
        response_data = navigator.request_route(initial_lat, initial_lng, destination)
        
        if response_data and 'steps' in response_data and response_data['steps']:
            steps = response_data['steps']
            
            # Reset reroute counter when we get a valid route
            reroute_attempts = 0
            
            # Follow the route
            success, new_lat, new_lng = navigator.follow_route(steps, initial_lat, initial_lng)
            
            # If navigation completed successfully
            if success:
                break
                
            # If we need to reroute
            if new_lat and new_lng:
                initial_lat, initial_lng = new_lat, new_lng
                reroute_attempts += 1
                continue
        
        else:
            print("❌ Không nhận được lộ trình hoặc lộ trình rỗng từ API.")
            reroute_attempts += 1
            
            if response_data:
                error_message = response_data.get('error', 'Không thể lấy lộ trình.')
                print(f"Lỗi API: {error_message}")
                voice_service.speak(f"Lỗi: {error_message}. Thử lại.")
            else:
                voice_service.speak("Không thể kết nối hoặc nhận dữ liệu từ máy chủ dẫn đường. Thử lại.")
            
            if reroute_attempts >= MAX_REROUTE_ATTEMPTS:
                print("❌ Đã thử tìm lại đường quá nhiều lần. Dừng chương trình.")
                voice_service.speak("Không thể tìm được đường đi sau nhiều lần thử.")
                break
    
    print("Kết thúc chương trình.")

if __name__ == "__main__":
    main()