"use client";

import { useState } from "react";
import ChatbotBubble from "../../components/ChatbotBubble";
import UserchatBubble from "../../components/UserchatBubble";
import { useRouter } from "next/navigation";

interface Chat {
	message: string;
	isBot: boolean;
}

const page = () => {
	const router = useRouter();
	const [botResponding, setBotResponding] = useState(false);
	const [inputPlaceholder, setInputPlaceholder] =
		useState("Type your message…");
	const [chats, setChats] = useState([
		{
			message: "Hello! Start asking me anything about the document!",
			isBot: true,
		},
		// {
		// 	message: "What is the document about?",
		// 	isBot: false,
		// },
		// {
		// 	message:
		// 		"The document is about the use of AI in the legal industry.",
		// 	isBot: true,
		// },
		// {
		// 	message: "What is AI?",
		// 	isBot: false,
		// },
		// {
		// 	message:
		// 		"Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.",
		// 	isBot: true,
		// },
		// {
		// 	message: "What is the legal industry?",
		// 	isBot: false,
		// },
		// {
		// 	message: "The legal industry is...",
		// 	isBot: true,
		// },
	] as Chat[]); // [ { message: string, isBot: boolean }

	// Handle sending message to bot and receiving response
	const sendPrompt = (message: string) => {
		setChats([...chats, { message, isBot: false }]);
		setBotResponding(true);
		setInputPlaceholder("bot is responding...");

		// send message to backend here!

		// receive response from backend here!

		// update chats with response from backend here!

		// set botResponding to false

		// set inputPlaceholder to "Type your message..."
	};

	return (
		<div className="flex flex-col items-center justify-center w-screen min-h-screen bg-slate-100 text-gray-800 p-10">
			<div className="flex justify-between my-3 rounded-lg max-w-xl">
				<div className="p-1 rounded-lg font-semibold text-sky-700">
					UploadedDocument.pdf
				</div>
				<button
					onClick={() => router.push("/")}
					className="bg-red-500 font-semibold p-2 text-sm text-white rounded-lg w-32 shadow-md ml-64">
					End Chat
				</button>
			</div>
			<div className="flex flex-col flex-grow w-full max-w-xl bg-white shadow-lg rounded-lg overflow-hidden">
				<div className="flex flex-col flex-grow h-0 p-4 overflow-auto">
					{chats.map((chat, index) => {
						if (chat.isBot) {
							return (
								<ChatbotBubble
									key={index}
									message={chat.message}
								/>
							);
						} else {
							return (
								<UserchatBubble
									key={index}
									message={chat.message}
								/>
							);
						}
					})}
				</div>

				<div className="bg-slate-200 p-3">
					<input
						className="flex items-center h-10 w-full rounded px-3 text-sm"
						type="text"
						disabled={botResponding}
						placeholder={inputPlaceholder}
						onKeyDown={(e) => {
							if (e.key === "Enter") {
								e.preventDefault();
								let message = e.target.value;
								e.target.value = "";
								sendPrompt(message);
							}
						}}
					/>
				</div>
			</div>
		</div>
	);
};

export default page;
