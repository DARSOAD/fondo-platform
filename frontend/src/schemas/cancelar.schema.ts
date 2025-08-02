import { z } from 'zod';

export const cancelarSchema = z.object({
  id_fondo: z.number({
    error: (issue) => issue.input === undefined ? "Selecciona un fondo" : "Selecciona al menos un fondo"
  })
});

export type CancelarFormData = z.infer<typeof cancelarSchema>;