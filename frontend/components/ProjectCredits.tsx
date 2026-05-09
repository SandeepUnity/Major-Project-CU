export function ProjectCredits() {
  return (
    <footer className="mt-auto border-t border-[var(--border)] bg-white/60 py-6 text-xs text-zinc-600 dark:bg-zinc-950/30 dark:text-zinc-400">
      <div className="container-app grid gap-4 sm:grid-cols-2 sm:gap-8">
        <div className="space-y-1">
          <p>
            <span className="font-medium text-zinc-800 dark:text-zinc-200">Student Name:</span> Sandeep
          </p>
          <p>
            <span className="font-medium text-zinc-800 dark:text-zinc-200">Enrolment No:</span>{" "}
            O24MSD110183
          </p>
        </div>
        <div className="space-y-1 sm:text-right">
          <p className="text-[var(--muted)]">Under the guidance of</p>
          <p>
            <span className="font-medium text-zinc-800 dark:text-zinc-200">Guide/Mentor Name:</span>{" "}
            Ms. Roshini Ganesh
          </p>
        </div>
      </div>
    </footer>
  );
}
