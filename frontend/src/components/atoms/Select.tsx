'use client';

import { SelectHTMLAttributes } from 'react';

type Option = {
  label: string;
  value: string | number;
};

type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  options: Option[];
  error?: string;
  placeholder?: string;
};

export default function Select({ options, error, placeholder, ...props }: SelectProps) {
  return (
    <div className="w-full">
      <select
        {...props}
        className="w-full border rounded px-3 py-2"
        defaultValue=""
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="text-red-600 text-sm mt-1">{error}</p>}
    </div>
  );
}
