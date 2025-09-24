import React from 'react';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Democratiza AI',
  description: 'Plataforma para análise e gestão de contratos',
};

const RootLayout = ({ children }) => {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
};

export default RootLayout;