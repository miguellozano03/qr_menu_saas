interface CategoryItemProps {
  text: string;
  isActive: boolean;
  onClick: () => void;
}

export const CategoryItem = ({
  text,
  isActive,
  onClick,
}: CategoryItemProps) => {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`
        px-6 py-2 w-32 shrink-0 
        text-sm rounded-sm font-bold transition-all duration-200 cursor-pointer 
        ${
          !isActive
            ? "bg-zinc-800 border border-zinc-700 text-zinc-200 hover:border-zinc-500 hover:text-white"
            : "bg-white text-zinc-950 shadow-sm scale-105"
        }
      `}
    >
      {text}
    </button>
  );
};
