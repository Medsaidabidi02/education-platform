import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EduPlatform - Modern Learning Experience",
  description: "A cutting-edge education platform with modern UI/UX design",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
