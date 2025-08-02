'use client';

import HistorialTransacciones from '@/components/organisms/HistorialTransacciones';

export default function HistorialPage() {
  return (
    <section className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Historial de Transacciones</h2>
      <p className="mb-6 text-gray-600">Aquí puedes ver todas tus suscripciones y cancelaciones realizadas.</p>
      <HistorialTransacciones />
    </section>
  );
}
