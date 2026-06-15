import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: {
    default: "AIResumeAnalyzer | Intelligent Resume Analysis",
    template: "%s · AIResumeAnalyzer",
  },
  description:
    "Six AI agents score your resume against ATS, find skill gaps, match jobs and coach your career in seconds.",
  keywords: ["resume", "ATS", "AI", "career", "job matching", "resume analyzer"],
  openGraph: {
    title: "AIResumeAnalyzer",
    description: "Six AI agents. One resume. Instant career insights.",
    type: "website",
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000"),
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <body className="min-h-full bg-background text-foreground">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
