import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MedAdReview - 의료광고 AI 심의 시스템",
  description: "AI 기반 의료광고 자동 심의 시스템",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
