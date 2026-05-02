const steps = [
  {
    number: "01",
    title: "Create your menu",
    description:
      "Add your categories, dishes, descriptions and photos through our simple editor.",
  },
  {
    number: "02",
    title: "Get your QR code",
    description:
      "We generate a unique QR instantly. Download it in high resolution, ready to print.",
  },
  {
    number: "03",
    title: "Place it on tables",
    description:
      "Customers scan and browse your menu right on their phone. No app needed.",
  },
];

export const HowItWorks = () => {
  return (
    <section className="flex flex-col items-center py-20 px-6 md:px-16 bg-[#1a1208]">
      <div className="flex flex-col items-center text-center gap-4 max-w-xl mb-16">
        <p className="text-xs font-semibold tracking-widest uppercase text-amber-700">
          How it works
        </p>
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-gray-50">
          Up and running in 3 steps
        </h2>
        <p className="text-amber-50/60">
          No technical knowledge required. If you can use a phone, you can set
          this up.
        </p>
      </div>

      <div className="flex flex-col md:flex-row gap-0 w-full max-w-4xl">
        {steps.map((step, index) => (
          <div key={step.number} className="flex flex-col md:flex-row flex-1">
            {/* Card */}
            <div className="flex flex-col items-center text-center gap-4 px-8">
              <div className="w-12 h-12 rounded-full bg-amber-500 flex items-center justify-center font-bold text-[#1a1208] text-sm shrink-0">
                {step.number}
              </div>
              <div>
                <h3 className="text-gray-100 font-semibold text-lg mb-2">
                  {step.title}
                </h3>
                <p className="text-amber-50/50 text-sm leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>

            {/* Connector */}
            {index < steps.length - 1 && (
              <>
                {/* Mobile: línea vertical */}
                <div className="flex justify-center my-6 md:hidden">
                  <div className="w-px h-12 bg-amber-900" />
                </div>
                {/* Desktop: línea horizontal */}
                <div className="hidden md:flex items-start pt-6 shrink-0">
                  <div className="h-px w-8 bg-amber-900 mt-0" />
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </section>
  );
};
