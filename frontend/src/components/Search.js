import React from 'react';

export default function Search ({firstDay, setFirstDay, lastDay, setLastDay, onSearch }){
    return (
      <div>
        <input type="month" onChange={(e) => setFirstDay(e.target.value)} />first_day
        <input type="month" onChange={(e) => setLastDay(e.target.value)} />last_day
        <button onClick={() => onSearch(firstDay, lastDay)}>Search</button>
      </div>
    );
  };
