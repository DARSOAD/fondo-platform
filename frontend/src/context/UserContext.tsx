'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { usuarioSaldo } from '@/services/fondosService';

type UserContextType = {
  userId: string;
  saldo: number | null;
  actualizarSaldo: () => Promise<void>; // función para refrescar saldo
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const userId = 'user-001'; // simulando el único ID de usuario
  const [saldo, setSaldo] = useState<number | null>(null);

  const actualizarSaldo = async () => {
    try {
      const data = await usuarioSaldo(userId);
      setSaldo(data.saldo); // asumiendo que backend devuelve { saldo: number }
    } catch (error) {
      console.error('Error al obtener saldo:', error);
    }
  };

  useEffect(() => {
    actualizarSaldo();
  }, []);

  return (
    <UserContext.Provider value={{ userId, saldo, actualizarSaldo }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error('useUser debe usarse dentro de <UserProvider>');
  return context;
};
