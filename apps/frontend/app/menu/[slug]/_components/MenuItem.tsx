import { PublicProduct } from "@/lib/types/menu/menu";

export const MenuItem = ({
  id,
  image_url,
  name,
  is_available,
  description,
  price,
}: PublicProduct) => {
  return (
    <article className="rounded-lg bg-white/30 border overflow-hidden flex">
      <div className="p-4 flex flex-col justify-between flex-1">
        <div>
          <h3 className="font-bold text-lg">{name}</h3>
          <p className="text-sm text-gray-700">
            {description}
          </p>
        </div>
        <span className="font-semibold">{price.toFixed(2)}</span>
      </div>
      <div className="bg-gray-200 h-32 w-32 shrink-0">
        <img src={image_url} alt="Artículo" className="w-full h-full object-cover" />
      </div>
    </article>
  );
};
