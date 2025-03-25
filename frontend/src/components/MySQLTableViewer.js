import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MySQLTableViewer = () => {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState(null);
  const [tableData, setTableData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;

  useEffect(() => {
    axios.get('http://localhost:5000/tables')
      .then(response => setTables(response.data))
      .catch(error => console.error('Ошибка загрузки таблиц:', error));
  }, []);

  const fetchTableData = (tableName) => {
    setLoading(true);
    axios.get(`http://localhost:5000/table/${tableName}`)
      .then(response => {
        setSelectedTable(tableName);
        setTableData(response.data.data);
        setColumns(response.data.columns);
        setCurrentPage(1);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка загрузки данных таблицы:', error);
        setLoading(false);
      });
  };

  // Постраничная навигация
  const indexOfLastRow = currentPage * rowsPerPage;
  const indexOfFirstRow = indexOfLastRow - rowsPerPage;
  const currentRows = tableData.slice(indexOfFirstRow, indexOfLastRow);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="mysql-table-viewer" style={{
      fontFamily: 'Arial, sans-serif',
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px'
    }}>
      <div style={{display: 'flex'}}>
        {/* Боковое меню таблиц */}
        <div style={{
          width: '200px',
          borderRight: '1px solid #ddd',
          paddingRight: '20px',
          marginRight: '20px'
        }}>
          <h2>Таблицы</h2>
          {tables.map(table => (
            <button
              key={table}
              onClick={() => fetchTableData(table)}
              style={{
                display: 'block',
                width: '100%',
                padding: '10px',
                margin: '5px 0',
                backgroundColor: selectedTable === table ? '#e0e0e0' : 'white',
                border: '1px solid #ddd',
                cursor: 'pointer'
              }}
            >
              {table}
            </button>
          ))}
        </div>

        {/* Область данных таблицы */}
        <div style={{flex: 1}}>
          {selectedTable && (
            <div>
              <h1>{selectedTable}</h1>

              {loading ? (
                <p>Загрузка...</p>
              ) : (
                <>
                  <table style={{
                    width: '100%',
                    borderCollapse: 'collapse',
                    marginBottom: '20px'
                  }}>
                    <thead>
                      <tr style={{backgroundColor: '#f2f2f2'}}>
                        {columns.map(column => (
                          <th key={column} style={{
                            border: '1px solid #ddd',
                            padding: '8px',
                            textAlign: 'left'
                          }}>
                            {column}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {currentRows.map((row, index) => (
                        <tr key={index} style={{borderBottom: '1px solid #ddd'}}>
                          {columns.map(column => (
                            <td key={column} style={{
                              border: '1px solid #ddd',
                              padding: '8px'
                            }}>
                              {row[column] !== null ? String(row[column]) : 'NULL'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  {/* Постраничная навигация */}
                  <div style={{display: 'flex', justifyContent: 'center'}}>
                    {Array.from({
                      length: Math.ceil(tableData.length / rowsPerPage)
                    }).map((_, index) => (
                      <button
                        key={index}
                        onClick={() => paginate(index + 1)}
                        style={{
                          margin: '0 5px',
                          padding: '5px 10px',
                          backgroundColor: currentPage === index + 1 ? '#007bff' : 'white',
                          color: currentPage === index + 1 ? 'white' : 'black',
                          border: '1px solid #ddd'
                        }}
                      >
                        {index + 1}
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MySQLTableViewer;