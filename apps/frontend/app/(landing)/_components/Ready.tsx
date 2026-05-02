import Link from "next/link";
import { Button } from "@/components/ui/button";

export const ReadyToGo = () => {
  return (
    <section className="flex flex-col items-center py-20 px-6 md:px-16 bg-[#110d05]">
      <div className="flex flex-col items-center text-center gap-4 max-w-xl mb-12 text-gray-50">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight">
          Ready to go digital?
        </h2>
        <p className="text-muted-foreground">
          Join 2,400+ restaurants already using QR Menu.
        </p>

        <div className="flex gap-4 justify-center">
          <Button
            size="lg"
            className="cursor-pointer bg-amber-500 hover:bg-amber-400 text-[#1a1208] font-bold border-0"
          >
            Create your menu
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="cursor-pointer border-amber-900 text-amber-100 hover:bg-amber-900/30 hover:text-amber-50 bg-transparent"
          >
            <Link href="/menu/demo">Watch demo</Link>
          </Button>
        </div>
      </div>
    </section>
  );
};
