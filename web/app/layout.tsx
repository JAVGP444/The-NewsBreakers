import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The NewsBreakers — Verificador de salud animal",
  description: "Consultoría para verificar información sobre brotes y enfermedades animales.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
