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
    <Carousel opts={{ dragFree: true }}>
      <CarouselContent className="gap-10">
        {categories?.map((category) => (
          <CarouselItem key={category.id} className="pl-2 basis-1/4 md:basis-1/6 ">
            <CategoryItem
              text={category.name}
              isActive={activeCategory === category.id}
              onClick={() => onSelect(activeCategory === category.id ? null : category.id)}
            />
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
    </Carousel>
  );
};