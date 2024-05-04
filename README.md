# weather-dashboard

This Python script generates an HTML file with weather data for a chosen city. 
It also includes an image related to the weather. 
The weather data is obtained from the IMGW (Institute of Meteorology and Water Management) public API: https://danepubliczne.imgw.pl/api/data/synop
That URLs should not include Polish characters directly. Using unidecode to convert station names with diacritics to their ASCII equivalents is indeed the correct approach.

The use of unidecode to handle Polish characters is a great solution. It ensures that station names with diacritics are properly converted to their ASCII equivalents. This way, you can avoid any issues related to character encoding. 

Data Retrieval from API:
- The script fetches (by requests package) weather data from the IMGW public API.
- It retrieves information such as temperature, wind speed, humidity, precipitation, and atmospheric pressure.

User Interaction:
- The user can select a specific weather station from the list of available stations.
- The script prompts the user to choose a station by displaying the station names.

HTML Template Rendering:
- The script uses the Jinja2 template engine to create an HTML report.
- It populates the template with the retrieved weather data for the chosen station.

Image Inclusion:
The script allows you to include an image related to the weather. You can choose any relevant image and save it in the same folder as the HTML file.

Customization:
You can customize the HTML template by modifying the template.html file. Feel free to add styling, additional information, or any other elements you’d like.
