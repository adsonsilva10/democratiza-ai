import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, ...props }) => {
  return (
    <div className="flex flex-col">
      {label && <label className="mb-1 text-sm font-medium">{label}</label>}
      <input
        className={`p-2 border rounded-md ${error ? 'border-red-500' : 'border-gray-300'}`}
        {...props}
      />
      {error && <span className="mt-1 text-sm text-red-500">{error}</span>}
    </div>
  );
};

export default Input;