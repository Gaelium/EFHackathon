"use client";

import { useState } from "react";
import ChatbotBubble from "./ChatbotBubble";
import UserchatBubble from "./UserchatBubble";
import { useRouter } from "next/navigation";

interface Chat {
	message: string;
	isBot: boolean;
}

const ChatInterface = () => {
	const router = useRouter();
	const [botResponding, setBotResponding] = useState(false);
	const [inputPlaceholder, setInputPlaceholder] =
		useState("Type your message…");
	const [chats, setChats] = useState([
		{
			message: "Hello! Start asking me anything about the document!",
			isBot: true,
		},
	] as Chat[]); // [ { message: string, isBot: boolean }

	// Handle sending message to bot and receiving response
	const sendPrompt = async (message: string) => {
		let prevChats = [...chats, { message, isBot: false }];
		setChats([...chats, { message, isBot: false }]);
		setBotResponding(true);
		setInputPlaceholder("bot is responding...");

		// sending message to the backend
		const response = await fetch("/api/chat", {
			method: "POST",
			body: JSON.stringify({ message }),
			headers: {
				"Content-Type": "application/json",
			},
		});

		// receiving response from the backend
		const data = await response.json();

		// update chats with response from backend here!
		setChats([...prevChats, { message: data.message, isBot: true }]);

		// set botResponding to false & inputPlaceholder to default
		setBotResponding(false);
		setInputPlaceholder("Type your message...");
	};

	return (
		<div className="flex flex-col items-stretch w-1/2">
			<div className="flex justify-between my-3 rounded-lg max-w-xl">
				<div className="p-1 rounded-lg font-semibold text-sky-700 cursor-default">
					<span className="text-lg pr-2">✧</span> Redoct Chat Bot
				</div>
				<button
					onClick={() => router.push("/")}
					className="bg-red-500 font-semibold p-2 text-sm text-white rounded-lg w-32 shadow-md">
					End Chat
				</button>
			</div>
			<div className="flex flex-col h-full w-full max-w-xl bg-white shadow-lg rounded-lg overflow-hidden">
				<div className="flex flex-col flex-grow p-4 overflow-auto h-full">
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

export default ChatInterface;
