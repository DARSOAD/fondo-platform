//# frontend/src/schemas/transaction.schema.ts
import { z } from 'zod';

export const transactionSchema = z.object({
  id_fondo: z.number({
    error: (issue) => issue.input === undefined ? "Selecciona un fondo" : "Selecciona al menos un fondo"
  }),
  medio_notificacion: z.enum(['email', 'sms'], {
    error: 'Selecciona un medio de notificación válido',
  }),
  usuario_contacto: z.string().min(1, "Ingresa un contacto"),
}).superRefine((data, ctx) => {
  if (data.medio_notificacion === "email") {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.usuario_contacto)) {
      ctx.addIssue({
        path: ['usuario_contacto'],
        code: "custom", // ✅ corregido
        message: 'Ingresa un email válido',
      });
    }
  }

  if (data.medio_notificacion === "sms") {
    const phoneRegex = /^\+\d{10,15}$/;
    if (!phoneRegex.test(data.usuario_contacto)) {
      ctx.addIssue({
        path: ['usuario_contacto'],
        code: "custom", // ✅ corregido
        message: 'El número debe estar en formato internacional (ej: +573001234567)',
      });
    }
  }
});

export type TransactionFormData = z.infer<typeof transactionSchema>;