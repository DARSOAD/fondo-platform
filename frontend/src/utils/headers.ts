export const defaultHeaders = (userId: string) => ({
    headers: {
      'Content-Type': 'application/json',
      'x-user-id': userId,
    },
  });