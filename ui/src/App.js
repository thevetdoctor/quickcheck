import React from 'react';
import News from './components/News';
// import bg from './photo-1605007493699-af65834f8a00.jpg';

function App() {
  const baseUrl = 'http://localhost:5000';

  return (
        <div className="p-5 text-center bg-gradient-to-r from-cyan-500 to-blue-700 h-full bg-cover">
          <h2 style={{fontFamily: 'Architects Daughter'}} className="text-3xl font-bold my-3 text-white">
            QuickCheck
          </h2>
          <News baseUrl={baseUrl} />
        </div>
  );
}

export default App;
