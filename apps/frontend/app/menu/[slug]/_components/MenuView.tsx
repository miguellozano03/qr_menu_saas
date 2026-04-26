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
    <main className="select-none paper-texture h-screen overflow-hidden flex flex-col md:h-auto md:overflow-visible md:min-h-screen p-4">
      <header className="md:shrink-0">
        <section className="flex justify-between items-center">
          <div />
          <h1 className="text-3xl font-bold">{profile.name}</h1>
          <CircleQuestionMark className="cursor-pointer" />
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
          <div key={category.id} className="mb-6">
            <h2 className="text-2xl font-bold mb-3">{category.name}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
                  className="text-gray-700 hover:text-red-500 block"
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
