'use client';

import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { transactionSchema, TransactionFormData } from '@/schemas/transaction.schema';
import { suscribirseAFondo } from '@/services/fondosService';
import { fondos } from '@/utils/fondosList';
import { useUser } from '@/context/UserContext';
import { useState } from 'react';
import NotificacionFields from '@/components/molecules/NotificacionFields';

import Modal from '@/components/molecules/Modal';
import Select from '@/components/atoms/Select';
import Button from '@/components/atoms/Button';
import axios from 'axios';

export default function SuscripcionForm() {
  const { userId, actualizarSaldo } = useUser();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [modalMensaje, setModalMensaje] = useState('');
  const [modalTitulo, setModalTitulo] = useState('');

  const methods = useForm<TransactionFormData>({
    resolver: zodResolver(transactionSchema),
  });

  const onSubmit = async (data: TransactionFormData) => {
    try {
      const result = await suscribirseAFondo(userId, data);
      await actualizarSaldo();
      setModalTitulo('Suscripción Exitosa');
      setModalMensaje('Te has suscrito correctamente al fondo.');
      setModalAbierto(true);
      console.log(result);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const status = error.response?.status;

        if (status === 400) {
          setModalTitulo('Error de solicitud');
          setModalMensaje(error.response?.data?.detail || 'Solicitud no válida.');
        } else {
          setModalTitulo('Error inesperado');
          setModalMensaje('Ocurrió un error inesperado. Intenta nuevamente más tarde.');
        }

        setModalAbierto(true);
        console.warn('Solicitud rechazada con status', status);
      } else {
        console.error('Error desconocido', error);
      }
    }
  };

  return (
    <>
      <FormProvider {...methods}>
        <form onSubmit={methods.handleSubmit(onSubmit)} className="space-y-4">
          <Select
            {...methods.register('id_fondo', { valueAsNumber: true })}
            options={fondos.map((f) => ({
              value: f.id,
              label: `${f.nombre} (Desde COP $${f.valor_minimo.toLocaleString('es-CO')})`,
            }))}
            placeholder="Selecciona un fondo"
            error={methods.formState.errors.id_fondo?.message}
          />

          <Select
            {...methods.register('medio_notificacion')}
            options={[
              { value: 'email', label: 'Email' },
              { value: 'sms', label: 'SMS' },
            ]}
            placeholder="Seleccione el medio de notificación"
            error={methods.formState.errors.medio_notificacion?.message}
          />

          <NotificacionFields />

          <Button type="submit" label="Suscribirse" />
        </form>
      </FormProvider>

      <Modal
        isOpen={modalAbierto}
        onClose={() => setModalAbierto(false)}
        title={modalTitulo}
      >
        <p>{modalMensaje}</p>
      </Modal>
    </>
  );
}
