import { LucideIcon } from "lucide-react";
import { QrCode, LayoutGrid, ImageIcon, Sparkles, Tag } from "lucide-react";

const features = [
  {
    icon: QrCode,
    title: "Scan & go",
    description:
      "Customers scan your QR and instantly see your menu. No app, no download, no friction.",
  },
  {
    icon: LayoutGrid,
    title: "Browse by category",
    description:
      "Navigate through your menu sections in one tap. Everything organized and easy to find.",
  },
  {
    icon: ImageIcon,
    title: "Dish details",
    description:
      "Photo, name, description and price for each dish. Let your food speak for itself.",
  },
  {
    icon: Tag,
    title: "Start for free",
    description:
      "Get started at no cost. Upgrade when you need more — no pressure.",
  },
  {
    icon: Sparkles,
    title: "Always up to date",
    description:
      "Update your menu anytime from your dashboard. Changes go live instantly.",
  },
];

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export const FeatureCard = ({
  icon: Icon,
  title,
  description,
}: FeatureCardProps) => {
  return (
    <article className="bg-[#fff9f0] border border-[#f5ddb5] rounded-2xl p-6 flex flex-col gap-3">
      <div className="w-10 h-10 bg-[#fde8b8] rounded-xl flex items-center justify-center shrink-0">
        <Icon className="w-5 h-5 text-[#b36b10]" />
      </div>
      <div>
        <h3 className="font-semibold text-[#1a1208] text-sm">{title}</h3>
        <p className="text-xs text-[#7a6245] leading-relaxed mt-1">
          {description}
        </p>
      </div>
    </article>
  );
};

export function Features() {
  return (
    <section id="features" className="flex flex-col items-center py-20 px-6 md:px-16 bg-amber-50">
      <div className="flex flex-col items-center text-center gap-4 max-w-xl mb-12">
        <p className="text-xs font-semibold tracking-widest uppercase text-amber-700">
          Features
        </p>
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight">
          Everything your menu needs
        </h2>
        <p className="text-muted-foreground">
          Simple tools, powerful results. Built for restaurants that want to
          move fast.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
        {features.map((f) => (
          <FeatureCard key={f.title} {...f} />
        ))}
      </div>
    </section>
  );
}
