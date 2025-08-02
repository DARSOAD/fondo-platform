'use client';

import { ButtonHTMLAttributes } from 'react';

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  label: string;
};

export default function Button({ label, className = '', ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded ${className}`}
    >
      {label}
    </button>
  );
}
