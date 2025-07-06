import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import StudentCard from '../components/StudentCard';
import { Student, SearchResponse } from '../types/thesis';
import { studentApi } from '../services/api';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [graduationYears, setGraduationYears] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [recentStudents, setRecentStudents] = useState<Student[]>([]);

  useEffect(() => {
    // Load graduation years and recent students on component mount
    const loadInitialData = async () => {
      try {
        const [years, students] = await Promise.all([
          studentApi.getGraduationYears(),
          studentApi.getStudents(0, 6) // Get 6 most recent students
        ]);
        setGraduationYears(years);
        setRecentStudents(students);
      } catch (error) {
        console.error('Failed to load initial data:', error);
      }
    };

    loadInitialData();
  }, []);

  const handleSearch = async (query: string, year?: number) => {
    if (!query.trim() && !year) {
      setSearchResults(null);
      return;
    }

    setLoading(true);
    try {
      const results = await studentApi.searchStudents(query, year, 1, 20);
      setSearchResults(results);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults({
        students: [],
        total: 0,
        page: 1,
        per_page: 20,
        total_pages: 0,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleStudentClick = (studentId: number) => {
    navigate(`/student/${studentId}`);
  };

  const handleYearClick = (year: number) => {
    navigate(`/year/${year}`);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center mb-4">
            <h1 className="text-4xl font-bold text-blue-900 mb-2">Московский государственный университет</h1>
            <h2 className="text-2xl font-semibold text-blue-700 mb-3">Кафедра математической статистики и случайных процессов</h2>
            <h3 className="text-3xl font-bold text-gray-900">База данных дипломных работ</h3>
          </div>
          <p className="text-gray-600 mt-2 text-center">
            Поиск и изучение дипломных работ студентов кафедры математической статистики
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Section */}
        <div className="mb-8">
          <SearchBar
            onSearch={handleSearch}
            graduationYears={graduationYears}
            loading={loading}
          />
        </div>

        {/* Search Results */}
        {searchResults && (
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold text-gray-900">Результаты поиска</h2>
              <span className="text-gray-600">
                Найдено {searchResults.total} {searchResults.total === 1 ? 'результат' : searchResults.total < 5 ? 'результата' : 'результатов'}
              </span>
            </div>
            
            {searchResults.students.length > 0 ? (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {searchResults.students.map((student) => (
                  <StudentCard
                    key={student.id}
                    student={student}
                    onClick={() => handleStudentClick(student.id)}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500">Не найдено студентов, соответствующих критериям поиска.</p>
              </div>
            )}
          </div>
        )}

        {/* Recent Students (shown when no search results) */}
        {!searchResults && recentStudents.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Последние добавления</h2>
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {recentStudents.map((student) => (
                <StudentCard
                  key={student.id}
                  student={student}
                  onClick={() => handleStudentClick(student.id)}
                />
              ))}
            </div>
          </div>
        )}

        {/* Browse by Year */}
        {graduationYears.length > 0 && (
          <div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Просмотр по году выпуска</h2>
            <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
              {graduationYears.map((year) => (
                <button
                  key={year}
                  onClick={() => handleYearClick(year)}
                  className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg hover:bg-blue-50 transition-all duration-200 text-center"
                >
                  <div className="text-2xl font-bold text-blue-600">{year}</div>
                  <div className="text-sm text-gray-600">Посмотреть дипломные работы</div>
                </button>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default HomePage;