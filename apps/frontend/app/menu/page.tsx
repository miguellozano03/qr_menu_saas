"use client";

import Link from 'next/link';
import { useState } from 'react';

export default function Menu() {
  const [count, setCount] = useState(0);
  return (
    <>
      <h1>Menu Page</h1>
      <nav>
        <Link href={"/"}>Go home</Link>
      </nav>

      <button onClick={() => setCount(count + 1)}>
        {count}
      </button>
    </>
  );
}
