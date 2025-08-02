'use client';

import Link from 'next/link';
import { useUser } from '@/context/UserContext';

export default function FondosLayout({ children }: { children: React.ReactNode }) {
  const { saldo } = useUser();

  return (
    <section className="min-h-screen bg-gray-50 text-gray-900">
      <header className="bg-white shadow-md px-4 py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-2">
        <Link href="/" className="text-blue-600 font-bold">
          <h1 className="text-xl font-semibold">Gestión de Fondos</h1>
        </Link>

        <nav className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 gap-1 sm:gap-0">
          <Link href="/fondos/suscribirse" className="text-green-600 hover:underline">
            Suscribirse
          </Link>
          <Link href="/fondos/cancelar" className="text-red-600 hover:underline">
            Cancelar
          </Link>
          <Link href="/fondos/historial" className="text-gray-700 hover:underline">
            Historial
          </Link>
          <span className="text-blue-700 font-medium sm:ml-4">
            Saldo: {saldo !== null ? `COP $${saldo.toLocaleString('es-CO')}` : '...'}
          </span>
        </nav>
      </header>

      <main className="p-6">{children}</main>
    </section>
  );
}
