import React, { useState, useEffect } from 'react';
import './App.css';
import DisplayMatButton from './components/DisplayMatButton';
import Board from './components/Board';
import Search from './components/Search';
import DisplayButton from './components/DisplayButton';
import SortButton from './components/SortButton';
import NextMonth from './components/NextMonth';
import { calculateForecastAverage, calculateDifferences, calculateAverageDifferences } from './function';

function App() {
  const today = new Date();
  const [firstDay, setFirstDay] = useState('2023-01');
  const [lastDay, setLastDay] = useState(`${today.getFullYear()}-${today.getMonth().toString().padStart(2, '0')}`);
  const [data, setData] = useState(null);
  const [nextMonth, setNextMonth] = useState(null);
  const [isGraph, setIsGraph] = useState(true);
  const [isDate, setIsDate] = useState(true);
  const [actualRates, setActualRates] = useState(null);
  const [forecastRates, setForecastRates] = useState(null);
  const [differences, setDifferences] = useState([]);
  const [averageDifferences, setAverageDifferences] = useState([]);
  const [resultMatrix, setResultMatrix] = useState([]);
  const [showMatrix, setShowMatrix] = useState(false); // Add showMatrix state

  const fetchData = async () => {
    try {
      const response = await fetch(`http://host.docker.internal:8000/?first_day=${firstDay}&last_day=${lastDay}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleSearch = async () => {
    fetchData();
  };

  // const sortData = async () => {
  //   const value = isDate ? 'date' : 'rate'; 
  // };

  const sortData = async () => {
    setIsDate(!isDate);
    const value = isDate ? 'date' : 'rate';
    try {
      console.log({value}); // Added log for when fetch begins
      const response = await fetch(`http://host.docker.internal:8000/sort?value=${value}`);
      console.log('Response Status:', response.status); // Log the response status
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const result = await response.json();
      console.log('sort data:', result); // Log the fetched data
      setData(result);
    } catch (error) {
      console.error('Error sort data:', error); // Log any errors
    }
  };

  const setDisplay = () => {
    setIsGraph(!isGraph);
  };

  useEffect(() => {
    if (data && data.exchange_rates && Array.isArray(data.exchange_rates)) {
      const mat = data.exchange_rates.map(entry => ({ date: entry.date, rate: entry.rate }));
      setActualRates(mat);

      const forecastData = calculateForecastAverage(data.exchange_rates);
      setForecastRates(forecastData);

      const differencesData = calculateDifferences(mat, forecastData);
      setDifferences(differencesData);
    }
  }, [data]);

  useEffect(() => {
    if (forecastRates && differences.length > 0) {
      const elementWiseProduct = forecastRates.map((row, index) => ({
        date: row.date,
        product: row.rate * differences[index].difference
      }));
      setResultMatrix(elementWiseProduct);
    }
  }, [forecastRates, differences]);

  useEffect(() => {
    fetchData(); 
  }, [firstDay, lastDay]);

  return (
    <div className="App">
      <header className="App-header">
        <Board data={data} isGraph={isGraph} isDate={isDate}/>
        <Search 
          firstDay={firstDay} 
          setFirstDay={setFirstDay} 
          lastDay={lastDay} 
          setLastDay={setLastDay} 
          onSearch={handleSearch} 
        />
        <DisplayButton onClick={setDisplay}/>
        <DisplayMatButton onClick={() => setShowMatrix(!showMatrix)} resultMatrix={resultMatrix} />
        <SortButton onClick={sortData}/>
        <NextMonth nextMonth={nextMonth}/>
      </header>
    </div>
  );
}

export default App;