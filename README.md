# ClimaCloset

ClimaCloset is an innovative application designed to seamlessly integrate real-time weather data with your personal wardrobe, offering smart, weather-appropriate outfit suggestions. Whether it's a sunny day or a rainy evening, ClimaCloset ensures you're perfectly dressed for the occasion, making daily outfit decisions effortless and fun.

## Features

- **Real-time Weather Data**: Fetches and displays current weather conditions.
- **Wardrobe Management**: Add, edit, and delete items in your virtual wardrobe.
- **Outfit Suggestions**: Offers smart clothing recommendations based on the weather.
- **Personalized Experience**: Tailor suggestions to fit your style and wardrobe preferences.

## Installation and Setup

Follow these steps to get ClimaCloset up and running on your local machine:

1. **Prerequisites**
   
   Ensure you have Python installed on your system. This application requires Python 3.6 or newer.

2. **Clone the Repository**
   
   ```bash
   git clone https://github.com/jiejun-j/ClimaCloset.git
   cd ClimaCloset

## Installation and Setup
Follow these steps to get ClimaCloset up and running on your local machine:

1. **Prerequisites:**
Ensure you have Python installed on your system. This application requires Python 3.6 or newer.

2. **Clone the Repository:**
    ```bash
    git clone https://github.com/jiejun-j/ClimaCloset.git
    cd ClimaCloset
    ```

3. **Install required libraries:**
    ```bash
    pip install reflex requests python-dotenv
    ```

4. **Initialize the application and database:**
    ```bash
    reflex init
    reflex db init
    ```
    
5. **Setup Environment Variables:**
    - Get API key from: https://openweathermap.org/api
    - Create a `.env` file in the root directory.
    - Add your OpenWeatherMap API key to the .env file:
    ```bash
    KEY=YOUR_OPENWEATHERMAP_API_KEY
    ```
    
6. **Preview the application locally:**
    ```bash
    reflex run
    ```
    Access the web interface by navigating to the URL provided in the command line output.
   
## Roadmap for Future Development

- **Weather Forecast Visualization**: Graphical weather forecasts for better planning.
- **Automatic City Detection**: Auto-detect user location for instant weather updates.
- **Enhanced Wardrobe Display**: Visualize wardrobe items with images or icons.
- **Personalized Outfit Recommendations**: Suggest complete outfit combinations.
- **Input Validation**: Ensure robust validation for all user inputs.
- **Multi-language Support**: Broaden accessibility with additional languages.
- **Social Sharing Feature**: Share outfit choices on social platforms.
- **Retail Integration**: Directly purchase recommended items from retail partners.

## Contributing

Contributions to ClimaCloset are welcome! Whether it's feature enhancements, bug fixes, or documentation improvements, your help is greatly appreciated. Please feel free to fork the repository and submit a pull request with your changes.

