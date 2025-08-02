'use client';

import CancelarForm from '@/components/organisms/CancelarForm';

export default function CancelarPage() {
  return (
    <section className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-4 text-red-600">Cancelar Suscripción</h2>
      <p className="mb-6 text-gray-600">
        Selecciona el fondo del que deseas cancelar tu suscripción. El valor invertido se reintegrará a tu saldo disponible.
      </p>
      <CancelarForm />
    </section>
  );
}
