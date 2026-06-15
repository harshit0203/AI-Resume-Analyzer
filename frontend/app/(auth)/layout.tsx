import Link from "next/link";
import { Logo } from "@/components/logo";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Brand panel */}
      <div className="relative hidden overflow-hidden lg:block">
        <div className="mesh-bg animate-aurora absolute inset-0" />
        <div className="grid-pattern absolute inset-0 opacity-30" />
        <div className="relative flex h-full flex-col justify-between p-12">
          <Link href="/">
            <Logo />
          </Link>
          <div>
            <h2 className="text-balance text-3xl font-semibold leading-tight">
              Land your next role with <span className="text-gradient">AI on your side.</span>
            </h2>
            <p className="mt-4 max-w-md text-muted-foreground">
              Six specialized agents analyze your resume, score ATS compatibility, match jobs and
              map your career path — in seconds.
            </p>
          </div>
          <p className="text-sm text-muted-foreground">
            Trusted by job seekers targeting top-tier product & AI companies.
          </p>
        </div>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-sm">{children}</div>
      </div>
    </div>
  );
}
