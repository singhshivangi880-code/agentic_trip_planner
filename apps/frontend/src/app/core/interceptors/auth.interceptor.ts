import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Mock Auth Token for Development (matches backend MockAuthProvider)
  const clone = req.clone({
    setHeaders: {
      Authorization: `Bearer dev-token`
    }
  });
  return next(clone);
};
