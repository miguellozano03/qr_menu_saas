import { PublicMenu, RestaurantProfile } from "@/lib/types/menu/menu";

export const mockProfile: RestaurantProfile = {
  name: "The Gilded Bun",
  description: "Artisan burgers, craft shakes, and golden vibes in the heart of the city. 🍔✨",
  logo_url: "https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=200&h=200&auto=format&fit=crop",
  slug: "the-gilded-bun",
  links: [
    { type: "instagram", url: "https://instagram.com/thegildedbun", postion: null },
    { type: "whatsapp", url: "https://wa.me/15550123456", postion: null },
    { type: "facebook", url: "https://facebook.com/thegildedbun", postion: null },
  ],
};

export const mockMenu: PublicMenu = {
  name: "The Gilded Bun",
  logo_url: "https://images.unsplash.com/photo-1552566626-52f8b828add9?q=80&w=200&h=200&auto=format&fit=crop",
  categories: [
    {
      id: 1,
      name: "Signature Burgers",
      position: 0,
      products: [
        { 
          id: 1, 
          name: "The Truffle Royale", 
          description: "Wagyu beef, truffle aioli, caramelized onions, and swiss cheese on a brioche bun.", 
          price: 18.50, 
          image_url: "https://images.unsplash.com/photo-1525059337994-6f2a1311b4d4?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 0 
        },
        { 
          id: 2, 
          name: "Spicy Bandit", 
          description: "Double patty, pepper jack, jalapeños, and our secret habanero gold sauce.", 
          price: 16.00, 
          image_url: "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 1 
        },
        { 
          id: 3, 
          name: "The Garden Heir", 
          description: "Plant-based patty, smashed avocado, heirloom tomatoes, and sprouts.", 
          price: 15.00, 
          image_url: "https://images.unsplash.com/photo-1512152272829-e3139592d56f?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 2 
        },
      ],
    },
    {
      id: 2,
      name: "Hand-Spun Shakes",
      position: 1,
      products: [
        { 
          id: 4, 
          name: "Midnight Cocoa", 
          description: "Dark chocolate, sea salt, and whipped cream topping.", 
          price: 8.00, 
          image_url: "https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 0 
        },
        { 
          id: 5, 
          name: "Golden Vanilla Bean", 
          description: "Madagascar vanilla with edible gold leaf flakes.", 
          price: 9.50, 
          image_url: "https://images.unsplash.com/photo-1541658016709-82535e94bc71?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 1 
        },
        { 
          id: 6, 
          name: "Strawberry Fields", 
          description: "Fresh macerated strawberries and organic whole milk.", 
          price: 7.50, 
          image_url: "https://images.unsplash.com/photo-1579954115545-a95591f28be0?q=80&w=800&auto=format&fit=crop", 
          is_available: false, 
          position: 2 
        },
      ],
    },
    {
      id: 3,
      name: "Sides & Starters",
      position: 2,
      products: [
        { 
          id: 7, 
          name: "Parmesan Truffle Fries", 
          description: "Hand-cut potatoes tossed in white truffle oil and aged parmesan.", 
          price: 9.00, 
          image_url: "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 0 
        },
        { 
          id: 8, 
          name: "Honey Garlic Wings", 
          description: "Crispy chicken wings glazed in a sticky honey-soy reduction.", 
          price: 12.00, 
          image_url: "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?q=80&w=800&auto=format&fit=crop", 
          is_available: true, 
          position: 1 
        },
      ],
    },
  ],
};