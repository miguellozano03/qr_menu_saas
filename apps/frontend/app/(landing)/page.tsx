import type { Metadata } from "next";
import {
  Navbar,
  Hero,
  Features,
  HowItWorks,
  ReadyToGo,
  Pricing,
  Footer
} from "./_components";

export const metadata: Metadata = {
  title: "QR Menu - Homepage",
};

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <Pricing />
      <ReadyToGo />
      <Footer />
    </div>
  );
}
