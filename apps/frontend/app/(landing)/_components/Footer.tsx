import { QrCode } from "lucide-react";

const links = [
  { label: "Features", href: "#features" },
  { label: "Pricing", href: "#pricing" },
  { label: "Demo", href:  "/menu/demo"},
];

export const Footer = () => {
  return (
    <footer className="bg-[#110d05] px-6 md:px-16 py-10">
      <div className="max-w-5xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex flex-col items-center md:items-start gap-2">
            <div className="flex items-center gap-2">
              <QrCode className="w-5 h-5 text-amber-500" />
              <span className="text-amber-50 font-bold text-lg">QR Menu</span>
            </div>
            <p className="text-sm text-zinc-600 max-w-[260px] text-center md:text-left">
              Helping restaurants go digital since 2024. Built with love for the
              food industry.
            </p>
          </div>

          <nav className="flex gap-6">
            {links.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-sm text-zinc-600 hover:text-amber-500 transition-colors"
              >
                {link.label}
              </a>
            ))}
          </nav>
        </div>

        <div className="border-t border-zinc-900 mt-8 pt-6 flex flex-col md:flex-row justify-between items-center gap-3">
          <p className="text-xs text-zinc-700">
            © {new Date().getFullYear()} QR Menu. All rights reserved.
          </p>
          <div className="flex gap-6">
            {["Privacy", "Terms"].map((item) => (
              <a
                key={item}
                href="#"
                className="text-xs text-zinc-700 hover:text-amber-500 transition-colors"
              >
                {item}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};
