import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { FaSort, FaSortUp, FaSortDown, FaPlus, FaEdit, FaTrash, FaSearch } from 'react-icons/fa';
import './MySQLTableViewer.css';

function MySQLTableViewer() {
  // Состояния для данных
  const [databases, setDatabases] = useState([]);
  const [selectedDB, setSelectedDB] = useState('');
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [tableData, setTableData] = useState([]);
  const [columns, setColumns] = useState([]);
  const [schema, setSchema] = useState([]);
  const [primaryKey, setPrimaryKey] = useState('id');
  
  // Состояния для UI
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');
  
  // Состояния для сортировки
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  
  // Состояния для поиска
  const [searchQuery, setSearchQuery] = useState('');
  
  // Состояния для редактирования
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [currentRecord, setCurrentRecord] = useState({});
  const [newRecord, setNewRecord] = useState({});

  const API_BASE_URL = 'http://localhost:5000/api';

  // Проверка статуса сервера при загрузке
  useEffect(() => {
    checkServerStatus();
    fetchDatabases();
  }, []);

  // Получение списка таблиц при выборе базы данных
  useEffect(() => {
    if (selectedDB) {
      fetchTables(selectedDB);
    } else {
      setTables([]);
      setSelectedTable('');
      setTableData([]);
      setColumns([]);
    }
  }, [selectedDB]);

  // Получение данных таблицы при выборе таблицы
  useEffect(() => {
    if (selectedDB && selectedTable) {
      fetchTableData(selectedDB, selectedTable);
      fetchTableSchema(selectedDB, selectedTable);
    } else {
      setTableData([]);
      setColumns([]);
      setSchema([]);
    }
  }, [selectedDB, selectedTable]);

  // Отфильтрованные и отсортированные данные
  const filteredAndSortedData = useMemo(() => {
    // Фильтрация по поисковому запросу
    let filteredData = tableData;
    if (searchQuery.trim() !== '') {
      const lowercaseQuery = searchQuery.toLowerCase();
      filteredData = tableData.filter(row => 
        Object.values(row).some(value => 
          value !== null && value.toString().toLowerCase().includes(lowercaseQuery)
        )
      );
    }

    // Сортировка по выбранному столбцу
    if (sortColumn) {
      return [...filteredData].sort((a, b) => {
        const valA = a[sortColumn];
        const valB = b[sortColumn];
        
        // Обработка null значений
        if (valA === null && valB === null) return 0;
        if (valA === null) return sortDirection === 'asc' ? 1 : -1;
        if (valB === null) return sortDirection === 'asc' ? -1 : 1;
        
        // Числовое сравнение
        if (!isNaN(valA) && !isNaN(valB)) {
          return sortDirection === 'asc' 
            ? Number(valA) - Number(valB) 
            : Number(valB) - Number(valA);
        }
        
        // Строковое сравнение
        return sortDirection === 'asc'
          ? String(valA).localeCompare(String(valB))
          : String(valB).localeCompare(String(valA));
      });
    }
    
    return filteredData;
  }, [tableData, searchQuery, sortColumn, sortDirection]);

  // Проверка статуса сервера
  const checkServerStatus = async () => {
    try {
      setStatusMessage('Проверка соединения с сервером...');
      const response = await axios.get(`${API_BASE_URL}/status`);
      if (response.data.status === 'ok') {
        setStatusMessage('Соединение с сервером установлено');
        setTimeout(() => setStatusMessage(''), 3000);
      } else {
        setStatusMessage('Проблема с подключением к серверу');
      }
    } catch (err) {
      setStatusMessage('Ошибка подключения к серверу API');
      console.error('Ошибка при проверке статуса сервера:', err);
    }
  };

  // Получение списка баз данных
  const fetchDatabases = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/databases`);
      setDatabases(response.data.databases || []);
    } catch (err) {
      console.error('Ошибка при получении баз данных:', err);
      setError('Ошибка при получении списка баз данных');
      setDatabases([]);
    } finally {
      setLoading(false);
    }
  };

  // Получение списка таблиц
  const fetchTables = async (database) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/tables`, {
        params: { database }
      });
      setTables(response.data.tables || []);
    } catch (err) {
      console.error('Ошибка при получении таблиц:', err);
      setError(`Ошибка при получении списка таблиц для базы данных ${database}`);
      setTables([]);
    } finally {
      setLoading(false);
    }
  };

  // Получение данных таблицы
  const fetchTableData = async (database, table) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/tables/${table}/data`, {
        params: { database }
      });
      setTableData(response.data.data || []);
      setColumns(response.data.columns || []);
    } catch (err) {
      console.error('Ошибка при получении данных таблицы:', err);
      setError(`Ошибка при получении данных таблицы ${table}`);
      setTableData([]);
      setColumns([]);
    } finally {
      setLoading(false);
    }
  };

  // Получение схемы таблицы
  const fetchTableSchema = async (database, table) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tables/${table}/schema-details`, {
        params: { database }
      });
      setSchema(response.data.schema || []);
      
      // Находим первичный ключ
      const primaryKeyColumn = response.data.schema.find(col => col.isPrimary);
      if (primaryKeyColumn) {
        setPrimaryKey(primaryKeyColumn.field);
      } else {
        setPrimaryKey('id'); // Значение по умолчанию
      }
    } catch (err) {
      console.error('Ошибка при получении схемы таблицы:', err);
    }
  };

  // Обработка сортировки
  const handleSort = (column) => {
    if (sortColumn === column) {
      // Если колонка та же, меняем направление
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // Если новая колонка, сортируем по возрастанию
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  // Обработчик добавления записи
  const handleAddRecord = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post(`${API_BASE_URL}/tables/${selectedTable}/add`, {
        database: selectedDB,
        record: newRecord
      });
      
      if (response.data.success) {
        setStatusMessage('Запись успешно добавлена');
        // Перезагружаем данные таблицы
        fetchTableData(selectedDB, selectedTable);
        // Закрываем форму и очищаем данные новой записи
        setShowAddForm(false);
        setNewRecord({});
      }
    } catch (err) {
      console.error('Ошибка при добавлении записи:', err);
      setError(`Ошибка при добавлении записи: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Обработчик обновления записи
  const handleUpdateRecord = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const recordId = currentRecord[primaryKey];
      
      const response = await axios.put(`${API_BASE_URL}/tables/${selectedTable}/update/${recordId}`, {
        database: selectedDB,
        record: currentRecord,
        id_column: primaryKey
      });
      
      if (response.data.success) {
        setStatusMessage('Запись успешно обновлена');
        // Перезагружаем данные таблицы
        fetchTableData(selectedDB, selectedTable);
        // Закрываем форму редактирования
        setShowEditForm(false);
        setCurrentRecord({});
      }
    } catch (err) {
      console.error('Ошибка при обновлении записи:', err);
      setError(`Ошибка при обновлении записи: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Обработчик удаления записи
  const handleDeleteRecord = async (record) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту запись?')) {
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const recordId = record[primaryKey];
      
      const response = await axios.delete(`${API_BASE_URL}/tables/${selectedTable}/delete/${recordId}`, {
        params: {
          database: selectedDB,
          id_column: primaryKey
        }
      });
      
      if (response.data.success) {
        setStatusMessage('Запись успешно удалена');
        // Перезагружаем данные таблицы
        fetchTableData(selectedDB, selectedTable);
      }
    } catch (err) {
      console.error('Ошибка при удалении записи:', err);
      setError(`Ошибка при удалении записи: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Открытие формы редактирования записи
  const openEditForm = (record) => {
    setCurrentRecord({...record});
    setShowEditForm(true);
    setShowAddForm(false);
  };

  // Открытие формы добавления записи
  const openAddForm = () => {
    // Создаем шаблон новой записи на основе схемы таблицы
    const recordTemplate = {};
    schema.forEach(col => {
      if (!col.isAutoIncrement) {
        recordTemplate[col.field] = null;
      }
    });
    
    setNewRecord(recordTemplate);
    setShowAddForm(true);
    setShowEditForm(false);
  };

  // Обработчики выбора базы данных и таблицы
  const handleDatabaseChange = (e) => {
    setSelectedDB(e.target.value);
    setSelectedTable('');
    // Сбрасываем состояние сортировки и поиска
    setSortColumn(null);
    setSortDirection('asc');
    setSearchQuery('');
  };

  const handleTableChange = (e) => {
    setSelectedTable(e.target.value);
    // Сбрасываем состояние сортировки и поиска
    setSortColumn(null);
    setSortDirection('asc');
    setSearchQuery('');
  };

  return (
    <div className="mysql-viewer">
      <header className="viewer-header">
        <h1>MySQL Table Viewer</h1>
      </header>
      
      {statusMessage && (
        <div className="status-message">
          {statusMessage}
        </div>
      )}
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      
      <div className="controls">
        <div className="control-group">
          <label>База данных:</label>
          <select
            value={selectedDB}
            onChange={handleDatabaseChange}
            disabled={loading}
          >
            <option value="">-- Выберите базу данных --</option>
            {databases.map((db) => (
              <option key={db} value={db}>{db}</option>
            ))}
          </select>
        </div>
        
        {selectedDB && (
          <div className="control-group">
            <label>Таблица:</label>
            <select
              value={selectedTable}
              onChange={handleTableChange}
              disabled={loading}
            >
              <option value="">-- Выберите таблицу --</option>
              {tables.map((table) => (
                <option key={table} value={table}>{table}</option>
              ))}
            </select>
          </div>
        )}
      </div>
      
      {selectedTable && (
        <div className="table-actions">
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder="Поиск..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <button className="add-button" onClick={openAddForm}>
            <FaPlus /> Добавить запись
          </button>
        </div>
      )}
      
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Загрузка данных...</p>
        </div>
      )}
      
      {/* Форма добавления записи */}
      {showAddForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>Добавить запись</h2>
            
            <div className="form-fields">
              {schema
                .filter(col => !col.isAutoIncrement) // Исключаем автоинкрементные поля
                .map(col => (
                  <div className="form-field" key={col.field}>
                    <label>{col.field}</label>
                    <input
                      type={col.type.includes('int') ? "number" : 
                            col.type.includes('date') ? "date" : 
                            "text"}
                      value={newRecord[col.field] || ''}
                      onChange={(e) => setNewRecord({
                        ...newRecord,
                        [col.field]: e.target.value === '' ? null : e.target.value
                      })}
                      placeholder={`${col.type} ${col.null === 'YES' ? '(необязательно)' : '(обязательно)'}`}
                    />
                    <span className="field-type">{col.type}</span>
                  </div>
                ))
              }
            </div>
            
            <div className="form-actions">
              <button onClick={handleAddRecord} disabled={loading}>Добавить</button>
              <button onClick={() => setShowAddForm(false)} className="cancel-button">Отмена</button>
            </div>
          </div>
        </div>
      )}
      
      {/* Форма редактирования записи */}
      {showEditForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>Редактировать запись</h2>
            
            <div className="form-fields">
              {schema.map(col => (
                <div className="form-field" key={col.field}>
                  <label>{col.field}</label>
                  <input
                    type={col.type.includes('int') ? "number" : 
                          col.type.includes('date') ? "date" : 
                          "text"}
                    value={currentRecord[col.field] || ''}
                    onChange={(e) => setCurrentRecord({
                      ...currentRecord,
                      [col.field]: e.target.value === '' ? null : e.target.value
                    })}
                    disabled={col.isPrimary && col.isAutoIncrement} // Блокируем первичный ключ с автоинкрементом
                    placeholder={col.type}
                  />
                  <span className="field-type">{col.type}</span>
                </div>
              ))}
            </div>
            
            <div className="form-actions">
              <button onClick={handleUpdateRecord} disabled={loading}>Сохранить</button>
              <button onClick={() => setShowEditForm(false)} className="cancel-button">Отмена</button>
            </div>
          </div>
        </div>
      )}
      
      {selectedTable && filteredAndSortedData.length > 0 && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th className="action-column">Действия</th>
                {columns.map((column) => (
                  <th 
                    key={column}
                    onClick={() => handleSort(column)}
                    className={sortColumn === column ? 'sorted' : ''}
                  >
                    {column}
                    {sortColumn === column ? (
                      sortDirection === 'asc' ? <FaSortUp /> : <FaSortDown />
                    ) : <FaSort />}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredAndSortedData.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  <td className="action-column">
                    <button className="edit-button" onClick={() => openEditForm(row)}>
                      <FaEdit />
                    </button>
                    <button className="delete-button" onClick={() => handleDeleteRecord(row)}>
                      <FaTrash />
                    </button>
                  </td>
                  {columns.map((column) => (
                    <td key={`${rowIndex}-${column}`}>
                      {row[column] !== null ? String(row[column]) : <span className="null-value">NULL</span>}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {selectedTable && filteredAndSortedData.length === 0 && !loading && (
        <div className="empty-table">
          {searchQuery ? 
            'По вашему запросу ничего не найдено' : 
            'Таблица не содержит данных'
          }
        </div>
      )}
    </div>
  );
}

export default MySQLTableViewer;