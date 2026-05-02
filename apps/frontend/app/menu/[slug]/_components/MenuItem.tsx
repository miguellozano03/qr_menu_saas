import { PublicProduct } from "@/lib/types/menu/menu";

export const MenuItem = ({
  image_url,
  name,
  description,
  price,
}: PublicProduct) => {
  return (
    <article className="pb-2 border border-zinc-800 rounded-xl overflow-hidden flex bg-zinc-900 hover:border-zinc-600 transition-all duration-300">
      <div className="p-3 md:p-4 flex flex-col justify-between flex-1 min-w-0">
        <div>
          <h3 className="text-zinc-100 font-bold text-base md:text-xl leading-tight">{name}</h3>
          <p className="text-xs md:text-sm text-zinc-500 mt-0.5 line-clamp-2">{description}</p>
        </div>
        <span className="text-zinc-400 font-semibold text-sm md:text-base mt-2">
          $ {price.toFixed(2)}
        </span>
      </div>
      <div className="h-24 w-24 md:h-32 md:w-32 shrink-0">
        <img
          src={image_url ?? undefined}
          alt="Artículo"
          className="w-full h-full object-cover p-2 md:p-3 rounded-2xl"
        />
      </div>
    </article>
  );
};