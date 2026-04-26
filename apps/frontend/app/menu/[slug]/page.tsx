import { MenuView } from "./_components";
import { PublicMenu, RestaurantProfile } from "@/lib/types/menu/menu";
import { mockMenu, mockProfile } from "@/lib/mocks/menu";

async function getMenu(slug: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_MENU_ENDPOINT}/${slug}`, {
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Error fetching menu");

  const data = await res.json();

  if (!data?.menu || !data?.profile) throw new Error("Invalid menu response");

  return {
    menu: data.menu as PublicMenu,
    profile: data.profile as RestaurantProfile,
  };
}

const USE_MOCK = process.env.USE_MOCK;

export default async function Menu({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  const { menu, profile } = USE_MOCK
    ? { menu: mockMenu, profile: mockProfile }
    : await getMenu(slug);

  return <MenuView menu={menu} profile={profile} />;
}