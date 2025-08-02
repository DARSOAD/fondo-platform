import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center py-10 px-4">
      <h1 className="text-4xl font-bold mb-6 text-center">Plataforma de Gestión de Fondos</h1>
      <p className="mb-8 text-lg text-center text-gray-600 max-w-md">
        Administra tus suscripciones, cancelaciones e historial de transacciones de forma sencilla.
      </p>

      <div className="flex flex-col md:flex-row gap-4">
        <Link
          href="/fondos/suscribirse"
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded text-center"
        >
          Suscribirse a un Fondo
        </Link>

        <Link
          href="/fondos/cancelar"
          className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded text-center"
        >
          Cancelar Suscripción
        </Link>

        <Link
          href="/fondos/historial"
          className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded text-center"
        >
          Ver Historial
        </Link>
      </div>
    </main>
  );
}
