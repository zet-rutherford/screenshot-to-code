import { useRef, useEffect } from "react";

interface Props {
  code: string;
}

function CodePreview({ code }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [code]);

  return (
    <div
      ref={scrollRef}
      className="w-full h-64 px-2 bg-black text-green-400 whitespace-pre-wrap 
      overflow-y-auto font-mono text-[10px] my-4 rounded"
    >
      {code}
    </div>
  );
}

export default CodePreview;
