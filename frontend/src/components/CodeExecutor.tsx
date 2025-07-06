import React, { useState } from 'react';
import { ExecutionResult } from '../types/thesis';

interface CodeExecutorProps {
  code: string;
  onExecute: (args?: string) => Promise<ExecutionResult>;
}

const CodeExecutor: React.FC<CodeExecutorProps> = ({ code, onExecute }) => {
  const [args, setArgs] = useState('');
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleExecute = async () => {
    setLoading(true);
    try {
      const executionResult = await onExecute(args.trim() || undefined);
      setResult(executionResult);
    } catch (error) {
      setResult({
        success: false,
        error: 'Не удалось выполнить код',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 p-6 rounded-lg">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Python код</h3>
      
      {/* Code Display */}
      <div className="bg-gray-900 text-green-400 p-4 rounded-md mb-4 overflow-x-auto">
        <pre className="text-sm font-mono whitespace-pre-wrap">{code}</pre>
      </div>

      {/* Arguments Input */}
      <div className="mb-4">
        <label htmlFor="args" className="block text-sm font-medium text-gray-700 mb-2">
          Аргументы (необязательно)
        </label>
        <input
          type="text"
          id="args"
          value={args}
          onChange={(e) => setArgs(e.target.value)}
          placeholder="Введите аргументы через запятую..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <p className="text-xs text-gray-500 mt-1">
          Пример: 1,2,3 или "привет","мир" или 10.5,20.3
        </p>
      </div>

      {/* Execute Button */}
      <button
        onClick={handleExecute}
        disabled={loading}
        className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Выполнение...' : 'Запустить код'}
      </button>

      {/* Results */}
      {result && (
        <div className="mt-4">
          <h4 className="text-md font-medium text-gray-900 mb-2">Результат:</h4>
          <div
            className={`p-4 rounded-md ${
              result.success
                ? 'bg-green-50 border border-green-200'
                : 'bg-red-50 border border-red-200'
            }`}
          >
            {result.success ? (
              <div>
                <div className="text-green-800 font-mono text-sm whitespace-pre-wrap">
                  {result.result || 'Код выполнен успешно (нет вывода)'}
                </div>
                {result.execution_time && (
                  <div className="text-green-600 text-xs mt-2">
                    Время выполнения: {result.execution_time.toFixed(3)}с
                  </div>
                )}
              </div>
            ) : (
              <div className="text-red-800 font-mono text-sm whitespace-pre-wrap">
                Ошибка: {result.error}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeExecutor;