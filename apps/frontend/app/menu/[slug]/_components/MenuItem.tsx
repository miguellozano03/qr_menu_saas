import { PublicProduct } from "@/lib/types/menu/menu";

export const MenuItem = ({
  image_url,
  name,
  description,
  price,
}: PublicProduct) => {
  return (
    <article className="pb-2 border border-zinc-800 rounded-xl overflow-hidden flex bg-zinc-900 hover:border-zinc-600 transition-all duration-300">
      <div className="p-4 flex flex-col justify-between flex-1">
        <div>
          <h3 className="text-zinc-100 font-bold text-xl">{name}</h3>
          <p className="text-sm text-zinc-500">{description}</p>
        </div>
        <span className="text-zinc-400 font-semibold"> $ {price.toFixed(2)}</span>
      </div>
      <div className="h-32 w-32 shrink-0">
        <img
          src={image_url ?? undefined}
          alt="Artículo"
          className="w-full h-full object-cover p-3 rounded-2xl"
        />
      </div>
    </article>
  );
};