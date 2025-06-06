import { useRef } from "react";

function ImagePreview({ src }: { src: string }) {
  const imgRef = useRef<HTMLImageElement>(null);

  const handleClick = () => {
    if (imgRef.current?.requestFullscreen) {
      imgRef.current.requestFullscreen();
    } else if ((imgRef.current as any)?.webkitRequestFullscreen) {
      (imgRef.current as any).webkitRequestFullscreen(); // Safari
    } else if ((imgRef.current as any)?.mozRequestFullScreen) {
      (imgRef.current as any).mozRequestFullScreen(); // Firefox
    } else if ((imgRef.current as any)?.msRequestFullscreen) {
      (imgRef.current as any).msRequestFullscreen(); // IE
    }
  };

  return (
    <img
      ref={imgRef}
      onClick={handleClick}
      src={src}
      alt="Reference"
      className="w-full cursor-pointer border border-gray-200 rounded-md"
      title="Click to view full screen"
    />
  );
}

export default ImagePreview;