"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
const Home = () => {
  const router = useRouter();
  const [file, setFile] = useState(null);

  // handle file input change
  const handleFileInputChange = (e: any) => {
    const file = e.target.files[0];
    setFile(file);
  };

  // handle start chatting
  const handleStartChatting = async () => {
    // do something with the file
    console.log("file: ", file);
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
      mode: "no-cors",
    });

    router.push("/chat");

    // send the file to backend here!
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="mt-4 mb-2 text-2xl font-bold text-gray-700 tracking-wide">
        Insert App Title Here
      </h1>
      <div className="mb-6 italic text-slate-700">
        Subtitle here - some slogan or vision for the company
      </div>

      <div className="flex flex-col items-center justify-center w-3/4">
        <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 hover:bg-gray-100">
          {file == null ? (
            <>
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg
                  className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 20 16"
                >
                  <path
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                  />
                </svg>
                <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  PDF, DOC, or TXT (MAX. 15 MB)
                </p>
              </div>
              <input
                id="dropzone-file"
                type="file"
                onChange={(e) => handleFileInputChange(e)}
                className="hidden"
              />
            </>
          ) : (
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <div>File upload successful!</div>
              <div className="mt-2 text-s text-gray-500 dark:text-gray-400">
                {file?.name}
              </div>
              <div className="mt-2 text-xs text-gray-500 italic">
                {(file?.size / 1000).toFixed(2)} MB
              </div>
            </div>
          )}
        </label>
        <button
          disabled={file == null}
          onClick={() => handleStartChatting()}
          className="bg-gray-300 mt-5 cursor-pointer hover:bg-gray-400 text-gray-800 font-bold py-3 px-5 rounded inline-flex items-center"
        >
          <span className="font-semibold">Start Chatting</span>
        </button>
      </div>
    </main>
  );
};

export default Home;
