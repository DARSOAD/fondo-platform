'use client';

import { useEffect, useState } from 'react';
import { useUser } from '@/context/UserContext';
import { obtenerHistorial } from '@/services/fondosService';
import Modal from '@/components/molecules/Modal';
import axios from 'axios';

type Transaccion = {
  id: string;
  tipo: 'apertura' | 'cancelacion';
  fondo_id: number;
  fondo_nombre: string;
  valor: number;
  medio: string;
  timestamp: string;
  categoria: string;
};

export default function HistorialTransacciones() {
  const { userId } = useUser();
  const [transacciones, setTransacciones] = useState<Transaccion[]>([]);
  const [modalAbierto, setModalAbierto] = useState(false);
  const [modalTitulo, setModalTitulo] = useState('');
  const [modalMensaje, setModalMensaje] = useState('');

  useEffect(() => {
    const fetchHistorial = async () => {
      try {
        const data = await obtenerHistorial(userId);
        setTransacciones(data);
      } catch (error) {
        if (axios.isAxiosError(error)) {
          const status = error.response?.status;

          if (status === 400 || status === 404) {
            setModalTitulo('Sin Transacciones');
            setModalMensaje(error.response?.data?.detail || 'Aún no has realizado ninguna transacción.');
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

    fetchHistorial();
  }, [userId]);

  return (
    <>
      <div className="space-y-4">
        {transacciones.map((tx) => (
          <div key={tx.id} className="p-4 border rounded shadow-sm bg-white">
            <p><strong>Fondo:</strong> {tx.fondo_nombre}</p>
            <p><strong>Tipo:</strong> {tx.tipo === 'apertura' ? 'Suscripción' : 'Cancelación'}</p>
            <p><strong>Valor:</strong> COP ${tx.valor.toLocaleString('es-CO')}</p>
            <p><strong>Categoría:</strong> {tx.categoria}</p>
            <p><strong>Fecha:</strong> {new Date(tx.timestamp).toLocaleString('es-CO')}</p>
          </div>
        ))}
      </div>

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
