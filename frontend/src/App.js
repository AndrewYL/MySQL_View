import React, { useState } from 'react';
import MySQLTableViewer from './components/MySQLTableViewer';

function App() {
  const [selectedView, setSelectedView] = useState('tables');

  return (
    <div className="App min-h-screen bg-gray-100">
      <div className="container mx-auto p-4">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-center text-gray-800">
            MySQL Database Viewer
          </h1>
        </header>

        <nav className="mb-4 flex justify-center space-x-4">
          <button
            className={`px-4 py-2 rounded ${
              selectedView === 'tables' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`}
            onClick={() => setSelectedView('tables')}
          >
            Таблицы
          </button>
          <button
            className={`px-4 py-2 rounded ${
              selectedView === 'relations' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-800'
            }`}
            onClick={() => setSelectedView('relations')}
          >
            Связи между таблицами
          </button>
        </nav>

        <main className="bg-white shadow-md rounded-lg p-6">
          {selectedView === 'tables' && <MySQLTableViewer />}
          {selectedView === 'relations' && (
            <div>
              {/* Здесь может быть компонент для отображения связей между таблицами */}
              <p>Связи между таблицами будут показаны здесь</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;