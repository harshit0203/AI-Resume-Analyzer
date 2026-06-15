import { cn } from "@/lib/utils";

/**
 * Custom AIResumeAnalyzer brand mark — an abstract "A" formed by an ascending
 * bar-chart, evoking resume analysis & growth. Avoids generic stock icons.
 */
export function LogoMark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "flex size-8 items-center justify-center rounded-lg bg-[linear-gradient(135deg,var(--primary),oklch(0.66_0.2_320))]",
        className
      )}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className="size-[18px]"
        aria-hidden="true"
      >
        <rect x="3" y="14" width="3.4" height="6" rx="1.2" fill="white" fillOpacity="0.65" />
        <rect x="10.3" y="9" width="3.4" height="11" rx="1.2" fill="white" fillOpacity="0.85" />
        <rect x="17.6" y="4" width="3.4" height="16" rx="1.2" fill="white" />
        <circle cx="5.1" cy="9" r="1.6" fill="white" />
        <path
          d="M5.1 9 L12 5 L19.3 5"
          stroke="white"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          opacity="0.9"
        />
      </svg>
    </span>
  );
}

export function Logo({
  className,
  showWordmark = true,
}: {
  className?: string;
  showWordmark?: boolean;
}) {
  return (
    <span className={cn("flex items-center gap-2 font-semibold", className)}>
      <LogoMark />
      {showWordmark && <span className="text-sm sm:text-base">AIResumeAnalyzer</span>}
    </span>
  );
}
