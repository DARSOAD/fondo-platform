'use client';

import SuscripcionForm from '@/components/organisms/SuscripcionForm';

export default function SuscribirsePage() {
  return (
    <section className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-4 text-blue-700">Suscribirse a un Fondo</h2>
      <p className="mb-6 text-gray-600">
        Selecciona el fondo al que deseas suscribirte e indica el medio de notificación.
      </p>
      <SuscripcionForm />
    </section>
  );
}
