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
        text-sm rounded-2xl font-bold transition-all duration-200 
        ${
          !isActive
            ? "bg-gray-100 border-zinc-200/60 text-gray-500 hover:bg-gray-200"
            : "bg-white border-red-500 text-red-500 shadow-sm scale-105"
        }
      `}
    >
      {text}
    </button>
  );
};
