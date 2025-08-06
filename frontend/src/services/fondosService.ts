import axios from 'axios';
import { defaultHeaders } from '@/utils/headers';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

console.log("API_URL (compilado):", API_URL);

export const suscribirseAFondo = async (
  userId: string, 
  data: { 
    id_fondo: number; 
    medio_notificacion: string;
    usuario_contacto: string;
  }) => {
  const response = await axios.post(`${API_URL}/fondos/suscribirse`, data, defaultHeaders(userId));
  return response.data;
};

export const usuarioSaldo = async (userId: string) => {
  const response = await axios.get(`${API_URL}/fondos/saldo`, defaultHeaders(userId));
  return response.data;
};

export const cancelarFondo = async (
  userId: string,
  data: { 
    id_fondo: number;
    medio_notificacion: string;
    usuario_contacto: string;
  }
) => {
  const response = await axios.post(`${API_URL}/fondos/cancelar`, data, defaultHeaders(userId));
  return response.data;
};

export const obtenerHistorial = async (userId: string) => {
  const response = await axios.get(`${API_URL}/fondos/historial`, defaultHeaders(userId));
  return response.data;
};
