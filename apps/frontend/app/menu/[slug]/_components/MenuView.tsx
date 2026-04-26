"use client";

import { useState } from "react";
import { CircleQuestionMark } from "lucide-react";
import { CategoryNav, MenuItem, ICON_MAP } from ".";
import { PublicMenu, RestaurantProfile } from "@/lib/types/menu/menu";

interface MenuViewProps {
  menu: PublicMenu;
  profile: RestaurantProfile;
}

export function MenuView({ menu, profile }: MenuViewProps) {
  const [activeCategory, setActiveCategory] = useState<number | null>(null);

  const visibleCategories = activeCategory
    ? menu.categories?.filter((cat) => cat.id === activeCategory)
    : menu.categories;

  return (
    <main className="select-none bg-zinc-950 h-screen overflow-hidden flex flex-col md:h-auto md:overflow-visible md:min-h-screen p-4">
      <header className="md:shrink-0">
        <section className="flex justify-between items-center">
          <div />
          <h1 className="text-3xl text-zinc-100 font-bold tracking-wide">{profile.name}</h1>
          <CircleQuestionMark className="cursor-pointer text-zinc-500 hover:text-zinc-300 transition-colors" />
        </section>
      </header>

      <nav className="mt-4 md:shrink-0">
        <CategoryNav
          categories={menu.categories ?? []}
          activeCategory={activeCategory}
          onSelect={setActiveCategory}
        />
      </nav>

      <section className="mt-6 flex-1 min-h-0 overflow-y-auto md:overflow-visible no-scrollbar">
        {visibleCategories?.map((category) => (
          <div key={category.id} className="mb-8">
            <h2 className="text-xl text-zinc-400 font-semibold mb-3 pb-2 border-b border-zinc-800 text-center tracking-widest uppercase">{category.name}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {category.products?.map((product) => (
                <MenuItem key={product.id} {...product} />
              ))}
            </div>
          </div>
        ))}
      </section>

      <footer className="mt-10 mb-6 md:shrink-0 flex justify-center">
        <nav className="w-full">
          <ul className="flex justify-center items-center gap-6">
            {profile.links?.map((link, index) => (
              <li key={index} className="transition-transform hover:scale-110">
                <a
                  href={link.url ?? "#"}
                  target="_blank"
                  rel="noreferrer"
                  className="text-zinc-600 hover:text-zinc-200 transition-colors block"
                >
                  <div className="[&>svg]:w-8 [&>svg]:h-8">
                    {ICON_MAP[link.type ?? "other"]}
                  </div>
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </footer>
    </main>
  );
}