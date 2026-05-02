"use client";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Navbar() {
  const [open, setOpen] = useState<boolean>(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-amber-50/95 backdrop-blur supports-[backdrop-filter]:bg-amber-50/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        <h1 className="text-xl font-bold cursor-pointer shrink-0">QR Menu</h1>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <a className="transition hover:text-amber-800 cursor-pointer" href="#hero">Home</a>
          <a className="transition hover:text-amber-800 cursor-pointer" href="#features">
            Features
          </a>
          <a className="transition hover:text-amber-800 cursor-pointer" href="#pricing">
            Pricing
          </a>
          <Button variant="outline" className="cursor-pointer ml-4">
            Login
          </Button>
        </nav>

        {/* Mobile Toggle */}
        <button
          className="inline-flex items-center justify-center rounded-md p-2 text-amber-900 md:hidden"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {open && (
        <div className="fixed inset-0 top-16 z-50 grid h-[calc(100vh-4rem)] grid-flow-row auto-rows-max overflow-auto p-6 pb-32 shadow-md animate-in slide-in-from-top-2 md:hidden bg-amber-50">
          <nav className="relative z-20 grid gap-6 rounded-md p-4">
            <a
              href="#"
              className="flex w-full items-center text-lg font-semibold hover:text-amber-700"
              onClick={() => setOpen(false)}
            >
              Home
            </a>
            <a
              href="#"
              className="flex w-full items-center text-lg font-semibold hover:text-amber-700"
              onClick={() => setOpen(false)}
            >
              Features
            </a>
            <a
              href="#"
              className="flex w-full items-center text-lg font-semibold hover:text-amber-700"
              onClick={() => setOpen(false)}
            >
              Pricing
            </a>
            <hr className="my-2 border-amber-200" />
            <Button className="w-full bg-amber-700 hover:bg-amber-800">
              Login
            </Button>
          </nav>
        </div>
      )}
    </header>
  );
}
