"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatbotBubble from "../../components/ChatbotBubble";
import UserchatBubble from "../../components/UserchatBubble";
import ChatInterface from "@/components/ChatInterface";
import FilesSidebar from "@/components/FilesSidebar";

interface Chat {
	message: string;
	isBot: boolean;
}

const page = () => {
	const router = useRouter();
	const [files, setFiles] = useState([
		{
			name: "dummy_data.pdf",
			size: 543000,
		},
	]);

	useEffect(() => {
		let oldFiles = JSON.parse(localStorage.getItem("files") || "[]");
		setFiles([...files, ...oldFiles]);
	}, []);

	return (
		<div className="flex flex-row items-stretch justify-center w-screen min-h-screen bg-slate-100 text-gray-800 p-10">
			<div className="flex flex-col items-center justify-center">
				<button
					onClick={() => router.push("/")}
					className="m-3 px-4 py-2 bg-slate-200 hover:bg-slate-300 rounded-lg text-slate-600 font-semibold">
					Add more documents
				</button>
				<FilesSidebar files={files} />
			</div>
			<ChatInterface />
		</div>
	);
};

export default page;
