import { z } from 'zod';

export const suscripcionSchema = z.object({
  id_fondo: z.number({
    error: (issue) => issue.input === undefined ? "Selecciona un fondo" : "Selecciona al menos un fondo"
  }),
  medio_notificacion: z.enum(['email', 'sms'], {
    error: 'Selecciona un medio de notificación válido',
  }),
});

export type SuscripcionFormData = z.infer<typeof suscripcionSchema>;