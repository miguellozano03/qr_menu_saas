import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";

const plans = [
  {
    name: "Free",
    price: 0,
    description: "Perfect to get started and see if it fits your restaurant.",
    features: [
      "1 QR menu",
      "Up to 30 dishes",
      "Basic customization",
      "QR code download",
    ],
    cta: "Get started free",
    featured: false,
  },
  {
    name: "Pro",
    price: 19,
    description: "For restaurants that want the full experience.",
    features: [
      "Unlimited menus",
      "Unlimited dishes",
      "Full customization",
      "Priority support",
    ],
    cta: "Start Pro — 14 days free",
    featured: true,
  },
];

export const Pricing = () => {
  return (
    <section id="pricing" className="flex flex-col items-center py-20 px-6 md:px-16 bg-amber-50">
      <div className="flex flex-col items-center text-center gap-4 max-w-xl mb-16">
        <p className="text-xs font-semibold tracking-widest uppercase text-amber-700">Pricing</p>
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight">Simple, honest pricing</h2>
        <p className="text-muted-foreground">Start free. Upgrade when you're ready.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`relative flex flex-col gap-6 rounded-2xl p-8 border ${
              plan.featured
                ? "bg-[#1a1208] border-amber-500 text-white"
                : "bg-white border-amber-200 text-zinc-900"
            }`}
          >
            {plan.featured && (
              <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-amber-500 text-[#1a1208] text-xs font-bold px-4 py-1 rounded-full">
                Most popular
              </span>
            )}

            <div>
              <p className={`text-xs font-semibold tracking-widest uppercase mb-3 ${plan.featured ? "text-amber-500" : "text-amber-700"}`}>
                {plan.name}
              </p>
              <p className="text-5xl font-bold tracking-tight">
                {plan.price === 0 ? "Free" : <><sup className="text-2xl font-medium">$</sup>{plan.price}<span className="text-lg font-normal opacity-60">/mo</span></>}
              </p>
              <p className={`text-sm mt-3 ${plan.featured ? "text-amber-50/60" : "text-muted-foreground"}`}>
                {plan.description}
              </p>
            </div>

            <ul className="flex flex-col gap-3">
              {plan.features.map((feature) => (
                <li key={feature} className="flex items-center gap-3 text-sm">
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 ${plan.featured ? "bg-amber-500/20" : "bg-amber-100"}`}>
                    <Check className={`w-3 h-3 ${plan.featured ? "text-amber-400" : "text-amber-700"}`} />
                  </div>
                  {feature}
                </li>
              ))}
            </ul>

            <Button
              size="lg"
              className={`w-full cursor-pointer mt-auto ${
                plan.featured
                  ? "bg-amber-500 hover:bg-amber-400 text-[#1a1208] font-bold"
                  : "bg-[#1a1208] hover:bg-zinc-800 text-white"
              }`}
            >
              {plan.cta}
            </Button>
          </div>
        ))}
      </div>
    </section>
  );
};