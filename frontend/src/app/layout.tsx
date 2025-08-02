import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { UserProvider } from '@/context/UserContext';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Gestión de Fondos',
  description: 'Plataforma para suscripción y cancelación de fondos de inversión',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <UserProvider>
          {children}
        </UserProvider>
      </body>
    </html>
  );
}