'use client';

import { useFormContext, useWatch } from 'react-hook-form';
import { TransactionFormData } from '@/schemas/transaction.schema';

export default function NotificacionFields() {
  const {
    register,
    formState: { errors },
    control,
  } = useFormContext<TransactionFormData>();

  const medio = useWatch({ control, name: 'medio_notificacion' });

  const label = medio === 'sms' ? 'Número de teléfono (formato internacional)' : 'Correo electrónico';
  const placeholder = medio === 'sms' ? '+573001234567' : 'ejemplo@correo.com';
  const inputType = medio === 'sms' ? 'tel' : 'email';

  return (
    <div className="flex flex-col space-y-1">
      <label htmlFor="usuario_contacto" className="text-sm font-medium text-gray-700">
        {label}
      </label>

      <input
        id="usuario_contacto"
        type={inputType}
        placeholder={placeholder}
        {...register('usuario_contacto')}
        className={`px-4 py-2 border rounded-md text-sm outline-none focus:ring-2 transition-all ${
          errors.usuario_contacto ? 'border-red-500 focus:ring-red-300' : 'border-gray-300 focus:ring-blue-300'
        }`}
      />

      {errors.usuario_contacto && (
        <span className="text-sm text-red-500">
          {errors.usuario_contacto.message}
        </span>
      )}
    </div>
  );
}
