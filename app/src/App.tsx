import beatMetadata from "../public/beats/metadata.json";

function App() {
  const padZeroes = (idx: number) => {
    let res = "";
    if (idx < 10) {
      res += "0";
    }
    if (idx < 100) {
      res += "0";
    }
    return res + idx;
  };
  return (
    <div className="p-0">
      <div className="text-lg tracking-[0.6em] flex group">
        {"beats@badends".split("").map((char, i) => (
          <span
            key={i}
            style={{
              display: "inline-block",
              // Animation only applies when parent is hovered (see CSS below)
            }}
            className={`group-hover:animate-jitter${i}`}
          >
            {char}
            <style>
              {`
            @keyframes jitter${i} {
          0% { transform: translate(0, 0) rotate(0deg);}
          20% { transform: translate(-0.5px, 0.5px) rotate(-1deg);}
          40% { transform: translate(-0.5px, -0.5px) rotate(1deg);}
          60% { transform: translate(0.5px, 0.5px) rotate(0deg);}
          80% { transform: translate(0.5px, -0.5px) rotate(1deg);}
          100% { transform: translate(0, 0) rotate(0deg);}
            }
            .group:hover .group-hover\\:animate-jitter${i} {
          animation: jitter${i} 0.1s infinite;
          animation-delay: ${Math.random() * 0.2}s;
            }
          `}
            </style>
          </span>
        ))}
      </div>
      {Object.entries(beatMetadata).map(([, obj], idx) => {
        return (
          <div
            className="flex gap-2 items-center border-b border-slate-200 p-2 text-sm"
            key={obj.filename}
          >
            <img
              src={obj.thumbnail}
              alt={obj.title}
              className="w-8 h-8 object-cover"
            />
            <span className={`text-slate-500`}>{padZeroes(idx)}</span>{" "}
            <a
              className="underline hover:text-red-500"
              target="_blank"
              href={obj.url}
            >
              yt
            </a>{" "}
            <a
              className="underline hover:text-blue-500"
              href={`beats/${obj.filename}`}
              download
            >
              dl
            </a>{" "}
            {obj.title}
            <div className="ml-auto text-right hidden sm:block">
              {new Date(obj.added).toLocaleString()}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default App;
