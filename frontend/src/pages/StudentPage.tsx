import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CodeExecutor from '../components/CodeExecutor';
import { Student, ExecutionResult } from '../types/thesis';
import { studentApi } from '../services/api';

const StudentPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [student, setStudent] = useState<Student | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStudent = async () => {
      if (!id) {
        setError('Student ID not provided');
        setLoading(false);
        return;
      }

      try {
        const studentData = await studentApi.getStudent(parseInt(id));
        setStudent(studentData);
      } catch (error) {
        console.error('Failed to load student:', error);
        setError('Failed to load student information');
      } finally {
        setLoading(false);
      }
    };

    loadStudent();
  }, [id]);

  const handleExecuteCode = async (args?: string): Promise<ExecutionResult> => {
    if (!student) {
      throw new Error('Student not loaded');
    }

    return await studentApi.executeCode(student.id, { args });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Загрузка информации о студенте...</p>
        </div>
      </div>
    );
  }

  if (error || !student) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Студент не найден</h1>
          <p className="text-gray-600 mb-4">{error || 'Запрашиваемый студент не найден.'}</p>
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
                ← Вернуться к поиску
              </button>
              <h1 className="text-3xl font-bold text-gray-900">{student.name}</h1>
              <p className="text-gray-600 mt-1">Выпуск {student.graduation_year} года</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid gap-8 lg:grid-cols-3">
          {/* Student Information */}
          <div className="lg:col-span-2 space-y-6">
            {/* Thesis Information */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">Информация о дипломной работе</h2>
              
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-2">Название</h3>
                  <p className="text-gray-700">{student.thesis_title}</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-medium text-gray-800 mb-2">Аннотация</h3>
                  <p className="text-gray-700 leading-relaxed">{student.thesis_summary}</p>
                </div>
              </div>
            </div>

            {/* Code Execution */}
            {student.python_code && (
              <CodeExecutor
                code={student.python_code}
                onExecute={handleExecuteCode}
              />
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Student Details */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Детали</h3>
              
              <div className="space-y-3">
                <div>
                  <span className="text-sm font-medium text-gray-500">Имя студента</span>
                  <p className="text-gray-900">{student.name}</p>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-gray-500">Год выпуска</span>
                  <p className="text-gray-900">{student.graduation_year}</p>
                </div>
                
                <div>
                  <span className="text-sm font-medium text-gray-500">Добавлено в базу</span>
                  <p className="text-gray-900">
                    {new Date(student.created_at).toLocaleDateString('ru-RU')}
                  </p>
                </div>
                
                {student.python_code && (
                  <div>
                    <span className="text-sm font-medium text-gray-500">Интерактивный код</span>
                    <p className="text-green-600 font-medium">Доступен</p>
                  </div>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Действия</h3>
              
              <div className="space-y-3">
                <button
                  onClick={() => navigate(`/year/${student.graduation_year}`)}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Посмотреть выпуск {student.graduation_year} года
                </button>
                
                <button
                  onClick={() => navigate('/')}
                  className="w-full border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Искать другие дипломные работы
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default StudentPage;