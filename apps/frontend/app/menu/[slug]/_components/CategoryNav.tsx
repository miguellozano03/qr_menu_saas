"use client";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import type { PublicCategory } from "@/lib/types/menu/menu";

import { CategoryItem } from "./CategoryItem";

interface CategoryNavProps {
  categories: PublicCategory[];
  activeCategory: number | null;
  onSelect: (id: number | null) => void;
}

export const CategoryNav = ({ categories, activeCategory, onSelect }: CategoryNavProps) => {
  return (
    <Carousel opts={{ dragFree: true }} className="w-full px-1">
      <CarouselContent className="-ml-2">
        {categories?.map((category) => (
          <CarouselItem
            key={category.id}
            className="pl-2 basis-1/3 sm:basis-1/4 md:basis-1/6"
          >
            <CategoryItem
              text={category.name}
              isActive={activeCategory === category.id}
              onClick={() => onSelect(activeCategory === category.id ? null : category.id)}
            />
          </CarouselItem>
        ))}
      </CarouselContent>
      {/* Flechas solo en desktop — en mobile el drag es suficiente */}
      <CarouselPrevious className="hidden md:flex" />
      <CarouselNext className="hidden md:flex" />
    </Carousel>
  );
};