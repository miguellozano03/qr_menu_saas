import Link from "next/link";

export default function Home() {
  return (
    <>
      <h1 className="text-4xl font-bold">Home</h1>
      <Link href={"/menu"}>Go to menu</Link>
    </>
  );
}