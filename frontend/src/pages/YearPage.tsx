import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import StudentCard from '../components/StudentCard';
import { Student } from '../types/thesis';
import { studentApi } from '../services/api';

const YearPage: React.FC = () => {
  const { year } = useParams<{ year: string }>();
  const navigate = useNavigate();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStudents = async () => {
      if (!year) {
        setError('Year not provided');
        setLoading(false);
        return;
      }

      try {
        const studentsData = await studentApi.getStudentsByYear(parseInt(year));
        setStudents(studentsData);
      } catch (error) {
        console.error('Failed to load students:', error);
        setError('Failed to load students for this year');
      } finally {
        setLoading(false);
      }
    };

    loadStudents();
  }, [year]);

  const handleStudentClick = (studentId: string) => {
    navigate(`/student/${studentId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Загрузка студентов...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Ошибка загрузки студентов</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Вернуться на главную
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <button
                onClick={() => navigate('/')}
                className="text-blue-600 hover:text-blue-800 mb-2 flex items-center"
              >
                ← Вернуться на главную
              </button>
              <h1 className="text-3xl font-bold text-gray-900">Выпуск {year} года</h1>
              <p className="text-gray-600 mt-1">
                {students.length} {students.length === 1 ? 'дипломная работа' : students.length < 5 ? 'дипломные работы' : 'дипломных работ'} выпускников {year} года
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {students.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {students.map((student) => (
              <StudentCard
                key={student.id}
                student={student}
                onClick={() => handleStudentClick(student.id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📚</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Дипломные работы не найдены</h2>
            <p className="text-gray-600 mb-6">
              Пока не добавлено ни одной дипломной работы для выпуска {year} года.
            </p>
            <button
              onClick={() => navigate('/')}
              className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Посмотреть другие годы
            </button>
          </div>
        )}
      </main>
    </div>
  );
};

export default YearPage;