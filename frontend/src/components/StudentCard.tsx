import React from 'react';
import { Student } from '../types/thesis';

interface StudentCardProps {
  student: Student;
  onClick?: (id: string) => void;
}

const StudentCard: React.FC<StudentCardProps> = ({ student, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(student.id);
    }
  };

  // Use new structure with fallback to legacy
  const title = student.thesis?.title || student.thesis_title || '';
  const summary = student.thesis?.summary || student.thesis_summary || '';
  const hasCode = student.code?.has_code || !!student.python_code;
  
  const formattedDate = new Date(student.added_date || student.created_at || '').toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div
      className={`bg-white p-6 rounded-lg shadow-md border border-gray-200 ${
        onClick ? 'cursor-pointer hover:shadow-lg hover:border-blue-300 transition-all duration-200' : ''
      }`}
      onClick={handleClick}
    >
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-semibold text-gray-900">{student.name}</h3>
        <span className="bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 rounded">
          {student.graduation_year}
        </span>
      </div>
      
      <h4 className="text-lg font-medium text-gray-800 mb-3">{title}</h4>
      
      <p className="text-gray-600 text-sm leading-relaxed mb-4 line-clamp-3">
        {summary}
      </p>
      
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span>
          Добавлено: {formattedDate}
        </span>
        {hasCode && (
          <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-medium">
            Есть код
          </span>
        )}
      </div>
    </div>
  );
};

export default StudentCard;