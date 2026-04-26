export type LinkType =
  | "instagram"
  | "facebook"
  | "tiktok"
  | "twitter"
  | "youtube"
  | "whatsapp"
  | "webiste"
  | "other";

export interface PublicLink {
  type: LinkType | null;
  url: string | null;
  postion: number | null;
}

export interface PublicProduct {
  id: number;
  name: string;
  description: string | null;
  price: number;
  image_url: string | null;
  is_available: boolean;
  position: number | null;
}

export interface PublicCategory {
  id: number;
  name: string;
  position: number | null;
  products: PublicProduct[];
}

export interface RestaurantProfile {
  name: string;
  description: string | null;
  logo_url: string | null;
  slug: string;
  links: PublicLink[];
}

export interface PublicMenu {
  name: string;
  logo_url: string | null;
  categories: PublicCategory[]
}
