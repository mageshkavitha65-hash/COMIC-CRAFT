import { useState } from "react";
import "./App.css";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState("");

  const API_KEY = import.meta.env.VITE_API_KEY;

  const searchWeather = async () => {
    if (!city) return;

    try {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${city}&units=metric&appid=${API_KEY}`
      );

      const data = await response.json();

      if (data.cod !== 200) {
        setError("City not found");
        setWeather(null);
        return;
      }

      setWeather(data);
      setError("");

    } catch {
      setError("Something went wrong");
    }
  };

  return (
    <div className="app">

      <h1>🌤️ Weather App</h1>

      <div>
        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <button onClick={searchWeather}>
          Search
        </button>
      </div>


      {error && <p>{error}</p>}


      {weather && (
        <div className="weather-card">
          <h2>{weather.name}</h2>

          <h1>
            {weather.main.temp}°C
          </h1>

          <p>
            {weather.weather[0].description}
          </p>

          <p>
            💧 Humidity: {weather.main.humidity}%
          </p>

          <p>
            💨 Wind: {weather.wind.speed} km/h
          </p>

        </div>
      )}

    </div>
  );
}

export default App;