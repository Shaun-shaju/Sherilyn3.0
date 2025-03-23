import streamlit as st
import requests

# OpenWeatherMap API Key (Replace with your own API Key)
API_KEY = st.secrets['weather']['apikey']
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

st.subheader("🌦️ Weather Forecast App")

cities = [
    "Abidjan", "Abu Dhabi", "Abuja", "Accra", "Addis Ababa", "Ahmedabad", "Aleppo", "Alexandria", "Algiers", 
    "Almaty", "Amman", "Amsterdam", "Anchorage", "Andorra la Vella", "Ankara", "Antananarivo", "Apia", "Arnold", 
    "Ashgabat", "Asmara", "Asuncion", "Athens", "Auckland", "Avarua", "Baghdad", "Baku", "Bamako", "Banda Aceh", 
    "Bandar Seri Begawan", "Bandung", "Bangkok", "Bangui", "Banjul", "Barcelona", "Barranquilla", "Basrah", 
    "Basse-Terre", "Basseterre", "Beijing", "Beirut", "Bekasi", "Belem", "Belgrade", "Belmopan", "Belo Horizonte", 
    "Bengaluru", "Berlin", "Bern", "Bishkek", "Bissau", "Bogota", "Brasilia", "Bratislava", "Brazzaville", 
    "Bridgetown", "Brisbane", "Brussels", "Bucharest", "Budapest", "Buenos Aires", "Bujumbura", "Bursa", "Busan", 
    "Cairo", "Cali", "Caloocan", "Camayenne", "Canberra", "Cape Town", "Caracas", "Casablanca", "Castries", 
    "Cayenne", "Charlotte Amalie", "Chengdu", "Chennai", "Chicago", "Chisinau", "Chittagong", "Chongqing", "Colombo", 
    "Conakry", "Copenhagen", "Cordoba", "Curitiba", "Daegu", "Daejeon", "Dakar", "Dallas", "Damascus", 
    "Dar es Salaam", "Delhi", "Denver", "Dhaka", "Dili", "Djibouti", "Dodoma", "Doha", "Dongguan", "Douala", 
    "Douglas", "Dubai", "Dublin", "Durban", "Dushanbe", "Faisalabad", "Fort-de-France", "Fortaleza", "Freetown", 
    "Fukuoka", "Funafuti", "Gaborone", "George Town", "Georgetown", "Gibraltar", "Gitega", "Giza", "Guadalajara", 
    "Guangzhou", "Guatemala City", "Guayaquil", "Gujranwala", "Gustavia", "Gwangju", "Hamburg", "Hanoi", "Harare", 
    "Havana", "Helsinki", "Ho Chi Minh City", "Hong Kong", "Honiara", "Honolulu", "Houston", "Hyderabad", 
    "Ibadan", "Incheon", "Isfahan", "Islamabad", "Istanbul", "Izmir", "Jaipur", "Jakarta", "Jeddah", "Jerusalem", 
    "Johannesburg", "Juarez", "Juba", "Kabul", "Kaduna", "Kampala", "Kano", "Kanpur", "Kaohsiung", "Karachi", 
    "Karaj", "Kathmandu", "Kawasaki", "Kharkiv", "Khartoum", "Khulna", "Kigali", "Kingsburg", "Kingston", 
    "Kingstown", "Kinshasa", "Kobe", "Kolkata", "Kota Bharu", "Kowloon", "Kuala Lumpur", "Kumasi", "Kuwait", 
    "Kyiv", "Kyoto", "La Paz", "Lagos", "Lahore", "Libreville", "Lilongwe", "Lima", "Lisbon", "Ljubljana", "Lome", 
    "London", "Los Angeles", "Luanda", "Lubumbashi", "Lusaka", "Luxembourg", "Macau", "Madrid", "Majuro", "Makassar", 
    "Malabo", "Male", "Mamoudzou", "Managua", "Manama", "Manaus", "Manila", "Maputo", "Maracaibo", "Maracay", 
    "Mariehamn", "Marigot", "Maseru", "Mashhad", "Mbabane", "Mecca", "Medan", "Medellin", "Medina", "Melbourne", 
    "Mexico City", "Miami", "Minsk", "Mogadishu", "Monaco", "Monrovia", "Montevideo", "Montreal", "Moroni", 
    "Moscow", "Mosul", "Multan", "Mumbai", "Muscat", "N'Djamena", "Nagoya", "Nairobi", "Nanchong", "Nanjing", 
    "Nassau", "Nay Pyi Taw", "New York", "Niamey", "Nicosia", "Nouakchott", "Noumea", "Novosibirsk", "Nuku'alofa", 
    "Nur-Sultan", "Nuuk", "Oranjestad", "Osaka", "Oslo", "Ottawa", "Ouagadougou", "Pago Pago", "Palembang", 
    "Palo Alto", "Panama", "Papeete", "Paramaribo", "Paris", "Perth", "Philadelphia", "Phnom Penh", "Phoenix", 
    "Podgorica", "Port Louis", "Port Moresby", "Port of Spain", "Port-Vila", "Port-au-Prince", "Porto Alegre", 
    "Porto-Novo", "Prague", "Praia", "Pretoria", "Pristina", "Puebla", "Pune", "Pyongyang", "Quezon City", "Quito", 
    "Rabat", "Rawalpindi", "Recife", "Reykjavik", "Riga", "Rio de Janeiro", "Riyadh", "Road Town", "Rome", "Roseau", 
    "Saint George's", "Saint Helier", "Saint John's", "Saint Peter Port", "Saint Petersburg", "Saint-Denis", 
    "Saint-Pierre", "Saipan", "Salvador", "San Antonio", "San Diego", "San Francisco", "San Jose", "San Juan", 
    "San Marino", "San Salvador", "Sanaa", "Santa Cruz de la Sierra", "Santiago", "Santo Domingo", "Sao Paulo", 
    "Sao Tome", "Sapporo", "Sarajevo", "Seattle", "Semarang", "Seoul", "Shanghai", "Sharjah", "Shenzhen", 
    "Singapore", "Skopje", "Sofia", "South Tangerang", "Soweto", "Stockholm", "Sucre", "Surabaya", "Surat", "Suva", 
    "Sydney", "Tabriz", "Taipei", "Tallinn", "Tangerang", "Tarawa", "Tashkent", "Tbilisi", "Tegucigalpa", "Tehran", 
    "Tel Aviv", "Thimphu", "Tianjin", "Tijuana", "Tirana", "Tokyo", "Toronto", "Torshavn", "Tripoli", "Tunis", 
    "Ulan Bator", "Vaduz", "Valencia", "Valletta", "Vancouver", "Victoria", "Vienna", "Vientiane", "Vilnius", 
    "Warsaw", "Washington", "Wellington", "Willemstad", "Windhoek", "Wuhan", "Xi'an", "Yamoussoukro", "Yangon", 
    "Yaounde", "Yekaterinburg", "Yerevan", "Yokohama", "Zagreb"
]

if "user_data" in st.session_state:
    # User Input
    city = st.selectbox("Enter city name", cities)
    city_bac = st.text_input("Enter city name (if your city is not included in the list)")
    if st.button("Get Weather"):
        if city or city_bac:
            if city_bac:
                params = {"q": city_bac, "appid": API_KEY, "units": "metric"}
                response = requests.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    weather = data["weather"][0]["description"].capitalize()
                    temp = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]
                    st.success(f"🌍 Weather in {city_bac}")
                    st.write(f"**🌤 Condition:** {weather}")
                    st.write(f"**🌡 Temperature:** {temp}°C")
                    st.write(f"**💧 Humidity:** {humidity}%")
                    st.write(f"**💨 Wind Speed:** {wind_speed} m/s")
            elif city:
                params = {"q": city, "appid": API_KEY, "units": "metric"}
                response = requests.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    weather = data["weather"][0]["description"].capitalize()
                    temp = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    wind_speed = data["wind"]["speed"]
                    st.success(f"🌍 Weather in {city}")
                    st.write(f"**🌤 Condition:** {weather}")
                    st.write(f"**🌡 Temperature:** {temp}°C")
                    st.write(f"**💧 Humidity:** {humidity}%")
                    st.write(f"**💨 Wind Speed:** {wind_speed} m/s")
            else:
                st.error("⚠️ City not found! Please enter a valid city name.")

    st.sidebar.info("Select or Enter your city name and click 'Get Weather' to see the forecast!")
else:
    st.error("You need to authenticate first. Please login or sign up.")