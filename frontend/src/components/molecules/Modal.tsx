'use client';

import { ReactNode } from 'react';
import Button from '@/components/atoms/Button';

type ModalProps = {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
};

export default function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 max-w-md w-full shadow-xl relative">
        {title && <h2 className="text-xl font-bold mb-4">{title}</h2>}
        <div className="text-gray-800">{children}</div>

        <div className="mt-6 text-right">
          <Button
            onClick={onClose}
            label="Cerrar"
          />
        </div>
      </div>
    </div>
  );
}
