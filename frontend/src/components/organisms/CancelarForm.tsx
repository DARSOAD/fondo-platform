'use client';

import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useUser } from '@/context/UserContext';
import { cancelarFondo } from '@/services/fondosService';
import { fondos } from '@/utils/fondosList';
import { useState } from 'react';

import Select from '@/components/atoms/Select';
import Button from '@/components/atoms/Button';
import Modal from '@/components/molecules/Modal';
import NotificacionFields from '@/components/molecules/NotificacionFields';
import axios from 'axios';

import { transactionSchema, TransactionFormData } from '@/schemas/transaction.schema';

export default function CancelarForm() {
  const { userId, actualizarSaldo } = useUser();
  const [modalAbierto, setModalAbierto] = useState(false);
  const [modalTitulo, setModalTitulo] = useState('');
  const [modalMensaje, setModalMensaje] = useState('');

  const methods = useForm<TransactionFormData>({
    resolver: zodResolver(transactionSchema),
  });

  const onSubmit = async (data: TransactionFormData) => {
    try {
      const result = await cancelarFondo(userId, data);
      await actualizarSaldo();
      setModalTitulo('Cancelación Exitosa');
      setModalMensaje('Te has desvinculado correctamente del fondo.');
      setModalAbierto(true);
      console.log(result);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const status = error.response?.status;

        if (status === 400 || status === 404) {
          setModalTitulo('No Suscrito');
          setModalMensaje(error.response?.data?.detail || 'No estás inscrito en este fondo.');
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
            placeholder="Selecciona el fondo a cancelar"
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

          <Button
            type="submit"
            label="Cancelar Suscripción"
            className="bg-red-600 hover:bg-red-700"
          />
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
