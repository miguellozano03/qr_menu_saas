import Link from "next/link";
import { Button } from "@/components/ui/button";

export function Hero() {
  return (
    <section
      id="hero"
      className="min-h-[calc(100vh-4rem)] flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16 px-6 md:px-16 text-center md:text-left bg-amber-50"
    >
      <div className="flex flex-col items-center md:items-start gap-4 max-w-xl">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
          Your restaurant's digital menu in minutes
        </h1>
        <p className="text-muted-foreground max-w-md">
          Create your menu, share the QR, and let your customers view it on
          their phones. Update anything, anytime
        </p>
        <div className="flex gap-4 justify-center md:justify-start">
          <Button size="lg" className="cursor-pointer">
            Create your menu
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="cursor-pointer"
            asChild
          >
            <Link href="/menu/demo">Watch demo</Link>
          </Button>
        </div>
      </div>

      {/* Demo Preview */}
      <div
        className="relative w-[260px] md:w-[300px] lg:w-[320px] shrink-0
                      rounded-t-[2.5rem] md:rounded-l-[2.5rem] md:rounded-r-none
                      border-8 border-b-0 md:border-b-8 md:border-r-0
                      border-black overflow-hidden shadow-2xl
                      h-[380px] md:h-[520px]"
      >
        <iframe src="/menu/demo" className="w-full h-full" />
        <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-amber-50 to-transparent md:hidden" />
        <div className="absolute top-0 right-0 bottom-0 w-16 bg-gradient-to-r from-transparent to-amber-50 hidden md:block" />
      </div>
    </section>
  );
}
